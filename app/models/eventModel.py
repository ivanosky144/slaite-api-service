from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, DateTime
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime

from config.database import Base

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    start_time = Column(Time)
    end_time = Column(Time)
    activity_id = Column(Integer, ForeignKey('activities.id', ondelete="CASCADE"))
    activity = relationship("Activity", back_populates="event", passive_deletes=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
