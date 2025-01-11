from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

Base = declarative_base()

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///babyscore.db')
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

# Action Log
class ActionLog(Base):
    __tablename__ = 'action_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    behavior = Column(String(255), nullable=False)   # 修改: 指定String长度为255
    score_type = Column(String(255), nullable=False) # "reward", "punishment"
    points_change = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Action
class Action(Base):
    __tablename__ = 'actions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)        # 修改: 指定String长度为255
    points_value = Column(Integer, nullable=False)
    score_type = Column(String(255), nullable=False) # "reward", "punishment"
    description = Column(String(255), nullable=True)  # 修改: 指定String长度为255
    

