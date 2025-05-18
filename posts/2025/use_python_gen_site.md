---
title: 使用 Python 生成静态网页
date: 2025-04-12
tags: [python, site]
category: [计算机]
---

# 使用 Python 生成静态网页

环境：

```bash
PS D:\workspace\blog> python --version

Python 3.12.0
```

步骤：

第一步，创建虚拟环境

```bash
uv venv
```

```bash
.\venv\Scripts\activate
```

第二步，下载依赖

```bash
uv pip install -r requirements.txt
```

第三步，生成索引（本地跳过这一步）

```bash
python .github\scripts\update_indexes.py
```

第四步，生成静态网页

```bash
python .github\scripts\static_gen.py
```

第五步，预览

```bash
python -m http.server -d site
```

在浏览器中访问 http://localhost:8000

## 创建新的文章

在 posts 文件夹下按照年份创建文件，格式为

```markdown
---
title: 标题
date: 2025-04-13
tags: [tag1, tag2]
category: [category]
---

# 标题
```

写完之后生成索引

```bash
python .github\scripts\update_indexes.py
```

生成静态网页

```bash
python .github\scripts\static_gen.py
```

本地预览

```bash
python -m http.server -d site
```

在浏览器中访问 http://localhost:8000

## 部署

该项目配置了 GitHub Actions 工作流，在你将代码推送到 GitHub 时自动构建和部署。

1. 确保已在 GitHub 仓库设置中启用了 GitHub Pages
2. 推送更改到 GitHub
3. GitHub Actions 将自动构建并部署网站

## 自定义

- 修改 `template.html` 更改网站布局
- 修改 `assets/styles.css` 更改网站样式
- 在 `static_gen.py` 文件的顶部修改网站标题和其他配置
