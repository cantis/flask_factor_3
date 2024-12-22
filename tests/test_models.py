"""Tests for models.py."""

import inspect
from typing import Generator

import pytest
from flask import Flask, g
from flask.testing import FlaskClient

from app import create_app
from models import Player, create_db, get_session


@pytest.fixture(scope='module')
def test_app() -> Generator[FlaskClient, None, None]:
    """Fixture to provide a test application context."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client



