from sqlalchemy import Column, ForeignKey, String, Integer, MetaData
from sqlalchemy.ext.declarative import declarative_base
from database.database import engine

Base = declarative_base()

metadata = MetaData()  # Управление схемой базы данных


class Poll(Base):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String(255), unique=True, nullable=False)
    creator_username = Column(
        String(50), nullable=False
    )  # Пользователь, создавший опрос


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(
        String(50), unique=True, nullable=False
    )  # Пользователь, проголосовавший
    poll_id = Column(Integer, ForeignKey("polls.id"), unique=True, nullable=False)


metadata.create_all(bind=engine)
