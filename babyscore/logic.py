from enum import Enum, auto

from babyscore.logger import log

# 初始化积分和等级
from babyscore.config import ACTIONS  # 从config.py中导入行为及其对应的积分变化
from babyscore.models import ActionLog  # 添加对模型的导入
from babyscore.db.service_action_log import ActionLogService



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

class LearningSystem:
    def __init__(self, session):
        # 添加行为日志列表
        self.session = session
        self.service_action_log = ActionLogService(session)


        self.current_level = "小小孩"
        self.current_sub_level = "非常初级的"
        self.sub_level_points = 100

        self.points_list = self.service_action_log.get_sum_from_db()
        self.current_points = self.points_list['total_points']
        self.current_reward_points = self.points_list['reward_points']
        self.current_punishment_points = self.points_list['punishment_points']

        self.action_logs = self.service_action_log.get_action_logs_from_db()  # 更新行为日志列表

        # 从config.py中读取行为及其对应的积分变化
        self.actions = ACTIONS


    # 获取当前等级和小等级
    def get_current_status(self):
        return {
            "current_level": self.current_level, 
            "current_sub_level": self.current_sub_level, 
            "current_points": self.points_list['total_points']
        }

    # update 积分
    def update_points(self, score_type, points):
        log.info(f"------- update_points: {score_type} {points}")
        self.current_points += points
        if score_type == "punishment":
            self.current_punishment_points += points
        elif score_type == "reward":
            self.current_reward_points += points
        else:
            log.error("Invalid score type")
            raise ValueError("Invalid score type")
        self.check_level_up()

    # 检查是否升级
    def check_level_up(self):
        sub_level_index = LEVELS[self.current_level].index(self.current_sub_level)
        if self.current_points >= (sub_level_index + 1) * self.sub_level_points:
            if sub_level_index < len(LEVELS[self.current_level]) - 1:
                self.current_sub_level = LEVELS[self.current_level][sub_level_index + 1]
                self.current_points -= (sub_level_index + 1) * self.sub_level_points
            else:
                print("当前小等级已满，请家长决定升级到下一个大等级。")


    # 处理行为
    def handle_action(self, actionType, action):
        if actionType == ActionType.reward.name or actionType == ActionType.punishment.name:
            score_type, points = self.actions[action]
            self.update_points(score_type, points)
            self.service_action_log.insert_log_action_item(score_type, action, points)
            self.action_logs = self.service_action_log.get_action_logs_from_db()  # 更新行为日志列表
        else:
            log.warning("未知的行为")
            return {"result": "error"}
        return {"result": "ok"}




