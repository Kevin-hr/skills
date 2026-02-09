---
name: agent-browser
description: 浏览器自动化 - 网页测试、表单填写、截图、数据提取。使用Playwright实现。触发词：浏览器自动化、网页测试、表单填写。
type: Browser Automation
category: Automation
version: 1.0.0
author: Claude Code
updated: 2026-02-09
tags: [browser, automation, playwright, testing]
---

# Browser Automation 浏览器自动化

使用 Playwright 实现浏览器自动化操作。

## 快速开始

| 场景 | 命令 |
|------|------|
| 打开页面 | `agent-browser open <url>` |
| 获取元素 | `agent-browser snapshot -i` |
| 点击元素 | `agent-browser click @e1` |
| 填写表单 | `agent-browser fill @e2 "文本"` |
| 关闭浏览器 | `agent-browser close` |

## 核心工作流

```
1. agent-browser open <url>     # 打开页面
2. agent-browser snapshot -i    # 获取交互元素 (@e1, @e2)
3. 使用元素引用进行交互
4. 页面变化后重新snapshot
```

## 导航命令

| 命令 | 说明 |
|------|------|
| `open <url>` | 打开URL |
| `back` | 后退 |
| `forward` | 前进 |
| `reload` | 刷新 |
| `close` | 关闭 |

## 快照命令

| 命令 | 说明 |
|------|------|
| `snapshot` | 完整可访问性树 |
| `snapshot -i` | 仅交互元素（推荐） |
| `snapshot -c` | 紧凑输出 |
| `snapshot -d 3` | 限制深度 |

## 交互命令

| 命令 | 说明 |
|------|------|
| `click @e1` | 点击 |
| `dblclick @e1` | 双击 |
| `fill @e2 "文本"` | 清空并输入 |
| `type @e2 "文本"` | 追加输入 |
| `hover @e1` | 悬停 |
| `scroll down 500` | 滚动 |

## 获取信息

| 命令 | 说明 |
|------|------|
| `get text @e1` | 获取文本 |
| `get html @e1` | 获取HTML |
| `get value @e1` | 获取输入值 |
| `get attr @e1 href` | 获取属性 |
| `get title` | 获取标题 |
| `get url` | 获取URL |

## 检查状态

| 命令 | 说明 |
|------|------|
| `is visible @e1` | 是否可见 |
| `is enabled @e1` | 是否可用 |
| `is checked @e1` | 是否选中 |

## 截图与PDF

| 命令 | 说明 |
|------|------|
| `screenshot` | 保存到临时目录 |
| `screenshot path.png` | 指定路径 |
| `screenshot --full` | 全页面截图 |
| `pdf output.pdf` | 保存为PDF |

## 等待命令

| 命令 | 说明 |
|------|------|
| `wait @e1` | 等待元素 |
| `wait 2000` | 等待毫秒 |
| `wait --text "成功"` | 等待文本 |
| `wait --load networkidle` | 等待网络空闲 |

## 语义定位器

| 命令 | 说明 |
|------|------|
| `find role button click --name "Submit"` | 按角色查找 |
| `find text "登录" click` | 按文本查找 |
| `find label "邮箱" fill "x@x.com"` | 按标签查找 |
| `find placeholder "搜索" type "关键词"` | 按占位符查找 |

## 浏览器设置

| 命令 | 说明 |
|------|------|
| `set viewport 1920 1080` | 设置视口 |
| `set device "iPhone 14"` | 模拟设备 |
| `set geo 37.77 -122.41` | 设置位置 |
| `set offline on` | 离线模式 |
| `set media dark` | 深色模式 |

## 全局选项

| 选项 | 说明 |
|------|------|
| `--session <name>` | 隔离会话 |
| `--json` | JSON输出 |
| `--headed` | 显示浏览器窗口 |
| `--proxy <url>` | 代理服务器 |
| `--full` | 全页面截图 |

## Changelog

### v1.0.0 (2026-02-08)
- 页面导航
- 元素交互
- 表单填写
- 截图/PDF
- 视频录制
- 网络拦截
- 代理支持
