# Agent Context: GitHub-Based Blog

## Project Overview

这是一个基于 GitHub 托管的极简 Markdown 博客。文章是纯 Markdown 文件，由仓库内用 Python 编写的自定义静态站点生成器（`.github/scripts/static_gen.py`）转换为完整的静态网站，并通过 GitHub Actions 自动构建、部署到 GitHub Pages。

站点支持：

- 自动生成目录（TOC）、侧边栏与面包屑
- Prism.js 代码语法高亮（含本地 Typst 语法与语言别名/标签）
- MathJax 数学公式与 Mermaid 图表，均按需加载
- 深色/浅色主题（自动/手动切换）
- 基于 Fuse.js 的客户端全文搜索（首页头部搜索框与搜索弹窗）
- RSS（`feed.xml`）、`sitemap.xml`、`robots.txt`、Open Graph / JSON-LD 等 SEO 输出
- Service Worker 缓存、图片灯箱、代码复制按钮、阅读进度条
- 静态资源指纹（`?v=<hash>`）用于缓存失效

## Technology Stack

该项目使用 Python（CI 中使用 3.12），依赖项来自 `requirements.txt`：

- `Markdown==3.8.1` - Markdown 渲染，启用 `toc`、`fenced_code`、`tables`、`sane_lists`、`attr_list`、`pymdownx.magiclink`、`pymdownx.superfences`、`pymdownx.highlight` 等扩展
- `python-frontmatter==1.1.0` - 解析 Markdown 的 YAML frontmatter
- `PyYAML==6.0.2` - YAML 解析
- `beautifulsoup4==4.13.3` - HTML 处理（链接重写、媒体增强、描述提取）
- `pymdown-extensions==11.0.1` - `superfences`（Mermaid 围栏代码块转换）等扩展
- `livereload==2.7.0` - 本地热重载开发服务器
- `soupsieve==2.9.0`、`typing_extensions==4.13.2` - 传递依赖

前端资源主要来自 jsDelivr CDN：Prism.js、MathJax 3、Mermaid 10、Fuse.js；站点自身的 CSS/JS 位于 `.github/static/`。

## Directory Structure

```
blog/
├── .github/
│   ├── workflows/
│   │   ├── build-deploy.yml    # 构建并部署到 GitHub Pages
│   │   └── update-indexes.yml  # 更新 README.md、tags.md、categories.md
│   ├── scripts/
│   │   ├── static_gen.py       # 静态站点生成器
│   │   ├── update_indexes.py   # 索引生成脚本
│   │   └── dev.py              # 本地热重载开发服务器
│   ├── templates/
│   │   └── base.html           # 页面模板（含主题、搜索、MathJax、Mermaid、SW 注册）
│   └── static/
│       ├── style.css           # 基础样式
│       ├── theme.css           # 深色/浅色主题
│       ├── main.js             # 交互逻辑（搜索、主题、目录、复制、灯箱等）
│       ├── prism-setup.js      # Prism 语言别名、标签与配置
│       ├── prism-typst.js      # Prism Typst 语法定义
│       ├── performance.js      # 性能监控
│       ├── sw.js               # Service Worker 缓存
│       └── favicon.svg         # 站点图标
├── .vscode/
│   ├── tasks.json              # 常用任务（建环境、构建、预览、热重载）
│   ├── settings.json
│   └── posts.code-snippets     # 新建文章 frontmatter 片段
├── .zed/
│   └── tasks.json              # Zed 任务配置
├── posts/                      # 按年份组织的文章
│   ├── 2024/
│   ├── 2025/
│   └── 2026/
├── README.md                   # 首页（包含自动生成的年份/月文章列表）
├── categories.md               # 自动生成的分类页
├── tags.md                     # 自动生成的标签页
├── requirements.txt            # Python 依赖
├── AGENTS.md                   # Agent 相关文档
├── .gitignore                  # 忽略 .venv、site、__pycache__ 等
└── site/                       # 生成输出目录（已忽略，不提交）
```

## Blog Post Structure

博客文章是包含 YAML frontmatter 的 Markdown 文件：

```markdown
---
title: Docker Desktop 学习笔记
date: 2025-11-24
tags: [docker]
category: [计算机]
draft: false
---

# Docker Desktop 学习笔记

Content here...
```

文章存储在 `posts/YYYY/` 目录中，`YYYY` 为发布年份。构建输出保持同样的相对路径：`posts/2025/xxx.md` → `site/posts/2025/xxx.html`。

### Frontmatter Fields

- `title`: 文章标题（必填）
- `date`: 发布日期，格式为 `YYYY-MM-DD`（必填；索引脚本依赖该字段排序）
- `tags`: 标签数组
- `category`: 分类数组（`static_gen.py` 也兼容 `categories` 字段，但 `update_indexes.py` 只读取 `category`，因此统一使用 `category`）
- `draft`: 可选布尔值，`true` 时 `static_gen.py` 跳过该文章，不生成页面
- `image`: 可选特色图片路径，用于 Open Graph / Twitter 卡片

注意：`update_indexes.py` 目前不会过滤 `draft: true`，因此草稿一旦提交仍会出现在 README、标签和分类索引中；发布前应改为 `false` 或不要提交草稿。

`static_gen.py` 的行为：

- 若缺少 `date`，尝试使用 git 首次提交日期；索引脚本没有该回退，仍应显式填写 `date`
- 通过 git 获取最后修改时间并展示
- 未提供描述时，从渲染后的正文提取约 180 字符作为 SEO 描述
- 自动将 `.md` 链接改写为 `.html`，外部链接在新标签页打开
- 自动为图片/iframe 添加懒加载等增强属性

## Building and Running

本地开发推荐使用热重载服务器：

```bash
uv venv

.venv\Scripts\activate

uv pip install -r requirements.txt

uv run .github\scripts\dev.py
```

`dev.py` 会先构建一次，然后监听根目录 `*.md`、`posts/**/*.md`、`.github/templates/**`、`.github/static/**` 与 `static_gen.py`，在变更时重新构建，并在 `http://127.0.0.1:8000` 提供服务。

一次性构建并预览：

```bash
uv run .github\scripts\static_gen.py
python -m http.server -d site
```

也可以直接使用编辑器任务：

- VS Code：`.vscode/tasks.json` 提供 `create venv`、`install dependencies`、`generate site & view site`、`dev server (hot reload)`、`remove .venv`、`remove site`
- Zed：`.zed/tasks.json` 提供同等任务

生成器入口与输出：

- 输入：根目录 `README.md`、`categories.md`、`tags.md` 以及 `posts/**/*.md`
- 输出：`site/`（先清空再生成）
- 根页面映射：`README.md` → `site/index.html`，`categories.md` → `site/categories.html`，`tags.md` → `site/tags.html`
- 额外产物：`site/search.json`、`site/sitemap.xml`、`site/robots.txt`、`site/feed.xml`、`site/404.html`、`site/static/`
- 文章目录中的图片/媒体（`.png`、`.jpg`、`.jpeg`、`.gif`、`.svg`、`.webp`、`.mp4`、`.mp3`、`.pdf`）会按原相对路径复制到 `site/`
- `SITE_URL` 环境变量可覆盖站点根地址；未设置时默认 `https://<owner>.github.io`
- 静态资源通过内容哈希添加 `?v=` 参数，避免缓存过期

本地验证：运行 `uv run .github\scripts\static_gen.py`，确认构建成功并检查 `site/index.html` 与相关文章页面。仓库没有自动化测试套件。

## GitHub Actions Workflows

### 1. 更新博客索引（`update-indexes.yml`）

- 触发条件：推送到 `main` 且变更包含 `posts/**`
- 安装 `pyyaml` 与 `python-frontmatter` 后运行 `python .github/scripts/update_indexes.py`
- 更新：
  - `README.md` 中 `<!-- BLOG-POST-LIST:START -->` 与对应结束标记之间的年份/月文章列表
  - `tags.md`（按标签分组，组内按日期倒序）
  - `categories.md`（按分类分组，组内按日期倒序）
- 以 `index - <Asia/Shanghai 时间>` 提交并推送回 `main`

不要手动编辑 README 中标记之间的内容，也不要手动维护 `tags.md`、`categories.md` 的条目。

### 2. 部署到 GitHub Pages（`build-deploy.yml`）

- 触发条件：`更新博客索引` 工作流完成后（`workflow_run`，`main` 分支），或手动 `workflow_dispatch`
- 使用 Python 3.12、`pip install -r requirements.txt`
- 设置 `SITE_URL=https://wardenxyz.github.io` 后运行 `static_gen.py`
- 使用 `DEPLOY_KEY` SSH 密钥克隆 `wardenxyz/wardenxyz.github.io`
- 通过 `rsync -av --delete site/* target_repo/` 同步生成结果
- 以 `Deploy - GMT+8 <时间>` 提交并推送到目标仓库

注意：由于部署由 `update-indexes` 的完成事件触发，只修改模板、脚本或静态资源（不涉及 `posts/**`）时不会自动重新部署，需要手动运行 `Deploy to GitHub Pages` 工作流。

## Development Conventions

### Post Creation

- 在 `posts/YYYY/` 目录中创建 Markdown 文件，文件名应能描述内容
- 包含 `title`、`date`、`tags`、`category` 的 YAML frontmatter
- 可使用 `.vscode/posts.code-snippets` 中的 `posts` 片段快速生成 frontmatter（包含 `draft` 字段）
- 文章资源与文章放在同一目录（或 `posts/` 下的相对位置），构建时会自动复制

### Content Guidelines

- 使用 Markdown 编写，围栏代码块由 Prism.js 高亮
- 代码块语言支持 `typst`、`powershell`（`ps1`/`ps`/`pwsh`）、`python`（`py`）、`js`、`markdown`（`md`）等；Typst 语法由本地 `prism-typst.js` 提供，其余语言由 Prism autoloader 按需加载
- `prism-setup.js` 中的别名：`ps1`/`ps`/`pwsh` → PowerShell，`typ` → Typst，`txt`/`text`/`plain` → plaintext，`iframe` → markup，`modelfile` → dockerfile
- 使用 `$...$` 与 `$$...$$` 书写数学公式；仅当页面包含公式时才加载 MathJax
- 使用 ` ```mermaid ` 代码块绘制 Mermaid 图表，构建时转换为 `.mermaid` 容器
- 使用相对路径引用文章资源，避免绝对路径

## Automatic Features

- **索引生成**：新增文章推送到 `main` 后，README.md、tags.md、categories.md 自动更新
- **搜索**：构建生成 `search.json`，前端使用 Fuse.js 提供头部搜索与 `?q=` 搜索弹窗，并支持结果高亮
- **主题**：`data-theme` + `localStorage` 记忆，支持自动跟随系统
- **SEO**：sitemap、robots、RSS、Open Graph、Twitter 卡片、canonical、JSON-LD
- **性能**：MathJax/Mermaid/Prism 语言按需加载，图片与 iframe 懒加载，静态资源哈希，Service Worker 缓存（`sw.js`，注册于 `base.html`）
- **交互**：代码复制按钮、图片灯箱、目录高亮、阅读进度条、移动端抽屉

## Deployment

站点通过 GitHub Actions 自动部署到 GitHub Pages：

1. 检出仓库（`fetch-depth: 0`，以便读取 git 日期）
2. 安装依赖并运行静态站点生成器
3. 克隆目标仓库 `wardenxyz/wardenxyz.github.io`
4. 使用 `rsync --delete` 同步 `site/` 内容
5. 提交并推送，使网站可通过 `https://wardenxyz.github.io` 访问
