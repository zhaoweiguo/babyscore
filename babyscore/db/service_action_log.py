from babyscore.models import ActionLog, Session, engine

from sqlalchemy import func
import datetime
class ActionLogService:
    
    def __init__(self, session):
        self.session = session

    # 查询数据总和
    def get_sum_from_db(self):
        total_points = self.session.query(func.sum(ActionLog.points_change)).scalar()
        reward_points = self.session.query(func.sum(ActionLog.points_change)).filter(ActionLog.score_type == 'reward').scalar()
        punishment_points = self.session.query(func.sum(ActionLog.points_change)).filter(ActionLog.score_type == 'punishment').scalar()

        total_points = total_points or 0
        reward_points = reward_points or 0
        punishment_points = punishment_points or 0

        return {
            "total_points": total_points,
            "reward_points": reward_points,
            "punishment_points": punishment_points
        }
        
    # 查询全部数据
    def get_action_logs_from_db(self):
        action_logs = self.session.query(ActionLog).order_by(ActionLog.timestamp).all()
        return [
            {
                'behavior': log.behavior, 
                'points_change': log.points_change, 
                'timestamp': log.timestamp
            } for log in action_logs
        ]


    # 插入一条行为日志
    def insert_log_action_item(self, score_type, action, points, actionDate):
        # timestamp = datetime.datetime.strptime(actionDate, "%Y-%m-%d %H:%M:%S")
        timestamp = datetime.datetime.strptime(actionDate, "%Y-%m-%d")
        new_log = ActionLog(score_type=score_type, behavior=action, points_change=points, timestamp=timestamp)
        self.session.add(new_log)
        self.session.commit()



if __name__ == "__main__":
    session = Session()
    service = ActionLogService(session)
    service.load_action_logs_from_db()






