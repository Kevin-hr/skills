---
name: project-amplifier
description: 项目放大器 - 将任意项目转化为病毒式传播内容。支持公众号写作、短视频脚本、全渠道分发。触发词：项目推广、公众号文章、短视频脚本。
type: Content Amplifier
category: Content Strategy
version: 1.0.0
author: Claude Code
updated: 2026-02-09
tags: [amplify, viral, content, distribution]
---

# Project Amplifier 项目放大器

将任意项目转化为病毒式传播内容。

## 核心工作流

```
项目分析 → 卖点提炼 → 公众号文章 → 短视频脚本 → 分发策略
```

## 快速开始

| 场景 | 命令 |
|------|------|
| 公众号文章 | `project-amplifier --format wechat --project "项目描述"` |
| 视频脚本 | `project-amplifier --format video --project "项目描述"` |
| 全渠道分发 | `project-amplifier --distribute --project "项目描述"` |

## 输入格式

```json
{
  "project": {
    "name": "项目名称",
    "description": "项目功能描述",
    "tech_stack": ["技术栈"],
    "features": ["核心功能"]
  },
  "target_audience": ["目标用户群体"],
  "goal": "转化目标"
}
```

## 输出内容

| 格式 | 内容要素 |
|------|---------|
| 公众号 | 标题、钩子、正文、结尾CTA |
| 短视频 | 3秒开头、痛点场景、解决方案、行动号召 |
| 分发策略 | 抖音/小红书/B站/微信差异化调整 |

## 风格标准

| 标准 | 说明 |
|------|------|
| 语言 | 中文 |
| 风格 | Dan Koe式 - 直接、钩子驱动 |
| 公众号长度 | 1500-2500字 |
| 短视频时长 | 45-60秒 |

## 触发场景

| 用户表达 | 触发条件 |
|---------|---------|
| "帮我写成公众号文章" | 生成公众号内容 |
| "适合发什么平台" | 分析分发策略 |
| "值得做推广吗" | 卖点分析 |
| "吸引老板的视频脚本" | 生成视频脚本 |
| "有什么卖点" | 提炼核心卖点 |

## Changelog

### v1.0.0 (2026-02-08)
- 项目分析
- 卖点提炼
- 公众号写作
- 短视频脚本
- 全渠道分发
