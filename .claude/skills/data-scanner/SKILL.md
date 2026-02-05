---
name: data-scanner
description: 数据掠食者 - 深度挖掘小红书痛点、闲鱼市场行情、搜索引擎关键词。遇到"挖掘数据"、"市场调研"、"竞品分析"时使用。
---

# Data Scanner Skill

## 功能

从以下平台获取真实市场数据：
- **小红书** - 痛点挖掘、用户评论分析
- **闲鱼** - 二手市场行情、价格调研
- **搜索引擎** - 关键词搜索量、长尾词挖掘

## 工具使用

```bash
# WebSearch 示例
WebSearch("小红书 痛点 收纳盒 2025")
WebSearch("闲鱼 二手 MacBook 价格 2025")
WebSearch("收纳盒 长尾关键词 搜索量")

# WebFetch 示例
WebFetch("https://www.xiaohongshu.com/explore/...")
```

## 输出格式

返回结构化数据：
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
