---
title: 跨系统避免换行符导致字节差异的方法
date: 2025-07-15
tags: [跨平台, 文件操作, 换行符, UTF-8, 字节控制]
category: [计算机]
---

# 跨系统避免换行符导致字节差异的方法

在不同操作系统下，会因为换行符导致字节差异，下面介绍了一个方法精确控制输出内容的字节。

## Linux 下

```bash
LC_ALL=C.UTF-8 echo -n "context" > file.txt
```

```bash
echo -n "context" | iconv -t UTF-8 > file.txt
```

## Windows 下

```ps1
[System.IO.File]::WriteAllBytes("file.txt", [System.Text.Encoding]::UTF8.GetBytes("content"))
```

## 注意事项

- 这两个命令都可以**精确控制输出内容的字节**，避免 Windows（`\r\n`）和 Linux（`\n`）因不同换行策略导致的字节不同。
- 在需要严格一致的文件内容（如校验哈希、跨平台脚本等场景）时，推荐使用上述方式。
