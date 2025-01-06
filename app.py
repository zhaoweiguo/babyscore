import os  # 添加导入os模块
from dotenv import load_dotenv  # 添加导入load_dotenv模块
from flask import Flask, render_template, request, jsonify
from datetime import datetime  # 修正缩进
import json
from logic import LearningSystem  # 添加对 LearningSystem 的导入
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, ActionLog, Session, engine

# 加载 .env 文件
load_dotenv("config/.env")

app = Flask(__name__)

app.static_folder = 'static'


session = Session()

# 创建全局的 LearningSystem 实例
system = LearningSystem(session)

# 添加数据库初始化函数
def init_db():
    Base.metadata.create_all(engine)

# 在应用启动时初始化数据库
@app.before_first_request
def startup_event():
    print("============================Database initialized")
    init_db()

@app.route("/", methods=['GET'])
def show_status():
    # 使用全局的 LearningSystem 实例
    current_level, current_sub_level, current_points = system.get_current_status().split(', ')
    current_level = current_level.split(': ')[1]
    current_sub_level = current_sub_level.split(': ')[1]
    current_points = current_points.split(': ')[1]
    # 添加 action_logs 参数的传递
    action_logs = system.action_logs
    return render_template("status.html", current_level=current_level, current_sub_level=current_sub_level, current_points=current_points, action_logs=action_logs)

@app.route("/action_logs", methods=['GET'])
def show_action_logs():
    # 使用全局的 LearningSystem 实例
    action_logs = system.action_logs
    return render_template("action_logs.html", action_logs=action_logs)

@app.route("/settings", methods=['GET'])
def show_settings():
    # 使用全局的 LearningSystem 实例
    current_level, current_sub_level, current_points = system.get_current_status().split(', ')
    current_level = current_level.split(': ')[1]
    current_sub_level = current_sub_level.split(': ')[1]
    current_points = current_points.split(': ')[1]
    # 传递行为日志列表到模板
    action_logs = system.action_logs
    return render_template("settings.html", current_level=current_level, current_sub_level=current_sub_level, current_points=current_points, action_logs=action_logs)

@app.route("/points_chart", methods=['GET'])
def show_points_chart():
    # 使用全局的 LearningSystem 实例
    action_logs = system.action_logs
    return render_template("points_chart.html", action_logs=action_logs)

@app.route("/handle_action", methods=['POST'])
def handle_action():
    # 使用全局的 LearningSystem 实例
    actionType = request.form['actionType']
    action = request.form['action']
    if actionType == 'reward':
        system.handle_action(action)
    elif actionType == 'punishment':
        system.handle_action(action)
    # 重新获取当前状态和行为日志
    current_level, current_sub_level, current_points = system.get_current_status().split(', ')
    current_level = current_level.split(': ')[1]
    current_sub_level = current_sub_level.split(': ')[1]
    current_points = current_points.split(': ')[1]
    action_logs = system.action_logs  # 获取最新的行为日志
    
    return jsonify({"current_level": current_level, "current_sub_level": current_sub_level, "current_points": current_points, "action_logs": action_logs})

@app.route("/get_action_logs/", methods=['GET'])
def get_action_logs():
    # 查询ActionLog表中的数据
    action_logs = session.query(ActionLog).order_by(ActionLog.timestamp).all()
    
    # 将查询结果转换为JSON格式
    logs = [{'behavior': log.behavior, 'points_change': log.points_change, 'timestamp': log.timestamp.isoformat()} for log in action_logs]
    return jsonify(logs)