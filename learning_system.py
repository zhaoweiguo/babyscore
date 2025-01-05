from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

# 假设 LearningSystem 类定义在 learning_system.py 文件的某个模块中
# 这里假设 LearningSystem 类定义在同文件夹下的 learning_system.py 文件中
from logic import LearningSystem

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 创建全局的 LearningSystem 实例
system = LearningSystem()

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
async def handle_action(action: str = Form(...)):
    # 使用全局的 LearningSystem 实例
    system.handle_action(action)
    # 重新获取当前状态和行为日志
    current_level, current_sub_level, current_points = system.get_current_status().split(', ')
    current_level = current_level.split(': ')[1]
    current_sub_level = current_sub_level.split(': ')[1]
    current_points = current_points.split(': ')[1]
    action_logs = system.action_logs  # 获取最新的行为日志
    return {"current_level": current_level, "current_sub_level": current_sub_level, "current_points": current_points, "action_logs": action_logs}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)