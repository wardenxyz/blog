---
title: 自用 git hook
date: 2025-06-13
tags: [git]
category: [计算机]
---

# 自用 git hook

## post-commit

路径：.git/hooks/post-commit

```bash
#!/bin/sh

# 定义计数器文件的路径
COUNTER_FILE=".git_commit_counter"

# 检查计数器文件是否存在，如果不存在，则初始化为0
if [ ! -f "$COUNTER_FILE" ]; then
    echo 0 > "$COUNTER_FILE"
fi

# 读取当前计数
count=$(cat "$COUNTER_FILE")
count=$((count+1))

# 更新计数器文件
echo $count > "$COUNTER_FILE"

# 每10次提交执行一次git push
if [ "$count" -eq 10 ]; then
    git push origin main
    # 重置计数器
    echo 0 > "$COUNTER_FILE"
fi
```

这个钩子用于自动计数提交次数，主要功能：

1. 创建/检查 `.git_commit_counter` 文件（需加入 `.gitignore`）
2. 读取并更新提交计数（每次提交 +1）
3. 每 10 次提交自动推送至远程

该脚本可减少手动推送次数，提高频繁提交时的工作效率。

---

## post-commit

路径：.git/hooks/post-commit

```bash
#!/bin/sh

git push origin main
```

这个钩子的作用是在每次成功提交（commit）后自动执行 git push 命令

---

## commit-msg

路径：.git/hooks/commit-msg

```bash
#!/bin/sh

# 获取当前时间，格式为年-月-日 时:分:秒
COMMIT_TIME=$(date "+%Y-%m-%d %H:%M:%S")

# 在提交信息末尾添加当前时间
echo "$COMMIT_TIME" >> $1
```

这个钩子会在提交信息之后添加当前时间
