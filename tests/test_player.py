"""Tests for player routes."""

from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlmodel import Session

from app import create_app
from models import Player, create_db, get_session
from services.player_service import PlayerService


@pytest.fixture(scope='module')
def client() -> Generator[FlaskClient, None, None]:
    """Fixture to provide a test application context."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        create_db()
        yield client


@pytest.fixture(scope='module')
def db_session(client: Flask):
    """Fixture to provide a database session."""
    with get_session() as session:
        yield session


def test_list_players(client: FlaskClient, db_session: Session) -> None:
    """Test listing players."""
    # Arrange
    service = PlayerService(db_session)
    service.add_player(Player(email='test1@example.com', password='password', name='Test User 1'))
    service.add_player(Player(email='test2@example.com', password='password', name='Test User 2'))

    # Act
    response = client.get('/players')

    # Assert
    assert response.status_code == 200
    assert b'Test User 1' in response.data
    assert b'Test User 2' in response.data


def test_add_player(client: FlaskClient) -> None:
    """Test adding a player."""
    # Arrange
    data = {'name': 'New Player', 'email': 'newplayer@example.com', 'password': 'password'}

    # Act
    response = client.post('/players', data=data, follow_redirects=True)

    # Assert
    assert response.status_code == 200
    assert b'New Player' in response.data


def test_edit_player(client: FlaskClient, db_session: Session) -> None:
    """Test editing a player."""
    # Arrange
    service = PlayerService(db_session)
    player = service.add_player(Player(email='edit@example.com', password='password', name='Edit User'))
    data = {
        'email': 'edited@example.com',
        'name': 'Edited User',
        'current_password': 'password',
        'new_password': 'newpassword',
        'password_attempts': '0',
        'reset_password': 'false',
        'is_active': 'true',
    }

    # Act
    response = client.post(f'/players/{player.id}', data=data, follow_redirects=True)

    # Assert
    assert response.status_code == 200
    assert b'Edited User' in response.data


def test_delete_player(client: FlaskClient, db_session: Session) -> None:
    """Test deleting a player."""
    # Arrange
    service = PlayerService(db_session)
    player = service.add_player(Player(email='delete@example.com', password='password', name='Delete User'))

    # Act
    response = client.delete(f'/players/{player.id}', follow_redirects=True)

    # Assert
    assert response.status_code == 200
    assert b'success' in response.data
