"""Campaign services."""

from sqlmodel import Session, select

from models import Campaign


class CampaignNotFoundError(Exception):
    """Custom error for campaign not found."""

    def __init__(self, campaign_id: int) -> None:
        """Initialize the error."""
        super().__init__(f'Campaign with ID {campaign_id} not found.')
        self.campaign_id = campaign_id
        self.message = f'Campaign with ID {campaign_id} not found.'


class CampaignService:
    """Service for campaign operations."""

    def __init__(self, session: Session) -> None:
        """Initialize the service."""
        self.session = session

    def list_campaigns(self) -> list[Campaign]:
        """List all campaigns."""
        return self.session.exec(select(Campaign)).all()

    def add_campaign(self, campaign: Campaign) -> Campaign:
        """Add a new campaign."""
        self.session.add(campaign)
        self.session.commit()
        self.session.refresh(campaign)
        return campaign

    def get_campaign(self, campaign_id: int) -> Campaign:
        """Get a campaign by ID."""
        campaign = self.session.get(Campaign, campaign_id)
        if not campaign:
            raise CampaignNotFoundError(campaign_id)
        return campaign

    def update_campaign(self, campaign_id: int, campaign_data: Campaign) -> Campaign:
        """Update a campaign by ID."""
        campaign = self.session.get(Campaign, campaign_id)
        if not campaign:
            raise CampaignNotFoundError(campaign_id)
        for key, value in campaign_data.model_dump().items():
            setattr(campaign, key, value)
        self.session.commit()
        self.session.refresh(campaign)
        return campaign

    def delete_campaign(self, campaign_id: int) -> None:
        """Delete a campaign by ID."""
        campaign = self.session.get(Campaign, campaign_id)
        if not campaign:
            raise CampaignNotFoundError(campaign_id)
        self.session.delete(campaign)
        self.session.commit()
