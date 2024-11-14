"""Application entry point."""

from dotenv import load_dotenv
from flask import Flask

from models import create_db, shutdown_db_session
from routes.home import home_bp

load_dotenv('.env')

def create_app() -> Flask:
    """Create a Flask application."""
    app = Flask(__name__)

    # Create the database
    create_db()

    # Register blueprints here
    app.register_blueprint(home_bp)

    # Teardown app context
    app.teardown_appcontext(shutdown_db_session)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
