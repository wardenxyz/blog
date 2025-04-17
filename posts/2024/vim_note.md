---
title: Vim 高效速查笔记
date: 2024-04-08
tags: [vim]
category: [计算机]
---

# Vim 高效速查笔记

## 核心模式（ESC切换普通模式）

| 模式     | 进入方式           | 状态栏提示   | 核心用途      |
| -------- | ------------------ | ------------ | ------------- |
| 普通模式 | 默认/按`ESC`或`jj` | -            | 导航/执行命令 |
| 插入模式 | `i I a A o O s S`  | INSERT       | 文本编辑      |
| 命令模式 | `:` 或 `/`         | 命令行输入区 | 执行复杂命令  |
| 可视模式 | `v V Ctrl+v`       | VISUAL       | 文本块选择    |

> 推荐配置：`.vimrc`添加 `inoremap jj <Esc>` 用`jj`替代ESC

## 高效操作体系

### ▶ 文件操作

```bash
vim file1                 # 打开单个文件
vim -O2 file1 file2       # 左右分屏打开两个文件
:sp filename              # 上下分屏打开新文件
Ctrl+w → ← ↑ ↓            # 分屏间跳转方向键
:q!                       # 强制退出不保存
:wq                       # 保存并退出
ZZ                        # 快速保存退出（普通模式）
```

### ▶ 光标移动（普通模式）

```vim
h/j/k/l       ←/↓/↑/→
w/e          下个单词首/尾
0/$          行首/行尾
gg/G         文件首/尾
Ctrl+f/b     下/上翻页
20G          跳转第20行
```

### ▶ 编辑神技

```vim
ddp         交换当前行与下一行
yyp         复制当前行
ci"         快速修改引号内容
dt)         删除到右括号前
guu/gUU     当前行全小/大写
>%          缩进当前代码块
```

### ▶ 搜索替换

```vim
/pattern    正向搜索（n/N跳转）
?pattern    反向搜索
:%s/old/new/gc   全局替换带确认
:'<,'>s/old/new  选区替换（可视模式选择后）
```

### ▶ 分屏管理

```vim
Ctrl+w v    垂直分屏
Ctrl+w s    水平分屏
Ctrl+w q    关闭当前分屏
Ctrl+w o    仅保留当前分屏
```

## 高频命令速查表

### 文本操作（普通模式）

| 命令 | 功能         | 示例               |
| ---- | ------------ | ------------------ |
| x    | 删除当前字符 | 3x 删3字符         |
| dw   | 删至词尾     | d2w 删2词          |
| D    | 删至行尾     |                    |
| p    | 粘贴         | "+p 粘贴系统剪贴板 |
| .    | 重复上次操作 |                    |

### 可视模式

```vim
v       字符选择模式
V       行选择模式
Ctrl+v  块选择模式
y       复制选中区域
d       删除选中区域
gv      重选上次选区
```

### 宏录制

```vim
qa      开始录制宏a
q       停止录制
@a      执行宏a
100@a   执行100次
:reg    查看所有宏
```

## 高阶技巧

### 多文件操作

```vim
:ls             查看打开文件列表
:b2             切换至第2个文件
:bd             关闭当前文件
:args *.txt     批量打开txt文件
```

### 代码折叠

```vim
zc      折叠当前代码块
zo      展开折叠
zR      展开所有折叠
zm      增加折叠层级
```

### 插件推荐

1. [NERDTree](https://github.com/preservim/nerdtree) - 文件树导航
2. [vim-airline](https://github.com/vim-airline/vim-airline) - 状态栏美化
3. [coc.nvim](https://github.com/neoclide/coc.nvim) - 智能补全

> 附：`vimtutor`命令可启动官方30分钟交互教程
