# NPFJ — Network Personality Factor Indicator

> 大一程序设计实践项目 · 选题二：MBTI 测试系统
> **自创 NPFJ 二分树路由测评体系**
>
> 技术栈：Python Flask（后端）+ Vue 3（前端）

---

## 目录
1. [项目简介](#项目简介)
2. [核心创新](#核心创新)
3. [快速启动](#快速启动)
4. [详细运行步骤](#详细运行步骤)
5. [项目结构](#项目结构)
6. [API 接口文档](#api-接口文档)
7. [题库格式说明](#题库格式说明)
8. [前端页面说明](#前端页面说明)
9. [团队分工](#团队分工)
10. [常见问题](#常见问题)

---

## 项目简介

一个动态二分树路由的人格测评系统。用户先做 5 题基准校准，然后逐层通过 4 个阶段的二分树（每阶段 5 题），最终决出 16 种人格类型。

同时，每道题的选项背后隐藏 5 个心理维度的权重分，在用户不知情的情况下累加生成 **五维心理雷达图**——这是本项目的核心创新点。

---

## 核心创新

### 1. 二分树路由（取代传统"算总分"）

传统的 MBTI 测试是"答完所有题 → 统一算分 → 出结果"。

NPFJ 不同：**每道题的选项决定了下一题是什么**。用户的每一次选择都是在走一条独一无二的决策路径。

```
Stage 0 (基准校准) ── 5 题
        │
Stage 1 (连接拓扑) ── 5 题 ── 答完 → 左走 N / 右走 S
        │
Stage 2 (探针模式) ── 5 题 ── 答完 → 左走 P / 右走 L
        │
Stage 3 (路由逻辑) ── 5 题 ── 答完 → 左走 F / 右走 R
        │
Stage 4 (输出格式) ── 5 题 ── 答完 → 左走 J / 右走 W
        │
      最终决出 16 种人格之一
```

### 2. 隐性权重五维雷达图

每道题的两个选项（A/B）除了决定路由方向，还隐藏了一组 5 维权重值。用户全程不知道自己在被"测心"，最终生成的雷达图反映的是**潜意识心理倾向**。

| 维度 | 通俗名 | 低端 ← | → 高端 |
|------|--------|--------|--------|
| 🔋 精神续航 | 你大脑需要什么奖励 | 高频刷新（多巴胺） | 深度长效（内啡肽） |
| 🧲 社交磁场 | 你需要被人看到吗 | 同温层渴望 | 单机沙盒 |
| 🛠️ 秩序洁癖 | 你喜欢掌控还是随缘 | 绝对掌控 | 随机探索 |
| ⚖️ 压力解压阀 | 上网是为了充电还是泄压 | 赛博充电 | 情绪断联 |
| 🧠 脑力劳作 | 你享受烧脑吗 | 掘根刨底 | 直通结论 |

---

## 快速启动

### 一行命令启动后端

```bash
cd backend
pip install flask flask-cors
python app.py
```

浏览器打开 `http://localhost:8080/api/health`，看到 `{"status": "ok"}` 就算成功了。

### 一行命令启动前端

```bash
cd npti-frontend
npm install
npm run dev
```

浏览器打开 `http://localhost:3000`，就能看到测试首页了。

---

## 详细运行步骤

### 第一步：装 Python（如果没装）

- 去 https://www.python.org/downloads/ 下载 Python 3.10+
- 安装时勾选 **"Add Python to PATH"**
- 装完后打开终端（PowerShell / CMD），验证：

```bash
python --version
```
显示 `Python 3.10.x` 或更高就行。

### 第二步：启动后端

```bash
cd backend
pip install flask flask-cors   # 第一次运行需要，装依赖
python app.py
```

看到以下输出说明启动成功：
```
🚀 NPFJ 后端启动成功！
  题库加载: 16 个题池
 * Running on http://127.0.0.1:8080
```

**这个终端窗口要一直开着**，不要关。

### 第三步：启动前端（新开一个终端）

```bash
cd npti-frontend
npm install              # 第一次运行需要，装依赖
npm run dev
```

看到以下输出说明启动成功：
```
VITE v5.x.x ready in xxx ms
➜  Local: http://localhost:3000
```

### 第四步：测试

浏览器打开 `http://localhost:3000` → 点击"开始测试" → 答题 → 出结果

---

## 项目结构

```
NPTI/
├── backend/                        ← Python 后端（核心代码在这里）
│   ├── app.py                      ← Flask 服务器，定义了 4 个 API 接口
│   ├── engine.py                   ← 二分树状态机 + 五维权重累加（核心算法）
│   ├── pools.json                  ← ⭐ 题库文件（你需要填这个）
│   └── requirements.txt            ← Python 依赖清单
│
├── npti-frontend/                  ← Vue 3 前端
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js              ← 开发代理配置（/api → localhost:8080）
│   └── src/
│       ├── main.js                 ← 入口
│       ├── App.vue                 ← 根组件
│       ├── router/index.js         ← 路由（首页/答题/结果）
│       ├── api/request.js          ← 封装好的 API 调用
│       ├── views/
│       │   ├── HomeView.vue        ← 首页
│       │   ├── TestView.vue        ← 答题页（动态路由）
│       │   └── ResultView.vue      ← 结果页（五维雷达图）
│       ├── components/
│       │   └── RadarChart.vue      ← 雷达图组件（自适应维度）
│       └── assets/style.css        ← 全局样式
│
├── docs/开发实战手册.md            ← 开发指南（团队参考）
├── .gitignore
└── README.md                       ← 本文件
```

---

## API 接口文档

### `GET /api/health`

健康检查。返回：
```json
{ "status": "ok", "total_pools": 16, "dimensions": [...], "weight_dims": [...] }
```

### `POST /api/session/create`

创建新测试会话。返回：
```json
{
  "session_id": "abc12345",
  "first_pool": 0,
  "pool_info": { "id": 0, "stage": 0, "name": "基准校准", "description": "..." }
}
```

### `GET /api/pool/<pool_id>`

获取某个题池的题目。返回内容不包含权重和路由信息。

参数：`pool_id` 从 0 到 15

返回：
```json
{
  "id": 0,
  "stage": 0,
  "name": "基准校准",
  "description": "...",
  "questions": [
    { "id": 1, "text": "题目文字", "options": [
      { "key": "A", "text": "选项A文字" },
      { "key": "B", "text": "选项B文字" }
    ]}
  ]
}
```

### `POST /api/pool/<pool_id>/submit`

提交当前题池的 5 个答案。

请求体：
```json
{ "answers": ["A", "B", "A", "A", "B"] }
```

未完成时返回：
```json
{
  "next_pool": 2,
  "stage": 1,
  "is_final": false,
  "route_result": "L",
  "next_pool_info": { "id": 2, "stage": 2, "name": "...", "description": "..." }
}
```

最终阶段返回：
```json
{
  "next_pool": null,
  "stage": 4,
  "is_final": true,
  "route_result": "L",
  "result_ready": true
}
```

### `POST /api/result`

最终结算，生成人格类型和五维雷达图数据。

返回：
```json
{
  "type": "NPFJ",
  "title": "全栈掌控者",
  "description": "人格描述文字...",
  "path_letters": [
    { "stage": "连接拓扑", "direction": "L", "letter": "N" },
    { "stage": "探针模式", "direction": "R", "letter": "L" },
    { "stage": "路由逻辑", "direction": "L", "letter": "F" },
    { "stage": "输出格式", "direction": "R", "letter": "W" }
  ],
  "dimensions": [
    { "name": "连接拓扑", "abbr": "N", "score": 8, "opposite": "S" }
  ],
  "radar_data": [
    { "name": "精神续航", "value": 65 },
    { "name": "社交磁场", "value": 42 },
    { "name": "秩序洁癖", "value": 78 },
    { "name": "压力解压阀", "value": 31 },
    { "name": "脑力劳作", "value": 89 }
  ]
}
```

---

## 题库格式说明

文件：`backend/pools.json`

### 整体结构

```json
{
  "meta": {
    "dimensions": ["N/S", "P/L", "F/R", "J/W"],
    "dimension_names": ["连接拓扑", "探针模式", "路由逻辑", "输出格式"],
    "weight_dims": ["精神续航", "社交磁场", "秩序洁癖", "压力解压阀", "脑力劳作"],
    "total_pools": 16,
    "questions_per_pool": 5
  },
  "pools": {
    "0": { ... },   // 基准校准
    "1": { ... },   // Stage 1
    "2": { ... },   // Stage 2
    ...
    "15": { ... }   // Stage 4
  }
}
```

### 每个题池的格式

```json
"0": {
  "stage": 0,
  "name": "基准校准",
  "description": "基础网络行为模式扫描",
  "route_map": { "L": 1, "R": 1 },
  "questions": [
    {
      "id": 1,
      "text": "题目文字？",
      "options": {
        "A": {
          "text": "选项A文字",
          "route": "L",
          "weights": [2, 0, 1, 0, 0]
        },
        "B": {
          "text": "选项B文字",
          "route": "R",
          "weights": [0, 2, 0, 1, 1]
        }
      }
    }
  ]
}
```

### 字段说明

| 字段 | 说明 | 填什么 |
|------|------|--------|
| `stage` | 阶段编号 0-4 | 0=基准, 1=连接拓扑, 2=探针模式, 3=路由逻辑, 4=输出格式 |
| `name` | 题池中文名 | 自己取 |
| `description` | 题池描述 | 给用户看的提示 |
| `route_map` | 路由映射 | L 走向和 R 走向分别去哪个题池（Stage 4 的去 J/W） |
| `questions` | 题目数组 | 每池 5 题 |
| `options.A.route` | 选 A 的走向 | `"L"` 或 `"R"` |
| `options.A.weights` | 选 A 的五维权重 | 5 个数字，范围 0-2，对应 [续航,磁场,秩序,泄压,脑力] |

### Stage 4 的 route_map 特殊处理

Stage 4（题池 8-15）的 `route_map` 走到 J 或 W 结束，没有下一题池：
```json
"route_map": { "L": "J", "R": "W" }
```

### 目前人格描述是占位的

`backend/engine.py` 里的 `PERSONALITY_MAP` 字典目前 16 种人格的描述都是占位文字，打开它把标题和描述换成你自己的就行。

### 快速填充题库的建议

1. 先定 **16 种人格的名称和描述**（每个人格一个外号 + 一段描述）
2. 再定 **4 个维度的定义**（N/S、P/L、F/R、J/W 分别代表什么）
3. 最后写题——每个题池 5 题，每题两个选项

---

## 前端页面说明

前端有三个页面，通过 Vue Router 切换：

| 页面 | 路由 | 说明 |
|------|------|------|
| 首页 | `/` | 标题 + 开始按钮 |
| 答题页 | `/test` | 动态路由答题，每 5 题一组 |
| 结果页 | `/result` | 显示人格类型 + 五维雷达图 |

答题页的流程：
1. 进入 → 创建会话 → 加载 Stage 0（基准校准）
2. 答 5 题 → 自动提交 → 路由到下一题池
3. 重复直到所有 4 个阶段完成
4. 跳转到结果页

前端所有逻辑都在 `npti-frontend/src/views/TestView.vue`，如果你想改页面上的文字或样式，就直接编辑这个文件。

---

## 团队分工

| 角色 | 负责内容 | 主要文件 |
|------|---------|---------|
| **Coder 1** | Vue 前端 + 页面样式 | `npti-frontend/src/views/*` |
| **Coder 2** | Python 后端 + 路由逻辑 | `backend/app.py`, `backend/engine.py` |
| **Coder 3** | 联调测试 + 五维雷达图 + ECharts | 联调 + `RadarChart.vue` |
| **成员 D** | 项目报告 | 同步截图 + 写文档 |
| **成员 E** | 演示视频 | 2-5 分钟，展示完整流程 |

---

## 常见问题

**Q: 后端端口被占用了？**
A: 打开 `backend/app.py`，把最后一行 `port=8080` 改成 `port=8081`，同时把前端 `vite.config.js` 里的 `target` 也改成 `http://localhost:8081`。

**Q: 题库怎么加题？**
A: 编辑 `backend/pools.json`，在对应题池的 `questions` 数组里按格式添加。改完不需要重启后端——Flask 会自动重新加载。

**Q: 人格描述在哪里改？**
A: `backend/engine.py` 里的 `PERSONALITY_MAP` 字典，把 16 种人格的标题和描述文字替换成你的。

**Q: 前后端联调不上？**
A: 先确认后端终端里有 `Running on http://127.0.0.1:8080`，然后访问 `http://localhost:8080/api/health` 看有没有返回 JSON。如果不行，检查端口是否被其他程序占了。

**Q: 报告里怎么写这个项目的创新点？**
A: 三个核心点：
1. **二分树动态路由**（不是算总分，而是路径决定类型）
2. **隐性权重五维雷达图**（选项背后的心理学权重，用户无感知）
3. **先验相关架构**（行为与动机解耦但统计相关，离群值产生深刻洞察）
