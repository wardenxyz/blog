---
title: B站嵌入代码
date: 2024-08-01
tags: [B站]
category: [计算机]
---

# B站嵌入代码

## 正常显示

在

```
<iframe src="//player.bilibili.com
```

之中添加 `https:` 变成

```
<iframe src="https://player.bilibili.com
```

## 修改屏幕尺寸

```
style="width:100%;aspect-ratio:16/9;"
```

```iframe
<iframe src="//player.bilibili.com/player.html?aid=425938140&bvid=BV1G3411M7BN&cid=584177306&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" style="width:100%;aspect-ratio:16/9;"></iframe>
```

## 禁止自动播放

如果不修改代码，会在打开文章页面的时候，视频就会直接自动从头开始播放，突然的声音可能带来不必要的惊吓，并且会让访问者错过开头，显得很突兀。

要取消自动播放，只需在视频 src=url 链接最后加上：&autoplay=0

```iframe
<iframe src="//player.bilibili.com/player.html?aid=425938140&bvid=BV1G3411M7BN&cid=584177306&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
```

## 更多B站嵌入代码修改

如果要更改更多B站视频嵌入代码设置选项，可以参考下面关于iframe引用的B站官方参数设置。

设置方法就是在src=url链接后面添加:&参数名=参数数值

比如弹幕关闭：&danmaku=0，以此类推

| 参数名                | 参数用途                      | 使用方法         |
| ------------------ | ------------------------- | ------------ |
| autoplay           | 是否自动播放(默认否)               | 1: 开启, 0: 关闭 |
| danmaku            | 默认弹幕开关(默认开启)              | 1: 开启, 0: 关闭 |
| muted              | 是否默认静音(默认否)               | 1: 开启, 0: 关闭 |
| hasMuteButton      | 一键静音按钮是否显示（默认不显示）         | 1: 开启, 0: 关闭 |
| hideCoverInfo      | 视频封面下方是都显示播放量弹幕量等信息(默认显示) | 1: 开启, 0: 关闭 |
| hideDanmakuButton  | 是否隐藏弹幕按钮（默认不隐藏）           | 1: 开启, 0: 关闭 |
| noFullScreenButton | 是否隐藏全屏按钮(默认显示)            | 1: 开启, 0: 关闭 |
| fjw                | 是否开始记忆播放(默认开启)            | 1: 开启, 0: 关闭 |
| t                  | 默认开始时间(默认0)               | 直接填写数值，单位秒   |




