import os  # 添加导入os模块
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timezone, timedelta  # 添加 timezone 和 timedelta 导入
import json
from sqlalchemy import desc

from babyscore.models import ActionLog, Session, engine
from babyscore.logic import LearningSystem  # 添加对 LearningSystem 的导入
from babyscore.logger import log
from babyscore import util_point_chart
from babyscore.db import create_table
from babyscore import config


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
    admin_param = request.args.get('isadmin', default='false').lower()
    isadmin = admin_param == 'true' or admin_param == '1'

    return render_template('status.html', isadmin=isadmin)

@app.route("/action_logs", methods=['GET'])
def show_action_logs():
    admin_param = request.args.get('isadmin', default='false').lower()
    isadmin = admin_param == 'true' or admin_param == '1'

    return render_template('action_logs.html', isadmin=isadmin)

@app.route("/settings", methods=['GET'])
def show_settings():
    admin_param = request.args.get('isadmin', default='true').lower()
    isadmin = admin_param == 'true' or admin_param == '1'

    today = datetime.now().strftime('%Y-%m-%d')  # 获取当前日期
    return render_template("settings.html", today=today, isadmin=isadmin)

@app.route("/points_chart", methods=['GET'])
def show_points_chart():
    admin_param = request.args.get('isadmin', default='false').lower()
    isadmin = admin_param == 'true' or admin_param == '1'

    return render_template('points_chart.html', isadmin=isadmin)

@app.route("/readme", methods=['GET'])
def readme():
    admin_param = request.args.get('isadmin', default='false').lower()
    isadmin = admin_param == 'true' or admin_param == '1'

    return render_template('readme.html', isadmin=isadmin)






@app.route("/api/status", methods=['GET'])
def get_status():
    # 使用全局的 LearningSystem 实例
    current_status = system.get_current_status()

    return jsonify({
        "current_level": current_status["current_level"],
        "current_sub_level": current_status["current_sub_level"],
        "current_total_points": current_status["current_total_points"],
        "current_reward_points": current_status["current_reward_points"],
        "current_punishment_points": current_status["current_punishment_points"],
        "current_exchange_points": current_status["current_exchange_points"],
        "current_can_exchange_points": current_status["current_canExchange_points"]
    })


@app.route("/api/handle_action", methods=['POST'])
def handle_action():
    """执行行动"""
    actionType = request.form['actionType']  # reward, punishment
    action = request.form['action']
    actionDate = request.form.get('actionDate', datetime.now().strftime('%Y-%m-%d'))  # 获取选择的日期，默认为当前日期
    log.debug(f"Received action: {action}, type: {actionType}, date: {actionDate}")
    result = system.handle_action(actionType, action, actionDate)  # 传递日期参数
    return jsonify(result)

@app.route("/api/points_data", methods=['GET'])
def get_points_data():
    """行为日志列表折线图"""
    group_by = request.args.get('group_by', "all")
    # 获取 time_unit 参数，默认为 'day'
    time_unit = request.args.get('time_unit', 'day')

    grouped_list = system.get_points_data(group_by, time_unit)

    return jsonify(grouped_list)


@app.route("/api/get_action_logs/", methods=['GET'])
def get_action_logs():
    """行为日志列表"""
    logs = system.get_action_logs()
    return jsonify(logs)

@app.route("/api/delete_action_log/<int:id>", methods=['DELETE'])
def delete_action_log(id):
    """行为日志删除"""
    if system.delete_action_log(id):
        return jsonify({'message': 'Action log deleted successfully'})
    else:
        return jsonify({'message': 'Action log not found'}), 404


@app.route("/api/reward_actions", methods=['GET'])
def get_actions():
    """获取行为列表"""
    actions = config.ACTIONS
    rewardActions = []
    punishmentActions = []
    exchangeActions = []
    for k, v in actions.items():
        action_type, score = v
        item = {"value": score, "text": k}
        if action_type=="punishment":
            punishmentActions.append(item)
        elif action_type=="reward":
            rewardActions.append(item)
        elif action_type=="exchange":
            exchangeActions.append(item)
    return jsonify({
        "rewardActions": rewardActions,
        "punishmentActions": punishmentActions,
        "exchangeActions": exchangeActions
    })





