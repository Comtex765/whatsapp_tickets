from os import getenv

from dotenv import load_dotenv

load_dotenv()

DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")

ENV = getenv("ENV", "development")
PORT = int(getenv("PORT", 8000))
META_HUB_TOKEN = getenv("META_HUB_TOKEN", "")

IS_PROD = ENV == "production"

API_TITLE = "Webhook WhatsApp"
API_VERSION = "1.0.0"

# URLs de documentación
DOCS_URL = None if IS_PROD else "/docs"
REDOC_URL = None if IS_PROD else "/redoc"
OPENAPI_URL = None if IS_PROD else "/openapi.json"


SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}" f"@[{DB_HOST}]:{DB_PORT}/{DB_NAME}"
)
