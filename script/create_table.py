from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
import datetime
import os
from dotenv import load_dotenv
from sqlalchemy.inspection import inspect  # 导入inspect模块

from models import Base, ActionLog

# 添加: 创建数据库引擎
# 添加: 加载.env文件
load_dotenv(dotenv_path='./config/.env')

# 添加: 从.env文件中获取DATABASE_URI
database_uri = os.getenv('DATABASE_URI', 'mysql+pymysql://root:sa@localhost:3306/babyscore')
engine = create_engine(database_uri)

# 确保ActionLog类定义在Base.metadata.create_all(engine)之前

# 添加: 创建所有表
Base.metadata.create_all(engine)

# 添加: 验证表是否创建成功
inspector = inspect(engine)
table_names = inspector.get_table_names()
if 'action_logs' in table_names:  # 修改: 表名为action_logs
    print("Table 'action_logs' created successfully.")
else:
    print("Failed to create table 'action_logs'.")
