---
name: file-compressor
description: 智能文件压缩 - 自动检测和压缩文件，保持独立压缩。触发词：压缩文件、批量压缩、定时任务。
type: File Compressor
category: Utilities
version: 1.0.0
author: Claude Code
updated: 2026-02-09
tags: [compress, file, batch, schedule]
---

# File Compressor 文件压缩器

自动检测和压缩文件，保持每个文件独立压缩（最小单元结构）。

## 快速开始

| 场景 | 命令 |
|------|------|
| 预览压缩 | `file-compressor --target ./downloads --mode preview` |
| 执行压缩 | `file-compressor --target ./downloads --mode auto` |
| 单文件压缩 | `file-compressor --file large_file.zip` |

## 支持格式

| 类型 | 格式 | 推荐工具 |
|------|------|---------|
| 图片 | PNG, JPG, WebP | TinyPNG, ImageMagick |
| 视频 | MP4, MOV, WebM | FFmpeg |
| 文档 | PDF, DOCX | Adobe, Pandoc |
| 通用 | gz, zip, 7z | 系统工具 |

## 默认规则

| 规则 | 值 | 说明 |
|------|------|------|
| 最小压缩大小 | 1MB | 大于此值才压缩 |
| 最大保留天数 | 7天 | 超过此天数才压缩 |
| 压缩格式 | gz | 独立压缩格式 |
| 跳过已压缩 | true | 不重复压缩 |

## 配置格式

```markdown
# 压缩配置

min_size_mb: 10      # 最小压缩大小 (MB)
max_age_days: 30     # 最大保留天数
keep_original: false # 是否保留原始文件

# 忽略规则
ignore_extensions: .exe, .zip, .gz, .7z
ignore_patterns: *temp*, *_backup*
```

## 定时任务

| 时间点 | 用途 |
|--------|------|
| 09:00 | 早间清理 |
| 12:00 | 午间整理 |
| 18:00 | 下班清理 |
| 22:00 | 夜间归档 |

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 压缩失败 | 检查文件格式是否支持 |
| 质量下降 | 提高质量参数 |
| 批量超时 | 使用并行处理 |
| 权限错误 | 检查目录写入权限 |

## Changelog

### v1.0.0 (2026-02-08)
- 自动文件检测
- 独立压缩模式
- 定时任务调度
- 配置管理
