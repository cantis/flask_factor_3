"""Player routes blueprint."""

from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from models import Player, get_session
from services.player_service import PlayerService

players_bp = Blueprint('players', __name__)

@players_bp.route('/players', methods=['GET'])
def list_players() -> str:
    """List all players."""
    with get_session() as session:
        service = PlayerService(session)
        players = service.list_players()
        return render_template('players/list.html', players=players)

@players_bp.route('/players/add', methods=['GET'])
def add_player_form() -> str:
    """Render the add player form."""
    return render_template('players/add_player.html')

@players_bp.route('/players', methods=['POST'])
def add_player() -> str:
    """Add a new player."""
    data = request.form
    if data['password'] != data['confirm_password']:
        return jsonify({'error': 'Passwords do not match'}), 400
    player_data = {
        'email': data['email'],
        'name': data['name'],
        'password': data['password'],
        'password_attempts': 0,
        'reset_password': False,
        'is_active': True,
    }
    with get_session() as session:
        service = PlayerService(session)
        service.add_player(Player(**player_data))
        return redirect(url_for('players.list_players'))

@players_bp.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id: int) -> str:
    """Get a player by ID."""
    with get_session() as session:
        service = PlayerService(session)
        player = service.get_player(player_id)
        return jsonify(player)

@players_bp.route('/players/<int:player_id>', methods=['PUT'])
def update_player(player_id: int) -> str:
    """Update a player by ID."""
    data = request.json
    with get_session() as session:
        service = PlayerService(session)
        player = service.update_player(player_id, data)
        return jsonify(player)

@players_bp.route('/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id: int) -> str:
    """Delete a player by ID."""
    with get_session() as session:
        service = PlayerService(session)
        service.delete_player(player_id)
        return '', 204
