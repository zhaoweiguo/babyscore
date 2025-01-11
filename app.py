import os  # 添加导入os模块
from dotenv import load_dotenv  # 添加导入load_dotenv模块
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timezone, timedelta  # 添加 timezone 和 timedelta 导入
import json
from logic import LearningSystem  # 添加对 LearningSystem 的导入
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, ActionLog, Session, engine

from logger import log
import util_point_chart

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



@app.route("/api/status", methods=['GET'])
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

@app.route("/api/handle_action", methods=['POST'])
def handle_action():
    # 使用全局的 LearningSystem 实例
    actionType = request.form['actionType']  # reward, punishment
    action = request.form['action']
    log.debug(f"Received action: {action}, type: {actionType}")
    result = system.handle_action(actionType, action)
    # 重新获取当前状态和行为日志
    # current_level, current_sub_level, current_points = system.get_current_status().split(', ')
    # current_level = current_level.split(': ')[1]
    # current_sub_level = current_sub_level.split(': ')[1]
    # current_points = current_points.split(': ')[1]
    # action_logs = system.action_logs  # 获取最新的行为日志
    # return jsonify({"current_level": current_level, "current_sub_level": current_sub_level, "current_points": current_points, "action_logs": action_logs})
    return jsonify(result)

@app.route("/api/points_data2", methods=['GET'])
def get_points_data2():
    # 获取 groupby 参数，默认为 'day'
    groupby = request.args.get('groupby', 'day')
    score_type = request.args.get('score_type', 'all') #  "reward", "punishment"

    if score_type=="all":
        action_logs = session.query(ActionLog).order_by(ActionLog.timestamp).all()
    else:
        # where score_type = "reward"
        action_logs = session.query(ActionLog).filter(ActionLog.score_type == score_type).order_by(ActionLog.timestamp).all()


    key = None
    grouped_data = {}
    for log in action_logs:
        print(f"{log.timestamp}  -  {log.points_change}   -   {log.id}   -  {log.behavior}")
        if groupby == 'day':
            key = log.timestamp.strftime('%Y-%m-%d')
        elif groupby == 'week':
            key = log.timestamp.strftime('%Y-%U')
        elif groupby == 'month':
            key = log.timestamp.strftime('%Y-%m')
        else:
            key = log.timestamp.strftime('%Y-%m-%d')
        if key not in grouped_data:
            grouped_data[key] = {'points': 0, 'count': 0}
        grouped_data[key]['points'] += log.points_change
        grouped_data[key]['count'] += 1

    return jsonify(grouped_data)

@app.route("/api/points_data", methods=['GET'])
def get_points_data():
    group_by = request.args.get('group_by', "all")
    # 使用全局的 LearningSystem 实例
    action_logs = session.query(ActionLog).order_by(ActionLog.timestamp).all()  # 修改: 从数据库查询ActionLog对象
    points_data = []
    # for log in action_logs:
    #     # 将时间戳转换为东八区时间
    #     timestamp_east8 = log.timestamp.astimezone(timezone(timedelta(hours=8)))
    #     points_data.append({
    #         'timestamp': timestamp_east8.isoformat(),
    #         'points_change': log.points_change,
    #         'behavior': log.behavior,
    #         "score_type": log.score_type
    #     })

    # 获取 groupby 参数，默认为 'day'
    groupby = request.args.get('groupby', 'day')

    # 默认按总积分计算
    if group_by == 'all':
        grouped_list = util_point_chart.group_by_time_unit(action_logs, groupby)
        
        # labels = [log['timestamp'] for log in points_data]
        # points = [log['points_change'] for log in points_data]
        # rewards = [point for point in points if point > 0]
        # punishments = [point for point in points if point < 0]

    # 根据score_type参数进行分组
    # @todo

    # total_grouped_data = group_by_time_unit(labels, points, groupby)
    # reward_grouped_data = group_by_time_unit(labels, rewards, groupby)
    # punishment_grouped_data = group_by_time_unit(labels, punishments, groupby)

    return jsonify(grouped_list)

@app.route("/api/get_action_logs/", methods=['GET'])
def get_action_logs():
    # 查询ActionLog表中的数据
    action_logs = session.query(ActionLog).order_by(ActionLog.timestamp).all()
    log.debug(f"Action logs: {action_logs}")
    
    # 将查询结果转换为JSON格式
    logs = [{'behavior': log.behavior, 'points_change': log.points_change, 'timestamp': log.timestamp.isoformat()} for log in action_logs]
    return jsonify(logs)

