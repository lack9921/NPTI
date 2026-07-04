# NPFJ — Network Personality Factor Indicator

> 大一程序设计实践项目 · 选题二：MBTI 测试系统
> 自创 NPFJ 二分树路由测评体系

---

## 运行方式

### 方式一：双击 EXE（推荐）

`backend/dist/NPFJ.exe` 为单文件可执行程序，双击运行后在浏览器访问：

```
http://localhost:8080
```

无需安装任何依赖。

### 方式二：Python 源码运行

```bash
cd backend
pip install flask flask-cors
python app.py
```

浏览器访问 `http://localhost:8080`。

---

## 项目结构

```
backend/              Python 后端源码 + 题库数据
  app.py              Flask API 入口
  engine.py           二分树路由引擎
  calculator.py       五维权重计算器
  pools.json          75 道题库
  reports.json        16 份人格分析报告
  dist/NPFJ.exe       可执行程序
frontend/             Vue 3 前端源码
README.md             本文件
```

---

## 技术栈

后端：Python 3 + Flask
前端：Vue 3 + Naive UI + ECharts
图表：ECharts 五维雷达图
