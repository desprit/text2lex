"""
Project config.
"""
import os
import logging
from logging.handlers import RotatingFileHandler

DEBUG = os.environ.get("DEBUG") in ["True", "1", 1, True]
API_SECRET = "c2bf3686-a81e-496b-b75e-7ae79f9fa311"

API_PORT = os.environ.get("API_PORT", 3031)

# PostgreSQL credentials
POSTGRES_USER = os.environ.get("POSTGRES_USER", "text2lex")
POSTGRES_PASS = os.environ.get("POSTGRES_PASSWORD", "text2lex")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.environ.get("POSTGRES_PORT", 5432))
POSTGRES_NAME = os.environ.get("POSTGRES_NAME", "text2lex")
POSTGRES_NAME_TEST = os.environ.get("POSTGRES_NAME_TEST", "text2lex_test")

# Redis settings
REDIS_HOST = os.environ.get("REDIS_HOST", "text2lex_redis")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_PASS = os.environ.get("REDIS_PASS")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_SERVICE_ROOT = os.path.join(PROJECT_ROOT, "backend/api/src")
NLP_SERVICE_ROOT = os.path.join(PROJECT_ROOT, "backend/nlp/src")

# Logging
logger = logging.getLogger("text2lex")
logger.setLevel(logging.DEBUG)

logging_path = os.environ.get("LOG_PATH", "/var/log/text2lex")
debug_log = "{}/debug.log".format(logging_path)
error_log = "{}/errors.log".format(logging_path)

fh = logging.FileHandler(debug_log)
ch = logging.FileHandler(error_log)
fh.setLevel(logging.DEBUG)
ch.setLevel(logging.ERROR)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)

log_handler = RotatingFileHandler(debug_log)
