"""Home route blueprint."""

from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home() -> str:
    """Home route."""
    return render_template('home/home.html')
