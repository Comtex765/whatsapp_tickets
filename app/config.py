from os import getenv

from dotenv import load_dotenv

load_dotenv()

DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")


print(f"el host es {DB_HOST}")
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}" f"@[{DB_HOST}]:{DB_PORT}/{DB_NAME}"
)
