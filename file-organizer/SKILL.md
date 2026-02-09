---
name: file-organizer
description: 智能文件分类器 - 理解文件上下文，查重去重，建议更好的目录结构。触发词：整理文件、分类归档、清理重复。
type: File Organizer
category: Utilities
version: 1.0.0
author: Claude Code
updated: 2026-02-09
tags: [organize, file, classify, duplicate]
---

# File Organizer 文件整理器

智能文件分类器，理解上下文，查重去重，建议更好的目录结构。

## 快速开始

| 场景 | 命令 |
|------|------|
| 整理目录 | `file-organizer --path ./downloads` |
| 查重模式 | `file-organizer --dedupe` |
| 生成结构 | `file-organizer --suggest` |

## 核心功能

| 功能 | 说明 |
|------|------|
| 结构分析 | 分析当前目录结构 |
| 查重去重 | 识别重复文件 |
| 分类建议 | 提出逻辑分组 |
| 自动整理 | 移动/重命名文件 |

## 分类规则

| 文件类型 | 目标目录 |
|---------|---------|
| 文档 (PDF, DOCX, TXT) | docs/ |
| 代码 (py, js, ts) | scripts/ |
| 配置 (json, yaml) | config/ |
| 图片 (png, jpg, svg) | assets/images/ |
| 视频 (mp4, mov) | assets/videos/ |
| 文档 (pdf, doc) | assets/docs/ |

## 社交媒体分类

| 模式 | 示例 | 目标目录 |
|------|------|---------|
| `wx_*.png` | wx_2wm.png | WeChat/ |
| `*小红书*.jpg` | xxx_来自小红书.jpg | XiaoHongShu/ |
| `*爆款*.png` | 爆款.png | Covers/ |
| `*AI*.png` | 开发思想.png | AI-Resources/ |

## 执行流程

```bash
# Step 1: 创建目录结构
mkdir -p WeChat XiaoHongShu Covers "AI-Resources" Unsorted

# Step 2: 批量移动
mv wx_*.png WeChat/ 2>/dev/null || true
mv *小红书*.jpg XiaoHongShu/ 2>/dev/null || true

# Step 3: 验证结果
du -sh WeChat XiaoHongShu Covers "AI-Resources"
```

## 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件 | YYYY-MM-DD-描述.ext | 2024-10-17-meeting-notes.md |
| 目录 | 小写字母，用连字符 | project-files |
| 前缀排序 | 01-current, 02-archive | 01-active-projects/ |

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 目录混乱 | 指定目标目录分析 |
| 重复文件 | 使用 `--dedupe` 查重 |
| 结构不合理 | 使用 `--suggest` 建议 |
| 误删文件 | 确认后再删除 |

## Changelog

### v1.0.0 (2026-02-08)
- 智能文件分类
- 重复文件检测
- 分类规则引擎
- 批量整理执行
