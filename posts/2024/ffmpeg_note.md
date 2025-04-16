---
title: ffmpeg 自用命令
date: 2024-04-08
tags: [ffmpeg]
category: [计算机]
---

# ffmpeg 自用命令

下载链接：[ffmpeg](https://www.gyan.dev/ffmpeg/builds/)

初学者用户建议选择 `ffmpeg-git-essentials.7z`

---

## 查看视频一共有多少帧数

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1 your_video_file.mp4
```

---

## 提升视频锐度

```bash
ffmpeg -i input.mp4 -vf "unsharp" output.mp4
```

---

## 提升视频分辨率

```bash
ffmpeg -i input.mp4 -vf "scale=3840:2160" output.mp4
```

---

## 查看视频分辨率

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 video.mp4
```

---

## 查看视频元数据

```bash
ffprobe -v quiet -print_format json -show_format your_video_file.mp4
```

---

## 把多个视频合并为一个视频

```txt
file 'input3.mp4'
file 'input1.mp4'
file 'input2.mp4'
```

把这个 `txt` 文件和待处理的视频放到同一文件夹下，`ffmpeg` 会按照从上倒下的顺序合并视频

然后，你可以使用以下命令合并视频：

```bash
ffmpeg -f concat -safe 0 -i files.txt -c copy output.mp4
```

---

## 视频转换为不同的格式

```bash
ffmpeg -i input.mp4 output.avi
```

---

## 剪切视频

```bash
ffmpeg -i input.mp4 -ss 00:00:30 -t 00:00:10 -c:v libx264 -c:a aac output.mp4
```

使用 ffmpeg 剪切视频，你可以使用 `-ss` 选项来指定开始时间，使用 `-t` 选项来指定持续时间。例如，如果你想从视频的第 30 秒开始，剪切 10 秒的视频，你可以使用以上命令

`-c copy` 指定了将原始数据流复制到输出文件，而不进行任何重新编码（用 `-c copy` 剪切的视频不会将视频重新编码，这种方式速度非常快，但可能会导致一些问题，因为它可能会在非关键帧（I帧）的位置切割视频，导致切割出来的视频在开始的一段时间内无法正常播放。所以我们用以上新的命令）

注意，时间可以用时:分:秒的格式指定，也可以直接用秒数指定。例如，`00:01:30` 和 `90` 都表示 1 分 30 秒。

---

## 把音频从视频中分离出来

```bash
ffmpeg -i input.mp4 -vn output.aac
```

在这里，`input.mp4` 是你的输入文件，`-vn` 选项禁用了视频流，`output.aac` 是输出的音频文件。

---

## 禁用音频，把视频文件分离出来

```bash
ffmpeg -i input.mp4 -an output.mp4
```

在这里，`input.mp4` 是你的输入文件，`-an` 选项禁用了音频流，`output.mp4` 是输出的视频文件。

---

## 改变音频格式

```bash
ffmpeg -i input.mp3 output.aac
```

---

## 调整视频的分辨率

```bash
ffmpeg -i input.mp4 -vf "scale=1280:720" output.mp4
```

在这里，`input.mp4` 是你的输入文件，`scale=1280:720` 是一个过滤器，用于将视频的分辨率调整为 `1280x720`，`output.mp4` 是输出文件。

---

## 添加视频水印

```bash
ffmpeg -i input.mp4 -i watermark.png -filter_complex "overlay=W-w-10:H-h-10" output.mp4
```

在这里，`input.mp4` 是你的输入视频文件，`watermark.png` 是你的水印图片，`overlay=W-w-10:H-h-10` 是一个过滤器，它将水印图片放在视频的右下角，离边缘 `10` 像素，`output.mp4` 是输出文件。

注意，`W` 和 `H` 分别代表视频的宽度和高度，`w` 和 `h` 分别代表水印的宽度和高度。你可以调整这些值来改变水印的位置。

---

## 转码视频

```bash
ffmpeg -i input.mp4 -b:v 1000k -b:a 128k output.mp4
```

`input.mp4` 是你的输入视频文件，`1000k` 是视频比特率，`128k` 是音频比特率，`output.mp4` 是输出文件。

---

## 倒放视频

```bash
ffmpeg -i input.mp4 -vf "reverse" output.mp4
```

`input.mp4` 是你的输入文件，`-vf "reverse"` 选项将视频流倒放，`output.mp4` 是输出的视频文件

---

## 录制当前页面视频

- Windows 下：

```bash
ffmpeg -f gdigrab -framerate 30 -i desktop output.mp4
```

- Linux 下：

```bash
ffmpeg -f x11grab -video_size 1920x1080 -framerate 30 -i :0.0 output.mp4
```

按下 `q` 停止录制

---

## 视频转换为 gif

```bash
ffmpeg -i input.mp4 -vf "fps=10,scale=320:-1:flags=lanczos" -c:v gif output.gif
```

在这个命令中：

- `input.mp4` 是你的输入视频文件。
- `-vf "fps=10,scale=320:-1:flags=lanczos"` 是一个视频过滤器链。`fps=10` 将帧率设置为 10 FPS（帧每秒），`scale=320:-1` 将输出 GIF 的宽度设置为 320 像素，高度会自动调整以保持宽高比，`flags=lanczos` 使用 Lanczos 重采样。
- `-c:v gif` 设置输出视频编码器为 GIF。
- `output.gif` 是输出的 GIF 文件。

---

## 将 GIF 转换为视频

```bash
ffmpeg -i input.gif output.mp4
```

---

## 查看视频尺寸

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 input.mp4
```

在这个命令中：

- `-v error` 仅显示错误消息。
- `-select_streams v:0` 选择第一个视频流。
- `-show_entries stream=width,height` 显示视频流的宽度和高度。
- `-of csv=s=x:p=0` 以 CSV 格式输出结果，字段之间用 'x' 分隔。
- `input.mp4` 是你要查看尺寸的视频文件。

这个命令会输出类似 `1280x720` 这样的结果，表示视频的宽度为 1280 像素，高度为 720 像素。

---

## 剪切视频画面

```bash
ffmpeg -i input.mp4 -filter:v "crop=300:200:10:20" output.mp4
```

在这个命令中：

- `-i input.mp4` 指定输入文件。
- `-filter:v "crop=300:200:10:20"` 应用视频过滤器。"crop=300:200:10:20" 指定了剪切区域的宽度、高度和左上角坐标。
- `output.mp4` 指定输出文件。

---

## 调整视频的亮度

```bash
ffmpeg -i input.mp4 -vf "eq=brightness=0.1" output.mp4
```

在这个命令中：

- `-i input.mp4` 指定输入文件。
- `-vf "eq=brightness=0.1"` 应用视频过滤器。"eq=brightness=0.1" 增加了视频的亮度。
- `output.mp4` 指定输出文件。

---

## 调整视频的对比度

```bash
ffmpeg -i input.mp4 -vf "eq=contrast=1.5" output.mp4
```

- `-i input.mp4` 指定输入文件。
- `-vf "eq=contrast=1.5"` 应用视频过滤器。"eq=contrast=1.5" 增加了视频的对比度。
- `output.mp4` 指定输出文件。

---

## 查看图片尺寸

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 image.jpg
```

在这个命令中：

- `-v error` 表示只打印错误消息。
- `-select_streams v:0` 表示选择第一个视频流，对于图片，它就是图片本身。
- `-show_entries stream=width,height` 表示只显示宽度和高度信息。
- `-of csv=s=x:p=0` 表示以 CSV 格式输出，并使用 x 作为分隔符。
- `image.jpg` 是你要检查的图片文件。

这个命令将输出图片的宽度和高度，格式为 `widthxheight`。

---

## m4s 的视频用 ffmpeg 转换为 mp3 bilibili

```bash
ffmpeg -i input.m4s -vn -ab 128k output.mp3
```

在这个命令中：

- `-i input.m4s` 指定了输入文件的名称，你需要将 `input.m4s` 替换为你的 m4s 文件的实际路径和名称。
- `-vn` 是一个选项，表示在处理视频时不包括任何视频流。这对于只处理音频文件非常有用。
- `-ab 128k` 设置了音频比特率为 128 kbit/s，你可以根据需要调整这个值。
- `output.mp3` 是输出文件的名称，你需要将 `output.mp3` 替换为你希望保存的 mp3 文件的路径和名称。

---

## 把 m4s 的视频转换为 mp4 bilibili

```bash
ffmpeg -i input.m4s -codec copy output.mp4
```

在这个命令中：

- `-i input.m4s` 指定了输入文件的名称，你需要将 `input.m4s` 替换为你的 m4s 文件的实际路径和名称。
- `-codec copy` 是一个选项，表示在处理视频时复制原始编码，不进行任何转码。
- `output.mp4` 是输出文件的名称，你需要将 `output.mp4` 替换为你希望保存的 mp4 文件的路径和名称。

请注意，这个命令假设你的 m4s 文件包含了可以直接复制到 mp4 容器中的音频和视频流。如果你的 m4s 文件中的音频或视频编码不兼容 mp4，你可能需要进行转码。

---

## 把视频和音频合并 bilibili

```bash
ffmpeg -i "your_video" -i "your_audio" -c:a aac -strict experimental "your_video.mp4
```

---

## ffmpeg 降低画质的命令

在使用 `ffmpeg` 进行视频处理时，有时需要降低视频的画质以减小文件大小或适应特定的网络传输需求。以下是一些常用的 `ffmpeg` 命令来降低视频画质：

1. **调整视频比特率（Bitrate）**：

```bash
ffmpeg -i input.mp4 -b:v 1000k output.mp4
```

这条命令将视频的比特率设置为 1000 kbps，从而降低视频的画质。比特率越低，画质越差。

2. **使用 CRF（Constant Rate Factor）**：

```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 28 output.mp4
```

CRF 是 x264 和 x265 编码器的一个参数，用于控制输出视频的质量。CRF 值越大，视频质量越低。默认值通常是 23，范围是 0-51。

3. **调整分辨率**：

```bash
ffmpeg -i input.mp4 -vf "scale=1280:720" output.mp4
```

这条命令将视频的分辨率调整为 1280x720，从而降低画质。分辨率越低，画质越差。

4. **同时调整比特率和分辨率**：

```bash
ffmpeg -i input.mp4 -b:v 800k -vf "scale=640:360" output.mp4
```

这条命令同时降低了视频的比特率和分辨率，进一步降低了画质。

5. **使用预设（Preset）**：

```bash
ffmpeg -i input.mp4 -c:v libx264 -preset veryslow -crf 28 output.mp4
```

预设参数控制编码速度和输出质量之间的平衡。`veryslow` 预设会花费更多时间进行编码，但通常能产生更好的压缩效果和更低的文件大小。其他预设有 `ultrafast`, `superfast`, `fast`, `medium`, `slow`, `slower` 等。

## 查看视频清晰度

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of default=noprint_wrappers=1 input_video.mp4
```

这个命令会打印出视频的清晰度
