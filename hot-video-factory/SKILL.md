---
name: hot-video-factory
description: 全自动热点视频流水线 - Agent Teams 并行编排版 v3.0，从热点发现到视频生成的全流程自动化。支持并行执行，4分钟生成成品。
type: Agent Teams Orchestration
category: Video Production Pipeline
model: opus
version: 3.0.0
author: Claude Code
created: 2026-02-06
updated: 2026-02-09
tags: [hot-topic, video, agent-teams, pipeline, automation, parallel]
agent_teams_enabled: true
---

# Hot Video Factory v3.0 🎬

> Agent Teams 并行编排版 - 从热点发现到视频生成的全自动流水线

## 快速开始

| 场景 | 命令 |
|------|------|
| 对话触发 | "生成一个关于 DeepSeek 的热点视频" |
| 指定主题 | `hot-video-factory --topic "AI降价潮" --platform 抖音` |
| 批量生成 | `hot-video-factory --batch topics.txt --parallel` |

## Agent Teams 架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Lead: Pipeline Coordinator (opus)           │
└─────────────────────────────────────────────────────────────┘
                              │
       ┌────────────┬───────────┼───────────┬────────────┐
       ▼            ▼           ▼           ▼            ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
   │ Topic   │ │ Script  │ │ Visual  │ │ Audio   │ │ Video   │
   │ Hunter  │ │Strat-   │ │ Artist  │ │Pro-     │ │ Editor  │
   │Sonnet 30s│ │ egist   │ │Sonnet 2m│ │ ducer   │ │Sonnet 1m│
   └─────────┘ │ Opus 90s│ └─────────┘ └─────────┘ └─────────┘
              └─────────┘
```

## Teammates 详情

| Teammate | Role | Model | Skills | Duration |
|----------|------|-------|--------|----------|
| topic-hunter | 热点发现专家 | sonnet | hot-topic-detector | 30s |
| script-strategist | 脚本策略师 | opus | viral-creative-lead, viral-memory-bank | 90s |
| visual-artist | 视觉艺术家 | sonnet | storyboard-creator, comfyui-image-generator | 120s |
| audio-producer | 音频制作师 | sonnet | audio-pipeline | 120s |
| video-editor | 视频剪辑师 | sonnet | html-video-generator, video-quality-checker | 60s |

## 输入格式

```json
{
  "topic": "DeepSeek vs OpenAI",
  "target_platform": "抖音",
  "duration_target": "60-90s",
  "style_preference": "AI对比"
}
```

## 输出格式

```json
{
  "pipeline_id": "uuid-v4",
  "status": "completed|failed|partial",
  "execution_time_seconds": 240,
  "quality_report": { "overall_score": 8.8 }
}
```

## v2.x vs v3.0 对比

| 对比项 | v2.x (串行) | v3.0 (并行) |
|--------|------------|-------------|
| 总耗时 | ~10分钟 | ~4分钟 |
| 执行模式 | 串行调用 | 并行编排 |
| 协调方式 | MCP Tools | Agent Teams |

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| Agent Teams 不可用 | 设置 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` |
| 脚本生成失败 | 回退到模板生成 |
| 图像生成超时 | 调整分辨率或步数 |

## Changelog

### v3.0.0 (2026-02-08)
- 重大升级: Agent Teams 并行架构
- 性能提升: 3min → 2min (并行)
- 清晰定位: 每个 teammate 职责明确

### v2.2.0 (2026-02-07)
- viral-creative-agent 替代 hot-video-script-generator
- 集成 DNA 病毒式传播规则
