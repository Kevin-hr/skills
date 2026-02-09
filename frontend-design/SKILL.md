---
name: frontend-design
description: 前端设计 - 创建独特、生产级的前端界面，避免通用AI美学。支持 Vue 3 + Vite + SCSS。触发词：构建界面、设计UI、美化前端。
type: Frontend Designer
category: Development
version: 1.0.0
author: Claude Code
updated: 2026-02-09
tags: [frontend, vue, design, ui, scss]
---

# Frontend Design 前端设计器

创建独特、生产级的前端界面，避免通用AI美学。

## 设计原则

| 原则 | 说明 |
|------|------|
| 大胆美学 | 极简主义或极繁主义，选择极端并执行 |
| 目的导向 | 明确解决什么问题、服务谁 |
| 差异化 | 令人难忘的独特记忆点 |
| 精细执行 | 每个细节都精心打磨 |

## 快速开始

| 场景 | 命令 |
|------|------|
| 启动项目 | `cd sau_frontend && npm install && npm run dev` |
| 清理端口 | `npx kill-port 5173 && npm run dev` |
| 测试页面 | `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5173/` |

## 项目结构

```
sau_frontend/
├── src/
│   ├── styles/
│   │   ├── reset.scss      # CSS Reset + 深色主题
│   │   ├── variables.scss  # 设计系统变量
│   │   └── index.scss      # 全局样式
│   ├── App.vue             # 根组件
│   └── main.js             # 入口
├── index.html              # Google Fonts
└── vite.config.js          # Vite配置
```

## 主题系统

| 主题 | 背景 | 主色调 | 字体 | 效果 |
|------|------|--------|------|------|
| 数字指挥中心 | `#0a0a0f` | `#6366f1` → `#a855f7` | Space Grotesk | 霓虹发光 + 玻璃拟态 |
| 极简纯净 | `#f8f8f8` | `#0071e3` | Inter + SF Pro | 柔和阴影 + 圆角 |
| 赛博朋克 | `#0d0d0d` | `#00ff88` → `#ff00ff` | Orbitron | 霓虹边框 + 扫描线 |

## 深色主题变量

```scss
$bg-darkest: #0a0a0f;
$bg-dark: #111118;
$bg-card: rgba(255, 255, 255, 0.03);
$text-primary: #ffffff;
$text-secondary: rgba(255, 255, 255, 0.6);
$border-light: rgba(255, 255, 255, 0.08);
```

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| Sass变量未定义 | 未正确import | 使用 `@use '@/styles/variables.scss' as *;` |
| 页面无法访问 | 端口占用 | `npx kill-port 5173` |
| 字体不加载 | Google Fonts缺失 | 确认index.html链接完整 |
| Element样式未覆盖 | 优先级问题 | 使用 `:deep()` 选择器 |

## 开发清单

- [ ] 变量文件使用 `@use` 语法
- [ ] 组件内样式引用变量
- [ ] 字体链接放在 `<head>` 中
- [ ] Vite配置 `host: '0.0.0.0'`
- [ ] 启动前清理端口
- [ ] 验证无控制台Sass错误

## Changelog

### v1.0.0 (2026-02-08)
- Vue 3 + Vite + SCSS 模板
- 深色/浅色主题系统
- 设计系统变量
- Element Plus 覆盖样式
