"""Character routes blueprint."""

from flask import Blueprint, jsonify, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField
from wtforms.validators import InputRequired

from models import Character, get_session
from services.character_service import CharacterService

characters_bp = Blueprint('characters', __name__)


class AddCharacterForm(FlaskForm):
    """Add character form."""
    character_name = StringField('Character Name', validators=[InputRequired('Character name is required')])
    player_id = IntegerField('Player ID', validators=[InputRequired('Player ID is required')])
    is_alive = BooleanField('Is Alive')
    campaign_id = IntegerField('Campaign ID', validators=[InputRequired('Campaign ID is required')])


class EditCharacterForm(FlaskForm):
    """Edit character form."""
    character_name = StringField('Character Name', validators=[InputRequired()])
    player_id = IntegerField('Player ID', validators=[InputRequired()])
    is_alive = BooleanField('Is Alive')
    campaign_id = IntegerField('Campaign ID', validators=[InputRequired()])


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
    return render_template('characters/character_add.html', form=AddCharacterForm())


@characters_bp.post('/characters')
def add_character() -> str:
    """Add a new character."""
    form = AddCharacterForm()
    if form.validate_on_submit():
        with get_session() as session:
            service = CharacterService(session)
            service.add_character(Character(**form.data))
            return redirect(url_for('characters.list_characters'))
    return render_template('characters/character_add.html', form=form)


@characters_bp.get('/characters/<int:character_id>/edit')
def edit_character_form(character_id: int) -> str:
    """Render the edit character form."""
    form = EditCharacterForm()
    with get_session() as session:
        service = CharacterService(session)
        character = service.get_character(character_id)
        if not character:
            return redirect(url_for('characters.list_characters'))

        form.character_name.data = character.character_name
        form.player_id.data = character.player_id
        form.is_alive.data = character.is_alive
        form.campaign_id.data = character.campaign_id
        return render_template('characters/character_edit.html', form=form, character=character)


@characters_bp.post('/characters/<int:character_id>')
def edit_character(character_id: int) -> str:
    """Update a character by ID."""
    form = EditCharacterForm()
    if form.validate_on_submit():
        with get_session() as session:
            service = CharacterService(session)
            service.update_character(character_id, Character(**form.data))
            return redirect(url_for('characters.list_characters'))
    return render_template('characters/character_edit.html', form=form)


@characters_bp.delete('/characters/<int:character_id>')
def delete_character(character_id: int) -> str:
    """Delete a character by ID."""
    with get_session() as session:
        service = CharacterService(session)
        service.delete_character(character_id)
        return jsonify({'success': True})
