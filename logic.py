# 定义等级和小等级
LEVELS = {
    "小小孩": ["非常初级的", "初级的", "正常的", "厉害的", "非常厉害的"],
    "中小孩": ["非常初级的", "初级的", "正常的", "厉害的", "非常厉害的"],
    "大小孩": ["非常初级的", "初级的", "正常的", "厉害的", "非常厉害的"],
    "小大人": ["非常初级的", "初级的", "正常的", "厉害的", "非常厉害的"],
    "中大人": ["非常初级的", "初级的", "正常的", "厉害的", "非常厉害的"],
    "大人": ["非常初级的", "初级的", "正常的", "厉害的", "非常厉害的"]
}

# 初始化积分和等级
from config import POSITIVE_ACTIONS, NEGATIVE_ACTIONS  # 从config.py中导入行为及其对应的积分变化
import datetime  # 导入datetime模块以记录时间

class LearningSystem:
    def __init__(self):
        self.current_level = "小小孩"
        self.current_sub_level = "非常初级的"
        self.current_points = 0
        self.sub_level_points = 100

        # 从config.py中读取行为及其对应的积分变化
        self.positive_actions = POSITIVE_ACTIONS
        self.negative_actions = NEGATIVE_ACTIONS

        # 添加行为日志列表
        self.action_logs = self.load_action_logs()

    # 获取当前等级和小等级
    def get_current_status(self):
        return f"当前等级: {self.current_level}, 当前小等级: {self.current_sub_level}, 当前积分: {self.current_points}"

    # 增加积分
    def add_points(self, points):
        self.current_points += points
        self.check_level_up()

    # 扣除积分
    def deduct_points(self, points):
        self.current_points = max(0, self.current_points - abs(points))  # 确保积分不会变成负数
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

    # 加载行为日志
    def load_action_logs(self):
        try:
            with open("action_logs.txt", "r") as file:
                return file.readlines()
        except FileNotFoundError:
            return []

    # 保存行为日志
    def save_action_logs(self):
        with open("action_logs.txt", "w") as file:
            file.writelines(self.action_logs)

    # 处理行为
    def handle_action(self, action):
        if action in self.positive_actions:
            points = self.positive_actions[action]
            self.add_points(points)
            log_entry = f"行为: {action}, 积分变化: +{points}, 时间: {datetime.datetime.now()}\n"  # 增加时间字段
            self.action_logs.append(log_entry)
            self.save_action_logs()  # 保存行为日志
        elif action in self.negative_actions:
            points = self.negative_actions[action]
            self.deduct_points(points)
            log_entry = f"行为: {action}, 积分变化: {points}, 时间: {datetime.datetime.now()}\n"  # 增加时间字段
            self.action_logs.append(log_entry)
            self.save_action_logs()  # 保存行为日志
        else:
            print("未知的行为")