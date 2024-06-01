from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, DateTime
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime

from config.database import Base

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String)
    status = Column(String)
    time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    activity_id = Column(Integer, ForeignKey('activities.id', ondelete="CASCADE"))
    user = relationship("User", back_populates="notifications", passive_deletes=True)
    activity = relationship("Activity", back_populates="notification", passive_deletes=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
