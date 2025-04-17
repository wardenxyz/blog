---
title: Pull Request 的步骤
date: 2024-12-01
tags: [git, pull request]
category: [计算机]
---

# Pull Request 的步骤

为开源项目提 Pull Request (PR) 的步骤如下：

## 1. Fork 仓库：
前往你要贡献的开源项目仓库，点击右上角的 "Fork" 按钮，这将创建该仓库的副本到你的 GitHub 账户下。

## 2. 克隆仓库：

在你的本地机器上克隆你 Fork 的仓库。例如：

```bash
git clone https://github.com/你的用户名/仓库名.git
```

然后进入克隆的仓库目录：

```bash
cd 仓库名
```

## 3. 创建新分支：

创建一个分支以进行你的更改，并切换到该分支。例如：

```bash
git checkout -b 新分支名
```

## 4. 进行更改：

在你的本地仓库中进行代码更改。确保遵循项目的代码规范和贡献指南。

## 5. 提交更改：

将你的更改添加并提交到新分支中。例如：

```bash
git add .
git commit -m "简要描述你的更改"
```

## 6. 推送到 GitHub：

将你的更改推送到你的 Fork 仓库中。例如：

```bash
git push origin 新分支名
```

## 7. 创建 Pull Request：

前往原始仓库的 GitHub 页面，你会看到一个提示，询问你是否要为你刚刚推送的分支创建 Pull Request。点击 "Compare & pull request" 按钮，填写 PR 的标题和描述，然后点击 "Create pull request"。

## 8. 与维护者沟通：

PR 提交后，项目维护者可能会对你的更改进行审查，并要求你做出一些修订。保持沟通，及时响应审查意见。

## 9. 合并 PR：

如果你的更改通过了审查，维护者将会合并你的 PR。你的贡献将被包含在项目中。

通过以上步骤，你就可以为开源项目贡献代码了。
