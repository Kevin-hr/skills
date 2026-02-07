---
name: video-quality-checker
description: AI 视频质量检验工具 - 检验AI生成视频是否符合最低质量标准
type: Quality Assurance
category: Video Production QA
model: haiku
version: 1.0.0
author: Claude Code
created: 2026-02-06
tags: [quality, video, checker, validation, ai-generation]
---

# Video Quality Checker

## Skill Metadata

| Field | Value |
|-------|-------|
| **Name** | video-quality-checker |
| **Type** | Quality Assurance |
| **Category** | Video Production QA |
| **Version** | 1.0.0 |
| **Model** | haiku |
| **Author** | Claude Code |

## Description

AI视频质量检验工具，用于检验AI生成视频是否符合最低质量标准。支持通义万相、Tongyi Wanxiang、Vidu等平台的视频产出检验，不符合标准时给出具体修改建议并打回重做。

## When to Use This Skill

使用此技能 PROACTIVELY 当需要：
- 检验AI生成视频的质量
- 确保视频符合发布标准
- 获取具体的修改建议
- 控制视频质量下限

## Core Capabilities

### Quality Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| 画面质量 | 25% | 分辨率、清晰度、色彩 |
| 音频质量 | 20% | 音量、清晰度、无杂音 |
| 内容质量 | 25% | 逻辑连贯、信息准确 |
| 时长合规 | 15% | 符合平台要求 |
| 平台规范 | 15% | 符合平台政策 |

### Supported Platforms

| Platform | Status | Notes |
|----------|--------|-------|
| 通义万相 | Supported | Full check |
| Tongyi Wanxiang | Supported | Full check |
| Vidu | Supported | Full check |
| 其他 | Partial | Basic check |

## Input/Output Schema

### Input Format

{
  "video": {
    "path": "/path/to/video.mp4",
    "duration_seconds": 75,
    "resolution": "1080x1920",
    "fps": 30
  },
  "source": "tongyi-wanxiang",
  "standards": {
    "min_duration": 60,
    "max_duration": 180,
    "min_resolution": "720p",
    "required_aspect_ratio": "9:16"
  },
  "check_types": ["all"]
}

### Output Format

{
  "check_id": "uuid",
  "timestamp": "2026-02-07T10:30:00Z",
  "status": "passed|failed|warning",
  "video_info": {
    "path": "/path/to/video.mp4",
    "duration": 75,
    "resolution": "1080x1920",
    "fps": 30,
    "format": "mp4"
  },
  "quality_scores": {
    "overall": 8.5,
    "visual": 9.0,
    "audio": 8.0,
    "content": 8.5,
    "compliance": 9.0
  },
  "checks": [
    {
      "check_id": "chk_001",
      "name": "分辨率检查",
      "status": "passed",
      "expected": ">=720p",
      "actual": "1080p",
      "score": 10
    },
    {
      "check_id": "chk_002",
      "name": "时长检查",
      "status": "passed",
      "expected": "60-180s",
      "actual": "75s",
      "score": 10
    },
    {
      "check_id": "chk_003",
      "name": "画面流畅度",
      "status": "warning",
      "expected": "无明显卡顿",
      "actual": "检测到2处轻微卡顿",
      "score": 7,
      "suggestion": "建议重新生成或后期补帧"
    }
  ],
  "suggestions": [
    {
      "priority": "high",
      "issue": "画面有2处轻微卡顿",
      "suggestion": "使用补帧工具处理或重新生成"
    }
  ],
  "decision": {
    "action": "approve|reject|revision_required",
    "reason": "视频质量达标，同意发布"
  }
}

## Quality Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Pass Rate | >95% | - | ? |
| False Reject Rate | <3% | - | ? |
| Check Consistency | >98% | - | ? |
| Processing Time | <30s | - | ? |

### Quality Score Thresholds

| Score Range | Grade | Action |
|-------------|-------|--------|
| 9.0+ | A+ | Auto-approve |
| 8.0-8.9 | A | Auto-approve |
| 7.0-7.9 | B | Minor revisions |
| 6.0-6.9 | C | Major revisions |
| <6.0 | F | Reject |

## Error Handling

### Failure Modes

| Error Type | Probability | Impact | Recovery Strategy |
|------------|-------------|--------|-------------------|
| Video Load Fail | 2% | High | Skip check, warn |
| Analysis Timeout | 5% | Medium | Partial check |
| Invalid Format | 3% | Medium | Skip unsupported |
| API Error | 1% | Medium | Retry once |

## Integration Patterns

### Pipeline Integration

html-video-generator
    |
    +-- Output: video file
    |
    +-- video-quality-checker
    |
    +-- Decision:
    |   +-- Approve: Continue to upload
    |   +-- Revision Required: Return to generator
    |   +-- Reject: Alert, end pipeline

### Check Flow

1. Load video file
2. Extract video/audio info
3. Run quality checks
4. Calculate scores
5. Generate suggestions
6. Make decision

## Quality Check Categories

### Technical Checks

| Check | Min Score | Description |
|-------|-----------|-------------|
| 分辨率 | 7.0 | 至少720p |
| 帧率 | 7.0 | 至少24fps |
| 码率 | 7.0 | 足够清晰 |
| 音频采样 | 7.0 | 44.1kHz+ |

### Content Checks

| Check | Min Score | Description |
|-------|-----------|-------------|
| 连贯性 | 7.0 | 场景切换自然 |
| 字幕同步 | 7.0 | 字幕与音频匹配 |
| 信息准确 | 7.0 | 无明显错误 |

### Compliance Checks

| Check | Min Score | Description |
|-------|-----------|-------------|
| 平台规范 | 8.0 | 符合平台政策 |
| 版权合规 | 10 | 无版权问题 |
| 内容安全 | 10 | 无违规内容 |

## Limitations & Disclaimers

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Subjective quality | Some variance | Multiple checks |
| Platform variations | Different standards | Platform-specific rules |

## Changelog

### Version 1.0.0 (2026-02-06)

- Initial release
- Multi-platform support
- Detailed quality scoring
- Revision suggestions
- Decision automation

---

Mission: Ensure every video meets quality standards before release.
