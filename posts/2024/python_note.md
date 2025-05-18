---
title: python 学习笔记
date: 2024-10-06
tags: [python]
category: [计算机]
---

# python 学习笔记

## 创建和使用虚拟环境

```bash
## 创建虚拟环境
python -m venv venv

## 使用 uv
uv venv

## 激活虚拟环境
.\venv\Scripts\activate  ## Windows
## 或者
source venv/bin/activate  ## macOS 和 Linux

## 安装第三方库
pip install requests

## 使用 uv
uv pip install requests

## 卸载第三方库
pip uninstall requests

## 使用 uv
uv pip uninstall requests

## 生成依赖文件
pip freeze > requirements.txt

## 使用 uv
uv pip freeze > requirements.txt

## 根据依赖文件下载第三方库
pip install -r requirements.txt

## 使用 uv
uv pip install -r requirements.txt

## 根据依赖文件卸载第三方库
pip uninstall -r requirements.txt -y

## 使用 uv
uv pip uninstall -r requirements.txt -y

## 停用虚拟环境
deactivate
```

## python 换源

清华源：

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

查看源

```bash
pip config list
```

输出：

```bash
global.index-url='https://pypi.tuna.tsinghua.edu.cn/simple'
```

恢复默认源：

```bash
pip config unset global.index-url
```

配置文件位置：

```bash
C:\Users\admin\AppData\Roaming\pip\pip.ini
```

## 修改 pip install 位置

在 `C:\Users\admin\AppData\Roaming\pip\pip.ini` 中写入

```txt
[global]
target = D:\Python\Python312\Lib\site-packages
```

## pip.ini 配置

```txt
[global]
target = D:\Python\Python312\Lib\site-packages
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
```

## 查看第三方库的位置

```bash
python -m site
```

```bash
uv python -m site
```

## 查看指定库的详细信息

```bash
pip show requests
```

```bash
uv pip show requests
```

```bash
Name: requests
Version: 2.25.1
Summary: Python HTTP for Humans.
Home-page: https://requests.readthedocs.io
Author: Kenneth Reitz
Author-email: me@kennethreitz.org
License: Apache 2.0
Location: /path/to/your/env/lib/python3.8/site-packages
Requires: certifi, chardet, idna, urllib3
Required-by:
```

## 查看 Python 已安装的第三方库

```bash
pip list
```

```bash
uv pip list
```

## python 列出依赖库

```bash
pip freeze > requirements.txt
```

```bash
uv pip freeze > requirements.txt
```