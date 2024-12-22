"""Application entry point."""

import os

from dotenv import load_dotenv
from flask import Flask

from models import create_db
from routes.home import home_bp
from routes.players import players_bp
from routes.campaigns import campaigns_bp
from routes.characters import characters_bp

load_dotenv('.env')

def create_app() -> Flask:
    """Create a Flask application."""
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'very_secret_key')

    # Create the database
    create_db()

    # Register blueprints here
    app.register_blueprint(home_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(campaigns_bp)
    app.register_blueprint(characters_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
