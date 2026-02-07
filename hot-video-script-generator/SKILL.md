---
name: hot-video-script-generator
description: 热点视频脚本生成器 - 基于5大核心原则自动生成爆款脚本
type: Script Generation Engine
category: Content Creation
model: sonnet
version: 2.0.0
author: Claude Code
created: 2026-02-06
tags: [script, video, hot-topic, viral, content]
requires: [account-niche-filter]
---

# Hot Video Script Generator

## Skill Metadata

| Field | Value |
|-------|-------|
| **Name** | hot-video-script-generator |
| **Type** | Script Generation Engine |
| **Category** | Content Creation |
| **Version** | 2.0.0 |
| **Model** | sonnet |
| **Author** | Claude Code |

## Description

热点视频脚本生成器，基于5大核心原则自动生成符合账号画像的爆款脚本。严格遵循有用、底层逻辑、热点入口、开头承诺、AI对比原则，自动进行质量检验，输出结构化 JSON 格式供下游流水线使用。

## When to Use This Skill

使用此技能 PROACTIVELY 当需要：
- 根据热点话题生成爆款视频脚本
- 按照5大核心原则生成内容
- 产出符合王总画像的定向内容
- 输出结构化 JSON 供自动化流水线使用

## Core Capabilities

### 5 Core Principles

| Principle | Weight | Description | Implementation |
|-----------|--------|-------------|----------------|
| 有用性 | 25% | 提供实际价值，解决用户痛点 | 干货输出 + 可操作建议 |
| 底层逻辑 | 25% | 解释为什么，而非只说什么 | 原理分析 + 逻辑推演 |
| 热点入口 | 20% | 蹭热点，获取流量 | 热点关联 + 趋势切入 |
| 开头承诺 | 15% | 开头给出明确价值承诺 | Hook设计 + 预期管理 |
| AI对比 | 15% | AI工具/方案横向对比 | 多维度评测 + 优劣势 |

### Script Types

| Type | Duration | Scenes | Use Case |
|------|----------|--------|----------|
| 干货型 | 60-90s | 20-25 | 知识输出 |
| 对比型 | 90-120s | 25-30 | AI工具评测 |
| 热点解读型 | 45-60s | 15-20 | 热点事件 |
| 教程型 | 120-180s | 30-40 | 技能教学 |

## Input/Output Schema

### Input Format

{
  "topic": "DeepSeek为什么免费",
  "target_platform": "抖音",
  "script_type": "干货型",
  "duration_target": "60-90s",
  "account_profile": {
    "name": "王总的AI工具库",
    "style": "专业实测",
    "tags": ["AI工具", "效率", "实测"]
  }
}

### Output Format

{
  "script_id": "uuid-v4",
  "version": "2.0.0",
  "metadata": {
    "topic": "DeepSeek为什么免费",
    "platform": "抖音",
    "type": "干货型",
    "duration_seconds": 75,
    "scene_count": 25
  },
  "structure": {
    "opening": {
      "type": "hook",
      "duration_seconds": 3,
      "content": "你知道吗？有一个AI工具刚刚宣布永久免费...",
      "commitment": "看完这条视频，让你彻底理解AI战争的底层逻辑"
    },
    "body": [
      {
        "section": 1,
        "title": "DeepSeek的战略意图",
        "duration_seconds": 15,
        "key_points": ["开源策略", "生态占领", "数据飞轮"]
      }
    ],
    "closing": {
      "type": "cta",
      "duration_seconds": 5,
      "content": "关注我，持续分享AI工具实测..."
    }
  },
  "scenes": [
    {
      "scene_id": 1,
      "timestamp": "0:00-0:03",
      "type": "opening",
      "visuals": ["AI界面", "免费标签动画"],
      "audio": ["背景音乐", "旁白"],
      "text_overlay": "永久免费？原因揭秘"
    }
  ],
  "quality_scores": {
    "overall": 8.7,
    "usefulness": 9.0,
    "logic_depth": 8.5,
    "hot_entry": 8.8,
    "opening_commitment": 9.0,
    "ai_comparison": 8.0,
    "compliance": 9.5
  },
  "5_principles_validation": {
    "usefulness": {"passed": true, "score": 9.0},
    "underlying_logic": {"passed": true, "score": 8.5},
    "hot_entry": {"passed": true, "score": 8.8},
    "opening_commitment": {"passed": true, "score": 9.0},
    "ai_comparison": {"passed": true, "score": 8.0}
  }
}

## Quality Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Overall Score | >8.0/10 | - | ? |
| Usefulness | >8.0/10 | - | ? |
| Logic Depth | >7.5/10 | - | ? |
| Hot Entry | >8.0/10 | - | ? |
| Opening Commitment | >8.5/10 | - | ? |
| AI Comparison | >7.0/10 | - | ? |
| Compliance Rate | >99% | - | ? |

### Quality Score Distribution

| Score Range | Grade | Action |
|-------------|-------|--------|
| 9.0+ | A+ | Auto-approve |
| 8.0-8.9 | A | Auto-approve |
| 7.0-7.9 | B | Minor review |
| 6.0-6.9 | C | Major review |
| <6.0 | F | Regenerate |

## Error Handling

### Failure Modes

| Error Type | Probability | Impact | Recovery Strategy |
|------------|-------------|--------|-------------------|
| Topic Not Clear | 5% | Medium | Ask for clarification |
| Account Profile Missing | 3% | High | Use default profile |
| Model Timeout | 8% | Medium | Retry with shorter prompt |
| Quality Score Too Low | 15% | Medium | Regenerate with feedback |

### Quality Gate

{
  "min_overall_score": 7.0,
  "min_individual_scores": {
    "usefulness": 7.0,
    "logic_depth": 6.5,
    "hot_entry": 7.0,
    "opening_commitment": 7.5,
    "ai_comparison": 6.0
  },
  "compliance_required": true,
  "max_regenerations": 3
}

## Integration Patterns

### Pipeline Integration

Input: hot-topic-detector + account-niche-filter
    |
    +-- hot-video-script-generator
    |
Output: JSON script --> comfyui-image-generator

### Downstream Consumers

| Consumer | Output Used | Format |
|----------|-------------|--------|
| comfyui-image-generator | scenes, visuals | JSON |
| html-video-generator | scenes, audio | JSON |
| viral-memory-bank | Full script | JSON |

## Script Structure Templates

### 干货型 (60-90s)

[开场 Hook: 3s]
  - 痛点切入 / 震惊数据 / 疑问抛出
[价值承诺: 2s]
  - 看完你将学会/理解/掌握...
[主体 Section 1: 20s]
  - 是什么（核心概念）
  - 为什么（底层逻辑）
[主体 Section 2: 25s]
  - 怎么做（实操步骤）
  - 避坑指南（常见错误）
[主体 Section 3: 20s]
  - 进阶技巧（高级用法）
  - 资源推荐（工具清单）
[结尾 CTA: 5s]
  - 关注引导
  - 互动引导

### 对比型 (90-120s)

[开场 Hook: 3s]
  - 对比结果预告 / 争议性结论
[价值承诺: 2s]
  - 看完你就知道该选哪个...
[对比维度介绍: 5s]
  - 价格对比 / 功能对比 / 性能对比
[深度对比 Section 1: 25s]
  - 工具A vs 工具B
  - 实际案例展示
[深度对比 Section 2: 25s]
  - 优劣势分析
  - 适用场景
[决策建议: 20s]
  - 选型建议
  - 使用建议
[结尾 CTA: 5s]

## Limitations & Disclaimers

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Real-time data | May be outdated | Add data freshness check |
| Subjective quality | Varies by topic | Human review option |
| Length constraints | May truncate | Adjust parameters |

## Changelog

### Version 2.0.0 (2026-02-06)

- Added 5 core principles validation
- Added quality scoring system
- Added compliance checking
- Added scene-by-scene breakdown
- Added 3 script type templates

### Version 1.0.0 (2026-01-XX)

- Initial release
- Basic script generation

---

Mission: Generate viral-ready video scripts that follow proven content principles and account positioning.
