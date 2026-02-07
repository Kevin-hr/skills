---
name: viral-memory-bank
description: 病毒记忆体 Agent - 智能记忆管理与知识进化引擎
type: Memory Management & Knowledge Evolution
category: AI Memory System
model: sonnet
version: 1.0.0
author: Claude Code
created: 2026-02-06
tags: [memory, knowledge, viral, evolution, storage]
---

# Viral Memory Bank

## Skill Metadata

| Field | Value |
|-------|-------|
| **Name** | viral-memory-bank |
| **Type** | Memory Management & Knowledge Evolution |
| **Category** | AI Memory System |
| **Version** | 1.0.0 |
| **Model** | sonnet |
| **Author** | Claude Code |

## Description

病毒记忆体 Agent，智能记忆管理与知识进化引擎。支持三层记忆持久化（user/project/local），提供脚本存储、策略查询、知识进化、脚本评估等功能，持续优化爆款内容DNA。

## When to Use This Skill

使用此技能 PROACTIVELY 当需要：
- 存储新的脚本和策略
- 查询爆款DNA规则
- 分析并进化知识库
- 评估脚本质量

## Core Capabilities

### Memory Tiers

| Tier | Scope | Persistence | Use Case |
|------|-------|-------------|----------|
| **user** | 跨项目共享 | 终身有效 | 通用爆款规则 |
| **project** | 当前项目 | 项目周期内 | 项目特定策略 |
| **local** | 当前会话 | 会话结束清除 | 临时实验 |

### Core Functions

| Function | Description |
|----------|-------------|
| **Ingest** | 存储新脚本/策略 |
| **Query** | 查询爆款DNA规则 |
| **Evolve** | 分析并进化知识库 |
| **Evaluate** | 评估脚本质量 |

## Input/Output Schema

### Input Format

{
  "operation": "ingest|query|evolve|evaluate",
  "tier": "user|project|local",
  "data": {
    "type": "script|strategy|rule|template",
    "content": {...}
  },
  "query": {
    "keywords": ["AI对比", "干货"],
    "filters": {
      "min_score": 8.0,
      "category": "对比型"
    }
  }
}

### Output Format

{
  "operation": "ingest|query|evolve|evaluate",
  "result": {
    "success": true,
    "id": "uuid",
    "message": "..."
  },
  "data": {...},
  "metadata": {
    "tier": "user",
    "created_at": "2026-02-07T10:30:00Z",
    "version": "1.0.0"
  }
}

## Quality Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Query Accuracy | >90% | - | ? |
| Evolution Improvement | >5%/cycle | - | ? |
| Storage Reliability | 99.9% | - | ? |
| Response Time | <100ms | - | ? |

## Error Handling

### Failure Modes

| Error Type | Probability | Impact | Recovery Strategy |
|------------|-------------|--------|-------------------|
| Storage Write Fail | 1% | High | Retry, alert |
| Query Timeout | 2% | Medium | Return cached |
| Memory Corruption | 0.1% | Critical | Restore from backup |

## Integration Patterns

### Pipeline Integration

hot-video-script-generator
    |
    +-- Output: script JSON
    |
    +-- viral-memory-bank
    |
    +-- Operations:
    |   +-- Ingest: Store successful scripts
    |   +-- Query: Get similar successful scripts
    |   +-- Evolve: Analyze patterns
    |   +-- Evaluate: Score new scripts

### Knowledge Evolution Cycle

1. **Collect**: Gather successful scripts
2. **Analyze**: Find patterns in top performers
3. **Evolve**: Update DNA rules
4. **Apply**: Use rules for new scripts
5. **Feedback**: Track performance

## Memory Schema

### Script Memory

{
  "script_id": "uuid",
  "type": "script",
  "tier": "project",
  "content": {
    "topic": "DeepSeek vs OpenAI",
    "type": "对比型",
    "platform": "抖音",
    "score": 9.2
  },
  "dna": {
    "hook_pattern": "对比结果预告",
    "structure_pattern": "总分总",
    "length_pattern": "90-120s"
  },
  "performance": {
    "views": 1000000,
    "likes": 50000,
    "shares": 10000
  },
  "tags": ["AI", "对比", "干货"]
}

### Strategy Memory

{
  "strategy_id": "uuid",
  "type": "strategy",
  "tier": "user",
  "content": {
    "name": "AI对比黄金公式",
    "rules": [
      "开头3秒必须有对比结论",
      "中间必须有数据支撑",
      "结尾必须有选型建议"
    ]
  },
  "success_rate": 0.85
}

## Limitations & Disclaimers

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Memory size | Limited storage | Auto-archive old |
| Evolution speed | Slow improvement | Parallel analysis |

## Changelog

### Version 1.0.0 (2026-02-06)

- Initial release
- Three-tier memory system
- Four core operations
- Knowledge evolution cycle

---

Mission: Continuously evolve viral content DNA through intelligent memory management.
