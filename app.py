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



@app.route("/status", methods=['GET'])
def get_status():
    # 使用全局的 LearningSystem 实例
    current_level, current_sub_level, current_points = system.get_current_status().split(', ')
    current_level = current_level.split(': ')[1]
    current_sub_level = current_sub_level.split(': ')[1]
    current_points = current_points.split(': ')[1]
    return jsonify({
        "current_level": current_level,
        "current_sub_level": current_sub_level,
        "current_points": current_points
    })

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

@app.route("/points_data", methods=['GET'])
def get_points_data():
    # 使用全局的 LearningSystem 实例
    action_logs = session.query(ActionLog).order_by(ActionLog.timestamp).all()  # 修改: 从数据库查询ActionLog对象
    points_data = []
    for log in action_logs:
        points_data.append({
            'timestamp': log.timestamp.isoformat(),
            'points_change': log.points_change
        })

    # 获取 groupby 参数，默认为 'day'
    groupby = request.args.get('groupby', 'day')

    # 添加时间分组函数
    def group_by_time_unit(labels, points, unit):
        grouped_data = {}
        for label, point in zip(labels, points):
            date = datetime.fromisoformat(label)
            key = None
            if unit == 'day':
                key = date.strftime('%Y-%m-%d')
            elif unit == 'week':
                # 修改: 使用 %Y-%U 格式化为 yyyy-week
                key = date.strftime('%Y-%U')
            elif unit == 'month':
                # 修改: 使用 %Y-%m 格式化为 yyyy-month
                key = date.strftime('%Y-%m')
            else:
                key = date.strftime('%Y-%m-%d')
            if key not in grouped_data:
                grouped_data[key] = {'points': 0, 'count': 0}
            grouped_data[key]['points'] += point
            grouped_data[key]['count'] += 1
        return [{'label': key, 'points': data['points']} for key, data in grouped_data.items()]

    # 初始化数据
    labels = [log['timestamp'] for log in points_data]
    points = [log['points_change'] for log in points_data]
    rewards = [point for point in points if point > 0]
    punishments = [point for point in points if point < 0]

    total_grouped_data = group_by_time_unit(labels, points, groupby)
    reward_grouped_data = group_by_time_unit(labels, rewards, groupby)
    punishment_grouped_data = group_by_time_unit(labels, punishments, groupby)

    return jsonify({
        'total': total_grouped_data,
        'rewards': reward_grouped_data,
        'punishments': punishment_grouped_data
    })

@app.route("/get_action_logs/", methods=['GET'])
def get_action_logs():
    # 查询ActionLog表中的数据
    action_logs = session.query(ActionLog).order_by(ActionLog.timestamp).all()
    
    # 将查询结果转换为JSON格式
    logs = [{'behavior': log.behavior, 'points_change': log.points_change, 'timestamp': log.timestamp.isoformat()} for log in action_logs]
    return jsonify(logs)

