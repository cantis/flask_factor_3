"""Campaign routes blueprint."""

from flask import Blueprint, jsonify, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField
from wtforms.validators import InputRequired

from models import Campaign, get_session
from services.campaign_service import CampaignService

campaigns_bp = Blueprint('campaigns', __name__)


class AddCampaignForm(FlaskForm):
    """Add campaign form."""
    name = StringField('Name', validators=[InputRequired('Name is required')])
    is_active = BooleanField('Active')


class EditCampaignForm(FlaskForm):
    """Edit campaign form."""
    name = StringField('Name', validators=[InputRequired()])
    is_active = BooleanField('Active')


@campaigns_bp.get('/campaigns')
def list_campaigns() -> str:
    """List all campaigns."""
    with get_session() as session:
        service = CampaignService(session)
        campaigns = service.list_campaigns()
        return render_template('campaigns/campaign_list.html', campaigns=campaigns)


@campaigns_bp.get('/campaigns/add')
def add_campaign_form() -> str:
    """Render the add campaign form."""
    return render_template('campaigns/campaign_add.html', form=AddCampaignForm())


@campaigns_bp.post('/campaigns')
def add_campaign() -> str:
    """Add a new campaign."""
    form = AddCampaignForm()
    if form.validate_on_submit():
        with get_session() as session:
            service = CampaignService(session)
            service.add_campaign(Campaign(**form.data))
            return redirect(url_for('campaigns.list_campaigns'))
    return render_template('campaigns/campaign_add.html', form=form)


@campaigns_bp.get('/campaigns/<int:campaign_id>/edit')
def edit_campaign_form(campaign_id: int) -> str:
    """Render the edit campaign form."""
    form = EditCampaignForm()
    with get_session() as session:
        service = CampaignService(session)
        campaign = service.get_campaign(campaign_id)
        if not campaign:
            return redirect(url_for('campaigns.list_campaigns'))

        form.name.data = campaign.name
        form.is_active.data = campaign.is_active
        return render_template('campaigns/campaign_edit.html', form=form, campaign=campaign)


@campaigns_bp.post('/campaigns/<int:campaign_id>')
def edit_campaign(campaign_id: int) -> str:
    """Update a campaign by ID."""
    form = EditCampaignForm()
    if form.validate_on_submit():
        with get_session() as session:
            service = CampaignService(session)
            service.update_campaign(campaign_id, Campaign(**form.data))
            return redirect(url_for('campaigns.list_campaigns'))
    return render_template('campaigns/campaign_edit.html', form=form)


@campaigns_bp.delete('/campaigns/<int:campaign_id>')
def delete_campaign(campaign_id: int) -> str:
    """Delete a campaign by ID."""
    with get_session() as session:
        service = CampaignService(session)
        service.delete_campaign(campaign_id)
        return jsonify({'success': True})
