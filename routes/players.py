"""Player routes blueprint."""

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import Email, InputRequired

from models import Player, get_session
from services.player_service import PlayerService

players_bp = Blueprint('players', __name__)


class AddPlayerForm(FlaskForm):
    """Add player form."""

    name = StringField('Name', validators=[InputRequired('Name is required')])
    email = StringField('Email', validators=[InputRequired('Email is required'), Email('Invalid email')])
    password = PasswordField('Password', validators=[InputRequired('Password is required')])


class EditPlayerForm(FlaskForm):
    """Edit player form."""

    email = StringField('Email', validators=[InputRequired(), Email()])
    name = StringField('Name', validators=[InputRequired()])
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password')
    password_attempts = StringField('Password Attempts', validators=[InputRequired()])
    reset_password = BooleanField('Reset Password')
    is_active = BooleanField('Active')


@players_bp.get('/players')
def list_players() -> str:
    """List all players."""
    with get_session() as session:
        service = PlayerService(session)
        players = service.list_players()
        return render_template('players/player_list.html', players=players)


@players_bp.get('/players/add')
def add_player_form() -> str:
    """Render the add player form."""
    return render_template('players/player_add.html', form=AddPlayerForm())


@players_bp.post('/players')
def add_player() -> str:
    """Add a new player."""
    form = AddPlayerForm()
    if form.validate_on_submit():
        with get_session() as session:
            service = PlayerService(session)
            service.add_player(Player(**form.data))
            return redirect(url_for('players.list_players'))
    return render_template('players/player_add.html', form=form)


@players_bp.get('/players/<int:player_id>')
def get_player(player_id: int) -> str:
    """Get a player by ID."""
    with get_session() as session:
        service = PlayerService(session)
        player = service.get_player(player_id)
        return jsonify(player)


@players_bp.get('/players/<int:player_id>/edit')
def edit_player_form(player_id: int) -> str:
    """Render the edit player form."""
    form = EditPlayerForm()
    with get_session() as session:
        service = PlayerService(session)
        player = service.get_player(player_id)
        if not player:
            return redirect(url_for('players.list_players'))

        form.email.data = player.email
        form.name.data = player.name
        form.password_attempts.data = player.password_attempts
        form.reset_password.data = player.reset_password
        form.is_active.data = player.is_active
        return render_template('players/player_edit.html', form=form, player=player)


@players_bp.post('/players/<int:player_id>')
def edit_player(player_id: int) -> str:
    """Update a player by ID."""
    form = EditPlayerForm()
    if form.validate_on_submit():
        data = form.data
        player_data = {
            'email': data['email'],
            'name': data['name'],
            'current_password': data['current_password'],
            'new_password': data['new_password'],
            'password_attempts': int(data['password_attempts']),
            'reset_password': 'reset_password' in data,
            'is_active': 'is_active' in data,
        }
        with get_session() as session:
            service = PlayerService(session)
            service.update_player(player_id, Player(**player_data))
            return redirect(url_for('players.list_players'))
    return jsonify({'error': 'Invalid request'}), 400


@players_bp.delete('/players/<int:player_id>')
def delete_player(player_id: int) -> str:
    """Delete a player by ID."""
    with get_session() as session:
        service = PlayerService(session)
        service.delete_player(player_id)
        return jsonify({'success': True})
