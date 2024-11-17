"""Player services."""

from sqlmodel import Session, select

from models import Player


class PlayerNotFoundError(Exception):
    """Custom error for player not found."""

    def __init__(self, player_id: int) -> None:
        """Initialize the error."""
        super().__init__(f'Player with ID {player_id} not found.')
        self.player_id = player_id
        self.message = f'Player with ID {player_id} not found.'


class PlayerService:
    """Service for player operations."""

    def __init__(self, session: Session) -> None:
        """Initialize the service."""
        self.session = session

    def list_players(self) -> list[Player]:
        """List all players."""
        return self.session.exec(select(Player)).all()

    def add_player(self, player: Player) -> Player:
        """Add a new player."""
        self.session.add(player)
        self.session.commit()
        self.session.refresh(player)
        return player

    def get_player(self, player_id: int) -> Player:
        """Get a player by ID."""
        player = self.session.get(Player, player_id)
        if not player:
            raise PlayerNotFoundError(player_id)
        return player

    def update_player(self, player_id: int, player_data: Player) -> Player:
        """Update a player by ID."""
        player = self.session.get(Player, player_id)
        if not player:
            raise PlayerNotFoundError(player_id)
        for key, value in player_data.model_dump().items():
            setattr(player, key, value)
        self.session.commit()
        self.session.refresh(player)
        return player

    def delete_player(self, player_id: int) -> None:
        """Delete a player by ID."""
        player = self.session.get(Player, player_id)
        if not player:
            raise PlayerNotFoundError(player_id)
        self.session.delete(player)
        self.session.commit()
