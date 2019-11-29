"""
Flask application fabric.
"""
from flask import Flask

from shared.config import API_SECRET
from views.authentication.authentication import bp as auth_bp
from views.upload.upload import bp as upload_bp
from views.history.history import bp as history_bp


app = Flask(__name__)
app.config["SECRET_KEY"] = API_SECRET

app.register_blueprint(auth_bp, url_prefix="/v1/api")
app.register_blueprint(upload_bp, url_prefix="/v1/api")
app.register_blueprint(history_bp, url_prefix="/v1/api")
