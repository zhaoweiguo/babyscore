import os  # 添加导入os模块
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timezone, timedelta  # 添加 timezone 和 timedelta 导入
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from babyscore.models import ActionLog, Session, engine
from babyscore.logic import LearningSystem  # 添加对 LearningSystem 的导入
from babyscore.logger import log
from babyscore import util_point_chart
from babyscore.db import create_table


app = Flask(__name__)

app.static_folder = '../static'
app.template_folder = '../templates'


session = Session()

print("============================Database initialized start")
create_table.create_db()
print("============================Database initialized end")
# 创建全局的 LearningSystem 实例
system = LearningSystem(session)

# 添加数据库初始化函数
# def init_db():
#     create_table.create_db()

# 在应用启动时初始化数据库
# @app.before_first_request
# def startup_event():
#     print("============================Database initialized")
#     init_db()

@app.route("/", methods=['GET'])
def show_status():
    return render_template("status.html")

@app.route("/action_logs", methods=['GET'])
def show_action_logs():
    return render_template("action_logs.html")

@app.route("/settings", methods=['GET'])
def show_settings():
    today = datetime.now().strftime('%Y-%m-%d')  # 获取当前日期
    return render_template("settings.html", today=today)

@app.route("/points_chart", methods=['GET'])
def show_points_chart():
    return render_template("points_chart.html")



@app.route("/api/status", methods=['GET'])
def get_status():
    # 使用全局的 LearningSystem 实例
    current_status = system.get_current_status()
    current_level = current_status["current_level"]
    current_sub_level = current_status["current_sub_level"]
    current_points = current_status["current_points"]

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
    actionDate = request.form.get('actionDate', datetime.now().strftime('%Y-%m-%d'))  # 获取选择的日期，默认为当前日期
    log.debug(f"Received action: {action}, type: {actionType}, date: {actionDate}")
    result = system.handle_action(actionType, action, actionDate)  # 传递日期参数
    return jsonify(result)

@app.route("/api/points_data", methods=['GET'])
def get_points_data():
    group_by = request.args.get('group_by', "all")
    # 使用全局的 LearningSystem 实例
    action_logs = session.query(ActionLog).order_by(ActionLog.timestamp).all()  # 修改: 从数据库查询ActionLog对象
    # 获取 time_unit 参数，默认为 'day'
    time_unit = request.args.get('time_unit', 'day')

    # 默认按总积分计算
    if group_by == 'all':
        grouped_list = util_point_chart.group_by_time_unit(action_logs, time_unit)
    # 根据score_type参数进行分组
    # @todo

    return jsonify(grouped_list)

@app.route("/api/get_action_logs/", methods=['GET'])
def get_action_logs():
    # 查询ActionLog表中的数据
    action_logs = session.query(ActionLog).order_by(ActionLog.timestamp).all()
    log.debug(f"Action logs: {action_logs}")
    
    # 将查询结果转换为JSON格式
    logs = [{'behavior': log.behavior, 'points_change': log.points_change, 'timestamp': log.timestamp.isoformat()} for log in action_logs]
    return jsonify(logs)