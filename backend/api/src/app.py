"""
Flask application fabric.
"""
from flask import Flask

from shared.config import API_SECRET


app = Flask(__name__)
app.config["SECRET_KEY"] = API_SECRET

# pylint: disable=wrong-import-position,unused-import
from views.authentication import authentication
