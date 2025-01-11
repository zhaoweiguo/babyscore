from babyscore.app import app  # 导入Flask应用对象

if __name__ == "__main__":
    app.run(debug=True, port=8888)  # 启动Flask应用，开启调试模式