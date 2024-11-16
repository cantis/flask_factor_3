"""Player routes blueprint."""

from flask import Blueprint, jsonify, render_template, request

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

@players_bp.route('/players', methods=['POST'])
def add_player() -> str:
    """Add a new player."""
    data = request.json
    with get_session() as session:
        service = PlayerService(session)
        player = service.add_player(data)
        return jsonify(player)

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
