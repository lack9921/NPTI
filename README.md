# NPFJ — Network Personality Factor Indicator

> 大一程序设计实践项目 · 选题二：MBTI 测试系统
> 自创 **NPFJ 二分树路由测评体系**
>
> 核心创新：动态路由二分树 + 隐性权重五维心理雷达图
>
> 技术栈：Python Flask（后端）+ Vue 3（前端）

---

## 🚀 快速启动

### 后端（Python Flask）

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端启动后访问 `http://localhost:8080/api/health` 验证。

### 前端（Vue 3）

```bash
cd npti-frontend
npm install
npm run dev
```

前端启动后访问 `http://localhost:3000`。

> 开发时 Vite 自动把 `/api/*` 转发到后端 `localhost:8080`。

## 🧠 核心架构

### 二分树路由系统

```
Stage 0 (基准校准) ── 5 题
        │
Stage 1 (连接拓扑) ── 5 题 ─→ 左 N / 右 S
        │
Stage 2 (探针模式) ── 5 题 ─→ 左 P / 右 L
        │
Stage 3 (路由逻辑) ── 5 题 ─→ 左 F / 右 R
        │
Stage 4 (输出格式) ── 5 题 ─→ 左 J / 右 W
        │
      16 种人格类型 + 五维心理雷达图
```

### 隐性权重五维图

每道题的选项背后隐藏 5 个心理维度的权重分，用户作答时不知道自己在被"测心"：

| 维度 | 低端 | 高端 |
|------|------|------|
| 🔋 精神续航 | 高频刷新（多巴胺） | 深度长效（内啡肽） |
| 🧲 社交磁场 | 同温层渴望 | 单机沙盒 |
| 🛠️ 秩序洁癖 | 绝对掌控 | 随机探索 |
| ⚖️ 压力解压阀 | 赛博充电 | 情绪断联 |
| 🧠 脑力劳作 | 掘根刨底 | 直通结论 |

## 📁 项目结构

```
NPFJ/
├── backend/                     # Python Flask 后端
│   ├── app.py                   # API 入口（4 个端点）
│   ├── engine.py                # 二分树状态机 + 权重累加器
│   ├── pools.json               # 题库文件（16 个题池 × 5 题）
│   └── requirements.txt         # pip 依赖
│
├── npti-frontend/               # Vue 3 前端（不变）
│   └── src/
│       ├── views/               # 首页 / 答题页 / 结果页
│       ├── components/          # 雷达图组件（5 维自适应）
│       └── api/request.js       # 新 API 封装
│
└── README.md
```

## 📡 API 接口

### `GET /api/pool/<id>` — 获取题池
### `POST /api/session/create` — 创建会话
### `POST /api/pool/<id>/submit` — 提交 5 题答案
### `POST /api/result` — 最终结算

## 📝 填充题库

编辑 `backend/pools.json`，每个题池的 `questions` 数组为空，需填充 5 题。

每题格式：
```json
{
  "id": 1,
  "text": "题目文字",
  "options": {
    "A": { "text": "选项A文字", "route": "L", "weights": [2,0,1,0,0] },
    "B": { "text": "选项B文字", "route": "R", "weights": [0,2,0,1,1] }
  }
}
```

- `route`: L 或 R，决定二分树走向
- `weights`: 五维权重 [精神续航, 社交磁场, 秩序洁癖, 压力解压阀, 脑力劳作]，每题每维 0-2 分
