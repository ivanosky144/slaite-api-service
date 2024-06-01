from sqlalchemy import Enum, Column, Integer, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base

class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    repeat_interval = Column(Enum("Once", "Daily", "Weekly", "Monthly", name="repeat_interval_enum"))
    schedule_id = Column(Integer, ForeignKey('schedules.id', ondelete="CASCADE"))
    notification = relationship("Notification", back_populates="activity", passive_deletes=True)
    schedule = relationship("Schedule", back_populates="activities", passive_deletes=True)
    event  = relationship("Event", back_populates="activity", uselist=False, passive_deletes=True)
    task = relationship("Task", back_populates="activity", uselist=False, passive_deletes=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
