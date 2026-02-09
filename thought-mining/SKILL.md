---
name: thought-mining
description: 思维挖掘助手 - 通过对话把零散想法倒出来、记录、整理成文章。覆盖从挖掘到成稿的完整流程。触发词：整理想法、写作辅助、成稿。
type: Writing Assistant
category: Content Creation
version: 1.0.0
author: Claude Code
updated: 2026-02-09
tags: [writing, thought, creative, draft]
---

# Thought Mining 思维挖掘助手

通过对话帮助用户把脑子里零散的想法倒出来、整理成文章。

## 五阶段流程

| 阶段 | 名称 | 目标 |
|------|------|------|
| 1 | 思维挖掘 | 把零散想法倒出来，记录成洞察点 |
| 2 | 选题确定 | 从洞察中找核心观点，确定文章方向 |
| 3 | 观点验证 | 联网搜索，验证理解是否正确 |
| 4 | 写作辅助 | 检查逻辑、润色文字、找金句 |
| 5 | 最终审核 | 发布前的最后检查 |

## 快速开始

| 场景 | 命令 |
|------|------|
| 开始写作 | `thought-mining --start --topic "文章主题"` |
| 继续挖掘 | `thought-mining --continue` |
| 进入写作 | `thought-mining --writing` |
| 最终审核 | `thought-mining --review` |

## 调度规则

| 触发条件 | 进入阶段 |
|---------|---------|
| 用户刚开始，没有洞察文件 | 阶段1 |
| 洞察数量达到15-20个 | 阶段2 |
| 用户说"方向对，可以写" | 阶段3 |
| 用户说"逻辑没问题，开始写" | 阶段4 |
| 用户说"差不多定稿了" | 阶段5 |

## 文件结构

```
stages/
├── 01-mining.md         # 思维挖掘
├── 02-topic.md          # 选题确定
├── 03-validation.md     # 观点验证
├── 04-writing.md        # 写作辅助
└── 05-review.md         # 最终审核

templates/
├── insights-template.md        # 洞察记录
└── writing-record-template.md  # 写作记录
```

## 交互原则

| 原则 | 说明 |
|------|------|
| 先倒后理 | 不要急着给结构，先让用户倒干净 |
| 保留风格 | 记录时保留用户原话风格 |
| 自然提问 | 像朋友聊天一样自然 |
| 用户控制 | 用户可随时说"继续"或"停一下" |

## Changelog

### v1.0.0 (2026-02-08)
- 五阶段完整流程
- 思维挖掘对话
- 选题确定
- 观点验证
- 写作辅助
- 最终审核
