import os

class Configuration:
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    PORT = int(os.environ.get("PORT", 3000))
    REGION = os.environ.get("REGION", "ap-south-1")
    LOCALSTACK_URL = os.environ.get("LOCALSTACK_URL", "http://localhost:4566")
