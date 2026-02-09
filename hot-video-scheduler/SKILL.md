---
name: hot-video-scheduler
description: 热点视频定时调度器 - 定时触发热点发现、过滤、生成、发布全流程。支持 cron 表达式，实现无人值守批量视频生产。
type: Scheduler & Orchestration
category: Video Production Automation
model: sonnet
version: 1.0.0
author: Claude Code
created: 2026-02-06
updated: 2026-02-09
tags: [scheduler, cron, automation, video-production]
---

# Hot Video Scheduler

定时触发热点视频生产流水线的调度器。

## 快速开始

| 场景 | 命令 |
|------|------|
| 每日调度 | `hot-video-scheduler --mode daily --time 08:00` |
| 每周调度 | `hot-video-scheduler --mode weekly --days Mon,Wed,Fri` |
| Cron 表达式 | `hot-video-scheduler --cron "0 9 * * 1-5"` |

## 调度模式

| 模式 | 配置示例 | 用途 |
|------|----------|------|
| daily | `{"time": "08:00"}` | 日更账号 |
| weekly | `{"days": ["Mon","Wed","Fri"]}` | 周更内容 |
| cron | `{"expression": "0 9 * * 1-5"}` | 复杂调度 |
| on-demand | 手动触发 | 临时需求 |

## 输入格式

```json
{
  "schedule": {
    "type": "daily|weekly|cron|on-demand",
    "config": { "time": "08:00" }
  },
  "pipeline_config": { "max_videos_per_run": 5 }
}
```

## 输出格式

```json
{
  "scheduler_id": "uuid",
  "status": "active",
  "next_execution": "2026-02-10T08:00:00Z"
}
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 调度错过 | 检查 cron 表达式格式 |
| 流水线超时 | 增加 timeout 配置 |
| 并发限制 | 降低 max_concurrent |

## Changelog

### v1.0.0 (2026-02-06)
- 支持 daily/weekly/cron 调度
- 流水线编排
