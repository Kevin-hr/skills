---
name: html-video-generator
description: HTML视频生成器 - 从HTML/CSS/JS动画快速生成MP4视频。使用Playwright录制+FFmpeg转换。触发词：HTML转视频、动画录制、FFmpeg转换。
type: Video Generator
category: Video Production
version: 1.0.0
author: Claude Code
updated: 2026-02-09
tags: [html, video, ffmpeg, playwright]
---

# HTML Video Generator HTML视频生成器

从 HTML/CSS/JS 动画快速生成 MP4 视频。

## 快速开始

| 场景 | 命令 |
|------|------|
| 录制视频 | `html-video-generator --record --html preview.html` |
| 转换视频 | `html-video-generator --convert input.webm` |
| 完整流程 | `html-video-generator --full --html preview.html` |

## HTML模板

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    .scene { opacity: 0; }
    .scene.active { opacity: 1; transition: all 0.8s; }
    .video { width: 1920px; height: 1080px; }
  </style>
</head>
<body>
  <div class="video">
    <div class="scene active">场景1</div>
    <div class="scene">场景2</div>
  </div>
  <script>
    // 自动切换场景
    let currentScene = 0;
    setInterval(() => {
      document.querySelectorAll('.scene').forEach((s, i) => {
        s.classList.toggle('active', i === currentScene);
      });
      currentScene = (currentScene + 1) % document.querySelectorAll('.scene').length;
    }, 5000);
  </script>
</body>
</html>
```

## 录制命令

```bash
# 方式A：Playwright录制
cd ai_xly
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: { dir: '../output', size: { width: 1920, height: 1080 } }
  });
  const page = await context.newPage();
  await page.goto('file://path/to/preview.html');
  await page.waitForTimeout(45000);
  await browser.close();
})();
"
```

## FFmpeg转换

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-preset` | 编码速度 | fast |
| `-crf` | 质量 (0-51) | 22 |
| `-c:a aac` | 音频编码 | - |
| `-y` | 覆盖输出 | - |

```bash
# 转换命令
ffmpeg -i input.webm -c:v libx264 -preset fast -crf 22 output.mp4 -y
```

## 常用参数

| 参数 | 说明 |
|------|------|
| `-preset ultrafast` | 最快编码 |
| `-preset slow` | 最高质量 |
| `-crf 18` | 接近无损 |
| `-crf 28` | 高压缩 |

## 输出规格

| 项目 | 值 |
|------|-----|
| 位置 | 项目目录/output/ |
| 格式 | H.264 MP4 |
| 分辨率 | 1920x1080 |
| 编解码器 | libx264 |

## 注意事项

| 项目 | 位置 |
|------|------|
| Playwright | ai_xly/node_modules/playwright |
| FFmpeg | WinGet安装包 |

## Changelog

### v1.0.0 (2026-02-08)
- HTML/CSS/JS动画录制
- Playwright视频录制
- FFmpeg格式转换
- 完整流程脚本
