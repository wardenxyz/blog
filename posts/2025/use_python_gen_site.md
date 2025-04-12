---
title: 使用 Python 生成静态网页
date: 2025-04-12
tags: [python, site]
category: [计算机]
---

# 使用 Python 生成静态网页

一个简单的静态网站生成器，专门为我的博客设计，支持将 Markdown 文件转换为 HTML 静态网站。

## 特点

- 支持 Markdown 语法
- 代码块语法高亮
- 表格渲染
- 有序和无序列表支持
- 窄页面设计（非全宽页面）
- 通过 GitHub Actions 自动构建和部署到 GitHub Pages
- 使用 Python 3.12 构建

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

1. 将你的 Markdown 文章放在 `posts/YYYY/` 目录中，其中 `YYYY` 是年份（例如 `2024`）
2. 确保每篇文章都有正确的 frontmatter 格式：

```markdown
---
title: 文章标题
date: YYYY-MM-DD
tags: [标签1, 标签2]
category: [分类]
---

# 文章内容开始
```

3. 运行静态网站生成器：

```bash
python static_gen.py
```

4. 生成的网站将位于 `site` 目录中

## 本地预览

生成网站后，您可以使用 Python 内置的 HTTP 服务器进行本地预览：

```bash
cd site
python -m http.server
```

然后在浏览器中访问 `http://localhost:8000` 查看网站。

## 部署

该项目配置了 GitHub Actions 工作流，在你将代码推送到 GitHub 时自动构建和部署。

1. 确保已在 GitHub 仓库设置中启用了 GitHub Pages
2. 推送更改到 GitHub
3. GitHub Actions 将自动构建并部署网站

## 自定义

- 修改 `template.html` 更改网站布局
- 修改 `assets/styles.css` 更改网站样式
- 在 `static_gen.py` 文件的顶部修改网站标题和其他配置
