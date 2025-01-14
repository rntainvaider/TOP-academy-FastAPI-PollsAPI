from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os

_ = load_dotenv()

username = os.getenv("username")
password = os.getenv("password")
localhost = os.getenv("localhost")
port = os.getenv("port")
db_name = os.getenv("db_name")

DATABASE_URL = (
    f"postgresql+psycopg2://{username}:{password}@{localhost}:{port}/{db_name}"
)

engine = create_engine(DATABASE_URL)

# Сессия для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
