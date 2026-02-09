---
name: obsidian-bases
description: Obsidian Bases - 创建和编辑 .base 数据库文件。支持视图、筛选器、公式、汇总。触发词：Obsidian数据库、 Bases语法、视图筛选。
type: Database Editor
category: Obsidian
version: 1.0.0
author: Claude Code
updated: 2026-02-09
tags: [obsidian, database, base, formula, view]
---

# Obsidian Bases 数据库

创建和编辑 Obsidian Bases (.base) 数据库文件。

## 文件结构

```yaml
filters:                    # 全局筛选器
  and: []
  or: []
formulas:                   # 公式定义
  total: "price * quantity"
properties:                 # 属性显示名
  name:
    displayName: "名称"
views:                      # 视图定义
  - type: table
    name: "表格视图"
```

## 筛选器语法

| 运算符 | 说明 |
|--------|------|
| `==` | 等于 |
| `!=` | 不等于 |
| `>` | 大于 |
| `<` | 小于 |
| `&&` | 并且 |
| `||` | 或者 |

```yaml
# 单条件
filters: 'status == "done"'

# AND 条件
filters:
  and:
    - 'status == "done"'
    - 'priority > 3'

# OR 条件
filters:
  or:
    - file.hasTag("book")
    - file.hasTag("article")

# 嵌套条件
filters:
  or:
    - file.hasTag("important")
    - and:
        - file.hasTag("book")
        - file.hasLink("Textbook")
```

## 视图类型

| 类型 | 说明 |
|------|------|
| `table` | 表格视图 |
| `cards` | 卡片视图 |
| `list` | 列表视图 |
| `map` | 地图视图 |

```yaml
views:
  - type: table
    name: "任务表格"
    order:
      - file.name
      - status
      - due_date
    summaries:
      price: Sum
      count: Average
```

## 公式函数

### 全局函数

| 函数 | 说明 |
|------|------|
| `date()` | 解析日期 |
| `duration()` | 解析时长 |
| `now()` | 当前时间 |
| `today()` | 当天日期 |
| `if()` | 条件判断 |
| `min()/max()` | 最小/最大值 |
| `file()` | 获取文件对象 |

### 日期函数

| 字段/函数 | 说明 |
|-----------|------|
| `date.year` | 年 |
| `date.month` | 月 |
| `date.day` | 日 |
| `date.format("YYYY-MM-DD")` | 格式化 |
| `(date - today()).days` | 天数差 |

### 字符串函数

| 函数 | 说明 |
|------|------|
| `contains()` | 包含子串 |
| `startsWith()` | 开头匹配 |
| `lower()` | 小写 |
| `replace()` | 替换 |
| `split()` | 分割 |

### 列表函数

| 函数 | 说明 |
|------|------|
| `contains()` | 包含元素 |
| `filter()` | 筛选 |
| `map()` | 映射 |
| `sort()` | 排序 |
| `unique()` | 去重 |

## 文件属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `file.name` | 字符串 | 文件名 |
| `file.path` | 字符串 | 完整路径 |
| `file.ext` | 字符串 | 扩展名 |
| `file.size` | 数字 | 文件大小 |
| `file.mtime` | 日期 | 修改时间 |
| `file.tags` | 列表 | 所有标签 |
| `file.links` | 列表 | 内部链接 |

## 汇总公式

| 名称 | 输入类型 | 说明 |
|------|---------|------|
| `Average` | 数字 | 平均值 |
| `Sum` | 数字 | 求和 |
| `Min/Max` | 数字 | 最小/最大值 |
| `Median` | 数字 | 中位数 |
| `Earliest` | 日期 | 最早 |
| `Latest` | 日期 | 最近 |
| `Count` | 任意 | 计数 |

## 常用模式

```yaml
# 按标签筛选
filters:
  and:
    - file.hasTag("project")

# 按文件夹筛选
filters:
  and:
    - file.inFolder("Notes")

# 按日期范围
filters:
  and:
    - 'file.mtime > now() - "7d"'

# 按属性值
filters:
  and:
    - 'status == "active"'
    - 'priority >= 3'
```

## 嵌入 Bases

```markdown
![[MyBase.base]]

<!-- 指定视图 -->
![[MyBase.base#View Name]]
```

## Changelog

### v1.0.0 (2026-02-08)
- Base 文件格式
- 筛选器语法
- 公式函数参考
- 视图类型定义
- 常用模式示例
