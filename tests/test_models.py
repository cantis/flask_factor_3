"""Tests for models.py."""

import inspect

import pytest
from flask import Flask, g

from models import Player, create_db, get_db_session, shutdown_db_session


@pytest.fixture(scope='module')
def test_app() -> Flask:
    """Fixture to provide a test application context."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    with app.app_context():
        yield app

def test_get_db_session(test_app: Flask) -> None:
    """Test get_db_session function."""
    # Arrange
    g.db_session = None

    # Act
    session = get_db_session()

    # Assert
    assert session is not None
    assert 'db_session' in g

def test_shutdown_db_session(test_app: Flask) -> None:
    """Test shutdown_db_session function."""
    # Arrange
    g.db_session = get_db_session()

    # Act
    shutdown_db_session()

    # Assert
    assert 'db_session' not in g

def test_create_db(test_app: Flask) -> None:
    """Test create_db function."""
    # Act
    create_db()

    # Assert
    engine = test_app.extensions['sqlalchemy'].db.engine
    assert inspect.isclass(Player)
    assert inspect.isfunction(create_db)
    assert Player.__table__.exists(bind=engine)

def test_player_model(test_app: Flask) -> None:
    """Test Player model."""
    # Arrange
    session = get_db_session()
    new_player = Player(email='test@example.com', password='password', name='Test User')

    # Act
    session.add(new_player)
    session.commit()
    retrieved_player = session.query(Player).filter_by(email='test@example.com').first()

    # Assert
    assert retrieved_player is not None
    assert retrieved_player.email == 'test@example.com'
    assert retrieved_player.name == 'Test User'
