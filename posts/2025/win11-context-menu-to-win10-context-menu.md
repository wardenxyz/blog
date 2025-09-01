---
title: win11 右键菜单切换到 win10 右键菜单
date: 2025-09-01
tags: [Windows, Terminal]
category: [计算机]
---

# win11 右键菜单切换到 win10 右键菜单

官方解答

https://learn.microsoft.com/zh-cn/answers/questions/4106782/windows11

在 win11 的终端运行：

```ps1
reg add "HKCU\Software\Classes\CLSID{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /f /ve
```

然后重启就可以切换到 win10 的右键菜单了。

恢复命令

```ps1
reg delete "HKCU\Software\Classes\CLSID{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /va /f
```
