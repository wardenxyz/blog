---
title: 回滚提交
date: 2025-04-14
tags: [git]
category: [计算机]
---

# 回滚提交

要强制回滚到前两个提交之前，可以使用以下 Git 命令：

1. 打开终端并导航到项目目录：

2. 查看提交历史以确认目标提交：

```bash
git log --oneline
```

3. 强制回滚到前两个提交之前（假设目标提交的哈希为 `abc123`）：

```bash
git reset --hard abc123
```

4. 如果需要将更改强制推送到远程仓库：

```bash
git push origin --force
```

**注意**：强制回滚和推送会覆盖远程仓库的历史记录
