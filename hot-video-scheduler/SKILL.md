---
name: hot-video-scheduler
description: 热点视频定时调度器 - 定时触发热点发现、过滤、生成、发布全流程
type: Scheduler & Orchestration
category: Video Production Automation
model: sonnet
version: 1.0.0
author: Claude Code
created: 2026-02-06
tags: [scheduler, cron, automation, video-production]
---

# Hot Video Scheduler

## Skill Metadata

| Field | Value |
|-------|-------|
| **Name** | hot-video-scheduler |
| **Type** | Scheduler & Orchestration |
| **Category** | Video Production Automation |
| **Version** | 1.0.0 |
| **Model** | sonnet |
| **Author** | Claude Code |

## Description

热点视频定时调度器，负责定时触发热点发现、账号匹配过滤、脚本生成、视频合成的全流程。支持每日、每周、cron 表达式等多种调度策略，实现无人值守的批量视频生产。

## When to Use This Skill

使用此技能 PROACTIVELY 当需要：
- 定时执行热点视频生产流水线
- 自动化每日视频发布计划
- 批量生产多个热点视频
- 设置 cron 表达式实现复杂调度
- 实现无人值守的内容生产

## Core Capabilities

### Scheduling Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| daily | 每天固定时间执行 | 日更账号 |
| weekly | 每周特定天执行 | 周更内容 |
| cron | 自定义 cron 表达式 | 复杂调度 |
| on-demand | 手动触发 | 临时需求 |
| event-driven | 事件触发 | 热点突发事件 |

## Input/Output Schema

### Input Format

{
  "schedule": {
    "type": "daily|weekly|cron|on-demand",
    "config": {
      "time": "08:00",
      "timezone": "Asia/Shanghai",
      "cron_expression": "* * * * *",
      "days_of_week": ["Mon", "Wed", "Fri"]
    }
  },
  "pipeline_config": {
    "topics_source": "hot_topic_detector",
    "filter_strategy": "account_niche_filter",
    "max_videos_per_run": 5
  },
  "execution": {
    "parallel": true,
    "max_concurrent": 3,
    "timeout_minutes": 30
  }
}

### Schedule Configurations

#### Daily Schedule

{
  "type": "daily",
  "config": {
    "time": "08:00",
    "timezone": "Asia/Shanghai"
  }
}

#### Weekly Schedule

{
  "type": "weekly",
  "config": {
    "days_of_week": ["Mon", "Wed", "Fri"],
    "time": "09:00",
    "timezone": "Asia/Shanghai"
  }
}

### Output Format

{
  "scheduler_id": "uuid",
  "status": "active|paused|failed",
  "execution_history": [
    {
      "run_id": "uuid",
      "started_at": "2026-02-07T08:00:00Z",
      "completed_at": "2026-02-07T08:15:00Z",
      "status": "completed",
      "pipelines_executed": 3
    }
  ],
  "next_execution": "2026-02-08T08:00:00Z"
}

## Quality Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Schedule Accuracy | >99% | - | ? |
| Pipeline Success Rate | >95% | - | ? |
| Avg Execution Time | <15 min | - | ? |
| Video Production Rate | 10/day | - | ? |

## Error Handling

### Failure Modes

| Error Type | Probability | Impact | Recovery Strategy |
|------------|-------------|--------|-------------------|
| Schedule Missed | 0.1% | Medium | Retry immediately, alert |
| Pipeline Timeout | 5% | High | Kill hanging jobs, retry |
| Resource Exhaustion | 3% | High | Reduce concurrency, queue |
| API Rate Limit | 10% | Medium | Backoff, queue |
| Network Failure | 2% | Medium | Retry with delay |

### Retry Configuration

{
  "max_attempts": 3,
  "initial_delay_seconds": 60,
  "backoff_multiplier": 2,
  "max_delay_seconds": 300
}

## Integration Patterns

### Pipeline Dependencies

hot-video-scheduler
    |
    +-- Trigger: cron/daily/weekly
    +-- hot-topic-detector
    +-- account-niche-filter
    +-- hot-video-factory
    +-- Notifications

### Event Triggers

| Event | Trigger | Action |
|-------|---------|--------|
| Hot Topic Alert | Trending score > 90 | Immediate pipeline run |
| Schedule Time | Cron match | Standard pipeline run |
| Manual Trigger | User command | On-demand pipeline run |

## Monitoring

### Health Check

{
  "status": "healthy",
  "active_schedules": 5,
  "queued_jobs": 0,
  "running_jobs": 2,
  "next_scheduled_run": "2026-02-07T08:00:00Z"
}

## Limitations & Disclaimers

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| API rate limits | May delay batch | Queue management |
| Resource constraints | Limited concurrency | Auto-scaling suggestion |
| Timezone issues | Schedule offset | Explicit timezone config |

## Changelog

### Version 1.0.0 (2026-02-06)

- Initial release
- Daily/Weekly/Cron scheduling
- Pipeline orchestration
- Retry logic
- Alerting system

---

Mission: Enable fully automated hot video production with reliable scheduling and monitoring.
