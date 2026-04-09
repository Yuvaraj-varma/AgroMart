# All settings live in app/core/config.py
# This file re-exports what db/ modules need
from app.core.config import settings

DATABASE_URL  = settings.DATABASE_URL
MONGODB_URL   = settings.MONGODB_URL
AGMARKNET_API_KEY = settings.AGMARKNET_API_KEY
AGMARKNET_URL = settings.AGMARKNET_URL
KAFKA_BOOTSTRAP   = settings.KAFKA_BOOTSTRAP
KAFKA_ORDER_TOPIC = settings.KAFKA_ORDER_TOPIC
