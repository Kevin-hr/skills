---
name: json-canvas
description: JSON Canvas - 创建和编辑 .canvas 画布文件。支持节点、边、群组、连接。触发词：JSON Canvas、画布文件、节点连接。
type: Canvas Editor
category: Obsidian
version: 1.0.0
author: Claude Code
updated: 2026-02-09
tags: [canvas, json, node, edge, obsidian]
---

# JSON Canvas 画布

创建和编辑 JSON Canvas 文件 (.canvas)。

## 文件结构

```json
{
  "nodes": [],
  "edges": []
}
```

## 节点类型

| 类型 | 说明 |
|------|------|
| `text` | 文本节点 (Markdown) |
| `file` | 文件引用节点 |
| `link` | 外部链接节点 |
| `group` | 群组容器节点 |

## 节点属性

| 属性 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | 唯一标识 (16位十六进制) |
| `type` | 是 | 节点类型 |
| `x` | 是 | X坐标 (像素) |
| `y` | 是 | Y坐标 (像素) |
| `width` | 是 | 宽度 (像素) |
| `height` | 是 | 高度 (像素) |
| `color` | 否 | 颜色 |

### Text 节点

```json
{
  "id": "6f0ad84f44ce9c17",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 400,
  "height": 200,
  "text": "# 标题\n\n**粗体**内容。"
}
```

> **注意**: JSON中换行必须用 `\n`，不要用 `\\n`

### File 节点

```json
{
  "id": "a1b2c3d4e5f67890",
  "type": "file",
  "x": 500,
  "y": 0,
  "width": 400,
  "height": 300,
  "file": "Attachments/diagram.png"
}
```

### Link 节点

```json
{
  "id": "c3d4e5f678901234",
  "type": "link",
  "x": 1000,
  "y": 0,
  "width": 400,
  "height": 200,
  "url": "https://obsidian.md"
}
```

### Group 节点

```json
{
  "id": "d4e5f6789012345a",
  "type": "group",
  "x": -50,
  "y": -50,
  "width": 1000,
  "height": 600,
  "label": "项目概览",
  "color": "4"
}
```

## 边 (Edges)

```json
{
  "id": "f67890123456789a",
  "fromNode": "节点A的id",
  "toNode": "节点B的id"
}
```

### 边的完整属性

| 属性 | 说明 |
|------|------|
| `fromSide` | 起始边: `top`, `right`, `bottom`, `left` |
| `toSide` | 终止边 |
| `fromEnd` | 起始端点: `none`, `arrow` |
| `toEnd` | 终止端点 |
| `color` | 线条颜色 |
| `label` | 标签文字 |

## 颜色系统

### 预设颜色

| 值 | 颜色 |
|------|------|
| `"1"` | 红色 |
| `"2"` | 橙色 |
| `"3"` | 黄色 |
| `"4"` | 绿色 |
| `"5"` | 青色 |
| `"6"` | 紫色 |

### 十六进制颜色

```json
{ "color": "#FF0000" }
```

## 推荐尺寸

| 节点类型 | 建议宽度 | 建议高度 |
|---------|---------|---------|
| 小文本 | 200-300 | 80-150 |
| 中文本 | 300-450 | 150-300 |
| 大文本 | 400-600 | 300-500 |
| 文件预览 | 300-500 | 200-400 |

## 布局指南

- 坐标可以是负数 (无限画布)
- X 向右增加，Y 向下增加
- 群组内留 20-50px 内边距
- 节点间距 50-100px
- 对齐到网格 (10 或 20 的倍数)

## 验证规则

1. 所有 `id` 值必须唯一
2. `fromNode`/`toNode` 必须引用存在的节点ID
3. 必填字段必须存在
4. `type` 必须是: `text`, `file`, `link`, `group`
5. `fromSide`/`toSide` 必须是: `top`, `right`, `bottom`, `left`
6. `fromEnd`/`toEnd` 必须是: `none`, `arrow`

## Changelog

### v1.0.0 (2026-02-08)
- 节点类型定义
- 边连接语法
- 颜色系统
- 布局指南
- 验证规则
