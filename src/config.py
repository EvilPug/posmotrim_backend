import os
from dotenv import load_dotenv


if not load_dotenv():
    raise Exception('.env file not found! Please create it in src folder!')

DB_USER = os.environ.get('DB_USER', default='postgres')
DB_PASS = os.environ.get('DB_PASS', default='postgres')
DB_HOST = os.environ.get('DB_HOST', default='localhost')
DB_PORT = os.environ.get('DB_PORT', default=5432)
DB_NAME = os.environ.get('DB_NAME', default=5432)

SECRET = os.environ.get('SECRET', default='super_secret')

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
