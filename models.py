from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class ActionLog(Base):
    __tablename__ = 'action_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    behavior = Column(String, nullable=False)
    points_change = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)