"""Tests for the character service."""

import pytest
from unittest.mock import MagicMock
from models import Character
from services.character_service import CharacterService

@pytest.fixture
def session():
    """Fixture for mocked database session."""
    return MagicMock()

@pytest.fixture
def service(session):
    """Fixture for character service."""
    return CharacterService(session)

def test_add_character(service: CharacterService, session):
    """Test adding a character."""
    # Arrange
    character = Character(name="Test Character", class_="Warrior", level=1)

    # Act
    service.add_character(character)

    # Assert
    session.add.assert_called_once_with(character)
    session.commit.assert_called_once()

def test_get_character(service: CharacterService, session):
    """Test getting a character."""
    # Arrange
    character = Character(id=1, name="Test Character", class_="Warrior", level=1)
    session.query().filter_by().first.return_value = character

    # Act
    result = service.get_character(character.id)

    # Assert
    assert result == character

def test_update_character(service: CharacterService, session):
    """Test updating a character."""
    # Arrange
    character = Character(id=1, name="Test Character", class_="Warrior", level=1)
    session.query().filter_by().first.return_value = character

    # Act
    character.name = "Updated Character"
    service.update_character(character.id, character)

    # Assert
    session.commit.assert_called_once()

def test_delete_character(service: CharacterService, session):
    """Test deleting a character."""
    # Arrange
    character = Character(id=1, name="Test Character", class_="Warrior", level=1)
    session.query().filter_by().first.return_value = character

    # Act
    service.delete_character(character.id)

    # Assert
    session.delete.assert_called_once_with(character)
    session.commit.assert_called_once()
