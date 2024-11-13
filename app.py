"""Application entry point."""

from flask import Flask

from routes.home import home_bp


def create_app() -> Flask:
    """Create a Flask application."""
    app = Flask(__name__)

    # Register blueprints here
    app.register_blueprint(home_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
