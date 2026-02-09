---
name: valuation-god
description: 估值之神 - 精算师视角，计算价格敏感度、ROI预测、收益模型。触发词：计算利润、估值、定价分析。
type: Valuation Calculator
category: Business Analysis
version: 1.0.0
author: Claude Code
updated: 2026-02-09
tags: [valuation, roi, pricing, profit]
---

# Valuation God 估值之神

精算师视角，计算价格敏感度、ROI预测、收益模型。

## 快速开始

| 场景 | 命令 |
|------|------|
| 计算利润 | `valuation-god --price 99 --cost 30 --volume 1000` |
| ROI预测 | `valuation-god --revenue 100000 --cost 50000` |
| 定价分析 | `valuation-god --analyze --product "AI课程"` |

## 核心公式

### 价格敏感度

```
Elasticity = (% Change in Quantity) / (% Change in Price)

Elasticity > 1: 弹性商品（降价有效）
Elasticity < 1: 刚性商品（可提价）
```

### ROI 预测

```
ROI = (Expected Revenue - Cost) / Cost * 100%

Monthly Revenue = Traffic * Conversion * Price
```

## 输入参数

```json
{
  "product_price": 99,
  "target_market_size": 1000000,
  "estimated_market_share": 0.01,
  "marketing_cost": 5000,
  "production_cost": 30
}
```

## 输出格式

```json
{
  "price_sensitivity": {
    "optimal_price": 89,
    "elasticity": 1.2,
    "recommendation": "建议降价10%提升销量"
  },
  "roi_prediction": {
    "conservative": 50,
    "expected": 120,
    "optimistic": 200,
    "break_even_months": 3
  }
}
```

## Changelog

### v1.0.0 (2026-02-08)
- 价格敏感度计算
- ROI 预测模型
- 收益模拟计算
