import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")
SERVICE_PORT = os.getenv("SERVICE_PORT", 8000)

# Document storage configuration
DOCUMENT_STORAGE_PATH = os.getenv("DOCUMENT_STORAGE_PATH", os.path.join(os.getcwd(), "storage", "documents"))
try:
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 10))
except Exception:
    MAX_FILE_SIZE_MB = 10
