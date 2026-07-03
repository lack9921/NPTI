# NPTI — Network Personality Test Indicator

> 大一程序设计实践项目 · 选题二：MBTI 测试系统（自创 NPTI 测评体系）
> 截止日期：2026 年 7 月 5 日

---

## 📋 项目简介

基于 **Java Spring Boot + Vue 3** 的在线人格测评系统。

用户回答 12 道题目，系统通过评分算法计算出用户的 NPTI 人格类型（4 个维度 × 2 种倾向 = 16 种人格），并以雷达图可视化展示结果。

## 👥 团队分工

| 角色 | 负责内容 | 主要文件 |
|------|---------|---------|
| **Coder 1** | Vue 3 前端（页面 + 路由 + 调接口） | `npti-frontend/src/views/*` |
| **Coder 2** | Spring Boot 后端（API + 算分逻辑 + 题库） | `npti-backend/src/main/java/com/npti/*` |
| **Coder 3** | ECharts 图表 + 联调 + 测试 + 黏合 | `RadarChart.vue` + 联调 |
| **成员 D** | 项目报告（同步写，截图素材） | `docs/` 参考开发文档 |
| **成员 E** | 演示视频（2-5 分钟，展示流程 + 雷达图） | — |

## 🚀 快速启动

### 后端（Coder 2 执行）

```bash
cd npti-backend

# Windows 执行（项目自带 mvnw.cmd，无需安装 Maven）
mvnw spring-boot:run

# Mac / Linux 执行
./mvnw spring-boot:run
```

后端启动后访问 `http://localhost:8080/api/test/questions` 验证。

### 前端（Coder 1 执行）

```bash
# 确保已安装 Node.js 18+
cd npti-frontend
npm install
npm run dev
```

前端启动后访问 `http://localhost:3000`。

> **开发时**：Vite 自动把 `/api/*` 请求转发到后端 `localhost:8080`，不需要手动处理后端地址。

### 前后端联调

前端页面操作完整流程：首页 → 答题（12 题）→ 提交 → 结果页（含雷达图）。

## 📁 项目结构

```
NPTI/
├── npti-backend/               # Spring Boot 后端
│   ├── pom.xml                 # Maven 依赖配置
│   └── src/main/java/com/npti/
│       ├── NptiApplication.java    # 启动入口
│       ├── config/CorsConfig.java  # 跨域配置
│       ├── controller/         # API 接口层
│       │   └── NptiController.java
│       ├── service/            # 业务逻辑层（核心算分）
│       │   └── NptiService.java
│       └── dto/                # 数据传输对象（接口契约）
│           ├── Result.java
│           ├── NptiRequest.java
│           └── NptiResponse.java
│
├── npti-frontend/              # Vue 3 前端
│   ├── index.html              # HTML 入口
│   ├── vite.config.js          # Vite 配置（含代理）
│   ├── package.json            # npm 依赖
│   └── src/
│       ├── main.js             # Vue 应用入口
│       ├── App.vue             # 根组件
│       ├── router/index.js     # 路由配置
│       ├── api/request.js      # API 请求封装
│       ├── views/              # 页面组件
│       │   ├── HomeView.vue    # 首页
│       │   ├── TestView.vue    # 答题页（核心）
│       │   └── ResultView.vue  # 结果页
│       ├── components/         # 可复用组件
│       │   └── RadarChart.vue  # ECharts 雷达图
│       └── assets/style.css    # 全局样式
│
├── docs/                       # 文档
│   └── 开发实战手册.md          # 完整开发指南
└── README.md                   # 本文件
```

## 🧠 核心算分逻辑

```
12 道题 → 4 个维度（每 3 题测一个维度）

维度            低分(<=6)   高分(>6)
──────────────────────────────
精力来源 (1-3)    E (外向)    I (内向)
认知方式 (4-6)    S (实感)    N (直觉)
决策方式 (7-9)    T (理性)    F (感性)
生活态度 (10-12)  J (计划)    P (随性)

每位字母 (A=1分, B=2分, C=3分, D=4分)
每个维度 3 题总分 3~12 分
```

组合成 16 种人格类型：ISTJ / ISFJ / INFJ / INTJ / ISTP / ISFP / INFP / INTP / ESTP / ESFP / ENFP / ENTP / ESTJ / ESFJ / ENFJ / ENTJ

## 🛠️ 技术栈

| 层 | 技术 |
|----|------|
| 后端框架 | Spring Boot 3.2 + Java 17 |
| 前端框架 | Vue 3 (Composition API) + Vite 5 |
| 路由 | Vue Router 4 |
| 图表 | ECharts 5 |
| HTTP 请求 | Axios |
| 协作工具 | VS Code + Live Share |

## 📦 打包（最后提交时用）

### 方案一：独立部署（推荐）

```bash
# 1. 前端打包
cd npti-frontend
npm run build    # 生成 dist/ 文件夹

# 2. 把 dist/ 移到后端的 static 目录
cp -r dist/ ../npti-backend/src/main/resources/static/

# 3. 后端打成可执行 jar
cd ../npti-backend
mvn clean package -DskipTests

# 4. 运行（所有页面都在这个 jar 里）
java -jar target/npti-backend-1.0.0.jar
```

之后访问 `http://localhost:8080` 即可看到完整页面，无需单独启动前端。

### 方案二：分开运行

直接分别启动前后端即可（开发时用这种方式）。

## 📝 核心 API 接口

### GET /api/test/questions

获取所有题目（不含答案）。

**返回格式：**
```json
{
  "code": 200,
  "message": "success",
  "data": [
    { "id": 1, "text": "周末你更倾向于？", "options": [
      { "key": "A", "text": "约朋友出去玩" },
      { "key": "B", "text": "在家打游戏或看书" },
      { "key": "C", "text": "参加线下活动聚会" },
      { "key": "D", "text": "一个人安静待着" }
    ]}
  ]
}
```

### POST /api/test/submit

提交 12 个答案，获取测试结果。

**请求体：**
```json
{ "answers": ["A", "B", "A", "C", "D", "A", "B", "A", "A", "C", "D", "B"] }
```

**返回格式：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "nptiType": "INTJ",
    "title": "建筑师型人格",
    "description": "富有想象力、战略性、果断...",
    "dimensions": [
      { "name": "精力来源", "abbr": "I", "score": 8, "opposite": "E" }
    ],
    "radarData": [
      { "name": "I/E", "value": 56 }
    ]
  }
}
```

## ✨ 加分项建议

1. **自创 NPTI 维度**（强烈推荐）—— 在 `NptiService.java` 里加一套程序员专属维度的算分（缩进派系/作息习惯等），报告中说明这是"自创测评体系"
2. **更多样化的雷达图** —— 修改 `RadarChart.vue` 的颜色和样式
3. **测试结果分享功能** —— 生成分享卡片或截图
4. **题库扩展** —— 在 QUESTIONS 里加更多题目，从中随机抽取 12 题

## 🔧 常见问题

**Q: 前端报跨域错误？**
A: Vite 开发时已经配了代理（`/api` → `localhost:8080`），正常情况下不会触发。如果部署时遇到，确保后端 `CorsConfig.java` 配置正确。

**Q: 后端启动时报端口被占用？**
A: 在 `application.yml` 里把 `server.port` 改为 8081（或其他可用端口），同时修改前端 `vite.config.js` 里 proxy 的 target 端口。

**Q: 如何改题目内容？**
A: 直接修改 `NptiService.java` 里的 `QUESTIONS`（静态代码块部分），注意每 3 题属于同一个维度。
