"""Player services."""

from typing import Any, dict, list

from sqlmodel import Session

from models import Player


class PlayerService:
    """Service for player operations."""

    def __init__(self, session: Session) -> None:
        """Initialize the service."""
        self.session = session

    def list_players(self) -> list[dict[str, Any]]:
        """List all players."""
        players = self.session.query(Player).all()
        return [player.dict() for player in players]

    def add_player(self, data: dict[str, Any]) -> dict[str, Any]:
        """Add a new player."""
        player = Player(**data)
        self.session.add(player)
        self.session.commit()
        self.session.refresh(player)
        return player.dict()

    def get_player(self, player_id: int) -> dict[str, Any]:
        """Get a player by ID."""
        player = self.session.get(Player, player_id)
        return player.dict()

    def update_player(self, player_id: int, data: dict[str, Any]) -> dict[str, Any]:
        """Update a player by ID."""
        player = self.session.get(Player, player_id)
        for key, value in data.items():
            setattr(player, key, value)
        self.session.commit()
        self.session.refresh(player)
        return player.dict()

    def delete_player(self, player_id: int) -> None:
        """Delete a player by ID."""
        player = self.session.get(Player, player_id)
        self.session.delete(player)
        self.session.commit()
