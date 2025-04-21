---
title: Typst 笔记
date: 2024-11-27
tags: [Typst]
category: [计算机]
---

# Typst 笔记

[Tyspt 官方文档](https://typst.app/docs)

## 导出命令

**Typst 导出格式总结**

Typst 支持多种导出格式，适用于不同场景`{p}` 参数为导出文件命名以下是主要格式及其特点：

## 1. PDF（默认格式）

```bash
typst c input.typ
```

```bash
typst c --pages 1-3 input.typ  # 仅导出第1-3页
```

## 2. PNG

```bash
typst c input.typ output.png
```

- 多页时必须使用 `{p}` 参数为导出文件命名

- 可通过 `--ppi` 调整分辨率（默认 144 PPI）`{p}` 参数为导出文件命名

```bash
typst c --ppi 300 input.typ "png-{0p}.png"  # 300 DPI，补零页码
```

## 3. SVG

```bash
typst c input.typ output.svg
```

- 多页时必须使用 `{p}` 参数为导出文件命名

```bash
typst c --pages 2,4-6 input.typ "svg-{0p}.svg"  # 导出第 2、4、5、6 页
```

## 4. HTML（实验性功能）

```bash
typst c --features html input.typ output.html
```

## 标题

```typst
= 第一级大标题
== 第二级大标题
```

## 无序列表

```typst
- 无序列表
```

## 有序列表

```typst
1. 有序列表
+ 有序列表
```

## 加重字体

```typst
*加重字体*
```

## 斜体

```typst
_斜体_
```

## 字体

全局：

```typst
#set text(font: "kaiti", fill: red, size: 12pt)
大小为12磅，字体为楷体的红色内容
```

局部：

```typst
#text(font: "kaiti", fill: red, size: 12pt)[大小为12磅，字体为楷体的红色内容]
```

## 位置

全局：

```typst
#set align(left)
居左
```

局部：

```typst
#align(left)[居左]
```

## 下划线

```typst
#underline[此处有下划线]
```

## 上划线

```typst
#overline[此处有上划线]
```

## 上标

```typst
#super[这里是上标内容]
```

## 下标

```typst
#sub[这里是下标内容]
```

## 删除线

```typst
#strike[被删除的内容]
```

## 高亮

```typst
#highlight[高亮内容]
```

## 链接

```typst
#link("https://baidu.com")[百度]
```

## 字间距 & 行间距

```typst
#set par(leading: 18pt) //行间距
#set text(tracking: 0.1pt) //字间距
```

## 文档属性

```typst
#set document(
  title: title,
  author: author,
  keywords: str,array,
  date: none, auto,datetime,
)
```

## 页边距

```typst
  #set page(margin: (
    top: 2.54cm, //上边距
    bottom: 2.54cm, //下边距
    right: 2.54cm, //右边距
    left: 2.54cm, //左边距
  ))
```

## 水印

```typst
#set page(background: rotate(45deg,
  text(50pt, fill: rgb("FFCBC4"))[
    *这是水印*
  ]
))
```

## 引用

```typst
#set quote(block: true) //开启引用块

#quote(attribution: [引用文本的来源])[
  引用的文本
]
```

## 大纲

```typst
#outline()
```

## 手动分页

```typst
#pagebreak()
```

## 插入图片

```typst
#image("4.jpeg")
```

```typst
#figure(
	image("图片路径", width: 10pt),
	caption: "说明"
)
```