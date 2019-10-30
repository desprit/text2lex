"""
Application entry point.
"""
from app import app
from shared.config import API_PORT, DEBUG


if __name__ == "__main__":
    app.run(port=API_PORT, debug=DEBUG)
