---
name: hot-video-factory
description: 全自动热点视频流水线 - MCP服务器 + 编排层
type: MCP Server & Orchestration Layer
category: Video Production Pipeline
model: opus
version: 2.0.0
author: Claude Code
created: 2026-02-06
tags: [hot-topic, video, mcp, pipeline, automation]
---

# Hot Video Factory

## Skill Metadata

| Field | Value |
|-------|-------|
| **Name** | hot-video-factory |
| **Type** | MCP Server & Orchestration Layer |
| **Category** | Video Production Pipeline |
| **Version** | 2.0.0 |
| **Model** | opus |

## Description

全自动热点视频流水线 MCP 服务器，编排 Skills 完成从热点发现到视频生成的全流程。V2.0专业分镜标准（每分钟25-30分镜）。

## When to Use This Skill

使用此技能 PROACTIVELY 当需要：
- 执行完整的热点视频生产流水线
- 自动化热点发现 → 脚本生成 → 分镜图生成 → 视频合成
- 批量生产多个热点视频

## Core Capabilities

### MCP Tools

| Tool | Description | Response Time |
|------|-------------|---------------|
| run_pipeline | 执行完整流水线 | < 10 min |
| check_status | 检查流水线状态 | < 5s |
| get_output | 获取输出结果 | < 5s |

### Pipeline Stages

Stage 1: [hot-topic-detector]     → 热点发现 (30s)
Stage 2: [account-niche-filter]   → 账号匹配过滤 (15s)
Stage 3: [hot-video-script-generator] → 脚本生成 (2min)
Stage 4: [comfyui-image-generator]    → 分镜图生成 (3min/batch)
Stage 5: [html-video-generator]       → 视频合成 (2min)
Stage 6: [video-quality-checker]       → 质量检验 (30s)

## Input/Output Schema

### Input Format

{
  "topic": "DeepSeek vs OpenAI",
  "target_platform": "抖音",
  "duration_target": "60-90s",
  "style_preference": "AI对比"
}

### Output Format

{
  "pipeline_id": "uuid-v4",
  "status": "completed|failed|partial",
  "execution_time_seconds": 450,
  "quality_report": {
    "overall_score": 8.8
  }
}

## Quality Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Pipeline Success Rate | >95% | ? |
| Average Execution Time | <10 min | ? |
| Script Quality Score | >8.0/10 | ? |

## Error Handling

### Failure Modes

| Error Type | Probability | Impact | Recovery Strategy |
|------------|-------------|--------|-------------------|
| Hot Topic API Timeout | 5% | Medium | Retry 3x with backoff |
| Script Generation Fail | 10% | High | Fallback to template |
| Image Gen API Error | 8% | Medium | Queue for retry |
| Video Synthesis Fail | 3% | Critical | Resume checkpoint |

## V2.0 Professional Storyboard Standard

| Metric | Value |
|--------|-------|
| Shots per minute | 25-30 |
| Scene duration | 2-4 seconds |
| Aspect ratio | 9:16 |
| Resolution | 1080x1920 |

## Limitations & Disclaimers

| Limitation | Mitigation |
|------------|------------|
| API rate limits | Queue system with backoff |
| Content moderation | Pre-filter + manual review |

## Changelog

### Version 2.0.0 (2026-02-06)

- Added V2.0专业分镜标准
- Added MCP Tools integration
- Added pipeline orchestration layer
- Added quality scoring system

---

Mission: Automate end-to-end hot video production with enterprise-grade reliability.
