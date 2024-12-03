import logging
from typing import Type

from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src import PROJECT_ENVS

logger = logging.getLogger(__name__)


class BaseRepository:
    def __init__(self, db_session: Session, model_schema: BaseModel, model_table: Type):
        self.db_session = db_session
        self.model_table = model_table
        self.model_schema = model_schema

    def alembic_to_pydantic(self, db_record: Type):
        if not db_record:
            return db_record
        if isinstance(db_record, list):
            return [self.model_schema.model_validate(record) for record in db_record]

        return self.model_schema.model_validate(db_record)

    def create(self, data: BaseModel) -> BaseModel:
        try:
            db_record = self.model_table(**data.model_dump())
            self.db_session.add(db_record)
            self.db_session.commit()
            return data
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred: {e}", extra={"error": e}, exc_info=PROJECT_ENVS.DEBUG)
            self.db_session.rollback()
            return None

    def read(self, _id: str) -> BaseModel:
        try:
            db_record = self.db_session.query(self.model_table).filter(self.model_table.id == _id).first()
            return self.alembic_to_pydantic(db_record)
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred: {e}", extra={"error": e}, exc_info=PROJECT_ENVS.DEBUG)
            return None

    def update(self, _id: str, data: BaseModel | dict, fields: list[str] = None) -> BaseModel:
        try:
            db_record = self.db_session.query(self.model_table).filter(self.model_table.id == _id).first()
            if db_record:
                default_fields = []
                if isinstance(data, BaseModel):
                    data = data.model_dump()
                    default_fields = [x for x in data.keys()]
                fields = fields or default_fields

                for field, value in data.items():
                    if field in fields and hasattr(db_record, field):
                        setattr(db_record, field, value)
                self.db_session.commit()
                return self.alembic_to_pydantic(db_record)
            return None
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred: {e}", extra={"error": e}, exc_info=PROJECT_ENVS.DEBUG)
            self.db_session.rollback()
            return None

    def delete(self, _id: str) -> int:
        try:
            row_count = self.db_session.query(self.model_table).filter(self.model_table.id == _id).delete()
            self.db_session.commit()
            return row_count
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred: {e}", extra={"error": e}, exc_info=PROJECT_ENVS.DEBUG)
            self.db_session.rollback()
            return 0
