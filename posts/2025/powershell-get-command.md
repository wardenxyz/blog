---
title: PowerShell Get-Command 命令
date: 2025-06-14
tags: [PowerShell, Windows]
category: [计算机]
---

# PowerShell Get-Command 命令

1. 检查所有 Path 变量

```powershell
$env:Path -split ';'
```

2. 用 Get-Command 检查 PowerShell 环境

```powershell
Get-Command typst
```

这个命令会告诉你 typst 的实际可执行文件路径或是否是别名/函数

3. 检查 scoop/shims 或其他包管理器路径

如果你用 scoop 安装的，路径可能类似 `C:\Users\<用户名>\scoop\shims`，在 Path 里则应该有这项

---

### 例子

假如你用 `Get-Command typst`，输出结果：

```
PS C:\Users\24109> Get-Command typst

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Application     typst.exe                                          0.0.0.0    D:\typst\typst.exe
```

说明你的 typst 可执行文件在 `D:\typst` 下

而如果是：

```
CommandType     Alias
-----------     -----
Alias           typst -> ...
```
说明它其实是 PowerShell 的别名

- 如果是 scoop/shims 之类的特殊路径，确认 scoop 的 shims 路径已加入 Path
