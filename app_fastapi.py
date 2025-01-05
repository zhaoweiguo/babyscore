from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime  # 修正缩进
import json
import sqlite3
from logic import LearningSystem  # 添加对 LearningSystem 的导入

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 创建全局的 LearningSystem 实例
system = LearningSystem()

# 添加数据库初始化函数
def init_db():
    conn = sqlite3.connect('babyscore.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS action_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            behavior TEXT NOT NULL,
            points_change INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# 在应用启动时初始化数据库
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/", response_class=HTMLResponse)
def show_status(request: Request):
    # 使用全局的 LearningSystem 实例
    current_level, current_sub_level, current_points = system.get_current_status().split(', ')
    current_level = current_level.split(': ')[1]
    current_sub_level = current_sub_level.split(': ')[1]
    current_points = current_points.split(': ')[1]
    # 添加 action_logs 参数的传递
    action_logs = system.action_logs
    return templates.TemplateResponse("status.html", {"request": request, "current_level": current_level, "current_sub_level": current_sub_level, "current_points": current_points, "action_logs": action_logs})

@app.get("/action_logs", response_class=HTMLResponse)
def show_action_logs(request: Request):
    # 使用全局的 LearningSystem 实例
    action_logs = system.action_logs
    return templates.TemplateResponse("action_logs.html", {"request": request, "action_logs": action_logs})

@app.get("/settings", response_class=HTMLResponse)
def show_settings(request: Request):
    # 使用全局的 LearningSystem 实例
    current_level, current_sub_level, current_points = system.get_current_status().split(', ')
    current_level = current_level.split(': ')[1]
    current_sub_level = current_sub_level.split(': ')[1]
    current_points = current_points.split(': ')[1]
    # 传递行为日志列表到模板
    action_logs = system.action_logs
    return templates.TemplateResponse("settings.html", {"request": request, "current_level": current_level, "current_sub_level": current_sub_level, "current_points": current_points, "action_logs": action_logs})

@app.get("/points_chart", response_class=HTMLResponse)
def show_points_chart(request: Request):
    # 使用全局的 LearningSystem 实例
    action_logs = system.action_logs
    return templates.TemplateResponse("points_chart.html", {"request": request, "action_logs": action_logs})

@app.post("/handle_action", response_class=JSONResponse)
async def handle_action(actionType: str = Form(...), action: str = Form(...)):
    # 使用全局的 LearningSystem 实例
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
    
    return {"current_level": current_level, "current_sub_level": current_sub_level, "current_points": current_points, "action_logs": action_logs}

@app.get("/get_action_logs/")
def get_action_logs():
    # 连接到SQLite数据库
    conn = sqlite3.connect('babyscore.db')
    cursor = conn.cursor()
    
    # 查询ActionLog表中的数据
    cursor.execute("SELECT behavior, points_change, timestamp FROM action_logs ORDER BY timestamp")
    action_logs = cursor.fetchall()
    
    # 关闭数据库连接
    cursor.close()
    conn.close()
    
    # 将查询结果转换为JSON格式
    logs = [{'behavior': log[0], 'points_change': log[1], 'timestamp': datetime.fromisoformat(log[2]).isoformat()} for log in action_logs]
    return logs
