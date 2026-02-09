---
name: find-skills
description: 技能发现器 - 搜索和安装 Claude Skills 生态中的技能。触发词：搜索技能、查找工具、列出技能。
type: Skill Finder
category: Utilities
version: 1.0.0
author: Claude Code
updated: 2026-02-09
tags: [search, skill, finder, install]
---

# Find Skills 技能发现器

搜索和安装 Claude Skills 生态中的技能。

## 快速开始

| 场景 | 命令 |
|------|------|
| 搜索技能 | `find-skills --keyword "react"` |
| 列出所有 | `find-skills --list` |
| 安装技能 | `find-skills --add owner/repo@skill` |

## 核心命令

| 命令 | 说明 |
|------|------|
| `npx skills find [query]` | 交互式搜索 |
| `npx skills add <package>` | 安装技能 |
| `npx skills check` | 检查更新 |
| `npx skills update` | 更新所有 |

## 搜索示例

| 用户需求 | 搜索命令 |
|---------|---------|
| React 优化 | `npx skills find react performance` |
| PR 审核 | `npx skills find pr review` |
| Changelog | `npx skills find changelog` |
| 部署工具 | `npx skills find deploy` |

## 技能分类

| 分类 | 示例查询 |
|------|---------|
| Web 开发 | react, nextjs, typescript |
| 测试 | testing, jest, playwright |
| DevOps | deploy, docker, ci-cd |
| 文档 | docs, readme, api-docs |
| 代码质量 | review, lint, refactor |

## 安装示例

```bash
# 安装 React 最佳实践
npx skills add vercel-labs/agent-skills@vercel-react-best-practices

# 全局安装，跳过确认
npx skills add <owner/repo@skill> -g -y
```

## 输出格式

```json
{
  "skills": [
    {
      "name": "vercel-react-best-practices",
      "description": "React 和 Next.js 性能优化指南",
      "install_command": "npx skills add vercel-labs/agent-skills@vercel-react-best-practices",
      "link": "https://skills.sh/..."
    }
  ],
  "total_count": 15
}
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 无匹配结果 | 扩大关键词范围 |
| 安装失败 | 检查网络连接 |
| 格式错误 | 检查命令语法 |
| 权限问题 | 使用 -g 全局安装 |

## Changelog

### v1.0.0 (2026-02-08)
- 技能搜索
- 安装支持
- 分类浏览
- 命令集成
