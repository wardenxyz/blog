---
title: 修改 npm node_modules 位置
date: 2025-06-20
tags: [node, npm, node_modules]
category: [计算机]
---

# 修改 npm node_modules 位置

修改 npm install 时的 node_modules 位置

```bash
npm config set prefix "D:\npm"
```

# 修改 npm cache 的位置

查看 npm cache 位置

```bash
npm config get cache
```

修改

```bash
npm config set cache "D:\npm\cache"
```
