---
name: skill-analyzer
description: 技能分析器 - 读取和分析 Claude skill 源文件。理解能力、触发词、绑定资源、MCP工具使用。触发词：分析技能、读取SKILL.md、技能结构。
type: Skill Analyzer
category: Utilities
version: 1.0.0
author: Claude Code
updated: 2026-02-09
tags: [analyze, skill, mcp, structure]
---

# Skill Analyzer 技能分析器

读取和分析 Claude skill 源文件，理解能力和结构。

## 快速开始

| 场景 | 命令 |
|------|------|
| 读取单个技能 | `skill-analyzer --read skill-name` |
| 批量读取 | `skill-analyzer --batch [skill1, skill2]` |
| 列出所有技能 | `skill-analyzer --list` |
| 技能对比 | `skill-analyzer --compare skill-a skill-b` |

## 技能结构

```
skill-name/
├── SKILL.md           # 必须（主文档）
├── scripts/           # 可选（脚本）
├── references/        # 可选（参考文档）
└── assets/            # 可选（资源文件）
```

## 分析能力

| 能力 | 说明 |
|------|------|
| 解析Frontmatter | 提取name、description |
| 识别触发词 | When to Use触发条件 |
| 列出资源 | scripts/references/assets |
| 检测MCP工具 | 扫描工具调用模式 |

## MCP工具检测

| 模式 | 说明 |
|------|------|
| `mcp__<server>__<tool>` | MCP工具调用 |
| "web search" | 网络搜索提及 |
| "analyze image" | 图片理解提及 |

## 输出格式

```json
{
  "skill": "skill-name",
  "description": "技能描述",
  "structure": {
    "SKILL.md": true,
    "scripts": 2,
    "references": 1,
    "assets": 0
  },
  "mcp_tools": ["mcp__MiniMax__web_search"],
  "capabilities": ["功能1", "功能2"]
}
```

## 常用任务

| 任务 | 参数 |
|------|------|
| 读取单个技能 | `--read skill-name` |
| 详细列表 | `--list --detailed` |
| 技能对比 | `--compare skill-a skill-b` |
| 检查MCP使用 | `--check skill-name --mcp mcp__*__web_search` |

## 路径参考

| 路径类型 | 位置 |
|---------|------|
| 主目录 | `C:\Users\52648\.claude\skills\` |
| 开发目录 | `C:\Users\52648\.gemini\antigravity\skills\` |

## Changelog

### v1.0.0 (2026-02-08)
- SKILL.md解析
- 目录结构分析
- MCP工具检测
- 批量技能列表
- 技能对比
