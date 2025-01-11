
from datetime import datetime, timezone, timedelta  # 添加 timezone 和 timedelta 导入
from models import Base, ActionLog, Session, engine


# 添加时间分组函数
def group_by_time_unit(action_list: list["ActionLog"], unit: str):
    total_grouped_data = {}
    reward_grouped_data = {}
    punishment_grouped_data = {}
    for action_log in action_list:
        date_iosformat = action_log.timestamp.astimezone(timezone(timedelta(hours=8))).isoformat()
        date = datetime.fromisoformat(date_iosformat)
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
        if key not in total_grouped_data:
            total_grouped_data[key] = {'points': 0, 'count': 0}
            reward_grouped_data[key] = {'points': 0, 'count': 0}
            punishment_grouped_data[key] = {'points': 0, 'count': 0}
        total_grouped_data[key]['points'] += action_log.points_change
        total_grouped_data[key]['count'] += 1
        if action_log.points_change > 0:
            reward_grouped_data[key]['points'] += action_log.points_change
            reward_grouped_data[key]['count'] += 1
        else:
            punishment_grouped_data[key]['points'] += action_log.points_change
            punishment_grouped_data[key]['count'] += 1
    
    total_grouped_list = [{'label': key, 'points': data['points'], 'count': data['count']} for key, data in total_grouped_data.items()]
    reward_grouped_list = [{'label': key, 'points': data['points'], 'count': data['count']} for key, data in reward_grouped_data.items()]
    punishment_grouped_list = [{'label': key, 'points': data['points'], 'count': data['count']} for key, data in punishment_grouped_data.items()]
    return {
        'total': total_grouped_list,
        'rewards': reward_grouped_list,
        'punishments': punishment_grouped_list
    }





if __name__ == '__main__':
    action_log1 = ActionLog(points_change=30, score_type='reward', behavior="行为1", timestamp=datetime.now())
    action_log2 = ActionLog(points_change=20, score_type='reward', behavior="行为2", timestamp=datetime.now())
    action_log3 = ActionLog(points_change=-10, score_type='punishment', behavior="行为3", timestamp=datetime.now())
    action_list = [action_log1, action_log2, action_log3]
    print(group_by_time_unit(action_list, 'month'))


# 添加时间分组函数
def group_by_time_unit2(labels, points, unit):
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
    return [{'label': key, 'points': data['points'], 'count': data['count']} for key, data in grouped_data.items()]




