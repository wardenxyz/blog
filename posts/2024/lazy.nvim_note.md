---
title: lazy.nvim 学习笔记
date: 2024-10-04
tags: [vim, lazy.nvim]
category: [计算机]
---

# lazy.nvim 学习笔记

两个命令，三个路径，两个命令是拉取 lazy.nvim 和拉取 init.lua 配置文件命令，三个路径是 lazy.nvim 的路径、init.lua 的路径和 Neovim 插件的路径

步骤：

## 第一个命令，拉取 lazy.nvim

```bash
git clone https://github.com/folke/lazy.nvim.git C:\Users\24109\AppData\Local\nvim-data\site\pack\packer\start\lazy.nvim
```

## 第二个命令，拉取 init.lua 配置文件

```bash
git clone https://gitee.com/sr1122/nvim.git C:\Users\24109\AppData\Local\nvim
```

## 下载插件

打开 Neovim，lazy.nvim 会自动下载插件，下载完成后，重启 Neovim

---

## 第一个路径，lazy.nvim 路径

```bash
C:\Users\admin\AppData\Local\nvim-data\site\pack\packer\start\lazy.nvim
```

## 第二个路径，init.lua 配置文件路径

```bash
C:\Users\24109\AppData\Local\nvim
```

## 第三个路径，Neovim 插件路径

```bash
C:\Users\admin\AppData\Local\nvim-data\lazy
```

这个里面放的就是你的插件
