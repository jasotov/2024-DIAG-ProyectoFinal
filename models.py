from sqlalchemy.orm import relationship
from db import db
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
)
from datetime import datetime


class User(db.Model):
   __tablename__ = "user"

   id = Column(Integer, primary_key=True, autoincrement=True)
   created_at = Column(DateTime, default=datetime.now)
   email = Column(String, nullable=False, unique=True)
   name = Column(String, nullable=False, unique=False)
   fav_movies = Column(String, nullable=False, unique=False)
   fav_series = Column(String, nullable=False, unique=False)
   kind_movies = Column(String, nullable=False, unique=False)

   messages = relationship("Message", back_populates="user")
   sessions = relationship("Session", back_populates="user")


class Message(db.Model):
   __tablename__ = "message"
   id = Column(Integer, primary_key=True, autoincrement=True)
   created_at = Column(DateTime, default=datetime.now)
   content = Column(Text, nullable=False)
   author = Column(String, nullable=False)  # 'user' or 'assistant'
   user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
   session_id = Column(Integer, ForeignKey("session.id"), nullable=False)
   user = relationship("User", back_populates="messages")
   session = relationship("Session", back_populates="messages")

class Session(db.Model):
   __tablename__ = "session"
   id = Column(Integer, primary_key=True, autoincrement=True)
   created_at = Column(DateTime, default=datetime.now)
   user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

   user = relationship("User", back_populates="sessions")
   messages = relationship("Message", back_populates="session")
