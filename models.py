"""Database models."""

import os
from contextlib import contextmanager

from flask import g
from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()
DATABASE_URL: str = os.getenv('DATABASE_URL')
engine = create_engine(url=DATABASE_URL, echo=True)


class Player(Base):
    """Player model."""

    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    password_attempts = Column(Integer, default=0)
    reset_password = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)


def create_db() -> None:
    """Create the database."""
    Base.metadata.create_all(engine)


@contextmanager
def get_session() -> scoped_session:
    """Provide a transactional scope around a series of operations."""
    session = scoped_session(sessionmaker(bind=engine))
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.remove()


def get_db_session() -> scoped_session:
    """Get a scoped session."""
    if 'db_session' not in g:
        g.db_session = scoped_session(sessionmaker(bind=engine))
    return g.db_session


def shutdown_db_session(exception: Exception = None) -> None:
    """Shutdown the database session."""
    db_session = g.pop('db_session', None)
    if db_session is not None:
        db_session.remove()
