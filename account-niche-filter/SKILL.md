---
name: account-niche-filter
description: 账号定位过滤器 - 根据账号画像过滤热点话题，匹配度高的才通过
type: Content Filter & Matcher
category: Account Intelligence
model: haiku
version: 1.0.0
author: Claude Code
created: 2026-02-06
tags: [filter, matching, account, niche]
---

# Account Niche Filter

## Skill Metadata

| Field | Value |
|-------|-------|
| **Name** | account-niche-filter |
| **Type** | Content Filter & Matcher |
| **Category** | Account Intelligence |
| **Version** | 1.0.0 |
| **Model** | haiku |
| **Author** | Claude Code |

## Description

账号定位过滤器，根据账号画像对热点话题进行匹配度评分，过滤不符合定位的热点，推荐最佳脚本类型。确保只有高匹配度的内容才会通过流水线。

## When to Use This Skill

使用此技能 PROACTIVELY 当需要：
- 过滤热点话题与账号定位的匹配度
- 评估内容与账号风格的契合程度
- 推荐最佳的内容类型和风格
- 确保内容产出符合账号调性

## Core Capabilities

### Matching Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| 话题匹配度 | 30% | 话题与账号领域相关程度 |
| 风格匹配度 | 25% | 内容风格与账号调性契合 |
| 受众匹配度 | 20% | 目标受众重合度 |
| 趋势匹配度 | 15% | 与热点趋势的契合度 |
| 转化匹配度 | 10% | 商业转化潜力 |

### Matching Scores

| Score Range | Grade | Action |
|-------------|-------|--------|
| 90-100 | A+ | Highly recommended |
| 80-89 | A | Recommended |
| 70-79 | B | Acceptable |
| 60-69 | C | Marginal |
| <60 | F | Filter out |

## Input/Output Schema

### Input Format

{
  "account_profile": {
    "name": "王总的AI工具库",
    "description": "分享AI工具实测和使用技巧",
    "tags": ["AI工具", "效率", "ChatGPT", "实测"],
    "style": "专业但亲切",
    "target_audience": {
      "age_range": "25-40",
      "interests": ["AI", "编程", "效率工具"],
      "pain_points": ["工具选择困难", "使用门槛高"]
    },
    "content_types": ["干货型", "对比型"],
    "avoid_topics": ["政治", "敏感话题"]
  },
  "topics": [
    {
      "id": "topic_001",
      "keyword": "DeepSeek免费",
      "category": "科技",
      "trending_score": 98,
      "related_keywords": ["AI", "开源", "大模型"]
    }
  ]
}

### Output Format

{
  "filter_id": "uuid",
  "timestamp": "2026-02-07T10:30:00Z",
  "passed_topics": [
    {
      "topic_id": "topic_001",
      "keyword": "DeepSeek免费",
      "match_score": 92,
      "match_grade": "A+",
      "match_details": {
        "topic_match": 95,
        "style_match": 90,
        "audience_match": 88,
        "trend_match": 85,
        "conversion_potential": 92
      },
      "recommended_script_type": "对比型",
      "recommended_style": "专业实测",
      "match_reasons": [
        "高热度： trending_score = 98",
        "高相关： tags匹配度 = 95%",
        "高转化潜力：适合账号受众"
      ]
    }
  ],
  "filtered_topics": [
    {
      "topic_id": "topic_005",
      "keyword": "某明星八卦",
      "match_score": 35,
      "match_grade": "F",
      "filter_reason": "话题与账号定位无关"
    }
  ],
  "statistics": {
    "total_topics": 20,
    "passed": 8,
    "filtered": 12,
    "pass_rate": "40%",
    "avg_match_score": 75
  }
}

## Quality Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Pass Rate | 30-50% | - | ? |
| Match Accuracy | >90% | - | ? |
| False Positive Rate | <5% | - | ? |
| Processing Time | <1s | - | ? |

## Error Handling

### Failure Modes

| Error Type | Probability | Impact | Recovery Strategy |
|------------|-------------|--------|-------------------|
| Account Profile Missing | 2% | High | Use default profile |
| Invalid Topic Format | 3% | Medium | Skip invalid topics |
| Score Calculation Error | 1% | Medium | Use fallback score |

## Integration Patterns

### Pipeline Integration

hot-topic-detector
    |
    +-- Output: raw topics
    |
    +-- account-niche-filter
    |
    +-- Output: filtered topics (match_score >= 70)
    |
    +-- hot-video-script-generator

### Recommended Script Types

| Match Score | Recommended Type |
|-------------|------------------|
| 90+ | 对比型（深度评测） |
| 80-89 | 干货型（知识输出） |
| 70-79 | 热点解读型 |
| <70 | 过滤 |

## Limitations & Disclaimers

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Subjective matching | May misclassify | Review threshold |
| New topics | Lower accuracy | Learning from feedback |

## Changelog

### Version 1.0.0 (2026-02-06)

- Initial release
- 5-dimension matching system
- Script type recommendation
- Quality scoring

---

Mission: Ensure only high-quality, well-matched content passes through the production pipeline.
