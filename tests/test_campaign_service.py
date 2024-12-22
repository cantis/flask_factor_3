"""Tests for the campaign service."""

import pytest
from unittest.mock import MagicMock
from models import Campaign
from services.campaign_service import CampaignService

@pytest.fixture
def session():
    """Fixture for mocked database session."""
    return MagicMock()

@pytest.fixture
def service(session):
    """Fixture for campaign service."""
    return CampaignService(session)

def test_add_campaign(service: CampaignService, session):
    """Test adding a campaign."""
    # Arrange
    campaign = Campaign(name="Test Campaign", is_active=True)

    # Act
    result = service.add_campaign(campaign)

    # Assert
    session.add.assert_called_once_with(campaign)
    session.commit.assert_called_once()
    assert result.id is not None 
    assert result.is_active is True

def test_get_campaign(service: CampaignService, session):
    """Test getting a campaign."""
    # Arrange
    campaign = Campaign(id=1, name="Test Campaign", is_active=True)
    session.query().filter_by().first.return_value = campaign

    # Act
    result = service.get_campaign(campaign.id)

    # Assert
    assert result == campaign

def test_update_campaign(service: CampaignService, session):
    """Test updating a campaign."""
    # Arrange
    campaign = Campaign(id=1, name="Test Campaign", is_active=True)
    session.query().filter_by().first.return_value = campaign

    # Act
    campaign.name = "Updated Campaign"
    service.update_campaign(campaign.id, campaign)

    # Assert
    session.commit.assert_called_once()

def test_delete_campaign(service: CampaignService, session):
    """Test deleting a campaign."""
    # Arrange
    campaign = Campaign(id=1, name="Test Campaign", is_active=True)
    session.query().filter_by().first.return_value = campaign

    # Act
    service.delete_campaign(campaign.id)

    # Assert
    session.delete.assert_called_once_with(campaign)
    session.commit.assert_called_once()

def test_list_campaigns(service: CampaignService, session):
    """Test listing all campaigns."""
    # Arrange
    campaigns = [Campaign(id=1, name="Test Campaign 1", is_active=True), Campaign(id=2, name="Test Campaign 2", is_active=False)]
    session.query().all.return_value = campaigns

    # Act
    result = service.list_campaigns()

    # Assert
    assert result == campaigns
