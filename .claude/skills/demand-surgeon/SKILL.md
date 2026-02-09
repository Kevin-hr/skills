---
name: demand-surgeon
description: 需求主刀医生 - 从评论中提取核心痛点，基于NLP进行情绪极性分析。遇到"分析需求"、"提取痛点"、"情绪分析"时使用。
---

# Demand Surgeon Skill

## 功能

- 从乱码般的评论中提取核心痛点
- 基于 NLP 的情绪极性分析
- 需求优先级排序

## 分析方法

### 痛点提取

1. 收集原始评论数据
2. 分词和关键词提取
3. 聚类相似痛点
4. 按出现频率排序

### 情绪分析

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
