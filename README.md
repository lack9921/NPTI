# NPTI — Network Personality Test Indicator

> 大一程序设计实践项目 · 选题二：MBTI 测试系统（自创 NPTI 测评体系）

**技术栈：** Java Spring Boot（后端）+ Vue 3（前端）

## 团队分工

| 角色 | 负责内容 |
|------|---------|
| Coder 1 | Vue 3 前端（页面 + 路由 + 调接口） |
| Coder 2 | Spring Boot 后端（API + 算分逻辑 + 题库） |
| Coder 3 | Echarts 图表 + 联调测试 + 黏合 |
| 成员 D | 项目报告 |
| 成员 E | 演示视频 |

## 项目结构

```
NPTI/
├── npti-frontend/          # Vue 3 前端
│   └── src/
│       ├── views/          # 页面文件
│       ├── components/     # 组件
│       ├── api/            # API 请求封装
│       └── assets/         # 静态资源
├── npti-backend/           # Spring Boot 后端
│   └── src/main/java/com/npti/
│       ├── controller/     # API 接口
│       ├── service/        # 业务逻辑（算分）
│       ├── dto/            # 数据传输对象
│       └── config/         # 跨域配置
├── docs/                   # 开发文档
└── assets/                 # 项目素材
```

## 开发协作

使用 VS Code Live Share 实时协同编辑。
