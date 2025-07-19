---
title: yt-dlp 使用
date: 2025-07-19
tags: [yt-dlp, 视频下载, python]
category: [计算机]
---

# yt-dlp 使用	

yt-dlp 是一个强大的视频下载工具，支持从多个网站下载视频和音频。它是 youtube-dl 的一个分支，提供了更多的功能和更好的性能。

这个工具比 [you-get](posts\2024\you-get_note.md) 好用，因为它是一个命令行工具，而不是一个 Python 库，使用起来更简单。

## 下载

[https://github.com/yt-dlp/yt-dlp/releases](https://github.com/yt-dlp/yt-dlp/releases)，下载最新版本的 yt-dlp 可执行文件，并将其放在系统的 PATH 中

## 基本用法

使用 [Cookie-Editor](https://microsoftedge.microsoft.com/addons/detail/cookieeditor/neaplmfkghagebokkhpjpoebhdledlfi?hl=zh-CN)，导出网站的 cookies，保存为 `cookies.txt` 文件。

示例命令：

```bash
yt-dlp --cookies "cookies.txt" https://x.com/i/status/xxxxxxxxxxxxxxxx
```

这将下载指定 URL 的视频或音频。
