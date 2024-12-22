"""Character routes blueprint."""

from flask import Blueprint, jsonify, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField
from wtforms.validators import InputRequired

from models import Campaign, Character, Player, get_session
from services.campaign_service import CampaignService
from services.character_service import CharacterService
from services.player_service import PlayerService

characters_bp = Blueprint('characters', __name__)


class AddCharacterForm(FlaskForm):
    """Add character form."""
    character_name = StringField('Character Name', validators=[InputRequired('Character name is required')])
    player_id = SelectField('Player', validators=[InputRequired('Player is required')], coerce=int)
    campaign_id = SelectField('Campaign', validators=[InputRequired('Campaign is required')], coerce=int)
    is_alive = BooleanField('Is Alive', default=True)


class EditCharacterForm(FlaskForm):
    """Edit character form."""
    character_name = StringField('Character Name', validators=[InputRequired()])
    player_id = SelectField('Player', validators=[InputRequired()], coerce=int)
    campaign_id = SelectField('Campaign', validators=[InputRequired()], coerce=int)
    is_alive = BooleanField('Is Alive')


@characters_bp.get('/characters')
def list_characters() -> str:
    """List all characters."""
    with get_session() as session:
        service = CharacterService(session)
        characters = service.list_characters()
        return render_template('characters/character_list.html', characters=characters)


@characters_bp.get('/characters/add')
def add_character_form() -> str:
    """Render the add character form."""
    form = AddCharacterForm()
    with get_session() as session:
        # Get players and campaigns for dropdowns
        player_service = PlayerService(session)
        campaign_service = CampaignService(session)
        players = player_service.list_players()
        campaigns = campaign_service.list_campaigns()

        form.player_id.choices = [(p.id, p.name) for p in players]
        form.campaign_id.choices = [(c.id, c.name) for c in campaigns]

    return render_template('characters/character_add.html', form=form)


@characters_bp.post('/characters')
def add_character() -> str:
    """Add a new character."""
    form = AddCharacterForm()
    with get_session() as session:
        # Populate choices for validation
        player_service = PlayerService(session)
        campaign_service = CampaignService(session)
        players = player_service.list_players()
        campaigns = campaign_service.list_campaigns()

        form.player_id.choices = [(p.id, p.name) for p in players]
        form.campaign_id.choices = [(c.id, c.name) for c in campaigns]

        if form.validate_on_submit():
            # Clean form data before creating character
            character_data = {
                'character_name': form.character_name.data,
                'player_id': form.player_id.data,
                'campaign_id': form.campaign_id.data,
                'is_alive': form.is_alive.data
            }
            service = CharacterService(session)
            service.add_character(Character(**character_data))
            return redirect(url_for('characters.list_characters'))

    return render_template('characters/character_add.html', form=form)


@characters_bp.get('/characters/<int:character_id>/edit')
def edit_character_form(character_id: int) -> str:
    """Render the edit character form."""
    form = EditCharacterForm()
    with get_session() as session:
        service = CharacterService(session)
        player_service = PlayerService(session)
        campaign_service = CampaignService(session)

        # Get current character
        character = service.get_character(character_id)
        if not character:
            return redirect(url_for('characters.list_characters'))

        # Populate choices
        players = player_service.list_players()
        campaigns = campaign_service.list_campaigns()
        form.player_id.choices = [(p.id, p.name) for p in players]
        form.campaign_id.choices = [(c.id, c.name) for c in campaigns]

        # Set form data
        form.character_name.data = character.character_name
        form.player_id.data = character.player_id
        form.campaign_id.data = character.campaign_id
        form.is_alive.data = character.is_alive
        return render_template('characters/character_edit.html', form=form, character=character)


@characters_bp.post('/characters/<int:character_id>')
def edit_character(character_id: int) -> str:
    """Update a character by ID."""
    form = EditCharacterForm()
    with get_session() as session:
        # Populate choices for validation
        player_service = PlayerService(session)
        campaign_service = CampaignService(session)
        players = player_service.list_players()
        campaigns = campaign_service.list_campaigns()

        form.player_id.choices = [(p.id, p.name) for p in players]
        form.campaign_id.choices = [(c.id, c.name) for c in campaigns]

        if form.validate_on_submit():
            service = CharacterService(session)
            character_data = {
                'character_name': form.character_name.data,
                'player_id': form.player_id.data,
                'campaign_id': form.campaign_id.data,
                'is_alive': form.is_alive.data
            }
            service.update_character(character_id, Character(**character_data))
            return redirect(url_for('characters.list_characters'))

        return render_template('characters/character_edit.html', form=form, character={'id': character_id})


@characters_bp.delete('/characters/<int:character_id>')
def delete_character(character_id: int) -> str:
    """Delete a character by ID."""
    with get_session() as session:
        service = CharacterService(session)
        service.delete_character(character_id)
        return jsonify({'success': True})
