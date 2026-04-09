from dotenv import load_dotenv
import os

load_dotenv()

# PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

# MongoDB
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")

# JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Agmarknet
AGMARKNET_API_KEY = os.getenv("AGMARKNET_API_KEY")
AGMARKNET_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

# Kafka
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
KAFKA_ORDER_TOPIC = os.getenv("KAFKA_ORDER_TOPIC", "order-topic")
