---
name: verdict-judge
description: 毒舌判官 - 最终决策者，生成PDF/Web报告，扫描法律和平台合规风险。触发词：生成报告、最终判决、风险评估。
type: Report Generator
category: Business Analysis
version: 1.0.0
author: Claude Code
updated: 2026-02-09
tags: [report, verdict, compliance, risk]
---

# Verdict Judge 毒舌判官

最终决策者，生成PDF/Web报告，扫描法律和平台合规风险。

## 快速开始

| 场景 | 命令 |
|------|------|
| 生成报告 | `verdict-judge --topic "AI课程" --format html` |
| 风险评估 | `verdict-judge --assess --product "AI工具"` |
| 最终判决 | `verdict-judge --verdict --data data.json` |

## 报告结构

```markdown
## 商业验证报告

### 1. 执行摘要
- 利润可行性评分: XX/100
- 建议: 通过/不通过/需优化

### 2. 数据洞察
- 市场规模分析
- 痛点验证结果
- 竞争格局

### 3. 财务预测
- 价格敏感度分析
- ROI 预测
- 盈亏平衡点

### 4. 风险评估
- 法律合规风险
- 平台政策风险
- 市场进入壁垒

### 5. 建议下一步
- 最小可行产品 (MVP) 方向
- 关键假设验证
```

## 风险检查清单

| 检查项 | 说明 |
|--------|------|
| 产品版权 | 是否涉及版权问题 |
| 平台规则 | 是否违反平台规则 |
| 法律纠纷 | 是否有法律风险 |
| 供应链 | 供应链是否可行 |

## 输出文件

| 格式 | 文件名 |
|------|--------|
| HTML | `report_{timestamp}.html` |
| PDF | `report_{timestamp}.pdf` |

## Changelog

### v1.0.0 (2026-02-08)
- 生成专业商业验证报告
- 法律合规风险扫描
- 最终可行性判决
