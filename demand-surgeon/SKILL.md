---
name: demand-surgeon
description: 需求主刀医生 - 从评论中提取核心痛点，基于NLP进行情绪极性分析。触发词：分析需求、提取痛点、情绪分析。
type: Demand Analyzer
category: Market Research
version: 1.0.0
author: Claude Code
updated: 2026-02-09
tags: [demand, pain-point, nlp, sentiment]
---

# Demand Surgeon 需求主刀医生

从评论中提取核心痛点，基于NLP进行情绪极性分析。

## 快速开始

| 场景 | 命令 |
|------|------|
| 分析需求 | `demand-surgeon --comments "评论.txt"` |
| 提取痛点 | `demand-surgeon --source xiaohongshu --url "链接"` |
| 情绪分析 | `demand-surgeon --sentiment --input data.json` |

## 核心功能

| 功能 | 说明 |
|------|------|
| 痛点提取 | 从乱码评论中提取核心需求 |
| 情绪分析 | NLP情绪极性判断 |
| 优先级排序 | 按频率/严重性排序 |

## 情绪极性

| 极性 | 表现 | 含义 |
|------|------|------|
| 正面 | "太爱了"、"终于找到" | 强需求 |
| 中性 | "还可以"、"一般" | 可优化点 |
| 负面 | "太贵"、"不好用" | 痛点 |

## 输出格式

```json
{
  "pain_points": [
    {
      "id": 1,
      "description": "价格太贵",
      "frequency": 45,
      "severity": "high",
      "emotion": "negative"
    }
  ],
  "sentiment_score": -0.35,
  "recommendations": ["降低价格", "提高性价比"]
}
```

## Changelog

### v1.0.0 (2026-02-08)
- 痛点提取算法
- 情绪极性分析
- 优先级排序
