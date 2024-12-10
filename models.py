"""Database models."""

import os
from contextlib import contextmanager
from typing import Generator

from sqlmodel import Field, Session, SQLModel, create_engine


def create_db(database_url: str = None) -> None:
    """Create the database."""
    if database_url is None:
        database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url)
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session(database_url: str = None) -> Generator[Session, None, None]:
    """Get a database session."""
    if database_url is None:
        database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url)
    with Session(engine) as session:
        yield session


class Player(SQLModel, table=True):
    """Player model."""

    id: int | None = Field(primary_key=True, index=True)
    email: str
    password: str  # Fixed typo here
    name: str
    password_attempts: int | None = 0
    reset_password: bool | None = False
    is_active: bool | None = True
