import json
import re
import xml.etree.ElementTree as ET
from typing import Optional, Union

import markdown  # type: ignore
from bs4 import BeautifulSoup


class TextUtils:
    """A class for handling various text processing operations."""

    @staticmethod
    def sanitize(text: str) -> str:
        """Remove null characters and control characters from text."""
        sanitized = text.replace("\u0000", "")
        return re.sub(r"[\x00-\x1F\x7F]", "", sanitized)

    @staticmethod
    def to_xml(item_type: str, items: list[dict[str, str]]) -> str:
        """Convert a list of dictionaries to XML format."""
        root = ET.Element("Items")
        for item in items:
            item_element = ET.SubElement(root, item_type)
            for key, value in item.items():
                element = ET.SubElement(item_element, key)
                element.text = str(value)

        return ET.tostring(root, encoding="unicode", method="xml")

    @staticmethod
    def fill_template(
        template: str,
        replacements: list[tuple[str, Union[str, list, dict, None]]],
    ) -> str:
        """Fill a template string with provided replacements."""
        for source, target in replacements:
            if target is None:
                target = "null"
            elif isinstance(target, (dict, list)):
                target = json.dumps(target)

            template = template.replace(source, str(target))

        return template

    @staticmethod
    def dict_to_string(data: dict) -> str:
        """Convert a dictionary to a formatted string representation."""
        def format_value(value: Union[list, dict, str]) -> str:
            if isinstance(value, list):
                return f"[{', '.join(format_value(item) for item in value)}]"
            elif isinstance(value, dict):
                return self.dict_to_string(value)
            return str(value)

        return " | ".join(f"{key}: {format_value(value)}" for key, value in data.items())

    @staticmethod
    def find_substring(text: str, substring: str) -> tuple[Optional[int], Optional[int]]:
        """Find the start and end positions of a substring in text."""
        start_index = text.find(substring)
        if start_index == -1:
            return None, None
        return start_index, start_index + len(substring)

    @staticmethod
    def markdown_to_plain_text(markdown_text: str) -> str:
        """Convert markdown text to plain text."""
        html = markdown.markdown(markdown_text)
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text()
