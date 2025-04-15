---
title: 用 you-get 下载B站视频
date: 2024-08-01
tags: [python, B站]
category: [计算机]
---

# 用 you-get 下载B站视频

## 1. 拉取 you-get

```bash
pip install you-get
```

## 2. 获取B站 cookies

在 edge 浏览器下载 [Cookie-Editor](https://microsoftedge.microsoft.com/addons/detail/cookieeditor/neaplmfkghagebokkhpjpoebhdledlfi?hl=zh-CN) 扩展，然后打开 [B站](https://bilibili.com)，通过 Cookie-Editor 导出B站的 cookie

> 导出格式要为 Netscape 格式，因为 you-get 目前只支持 Mozilla 的 cookies.sqlite 和 Netscape 的 cookies.txt 两种格式的 cookies，所以我们需要导出符合格式的 cookies

## 3. 下载视频

把保存好的 cookies.txt 放到你所执行命令的目录下，然后执行

```
you-get --cookies=cookies.txt "https://www.bilibili.com/video/BVxxxxxx"
```

命令

you-get 会默认下载最高清晰度

就 ok 了
