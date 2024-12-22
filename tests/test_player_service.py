"""Tests for PlayerService."""

from unittest.mock import MagicMock

import pytest
from sqlmodel import Session

from models import Player
from services.player_service import PlayerNotFoundError, PlayerService


@pytest.fixture
def mock_session() -> MagicMock:
    """Fixture for mocking the database session."""
    return MagicMock(spec=Session)


@pytest.fixture
def player_service(mock_session: MagicMock) -> PlayerService:
    """Fixture for providing a PlayerService instance."""
    return PlayerService(session=mock_session)


def test_list_players(player_service: PlayerService, mock_session: MagicMock) -> None:
    """Test listing all players."""
    # Arrange
    mock_session.exec.return_value.all.return_value = [Player(id=1, name='John Doe', email='john@example.com')]

    # Act
    players = player_service.list_players()

    # Assert
    assert len(players) == 1
    assert players[0].name == 'John Doe'


def test_add_player(player_service: PlayerService, mock_session: MagicMock) -> None:
    """Test adding a new player."""
    # Arrange
    new_player = Player(name='Jane Doe', email='jane@example.com')
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    # Act
    player = player_service.add_player(new_player)

    # Assert
    mock_session.add.assert_called_once_with(new_player)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(new_player)
    assert player == new_player


def test_get_player(player_service: PlayerService, mock_session: MagicMock) -> None:
    """Test getting a player by ID."""
    # Arrange
    player_id = 1
    mock_session.get.return_value = Player(id=player_id, name='John Doe', email='john@example.com')

    # Act
    player = player_service.get_player(player_id)

    # Assert
    assert player.id == player_id
    assert player.name == 'John Doe'


def test_get_player_not_found(player_service: PlayerService, mock_session: MagicMock) -> None:
    """Test getting a player by ID when not found."""
    # Arrange
    player_id = 1
    mock_session.get.return_value = None

    # Act & Assert
    with pytest.raises(PlayerNotFoundError):
        player_service.get_player(player_id)


def test_update_player(player_service: PlayerService, mock_session: MagicMock) -> None:
    """Test updating a player by ID."""
    # Arrange
    player_id = 1
    existing_player = Player(id=player_id, name='John Doe', email='john@example.com')
    updated_data = Player(name='John Smith', email='johnsmith@example.com')
    mock_session.get.return_value = existing_player

    # Act
    updated_player = player_service.update_player(player_id, updated_data)

    # Assert
    assert updated_player.name == 'John Smith'
    assert updated_player.email == 'johnsmith@example.com'


def test_update_player_not_found(player_service: PlayerService, mock_session: MagicMock) -> None:
    """Test updating a player by ID when not found."""
    # Arrange
    player_id = 1
    updated_data = Player(name='John Smith', email='johnsmith@example.com')
    mock_session.get.return_value = None

    # Act & Assert
    with pytest.raises(PlayerNotFoundError):
        player_service.update_player(player_id, updated_data)


def test_delete_player(player_service: PlayerService, mock_session: MagicMock) -> None:
    """Test deleting a player by ID."""
    # Arrange
    player_id = 1
    mock_session.get.return_value = Player(id=player_id, name='John Doe', email='john@example.com')

    # Act
    player_service.delete_player(player_id)

    # Assert
    mock_session.delete.assert_called_once()
    mock_session.commit.assert_called_once()


def test_delete_player_not_found(player_service: PlayerService, mock_session: MagicMock) -> None:
    """Test deleting a player by ID when not found."""
    # Arrange
    player_id = 1
    mock_session.get.return_value = None

    # Act & Assert
    with pytest.raises(PlayerNotFoundError):
        player_service.delete_player(player_id)
