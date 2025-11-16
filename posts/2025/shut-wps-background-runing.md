---
title: 关闭 WPS 后台运行
date: 2025-06-03
tags: [WPS]
category: [计算机]
---

# 关闭 WPS 后台运行

搬运自：https://www.zhihu.com/question/498031038

## 第一步

在 WPS 的安装路径下找到一个名为 `ksomisc.exe` 的文件，路径为

```
D:\Kingsoft\WPS Office\12.1.0.21171\office6\ksomisc.exe
```

点击 `ksomisc.exe`，进入到 “WPS综合修复/配置工具” 界面，进入 “高级” 界面，把里面 “功能定制” 和 “升级设置” 两个页面下的选项关掉

## 第二步

还是在 `D:\Kingsoft\WPS Office\12.1.0.21171\office6` 路径下，找到以下五个文件

```
wpscenter.exe
```

```
wpscloudlaunch.exe
```

```
wpscloudsvr.exe
```

```
wpscloudsvrimp.dll
```

```
wpsrenderer.exe
```

全删了，并右键新建五个 txt 文件，把名字改为以上五个名字，占用位置，以防死灰复燃

## 第三步

打开 “控制面板”，打开 “Windows 工具”，打开 “服务”

在 “服务” 界面中找到一个名为 “WPS Office Cloud Service” 的选项，右键点击属性，把里面 “常规” 项下的 “启动类型” 改为禁用，确定退出

# 关闭 WPS 增量备份

来源：https://www.bilibili.com/video/BV1QYEkzvEWQ

在 WPS 主页的右上角找到 “全局设置”，打开下面的 “设置”

在 “设置” 界面找到 “打开备份中心”

在 “备份中心” 界面中找到 “本地备份设置”，点击 “关闭备份” 按钮，关闭增量备份功能
