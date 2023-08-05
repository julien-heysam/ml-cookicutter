DECLARE look_back_window INT64 DEFAULT @look_back_window;

-- extract all key value pairs as an array from a json dict
-- input: json string with a dictionary
-- returns:  list of struct <key, value>
CREATE TEMP  FUNCTION EXTRACT_KV_PAIRS(json_str STRING)
RETURNS ARRAY<STRUCT<key STRING, value STRING>>
LANGUAGE js AS """
  try{
    const json_dict = JSON.parse(json_str);
    const all_kv = Object.entries(json_dict).map(
        (r)=>Object.fromEntries([["key", r[0]],["value",
                                   JSON.stringify(r[1])]]));
    return all_kv;
  } catch(e) { return [{"key": "error","value": e}];}
""";


WITH
  -- extract ticket field that are mandatory, not deleted, having a dropdown input
  mandatory_fields AS (
    SELECT
      id,
      account_id,
      label,
      created_datetime,
      deactivated_datetime,
      deleted_datetime,
      required,
      input_type,
    FROM `gorgias-pipeline-production.analytics.custom_field_view`
    WHERE TRUE
      AND required = TRUE
      AND input_type='dropdown'
      AND deleted_datetime IS NULL
  ),
  -- extract ticket field labels from the json
  extracted_ticket_labels as (
    SELECT
      account_id,
      ticket_id,
      created_datetime,
      EXTRACT_KV_PAIRS(TO_JSON_STRING(values)) as kv_list
    FROM `gorgias-pipeline-production.analytics.custom_fields_ticket_values_view`
  ),
  -- now expand the list into individual rows
  unnested_ticket_labels AS(
    SELECT
      account_id,
      ticket_id,
      created_datetime,
      CAST(kv_pair.key AS INT64) AS custom_field_id,
      kv_pair.value AS custom_field_value
    FROM extracted_ticket_labels
    CROSS JOIN UNNEST (kv_list) as kv_pair
  ),
  -- now build the ground truth of the custom field labels
  custom_field_ground_truth AS (
    SELECT
      unnested_ticket_labels.account_id           AS account_id,
      unnested_ticket_labels.ticket_id            AS ticket_id,
      unnested_ticket_labels.custom_field_id      AS custom_field_id,
      mandatory_fields.label                      AS custom_field_label,
      unnested_ticket_labels.custom_field_value   AS custom_field_value,

      mandatory_fields.required                   AS custom_field_is_required,
      mandatory_fields.input_type                 AS custom_field_input_type,

      unnested_ticket_labels.created_datetime     AS labeling_datetime,
      mandatory_fields.created_datetime           AS custom_field_creation_datetime,
      mandatory_fields.deactivated_datetime       AS custom_field_deactivation_datetime,
      mandatory_fields.deleted_datetime           AS custom_field_deletion_datetime,

    FROM unnested_ticket_labels
      LEFT JOIN mandatory_fields
        ON mandatory_fields.id = unnested_ticket_labels.custom_field_id
        AND mandatory_fields.account_id = unnested_ticket_labels.account_id
    WHERE required IS NOT NULL
  ),
  -- select the ticket_id created in the last look_back_window days
  tickets_created_in_look_back_window AS (
    SELECT
      id
    FROM (
      SELECT
        * EXCEPT(__kafka_offset, __kafka_partition)
      FROM
        gorgias-pipeline-production.analytics.ticket
      WHERE
        DATE(__event_timestamp)  > DATE_SUB(CURRENT_DATE(), INTERVAL look_back_window DAY)
      QUALIFY
        ROW_NUMBER() OVER (PARTITION BY account_id, id ORDER BY __event_timestamp DESC) = 1
    )
    WHERE
      __deleted IS FALSE
  ),
  -- ticket message view query
  local_ticket_message_view AS (
    SELECT
      account_id,
      ticket_id,
      channel,
      subject,
      from_agent,
      message_id,
      created_datetime,
      stripped_text,
      via,
    FROM (
      SELECT
        * EXCEPT(__kafka_offset, __kafka_partition)
      FROM
        gorgias-pipeline-production.analytics.ticket_message
      WHERE
        DATE(__event_timestamp)  > DATE_SUB(CURRENT_DATE(), INTERVAL look_back_window DAY)
      QUALIFY
        ROW_NUMBER() OVER (PARTITION BY account_id, id ORDER BY __event_timestamp DESC) = 1
    )
    WHERE
      __deleted IS FALSE
  ),
  -- select the first message associated with each ticket_id in the last look_back_window days
  first_ticket_messages AS (
    SELECT DISTINCT
      account_id,
      ticket_id,
      FIRST_VALUE(channel) OVER (PARTITION BY ticket_id ORDER BY created_datetime ASC) AS channel,
      FIRST_VALUE(subject) OVER (PARTITION BY ticket_id ORDER BY created_datetime ASC) AS subject,
      FIRST_VALUE(from_agent) OVER (PARTITION BY ticket_id ORDER BY created_datetime ASC) AS from_agent,
      FIRST_VALUE(message_id) OVER (PARTITION BY ticket_id ORDER BY created_datetime ASC) AS message_id,
      FIRST_VALUE(created_datetime) OVER (PARTITION BY ticket_id ORDER BY created_datetime ASC) AS created_datetime,
      FIRST_VALUE(stripped_text) OVER (PARTITION BY ticket_id ORDER BY created_datetime ASC) AS message_body,
      FIRST_VALUE(via) OVER (PARTITION BY ticket_id ORDER BY created_datetime ASC) AS via,
    FROM local_ticket_message_view -- gorgias-pipeline-production.`analytics.ticket_message_view`
    WHERE TRUE
      -- AND DATE(__event_timestamp) > DATE_SUB(CURRENT_DATE(), INTERVAL look_back_window DAY)
      AND ticket_id IN (SELECT ticket_id FROM custom_field_ground_truth)
      AND ticket_id IN (SELECT id FROM tickets_created_in_look_back_window)
      -- ORDER BY ticket_id, created_datetime
  ),

  labelled_first_ticket_messages AS (
    SELECT
      custom_field_ground_truth.account_id,
      custom_field_ground_truth.ticket_id,
      custom_field_ground_truth.custom_field_id,
      custom_field_ground_truth.custom_field_label,
      custom_field_ground_truth.custom_field_value,
      first_ticket_messages.subject,
      first_ticket_messages.message_body,

      first_ticket_messages.via,
      first_ticket_messages.created_datetime,
      custom_field_ground_truth.labeling_datetime,

      custom_field_ground_truth.custom_field_is_required,
      custom_field_ground_truth.custom_field_input_type,
      first_ticket_messages.from_agent,
      first_ticket_messages.channel,
      first_ticket_messages.message_id,
    FROM first_ticket_messages
    LEFT JOIN custom_field_ground_truth
      ON custom_field_ground_truth.ticket_id = first_ticket_messages.ticket_id
      AND custom_field_ground_truth.account_id = first_ticket_messages.account_id
    WHERE TRUE
    AND first_ticket_messages.channel = "email"
    AND first_ticket_messages.from_agent IS FALSE
    AND custom_field_ground_truth.custom_field_label = "Contact Reason"
  )

SELECT * FROM labelled_first_ticket_messages
