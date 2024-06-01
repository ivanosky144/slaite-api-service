from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, DateTime
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime
from config.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    schedules = relationship("Schedule", back_populates="user", uselist=True, passive_deletes=True)
    notifications = relationship("Notification", back_populates="user", uselist=True, passive_deletes=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)