---
name: hot-topic-detector
description: 热点检测器 - 从微博/抖音/百度等平台抓取热搜，支持关键词精准过滤。触发词：今日热点、趋势分析、选题推荐。
type: Data Collector
category: Hot Topic Discovery
version: 2.0.0
author: Claude Code
updated: 2026-02-09
tags: [hot-topic, trends, social-media, data-collection]
---

# Hot Topic Detector 热点检测器

从微博、抖音、百度、小红书等平台抓取实时热搜，支持关键词精准过滤。

## 快速开始

| 场景 | 命令 |
|------|------|
| 今日热点 | `hot-topic-detector --today` |
| 精准过滤 | `hot-topic-detector --keywords "AI,DeepSeek"` |
| 趋势分析 | `hot-topic-detector --trend --days 7` |

## 工作模式

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| 全量模式 | 抓取所有热点 | 发现新选题 |
| 精准模式 | 关键词过滤 | 定向内容生产 |

## 支持平台

| 平台 | 数据类型 | 更新频率 |
|------|---------|---------|
| 微博 | 热搜榜 | 实时 |
| 抖音 | 热点榜 | 实时 |
| 百度 | 热搜榜 | 实时 |
| 小红书 | 笔记热度 | 实时 |

## 输入参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `mode` | string | precise | 采集模式 |
| `keywords` | array | [] | 过滤关键词 |
| `filters` | object | {} | 过滤条件 |
| `time_range` | object | {} | 时间范围 |

## 输出格式

```json
{
  "detection_id": "uuid",
  "timestamp": "2026-02-07T10:30:00Z",
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
      "related_keywords": ["AI", "开源", "大模型"]
    }
  ],
  "statistics": {
    "total_topics_found": 100,
    "matched_topics": 15,
    "avg_trending_score": 75,
    "top_category": "科技"
  }
}
```

## 质量指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 数据新鲜度 | <5分钟 | 更新延迟 |
| 检测准确率 | >90% | 匹配精度 |
| 话题覆盖率 | >95% | 覆盖范围 |
| 误报率 | <10% | 错误率 |

## 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| API超时 | 网络问题 | 退避重试 |
| 频率限制 | 请求过多 | 等待重试 |
| 网络错误 | 连接问题 | 立即重试 |
| 数据解析错误 | 格式变更 | 跳过记录 |

## 集成关系

```
hot-topic-detector → topics → account-niche-filter → recommendations
                        ↓
              hot-video-script-generator
```

## Changelog

### v2.0.0 (2026-02-06)
- 多平台支持
- 全量/精准模式
- 热度评分计算
- 集成模式文档
