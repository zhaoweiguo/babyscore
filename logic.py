from enum import Enum, auto

from logger import log


# 定义等级和小等级
LEVELS = {
    "小小孩": ["非常初级的", "初级的", "正常的", "厉害的", "非常厉害的"],
    "中小孩": ["非常初级的", "初级的", "正常的", "厉害的", "非常厉害的"],
    "大小孩": ["非常初级的", "初级的", "正常的", "厉害的", "非常厉害的"],
    "小大人": ["非常初级的", "初级的", "正常的", "厉害的", "非常厉害的"],
    "中大人": ["非常初级的", "初级的", "正常的", "厉害的", "非常厉害的"],
    "大人": ["非常初级的", "初级的", "正常的", "厉害的", "非常厉害的"]
}

class ActionType(Enum):
    reward="reward"
    punishment="punishment"


# 初始化积分和等级
from config import ACTIONS  # 从config.py中导入行为及其对应的积分变化
import datetime  # 导入datetime模块以记录时间
from models import ActionLog  # 添加对模型的导入

class LearningSystem:
    def __init__(self, session):
        self.current_level = "小小孩"
        self.current_sub_level = "非常初级的"
        self.current_points = 0
        self.sub_level_points = 100

        # 从config.py中读取行为及其对应的积分变化
        self.actions = ACTIONS

        # 添加行为日志列表
        self.session = session
        self.action_logs = self.load_action_logs_from_db()

    # 获取当前等级和小等级
    def get_current_status(self):
        return f"当前等级: {self.current_level}, 当前小等级: {self.current_sub_level}, 当前积分: {self.current_points}"

    # update 积分
    def update_points(self, points):
        self.current_points += points
        self.check_level_up()

    # # 增加积分
    # def add_points(self, points):
    #     self.current_points += points
    #     self.check_level_up()

    # # 扣除积分
    # def deduct_points(self, points):
    #     self.current_points = max(0, self.current_points - abs(points))  # 确保积分不会变成负数
    #     self.check_level_up()

    # 检查是否升级
    def check_level_up(self):
        sub_level_index = LEVELS[self.current_level].index(self.current_sub_level)
        if self.current_points >= (sub_level_index + 1) * self.sub_level_points:
            if sub_level_index < len(LEVELS[self.current_level]) - 1:
                self.current_sub_level = LEVELS[self.current_level][sub_level_index + 1]
                self.current_points -= (sub_level_index + 1) * self.sub_level_points
            else:
                print("当前小等级已满，请家长决定升级到下一个大等级。")

    def load_action_logs_from_db(self):
        action_logs = self.session.query(ActionLog).order_by(ActionLog.timestamp).all()
        return [{'behavior': log.behavior, 'points_change': log.points_change, 'timestamp': log.timestamp} for log in action_logs]

    # 处理行为
    def handle_action(self, actionType, action):
        if actionType == ActionType.reward.name or actionType == ActionType.punishment.name:
            score_type, points = self.actions[action]
            self.update_points(points)
            self.log_action(score_type, action, points)
        else:
            log.warning("未知的行为")
            return {"result": "error"}
        return {"result": "ok"}

    def log_action(self, score_type, action, points):
        new_log = ActionLog(score_type=score_type, behavior=action, points_change=points)
        self.session.add(new_log)
        self.session.commit()
        self.action_logs = self.load_action_logs_from_db()  # 更新行为日志列表