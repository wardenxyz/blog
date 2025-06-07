---
title: Typst 语法简单介绍
date: 2025-06-07
tags: [Typst]
category: [计算机, AI]
---

# Typst 语法简单介绍

# wardenxyz: 解释下 Typst 的 let 和 show

GitHub Copilot: Typst 中的 `let` 和 `show` 是两个核心概念，用于变量绑定和内容样式化：

## `let` - 变量绑定

`let` 用于创建变量或函数绑定：

```typst
// 绑定简单值
#let name = "张三"
#let age = 25

// 绑定函数
#let greet(person) = [Hello, #person!]

// 使用变量
#name 今年 #age 岁
#greet("李四")
```

`let` 的特点：
- 创建不可变绑定
- 支持函数定义
- 作用域局限于当前块

## `show` - 样式规则

`show` 用于定义元素的显示样式：

```typst
// 为特定元素类型设置样式
#show heading: it => [
  #set text(fill: blue)
  #it.body
]

// 为特定内容设置样式
#show "重要": strong

// 条件样式
#show heading.where(level: 1): it => [
  #set text(size: 20pt)
  #it
]

= 标题一
这是*重要*内容。
```

`show` 的用法：
- `show selector: transformation` - 基本语法
- 可以匹配元素类型、内容或条件
- 变换函数接收匹配的内容并返回新内容

## 组合使用

```typst
#let emphasis-color = red
#show strong: it => text(fill: emphasis-color, it)

这是*强调*文本。
```

这两个功能让 Typst 具有强大的自定义能力，`let` 管理数据和逻辑，`show` 控制视觉呈现。

# wardenxyz: Typst 的函数是什么

GitHub Copilot: 在 Typst 中，函数是可重用的代码块，用于封装逻辑和生成内容。

## 函数定义

使用 `let` 定义函数：

```typst
// 简单函数
#let greet(name) = [Hello, #name!]

// 带默认参数的函数
#let format-date(day, month: "January", year: 2024) = [
  #day #month, #year
]

// 返回内容的函数
#let highlight(content, color: red) = [
  #text(fill: color, weight: "bold")[#content]
]
```

## 函数特点

- **参数支持**：可以有位置参数和命名参数
- **默认值**：参数可以有默认值
- **返回内容**：函数返回 Typst 内容，用方括号 `[]` 包围
- **闭包特性**：可以访问外部作用域的变量

## 高阶函数

```typst
// 接受函数作为参数
#let apply-style(content, styler) = styler(content)

#let make-bold = content => strong(content)
#let make-italic = content => emph(content)

#apply-style("重要文本", make-bold)
#apply-style("强调文本", make-italic)
```

## 实际应用

```typst
// 创建卡片组件
#let card(title, content, color: gray) = [
  #rect(
    fill: color.lighten(80%),
    stroke: color,
    inset: 1em,
    radius: 4pt
  )[
    #strong(title)
    #v(0.5em)
    #content
  ]
]

#card("提示", [这是一个提示信息], color: blue)
```

函数让 Typst 代码更模块化和可重用，是构建复杂文档的重要工具。

# wardenxyz: let 后面带着的是变量和函数，那 show 呢

GitHub Copilot: `show` 后面跟着的是**选择器**和**变换函数**，用于定义样式规则。

## `show` 的结构

基本语法：`#show selector: transformation`

### 选择器类型

```typst
// 1. 元素类型选择器
#show heading: it => [...]
#show strong: it => [...]
#show table: it => [...]

// 2. 字符串内容选择器
#show "重要": strong
#show "TODO": it => text(fill: red)[#it]

// 3. 正则表达式选择器
#show regex("r\d+"): it => text(fill: blue)[#it]

// 4. 条件选择器
#show heading.where(level: 1): it => [...]
#show table.where(columns: 3): it => [...]

// 5. 函数选择器
#show raw.where(lang: "python"): it => [...]
```

### 变换函numeric

```typst
// 1. 简单替换
#show "重要": strong

// 2. 函数变换
#show heading: it => [
  #set text(fill: blue, size: 1.2em)
  #it.body
]

// 3. 复杂变换
#show figure: it => [
  #rect(stroke: gray)[
    #it.body
    #align(center)[#emph(it.caption)]
  ]
]
```

## 与 `let` 的区别

- **`let`**：定义变量和函数，用于数据存储和逻辑封装
- **`show`**：定义样式规则，用于控制内容的视觉呈现

```typst
// let: 定义数据和逻辑
#let my-color = blue
#let format-title(content) = strong(content)

// show: 定义样式规则
#show heading: it => format-title(it.body)
#show strong: text(fill: my-color)
```

`show` 本质上是声明式的样式系统，告诉 Typst "当遇到某种内容时，如何显示它"。

# wardenxyz: Typst 除了这两个还有什么重要的语法点吗

GitHub Copilot: 除了 `let` 和 `show`，Typst 还有以下重要语法点：

## `#set` - 设置样式

用于设置元素的默认样式：

```typst
// ...existing code...

// 设置全局文本样式
#set text(font: "Source Han Serif", size: 12pt)

// 设置标题样式
#set heading(numbering: "1.")

// 设置页面样式
#set page(margin: 2cm, numbering: "1")

// 局部设置
#set text(fill: red)
这段文字是红色的
#set text(fill: black) // 恢复默认
```

## `#import` 和 `#include` - 模块系统

```typst
// 导入其他文件的函数
#import "utils.typ": helper-function, my-card

// 包含其他文件的内容
#include "chapter1.typ"

// 导入包
#import "@preview/cetz:0.1.0": canvas, draw
```

## 内容块和代码模式

```typst
// 内容模式（默认）
这是普通文本

// 代码模式（#开头）
#let x = 5
#if x > 3 { [x 大于 3] }

// 内容块（方括号）
#let message = [
  这是一个内容块
  可以包含 *格式化* 文本
]
```

## 条件语句和循环

```typst
// 条件语句
#let score = 85
#if score >= 90 {
  [优秀]
} else if score >= 80 {
  [良好]
} else {
  [需要努力]
}

// 循环
#for i in range(1, 4) {
  [第 #i 项]
}

// 数组遍历
#let items = ("苹果", "香蕉", "橙子")
#for item in items {
  [- #item]
}
```

## 内置函数和方法

```typst
// 数学函数
#calc.pow(2, 3) // 8
#calc.sin(calc.pi / 2) // 1

// 字符串操作
#"Hello World".split(" ") // ("Hello", "World")
#upper("typst") // "TYPST"

// 数组操作
#(1, 2, 3).len() // 3
#(1, 2, 3).at(1) // 2
```

## `#context` - 上下文访问

```typst
// 访问页面信息
#context {
  let page-num = here().page()
  [当前第 #page-num 页]
}

// 访问计数器
#context {
  [当前标题编号：#counter(heading).display()]
}
```

这些语法点配合使用，让 Typst 具备了完整的编程和排版能力。

# wardenxyz: polygon 呢，这个的用处

GitHub copilot: `polygon` 是 Typst 中用于绘制多边形的函数，主要用于创建几何图形和装饰元素。

## 基本用法

```typst
// 绘制三角形
#polygon(
  (0pt, 0pt),
  (20pt, 0pt),
  (10pt, 15pt)
)

// 绘制正方形
#polygon(
  (0pt, 0pt),
  (20pt, 0pt),
  (20pt, 20pt),
  (0pt, 20pt)
)

// 设置样式
#polygon(
  fill: blue,
  stroke: red + 2pt,
  (0pt, 0pt),
  (30pt, 0pt),
  (15pt, 25pt)
)
```

## 实际应用场景

### 1. 创建箭头和指示符

```typst
// 右箭头
#let right-arrow = polygon(
  fill: black,
  (0pt, 5pt),
  (10pt, 5pt),
  (10pt, 8pt),
  (15pt, 4pt),
  (10pt, 0pt),
  (10pt, 3pt),
  (0pt, 3pt)
)

流程：开始 #right-arrow 处理 #right-arrow 结束
```

### 2. 装饰性元素

```typst
// 星形装饰
#let star = polygon(
  fill: aqua,
  (10pt, 0pt),
  (12pt, 6pt),
  (18pt, 6pt),
  (14pt, 10pt),
  (16pt, 16pt),
  (10pt, 13pt),
  (4pt, 16pt),
  (6pt, 10pt),
  (2pt, 6pt),
  (8pt, 6pt)
)

#align(center)[
  #star 重要提示 #star
]
```

### 3. 图表和示意图

```typst
// 创建简单的流程图节点
#let diamond(content) = box(
  polygon(
    fill: yellow.lighten(60%),
    stroke: blue,
    (15pt, 0pt),
    (30pt, 15pt),
    (15pt, 30pt),
    (0pt, 15pt)
  )
)

#diamond[]
```

### 4. 与其他元素结合

```typst
// 带边框的提示框
#let warning-box(content) = [
  #polygon(
    fill: orange.lighten(80%),
    stroke: orange + 1pt,
    (0pt, 0pt),
    (100pt, 0pt),
    (100pt, 40pt),
    (0pt, 40pt)
  )
  #place(dx: 10pt, dy: 10pt)[#content]
]

#warning-box([这是警告信息])
```

## 参数说明

- **坐标点**：定义多边形的顶点
- **fill**：填充色
- **stroke**：描边样式
- **closed**：是否闭合（默认 true）

`polygon` 特别适合创建自定义图形、图标、装饰元素和简单的几何图表。

# wardenxyz: 那我怎么知道哪个点是哪个点

GitHub copilot: 在 `polygon` 中确定坐标点位置可以通过以下方法：

## 坐标系统理解

Typst 使用**左上角为原点 (0, 0)** 的坐标系：
- **x 轴**：向右为正
- **y 轴**：向下为正

```typst
// 可视化坐标点
#let show-points(points) = {
  for (i, point) in points.enumerate() {
    place(dx: point.at(0), dy: point.at(1))[
      #circle(radius: 2pt, fill: red)
      #text(size: 8pt, fill: blue)[#i]
    ]
  }
}

// 示例：三角形的点
#let triangle-points = (
  (0pt, 0pt),    // 点0: 左上角
  (40pt, 0pt),   // 点1: 右上角  
  (20pt, 30pt)   // 点2: 底部中心
)

#polygon(..triangle-points, fill: yellow.lighten(80%), stroke: black)
#show-points(triangle-points)
```

## 调试技巧

### 1. 逐步添加点

```typst
// 先画两个点
#polygon((0pt, 0pt), (30pt, 0pt))

// 再加第三个点
#polygon((0pt, 0pt), (30pt, 0pt), (15pt, 25pt))

// 继续添加...
```

### 2. 使用网格背景

```typst
// 创建网格帮助定位
#let grid(width: 100pt, height: 100pt) = {
  for x in range(0, int(width / 10pt) + 1) {
    line(start: (x * 10pt, 0pt), end: (x * 10pt, height), stroke: gray + 0.5pt)
  }
  for y in range(0, int(height / 10pt) + 1) {
    line(start: (0pt, y * 10pt), end: (width, y * 10pt), stroke: gray + 0.5pt)
  }
}

#grid()
#polygon((10pt, 10pt), (40pt, 20pt), (30pt, 50pt), fill: blue.lighten(70%))
```

### 3. 标注坐标

```typst
#let labeled-polygon(..points) = {
  polygon(..points, fill: yellow.lighten(80%))
  for (i, point) in points.pos().enumerate() {
    place(dx: point.at(0) - 5pt, dy: point.at(1) - 10pt)[
      #text(size: 8pt, fill: red)[
        (#point.at(0), #point.at(1))
      ]
    ]
  }
}

#labeled-polygon(
  (0pt, 0pt),
  (30pt, 10pt), 
  (25pt, 40pt),
  (5pt, 35pt)
)
```

## 常用形状的点序

```typst
// 正方形（顺时针）
#polygon(
  (0pt, 0pt),    // 左上
  (30pt, 0pt),   // 右上
  (30pt, 30pt),  // 右下
  (0pt, 30pt)    // 左下
)

// 箭头
#polygon(
  (0pt, 10pt),   // 箭尾上
  (20pt, 10pt),  // 箭身上
  (20pt, 5pt),   // 箭头上
  (30pt, 15pt),  // 箭头尖
  (20pt, 25pt),  // 箭头下
  (20pt, 20pt),  // 箭身下
  (0pt, 20pt)    // 箭尾下
)
```

建议先在纸上画出草图，标记好坐标，再转换为代码。

# wardenxyz: 顺序是从左上第一个点开始顺时针旋转吗

GitHub copilot: **不一定**，`polygon` 的点顺序是按照你提供的坐标顺序依次连接，不强制要求从左上角开始或顺时针。

## 点的连接规则

```typst
// 点按提供顺序连接：0→1→2→3→...→0（自动闭合）

// 你的例子分析：
#polygon((0pt, 0pt), (30pt, 0pt), (30pt, 25pt), (15pt, 25pt))
//       点0: 左上    点1: 右上      点2: 右下      点3: 左下偏右

// 连接顺序：(0,0) → (30,0) → (30,25) → (15,25) → 回到(0,0)
```

## 不同顺序的效果

```typst
// 顺时针绘制矩形
#polygon(
  (0pt, 0pt),    // 左上
  (40pt, 0pt),   // 右上  
  (40pt, 30pt),  // 右下
  (0pt, 30pt),   // 左下
  fill: blue.lighten(80%)
)

#v(1em)

// 逆时针绘制（结果相同）
#polygon(
  (0pt, 0pt),    // 左上
  (0pt, 30pt),   // 左下
  (40pt, 30pt),  // 右下
  (40pt, 0pt),   // 右上
  fill: red.lighten(80%)
)

#v(1em)

// 乱序连接（会产生交叉）
#polygon(
  (0pt, 0pt),    // 左上
  (40pt, 30pt),  // 右下
  (40pt, 0pt),   // 右上
  (0pt, 30pt),   // 左下
  fill: green.lighten(80%)
)
```

## 最佳实践

1. **简单图形**：顺时针或逆时针都可以
2. **复杂图形**：建议按边界顺序连接，避免交叉
3. **调试技巧**：使用点可视化函数查看连接顺序

```typst
// 启用点可视化来调试
#let show-points(points) = {
  for (i, point) in points.enumerate() {
    place(dx: point.at(0), dy: point.at(1))[
      #circle(radius: 2pt, fill: red)
      #text(size: 8pt, fill: blue)[#i]
    ]
  }
}

#let my-points = ((0pt, 0pt), (30pt, 0pt), (30pt, 25pt), (15pt, 25pt))
#polygon(..my-points, fill: yellow.lighten(80%))
#show-points(my-points)
```

关键是理解 Typst 会按你提供的点的顺序依次连线，最后自动闭合到第一个点。

# wardenxyz: 解释代码

```typst
#polygon.regular(
  fill: blue.lighten(80%),
  stroke: blue,
  size: 30pt,
  vertices: 3,
)
```

GitHub Copilot: 这段代码使用了 Typst 语言来绘制一个正多边形。让我来解释各个参数的作用：

## 代码解释

```typst
#polygon.regular(
  fill: blue.lighten(80%),      // 填充颜色：蓝色变浅80%
  stroke: blue,                 // 边框颜色：蓝色
  size: 30pt,                   // 大小：30点
  vertices: 3,                  // 顶点数：3个（绘制三角形）
)
```

**各参数说明：**

- `fill: blue.lighten(80%)` - 设置多边形的填充颜色为浅蓝色（将蓝色亮度提高80%）
- `stroke: blue` - 设置多边形边框的颜色为蓝色
- `size: 30pt` - 设置多边形的大小为30点
- `vertices: 3` - 设置多边形的顶点数为3，因此绘制的是一个三角形

**最终效果：** 这段代码会生成一个浅蓝色填充、蓝色边框的正三角形，大小为30点。

# wardenxyz: .regular 是什么意思

GitHub Copilot: `.regular` 是 Typst 中 `polygon` 模块的一个方法，用于创建**正多边形**。

## 含义解释

- **`.regular`** = "规则的"、"正的"
- 表示创建的多边形是**正多边形**（所有边长相等，所有内角相等）

## 与其他多边形方法的区别

在 Typst 中，`polygon` 有不同的方法：

```typst
// 正多边形 - 所有边和角都相等
#polygon.regular(vertices: 3, size: 30pt)  // 正三角形

// 不规则多边形 - 通过具体坐标点定义
#polygon((0pt, 0pt), (10pt, 0pt), (5pt, 10pt))  // 任意三角形
```

## 为什么使用 .regular

使用 `.regular` 的优势：
- **简单**: 只需指定顶点数和大小
- **规整**: 自动生成完美的正多边形
- **灵活**: 通过 `vertices` 参数可以创建任意正多边形（三角形、正方形、五边形等）

在你的代码中，`vertices: 3` 配合 `.regular` 创建了一个正三角形。

# wardenxyz: curve 和 polygon 的异同

GitHub Copilot: ## Curve 和 Polygon 的异同

### **相同点**
- 都是 Typst 中用于绘制图形的函数
- 都可以设置颜色、填充、边框等样式属性
- 都支持坐标点定义图形形状

### **主要区别**

| 特性 | `polygon` | `curve` |
|------|-----------|---------|
| **图形类型** | 多边形（直线段连接） | 曲线（平滑曲线） |
| **边缘特征** | 直线边缘，有明确顶点 | 平滑曲线边缘 |
| **封闭性** | 自动封闭图形 | 可开放或封闭 |

### **使用示例对比**

```typst
// Polygon - 直线连接的多边形
#polygon((0pt, 0pt), (20pt, 0pt), (10pt, 15pt))  // 三角形

// Polygon 正多边形
#polygon.regular(vertices: 6, size: 20pt)  // 正六边形

// Curve - 平滑曲线
#path(
  fill: red.lighten(80%),
  stroke: red,
  closed: true,
  ((0pt, 0pt), (20pt, 0pt), (10pt, 15pt))
)
```

### **选择建议**
- **使用 `polygon`**: 需要绘制有明确边角的图形（三角形、四边形、星形等）
- **使用 `curve`**: 需要绘制平滑的曲线图形（圆润的形状、波浪线等）

在你的代码中，`polygon` 适合绘制三角形这种有明确顶点的几何图形。
