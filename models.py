"""Database models."""

import os
from contextlib import contextmanager
from typing import Generator, List, Optional

from sqlmodel import Field, Session, SQLModel, create_engine, Relationship


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


class Campaign(SQLModel, table=True):
    """Campaign model."""
    id: int | None = Field(default=None, primary_key=True)
    name: str
    is_active: bool = True
    characters: List["Character"] = Relationship(back_populates="campaign")


class Character(SQLModel, table=True):
    """Character model."""
    id: int | None = Field(default=None, primary_key=True)
    character_name: str
    player_id: int = Field(foreign_key="player.id")
    is_alive: bool = True
    campaign_id: int = Field(foreign_key="campaign.id")
    player: "Player" = Relationship(back_populates="characters")
    campaign: "Campaign" = Relationship(back_populates="characters")


class Player(SQLModel, table=True):
    """Player model."""

    id: int | None = Field(primary_key=True, index=True)
    email: str
    password: str
    name: str
    password_attempts: int | None = 0
    reset_password: bool | None = False
    is_active: bool | None = True
    characters: List["Character"] = Relationship(back_populates="player")
