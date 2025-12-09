# Agent Context: GitHub-Based Blog

## Project Overview

这是一个基于 GitHub 托管的极简 Markdown 博客，完全使用纯 Markdown 文件和 GitHub 的原生功能构建。该项目使用一个用 Python 编写的自定义静态站点生成器，将包含 Frontmatter 的 Markdown 文件转换为完整的静态网站。该博客具有自动生成分类、标签索引以及按年月组织所有文章的主页的功能。

该项目设计为托管在 GitHub Pages 上，并使用 GitHub Actions 进行自动化构建和部署。网站包含以下功能：

- 自动生成目录
- 代码语法高亮
- 支持 MathJax 数学公式
- 支持 Mermaid 图表渲染
- 深色/浅色主题支持
- 全文搜索功能
- RSS 订阅源生成
- 通过站点地图和 Open Graph 标签进行 SEO 优化

## Technology Stack

该项目使用 Python，依赖项如下（来自 requirements.txt）：

- `Markdown==3.8` - 用于 Markdown 处理
- `python-frontmatter==1.1.0` - 用于处理 Markdown 文件中的 YAML 前置元数据
- `PyYAML==6.0.2` - 用于 YAML 解析
- `beautifulsoup4==4.13.3` - 用于 HTML 处理
- `pymdown-extensions==10.12` - 用于 Markdown 处理的扩展

## Directory Structure

```
blog/
├── .github/                 # GitHub Actions workflows and site generation scripts
│   ├── workflows/
│   │   ├── build-deploy.yml # Deploy to GitHub Pages workflow
│   │   └── update-indexes.yml # Update indexes workflow
│   ├── scripts/
│   │   ├── static_gen.py    # Static site generator
│   │   └── update_indexes.py # Updates README.md, tags.md, categories.md
│   ├── templates/
│   │   └── base.html        # HTML template for generated pages
│   └── static/
│       ├── style.css        # Base CSS styles
│       ├── theme.css        # Theme (dark/light mode) CSS
│       ├── main.js          # Site JavaScript
│       ├── favicon.svg      # Site favicon
│       ├── sw.js            # Service worker for caching
│       └── performance.js   # Performance monitoring script
├── posts/                   # Markdown blog posts organized by year
│   ├── 2024/                # Posts from 2024
│   └── 2025/                # Posts from 2025
│   └── ....
│   └── ....
├── README.md               # Main blog page with all posts
├── categories.md           # Auto-generated categories page
├── tags.md                 # Auto-generated tags page
├── AGENTS.md               # Agent-related documentation
├── requirements.txt        # Python dependencies
└── .gitignore              # Git ignore rules
```

## Blog Post Structure

博客文章使用包含元数据的 YAML frontmatter 的 Markdown 文件编写：

```markdown
---
title: Docker Desktop 学习笔记
date: 2025-11-24
tags: [docker]
category: [计算机]
---

# Docker Desktop 学习笔记

Content here...
```

文章存储在 `posts/YYYY/` 目录中，其中 YYYY 是发布的年份。

## Building and Running

### Local Development

由于这是一个仅包含 Markdown 的仓库，且由 GitHub Actions 构建，因此没有正式的本地开发构建系统。不过，若要在本地生成静态网站：

```bash
uv venv

.venv\Scripts\activate

uv pip install -r requirements.txt

uv run .github\scripts\static_gen.py

python -m http.server -d site
```

### GitHub Actions Workflows

该项目使用两个主要的 GitHub Actions 工作流：

1. **更新博客索引** (`update-indexes.yml`):
   - 当 posts/ 目录发生变化时，在推送到 main 分支时触发
   - 根据文章内容更新 README.md、tags.md 和 categories.md
   - 将更改提交回仓库

2. **部署到 GitHub Pages** (`build-deploy.yml`):
   - 在 update-indexes 工作流完成后触发
   - 使用 static_gen.py 生成整个静态网站
   - 将网站部署到配置的 GitHub Pages 仓库
   - 需要一个 DEPLOY_KEY 密钥用于部署

## Development Conventions

### Post Creation

- 在 `posts/YYYY/` 目录中创建 Markdown 文件
- 包含包含 `title`、`date`、`tags` 和 `category` 的 YAML frontmatter
- 使用能反映内容的描述性文件名

### Frontmatter Fields

- `title`: 文章标题
- `date`: 发布日期，格式为 YYYY-MM-DD
- `tags`: 文章的标签数组
- `category`: 文章的分类数组

### Content Guidelines

- 使用 Markdown 格式编写
- 使用围栏代码块来展示代码片段
- 支持使用 `$...$` 和 `$$...$$` 语法书写数学表达式
- 支持使用 mermaid 代码块绘制 Mermaid 图表

## Automatic Features

- **索引生成**: 当添加新文章时，README.md、tags.md 和 categories.md 会自动更新
- **SEO 优化**: 自动生成 sitemap.xml、robots.txt 和 RSS 订阅源
- **主题支持**: 内置深色/浅色主题，支持自动切换
- **搜索功能**: 使用 Fuse.js 的客户端搜索
- **性能优化**: 图片和 iframe 的懒加载、代码分割以及 CDN 使用

## Deployment

该网站通过 GitHub Actions 自动部署到 GitHub Pages。工作流程如下：

1. 检出仓库
2. 运行静态站点生成器
3. 将生成的文件推送到指定的 GitHub Pages 仓库
4. 使网站可通过 `https://warednxyz.github.io` 访问
