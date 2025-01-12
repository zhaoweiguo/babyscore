import os
from dotenv import load_dotenv  # 添加导入load_dotenv模块


# 加载 .env 文件
load_dotenv("config/.env")

ACTIONS = {
    "生活：按时睡觉，起床5": ("reward", 5),
    "生活：学习后整理书桌": ("reward", 1),
    "生活：不挑食、不剩饭、不浪费": ("reward", 1),
    "生活：爱护书本、文具、玩具": ("reward", 1),
    "生活：主动做好洗漱准备": ("reward", 1),
    "生活：控制情绪一天不发脾气10": ("reward", 10),
    "学习：认真完成作业": ("reward", 1),
    "学习：每日练字": ("reward", 1),
    "学习：每日阅读": ("reward", 1),
    "学习：每日练口算练习": ("reward", 1),
    "学习：复习当天学习的知识": ("reward", 1),
    "学习：主动学习英语、拼音": ("reward", 1),
    "加分：主动做家务": ("reward", 1),
    "加分：听写、计算全对": ("reward", 1),
    "加分：被老师表扬": ("reward", 1),
    "加分：照顾、安慰妹妹": ("reward", 1),
    "加分：有进步": ("reward", 1),

    "生活：晚睡、赖床5": ("punishment", -5),
    "生活：吃饭挑食": ("punishment", -1),
    "生活：不讲究卫生2": ("punishment", -2),
    "生活：有问有答3次不应2": ("punishment", -2),
    "生活：做事拖拉": ("punishment", -1),
    "生活：忘记洗漱准备": ("punishment", -1),
    "学习：作业拖拉": ("punishment", -1),
    "学习：学习不认真3": ("punishment", -3),
    "学习：没有完成作业2": ("punishment", -2),
    "学习：错题不订正": ("punishment", -1),
    "品德：打人、骂人3": ("punishment", -3),
    "品德：说谎、没礼貌、乱发脾气3": ("punishment", -3),
    "品德：和妹妹打架5": ("punishment", -5),
    
    
    
}

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///babyscore.db')




