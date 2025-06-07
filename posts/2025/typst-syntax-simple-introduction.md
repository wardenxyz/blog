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

````typst
// 绑定简单值
#let name = "张三"
#let age = 25

// 绑定函数
#let greet(person) = [Hello, #person!]

// 使用变量
#name 今年 #age 岁
#greet("李四")
````

`let` 的特点：
- 创建不可变绑定
- 支持函数定义
- 作用域局限于当前块

## `show` - 样式规则

`show` 用于定义元素的显示样式：

````typst
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
````

`show` 的用法：
- `show selector: transformation` - 基本语法
- 可以匹配元素类型、内容或条件
- 变换函数接收匹配的内容并返回新内容

## 组合使用

````typst
#let emphasis-color = red
#show strong: it => text(fill: emphasis-color, it)

这是*强调*文本。
````

这两个功能让 Typst 具有强大的自定义能力，`let` 管理数据和逻辑，`show` 控制视觉呈现。

# wardenxyz: Typst 的函数是什么

GitHub Copilot: 在 Typst 中，函数是可重用的代码块，用于封装逻辑和生成内容。

## 函数定义

使用 `let` 定义函数：

````typst
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
````

## 函数特点

- **参数支持**：可以有位置参数和命名参数
- **默认值**：参数可以有默认值
- **返回内容**：函数返回 Typst 内容，用方括号 `[]` 包围
- **闭包特性**：可以访问外部作用域的变量

## 高阶函数

````typst
// 接受函数作为参数
#let apply-style(content, styler) = styler(content)

#let make-bold = content => strong(content)
#let make-italic = content => emph(content)

#apply-style("重要文本", make-bold)
#apply-style("强调文本", make-italic)
````

## 实际应用

````typst
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
````

函数让 Typst 代码更模块化和可重用，是构建复杂文档的重要工具。

# wardenxyz: let 后面带着的是变量和函数，那 show 呢

GitHub Copilot: `show` 后面跟着的是**选择器**和**变换函数**，用于定义样式规则。

## `show` 的结构

基本语法：`#show selector: transformation`

### 选择器类型

````typst
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
````

### 变换函numeric

````typst
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
````

## 与 `let` 的区别

- **`let`**：定义变量和函数，用于数据存储和逻辑封装
- **`show`**：定义样式规则，用于控制内容的视觉呈现

````typst
// let: 定义数据和逻辑
#let my-color = blue
#let format-title(content) = strong(content)

// show: 定义样式规则
#show heading: it => format-title(it.body)
#show strong: text(fill: my-color)
````

`show` 本质上是声明式的样式系统，告诉 Typst "当遇到某种内容时，如何显示它"。

# wardenxyz: Typst 除了这两个还有什么重要的语法点吗

GitHub Copilot: 除了 `let` 和 `show`，Typst 还有以下重要语法点：

## `#set` - 设置样式

用于设置元素的默认样式：

````typst
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
````

## `#import` 和 `#include` - 模块系统

````typst
// 导入其他文件的函数
#import "utils.typ": helper-function, my-card

// 包含其他文件的内容
#include "chapter1.typ"

// 导入包
#import "@preview/cetz:0.1.0": canvas, draw
````

## 内容块和代码模式

````typst
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
````

## 条件语句和循环

````typst
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
````

## 内置函数和方法

````typst
// 数学函数
#calc.pow(2, 3) // 8
#calc.sin(calc.pi / 2) // 1

// 字符串操作
#"Hello World".split(" ") // ("Hello", "World")
#upper("typst") // "TYPST"

// 数组操作
#(1, 2, 3).len() // 3
#(1, 2, 3).at(1) // 2
````

## `#context` - 上下文访问

````typst
// 访问页面信息
#context {
  let page-num = here().page()
  [当前第 #page-num 页]
}

// 访问计数器
#context {
  [当前标题编号：#counter(heading).display()]
}
````

这些语法点配合使用，让 Typst 具备了完整的编程和排版能力。
