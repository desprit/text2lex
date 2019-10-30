"""
Redis settings.
"""
import os

REDIS_PASSWORD = os.environ.get("REDIS_PASS")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
QUEUES = ["low"]