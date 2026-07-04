"""
NPFJ — Network Personality Factor Indicator
============================================
大一程序设计实践项目 · 选题二：MBTI 测试系统

一键启动（确保已安装 flask 和 flask-cors）：
    pip install flask flask-cors
    python run.py

然后在浏览器打开 http://localhost:8080
"""

import sys
import os

# 将 backend 加入模块搜索路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from backend.app import app

if __name__ == "__main__":
    print("=" * 54)
    print("  NPFJ — Network Personality Factor Indicator")
    print("  🖥  http://localhost:8080")
    print("=" * 54)
    app.run(host="0.0.0.0", port=8080, debug=True)
