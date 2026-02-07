---
name: hot-topic-detector
description: 热点检测器 - 从微博/抖音/百度等平台抓取热搜，支持关键词精准过滤
type: Data Collector & Intelligence
category: Hot Topic Discovery
model: sonnet
version: 2.0.0
author: Claude Code
created: 2026-02-06
tags: [hot-topic, trends, social-media, data-collection]
---

# Hot Topic Detector

## Skill Metadata

| Field | Value |
|-------|-------|
| **Name** | hot-topic-detector |
| **Type** | Data Collector & Intelligence |
| **Category** | Hot Topic Discovery |
| **Version** | 2.0.0 |
| **Model** | sonnet |
| **Author** | Claude Code |

## Description

热点检测器，从微博、抖音、百度、小红书等平台抓取实时热搜，支持关键词精准过滤。提供全量模式和精准模式两种工作方式，全量模式获取所有热点，精准模式仅返回与指定关键词匹配的热点。

## When to Use This Skill

使用此技能 PROACTIVELY 当需要：
- 获取当前热点话题
- 监控特定关键词的热度变化
- 分析热点发展趋势
- 为视频内容生产提供选题支持

## Core Capabilities

### Working Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **全量模式** | 抓取所有热点 | 发现新选题 |
| **精准模式** | 关键词过滤匹配 | 定向内容生产 |

### Supported Platforms

| Platform | Data Type | Update Frequency |
|----------|------------|-----------------|
| 微博 | 热搜榜 | Real-time |
| 抖音 | 热点榜 | Real-time |
| 百度 | 热搜榜 | Real-time |
| 小红书 | 笔记热度 | Real-time |

## Input/Output Schema

### Input Format

{
  "mode": "precise|all",
  "keywords": ["AI", "ChatGPT", "DeepSeek"],
  "filters": {
    "min_trending_score": 60,
    "max_results": 50,
    "categories": ["科技", "互联网"]
  },
  "time_range": {
    "start": "2026-02-07T00:00:00Z",
    "end": "2026-02-07T23:59:59Z"
  }
}

### Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| mode | string | No | precise | 采集模式 |
| keywords | array | No | [] | 过滤关键词 |
| filters | object | No | {} | 过滤条件 |
| time_range | object | No | {} | 时间范围 |

### Output Format

{
  "detection_id": "uuid",
  "timestamp": "2026-02-07T10:30:00Z",
  "platform": "微博",
  "mode": "precise",
  "topics": [
    {
      "id": "topic_001",
      "keyword": "DeepSeek免费",
      "rank": 1,
      "trending_score": 98,
      "heat_index": 12500000,
      "trend_direction": "up",
      "trend_change_percent": 25.5,
      "category": "科技",
      "related_keywords": ["AI", "开源", "大模型"],
      "first_seen": "2026-02-07T08:00:00Z",
      "last_updated": "2026-02-07T10:30:00Z"
    }
  ],
  "statistics": {
    "total_topics_found": 100,
    "matched_topics": 15,
    "avg_trending_score": 75,
    "top_category": "科技"
  }
}

## Quality Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Data Freshness | <5 min | - | ? |
| Detection Accuracy | >90% | - | ? |
| Topic Coverage | >95% | - | ? |
| False Positive Rate | <10% | - | ? |

## Error Handling

### Failure Modes

| Error Type | Probability | Impact | Recovery Strategy |
|------------|-------------|--------|-------------------|
| Platform API Timeout | 10% | Medium | Retry with backoff |
| Rate Limit Exceeded | 15% | Medium | Wait and retry |
| Network Error | 5% | Medium | Retry immediately |
| Data Parse Error | 3% | Low | Skip and log |
| Platform Blocked | 1% | High | Switch platform |

## Integration Patterns

### Pipeline Integration

hot-topic-detector
    |
    +-- Input: keywords, filters
    |
    +-- Output: topics array
    |
    +-- account-niche-filter (next stage)

### Downstream Consumers

| Consumer | Input Used | Purpose |
|----------|-------------|---------|
| account-niche-filter | topics, keywords | 账号匹配过滤 |
| hot-video-script-generator | matched_topics | 脚本选题 |
| hot-video-factory | trending_topics | 流水线输入 |

## Limitations & Disclaimers

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| API rate limits | Data delay | Multiple sources |
| Platform restrictions | Missing data | Fallback sources |
| Real-time delay | 5-15 min | Cache recent data |

## Changelog

### Version 2.0.0 (2026-02-06)

- Added multi-platform support
- Added precise/all modes
- Added trending score calculation
- Added integration patterns

---

Mission: Provide accurate, real-time hot topic intelligence for content production.
