---
title: GitHub page 搭建学习笔记
date: 2024-10-09
tags: [GitHub]
category: [计算机]
---

# GitHub page 搭建学习笔记

## git 生成 SSH 密钥

```bash
ssh-keygen -t ed25519 -C "your_email@example.com" -f ./id_rsa
```

其中 `id_rsa` 是私钥，`id_rsa.pub` 是公钥

## 私钥放在 markdown 帖子所在仓库

settings ——> Secrets and variables ——> Actions ——> New repository secret 添加 SSH 私钥，名称是：

```yaml
DEPLOY_KEY
```

## 公钥放在 username.github.io 仓库

settings ——> Deploy keys ——> Add deploy key

勾选 Allow write access

## GitHub Action 配置

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: 检出仓库
      uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: 设置 Node.js 环境 # 根据 SSG 来确定环境 # [!code highlight]
      uses: actions/setup-node@v3
      with:
        node-version: '>=20.18.0'

    - name: 下载依赖 # [!code highlight]
      run: |
        npm install

    - name: 构建 vitepress # [!code highlight]
      run:  npx vitepress build

    - name: 设置 SSH 密钥
      run: |
        mkdir -p ~/.ssh
        echo "${{ secrets.DEPLOY_KEY }}" > ~/.ssh/id_rsa
        chmod 600 ~/.ssh/id_rsa
        ssh-keyscan github.com >> ~/.ssh/known_hosts

    - name: 克隆目标仓库 # [!code highlight]
      run: |
        git clone git@github.com:wardenxyz/wardenxyz.github.io.git target_repo

    - name: 复制生成的文件到目标仓库 # 根据 SSG 来确定复制文件路径 # [!code highlight]
      run: |
        rsync -av --delete html/* target_repo/

    - name: 提交并推送更改到目标仓库
      run: |
        cd target_repo
        git config --global user.name 'GitHub Actions'
        git config --global user.email 'actions@github.com'
        git add .
        git commit -m "Deploy - $(date -u '+%Y-%m-%d %H:%M:%S' -d '8 hour')"
        git push origin main
```
