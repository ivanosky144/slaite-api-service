from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime

from config.database import Base

class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    color = Column(String, nullable=True)
    user = relationship("User", back_populates="schedules")
    activities = relationship("Activity", back_populates="schedule", uselist=True, passive_deletes=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


    