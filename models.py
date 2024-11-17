"""Database models."""

import os
from contextlib import contextmanager

from flask import g
from sqlmodel import Field, Session, SQLModel, create_engine

DATABASE_URL: str = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})


def create_db() -> None:
    """Create the database."""
    SQLModel.metadata.create_all(engine)

@contextmanager
def get_session():
    """Get a database session."""
    with Session(engine) as session:
        yield session


class Player(SQLModel, table=True):
    """Player model."""

    id: int | None = Field(primary_key=True, index=True)
    email: str
    password: str  # Fixed typo here
    name: str
    password_attempts: int
    reset_password: bool | None = False
    is_active: bool | None = True
