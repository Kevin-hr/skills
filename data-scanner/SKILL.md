---
name: data-scanner
description: 数据掠食者 - 深度挖掘小红书痛点、闲鱼市场行情、搜索引擎关键词。触发词：挖掘数据、市场调研、竞品分析。
type: Data Scanner
category: Market Research
version: 1.0.0
author: Claude Code
updated: 2026-02-09
tags: [data, scanner, xiaohongshu, xianyu]
---

# Data Scanner 数据掠食者

深度挖掘小红书痛点、闲鱼市场行情、搜索引擎关键词。

## 快速开始

| 场景 | 命令 |
|------|------|
| 挖掘痛点 | `data-scanner --platform xiaohongshu --keyword "收纳盒"` |
| 市场行情 | `data-scanner --platform xianyu --keyword "MacBook"` |
| 关键词挖掘 | `data-scanner --keyword "AI工具" --engine baidu` |

## 支持平台

| 平台 | 功能 |
|------|------|
| 小红书 | 痛点挖掘、用户评论分析 |
| 闲鱼 | 二手市场行情、价格调研 |
| 搜索引擎 | 关键词搜索量、长尾词挖掘 |

## 输出格式

```json
{
  "platform": "xiaohongshu",
  "data_type": "pain_points",
  "items": [
    {"keyword": "收纳盒", "volume": 15000, "pain_point": "太占空间"}
  ],
  "sources": ["链接1", "链接2"]
}
```

## 工作流程

1. 解析用户需求，确定目标平台
2. 使用 WebSearch 搜索相关数据
3. 使用 WebFetch 获取详细内容
4. 结构化整理数据
5. 标注数据来源和时间戳

## Changelog

### v1.0.0 (2026-02-08)
- 支持3大平台数据挖掘
- 集成搜索引擎关键词分析
