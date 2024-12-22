"""Character services."""

from sqlmodel import Session, select

from models import Campaign, Character, Player


class CharacterNotFoundError(Exception):
    """Custom error for character not found."""

    def __init__(self, character_id: int) -> None:
        """Initialize the error."""
        super().__init__(f'Character with ID {character_id} not found.')
        self.character_id = character_id
        self.message = f'Character with ID {character_id} not found.'


class CharacterService:
    """Service for character operations."""

    def __init__(self, session: Session) -> None:
        """Initialize the service."""
        self.session = session

    def list_characters(self) -> list[Character]:
        """List all characters with player and campaign info."""
        statement = (
            select(Character, Player.name.label("player_name"), Campaign.name.label("campaign_name"))
            .join(Player, Character.player_id == Player.id)
            .join(Campaign, Character.campaign_id == Campaign.id)
        )
        results = self.session.exec(statement).all()
        return results

    def list_characters_in_campaign(self, campaign_id: int) -> list[Character]:
        """List all characters in a campaign."""
        return self.session.exec(select(Character).where(Character.campaign_id == campaign_id)).all()

    def add_character(self, character: Character) -> Character:
        """Add a new character."""
        self.session.add(character)
        self.session.commit()
        self.session.refresh(character)
        return character

    def get_character(self, character_id: int) -> Character:
        """Get a character by ID."""
        character = self.session.get(Character, character_id)
        if not character:
            raise CharacterNotFoundError(character_id)
        return character

    def update_character(self, character_id: int, character_data: Character) -> Character:
        """Update a character by ID."""
        character = self.session.get(Character, character_id)
        if not character:
            raise CharacterNotFoundError(character_id)
        for key, value in character_data.model_dump().items():
            setattr(character, key, value)
        self.session.commit()
        self.session.refresh(character)
        return character

    def delete_character(self, character_id: int) -> None:
        """Delete a character by ID."""
        character = self.session.get(Character, character_id)
        if not character:
            raise CharacterNotFoundError(character_id)
        self.session.delete(character)
        self.session.commit()
