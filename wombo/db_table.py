import logging
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean

from wombo.database import drop_table_if_exists, DB_ENGINE, DatabaseSession, DatabaseRecord

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UserWithoutURLRecord(DatabaseRecord):
    __tablename__ = "users"

    id = Column(String, primary_key=True, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    profile_bio = Column(String, nullable=True)
    website_link = Column(String, nullable=True)
    is_public = Column(Boolean, default=True, nullable=False)
    is_flagged = Column(Boolean, default=False, nullable=False)

    def key(self):
        return self.id, self.username

    def __hash__(self):
        return hash(self.key())

    def __eq__(self, other):
        if isinstance(other, UserWithoutURLRecord):
            return self.key() == other.key()
        return NotImplemented


def create_clean_table_if_needed():
    drop_table_if_exists(DB_ENGINE, UserWithoutURLRecord.__tablename__)
    DatabaseRecord.metadata.create_all(
        DB_ENGINE,
        tables=[UserWithoutURLRecord.__table__])
    with DatabaseSession() as db:
        # Just to ensure everything is clean
        db.query(UserWithoutURLRecord).delete(synchronize_session=False)
        db.commit()
    logger.info("Created UserWithoutURLRecord table")

    user_without_profile_bio = add_user_record(UserWithoutURLRecord(
        id="1",
        username="1",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    ))


def add_user_record(row: UserWithoutURLRecord):
    with DatabaseSession() as db:
        print(f"Inserting user : {row}")
        db.add(row)
        db.commit()
        db.refresh(row)
        return row



