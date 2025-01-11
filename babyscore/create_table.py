from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
import datetime
import os
from dotenv import load_dotenv
from sqlalchemy.inspection import inspect  # 导入inspect模块

from babyscore.models import Base, ActionLog, engine

# 添加: 创建所有表
Base.metadata.create_all(engine)

# 添加: 验证表是否创建成功
inspector = inspect(engine)
table_names = inspector.get_table_names()
if 'action_logs' in table_names:  # 修改: 表名为action_logs
    print("Table 'action_logs' created successfully.")
else:
    print("Failed to create table 'action_logs'.")
