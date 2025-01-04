from flask import Flask, render_template, request, jsonify

# 导入业务逻辑模块
from logic import LearningSystem

app = Flask(__name__)

# 创建全局的 LearningSystem 实例
system = LearningSystem()

@app.route('/')
def show_status():
    # 使用全局的 LearningSystem 实例
    current_level, current_sub_level, current_points = system.get_current_status().split(', ')
    current_level = current_level.split(': ')[1]
    current_sub_level = current_sub_level.split(': ')[1]
    current_points = current_points.split(': ')[1]
    # 传递行为日志列表到模板
    action_logs = system.action_logs
    return render_template('status.html', current_level=current_level, current_sub_level=current_sub_level, current_points=current_points, action_logs=action_logs)

@app.route('/handle_action', methods=['POST'])
def handle_action():
    action = request.form['action']
    # 使用全局的 LearningSystem 实例
    system.handle_action(action)
    # 重新获取当前状态和行为日志
    current_level, current_sub_level, current_points = system.get_current_status().split(', ')
    current_level = current_level.split(': ')[1]
    current_sub_level = current_sub_level.split(': ')[1]
    current_points = current_points.split(': ')[1]
    action_logs = system.action_logs  # 获取最新的行为日志
    return jsonify({
        'current_level': current_level,
        'current_sub_level': current_sub_level,
        'current_points': current_points,
        'action_logs': action_logs
    })

if __name__ == "__main__":
    app.run(debug=True)