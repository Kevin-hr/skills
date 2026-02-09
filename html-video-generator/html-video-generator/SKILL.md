---
name: html-video-generator
description: 从 HTML/CSS/JS 动画快速生成 MP4 视频
metadata:
  tags: video, html, ffmpeg, playwright, recording
---

## 使用场景

当用户需要把 HTML/CSS/JS 动画转换为 MP4 视频时使用。

## 完整流程（复制即用）

### 1. HTML 文件结构

创建 `preview.html`：
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    /* 动画效果 */
    .scene { opacity: 0; }
    .scene.active { opacity: 1; transition: all 0.8s; }
    /* 视频尺寸 */
    .video { width: 1920px; height: 1080px; }
  </style>
</head>
<body>
  <div class="video">
    <div class="scene active">场景1</div>
    <div class="scene">场景2</div>
  </div>
  <script>
    // 自动切换场景（每5秒）
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

### 2. 录制视频

**方式 A：使用 Playwright（已安装的项目）**
```bash
cd 项目目录
node -e "
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: { dir: './output', size: { width: 1920, height: 1080 } }
  });

  const page = await context.newPage();
  await page.goto('file://项目路径/preview.html');

  console.log('开始录制...');
  await page.waitForTimeout(45000); // 根据需要调整时长

  await browser.close();
  console.log('完成！');
})();
"
```

**方式 B：独立脚本**
```bash
# 在有 playwright 的项目执行
cd ai_xly
node -e "
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: { dir: '../showcase-video/output', size: { width: 1920, height: 1080 } }
  });

  const page = await context.newPage();
  await page.goto('file://C:/Users/52648/Documents/GitHub/showcase-video/preview.html');

  console.log('开始录制 45 秒...');
  await page.waitForTimeout(48000);

  await browser.close();
  console.log('完成！');
})();
"
```

### 3. 转换为 MP4

```bash
cd 项目目录

# 检查输出文件
ls output/

# 转换（FFmpeg 已安装）
ffmpeg -i output/xxx.webm -c:v libx264 -preset fast -crf 22 showcase-video.mp4 -y
```

## 常用参数

| 参数 | 说明 |
|------|------|
| `-preset fast` | 编码速度，fast 平衡质量和速度 |
| `-crf 22` | 质量 0-51，越低越好，默认 23 |
| `-c:a aac` | 音频编码 |
| `-y` | 覆盖已有文件 |

## 输出

- **位置**: `项目目录/showcase-video.mp4`
- **格式**: H.264 MP4
- **分辨率**: 1920x1080

## 快速命令模板

```bash
# 1. 录制
cd ai_xly && node -e "
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: { dir: '../showcase-video/output', size: { width: 1920, height: 1080 } }
  });

  const page = await context.newPage();
  await page.goto('file://C:/Users/52648/Documents/GitHub/项目名/preview.html');
  await page.waitForTimeout(录制毫秒数);
  await browser.close();
})();
"

# 2. 转换
cd showcase-video && ffmpeg -i output/xxx.webm -c:v libx264 -preset fast -crf 22 showcase-video.mp4 -y
```

## 注意事项

1. **Playwright 已安装位置**: `ai_xly/node_modules/playwright`
2. **FFmpeg 已安装**: `C:\Users\52648\AppData\Local\Microsoft\WinGet\Packages\...\ffmpeg.exe`
3. **HTML 中用 JS 控制场景切换**，比纯 CSS 更灵活
4. **录制时长 = 实际需要时长 + 缓冲时间**
