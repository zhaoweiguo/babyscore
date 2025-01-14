from babyscore.models import ActionLog, Session, engine

from sqlalchemy import func, exc, desc
import datetime
class ActionLogService:
    
    def __init__(self, session):
        self.session = session

    # 查询数据总和
    def get_sum_from_db(self):
        try:
            total_points = self.session.query(func.sum(ActionLog.points_change)).filter(ActionLog.score_type != 'exchange').scalar()
            reward_points = self.session.query(func.sum(ActionLog.points_change)).filter(ActionLog.score_type == 'reward').scalar()
            punishment_points = self.session.query(func.sum(ActionLog.points_change)).filter(ActionLog.score_type == 'punishment').scalar()
            exchange_points = self.session.query(func.sum(ActionLog.points_change)).filter(ActionLog.score_type == 'exchange').scalar()

            total_points = total_points or 0
            reward_points = reward_points or 0
            punishment_points = punishment_points or 0
            exchange_points = exchange_points or 0

            return {
                "total_points": total_points,
                "reward_points": reward_points,
                "punishment_points": punishment_points,
                "exchange_points": exchange_points
            }
        except exc.SQLAlchemyError as e:
            print(f"------- SQLAlchemyError: {e}")
            session.rollback()  # Reset the session to a usable state
            return {}
        except Exception as e:
            print(f"------- Exception: {e}")
            session.rollback()
            return {}

        
    # 查询全部数据
    def get_action_logs_from_db(self):
        try:
            action_logs = self.session.query(ActionLog).order_by(ActionLog.timestamp).all()
            return [
                {
                    'behavior': log.behavior, 
                    'points_change': log.points_change,
                    'score_type': log.score_type,
                    'timestamp': log.timestamp
                } for log in action_logs
            ]
        except exc.SQLAlchemyError as e:
            print(f"------- SQLAlchemyError: {e}")
            session.rollback()  # Reset the session to a usable state
            return []
        except Exception as e:
            print(f"------- Exception: {e}")
            session.rollback()
            return []


    # 插入一条行为日志
    def insert_log_action_item(self, score_type, action, points, actionDate):
        try:
            # timestamp = datetime.datetime.strptime(actionDate, "%Y-%m-%d %H:%M:%S")
            timestamp = datetime.datetime.strptime(actionDate, "%Y-%m-%d")
            new_log = ActionLog(score_type=score_type, behavior=action, points_change=points, timestamp=timestamp)
            self.session.add(new_log)
            self.session.commit()
        except exc.SQLAlchemyError as e:
            print(f"------- SQLAlchemyError: {e}")
            session.rollback()  # Reset the session to a usable state
        except Exception as e:
            print(f"------- Exception: {e}")
            session.rollback()


    def get_points_data(self, group_by='all', time_unit='day'):
        try:
            action_logs = self.session.query(ActionLog).order_by(ActionLog.timestamp).all()  # 修改: 从数据库查询ActionLog对象
            return action_logs
        except exc.SQLAlchemyError as e:
            print(f"------- SQLAlchemyError: {e}")
            session.rollback()  # Reset the session to a usable state
            return []
        except Exception as e:
            print(f"------- Exception: {e}")
            session.rollback()
            return []


    def get_action_logs(self):
        try:
            # 查询ActionLog表中的数据，按时间倒序
            action_logs = self.session.query(ActionLog).order_by(desc(ActionLog.timestamp)).all()
            return action_logs
        except exc.SQLAlchemyError as e:
            print(f"------- SQLAlchemyError: {e}")
            session.rollback()  # Reset the session to a usable state
            return []
        except Exception as e:
            print(f"------- Exception: {e}")
            session.rollback()
            return []

    def delete_action_log(self, id):
        try:
            action_log = self.session.query(ActionLog).filter_by(id=id).first()
            if action_log:
                session.delete(action_log)
                session.commit()
                return True
        except exc.SQLAlchemyError as e:
            print(f"------- SQLAlchemyError: {e}")
            session.rollback()  # Reset the session to a usable state
            return False
        except Exception as e:
            print(f"------- Exception: {e}")
            session.rollback()
            return False



if __name__ == "__main__":
    session = Session()
    service = ActionLogService(session)
    service.load_action_logs_from_db()






