# NPFJ — 使用方式

### 🅰 一体模式

开箱即用，一个命令跑全部。不需要 Node.js。

```bash
pip install flask flask-cors
python run.py
```

浏览器打开 **http://localhost:8080**。

---

### 🅱 开发模式

前后端分离，改了哪边 hot reload 哪边。需要 Node.js。

```bash
# 终端 1：后端
cd backend && pip install flask flask-cors && python app.py

# 终端 2：前端
cd frontend && npm install && npm run dev
```

浏览器打开 **http://localhost:3000**。

---

### 🅲 构建模式

一键打包成 zip，老师解压即用。

```bash
# macOS / Linux
bash build.sh

# Windows
双击 build.bat
```

在项目根目录生成 `NPFJ-交付包.zip`。