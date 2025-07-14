---
title: 从 git 提交中移除文件
date: 2024-04-08
tags: [git]
category: [计算机]
---

# 从 git 提交中移除文件

## 移除单个文件的提交历史

删除一个文件的提交历史，git 官方推荐一个 python 工具 [`git filter-repo`](https://github.com/newren/git-filter-repo)，下面是命令

```bash
uv venv
```

```bash
.venv\Scripts\activate
```

```bash
uv pip install git-filter-repo
```

```bash
git filter-repo --path templates.json --invert-paths --force
```

这个命令会从所有分支的所有提交历史中删除 `templates.json` 文件

## 移除一个文件夹的提交历史

```bash
git filter-repo --path myfolder/ --invert-paths --force
```

这个命令会删除 `myfolder/` 文件夹及其该文件夹下所有内容的提交历史
