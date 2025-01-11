import os

ACTIONS = {
    "没有发脾气": {"reward", 20},
    "努力完成学习": {"reward", 30},
    "按时睡觉": {"reward", 10},
    "发脾气": {"punishment", -20},
    "没有完成学习": {"punishment", -30},
    "没有按时睡觉": {"punishment", -10}
    
}

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///babyscore.db')


# # 定义行为及其对应的积分变化
# POSITIVE_ACTIONS = {
#     "没有发脾气": 20,
#     "努力完成学习": 30,
#     "按时睡觉": 10
# }

# NEGATIVE_ACTIONS = {
#     "发脾气": -20,
#     "没有完成学习": -30,
#     "没有按时睡觉": -10
# }