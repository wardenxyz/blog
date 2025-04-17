---
title: git-sizer 学习笔记
date: 2024-10-01
tags: [git]
category: [计算机]
---

# git-sizer 学习笔记

## git-sizer 命令输出

```bash
$ git-sizer --verbose

Processing blobs: 1215
Processing trees: 1086
Processing commits: 513
Matching commits to trees: 513
Processing annotated tags: 0
Processing references: 2
| Name                         | Value     | Level of concern               |
| ---------------------------- | --------- | ------------------------------ |
| Overall repository size      |           |                                |
| * Commits                    |           |                                |
|   * Count                    |   513     |                                |
|   * Total size               |   148 KiB |                                |
| * Trees                      |           |                                |
|   * Count                    |  1.09 k   |                                |
|   * Total size               |  1.34 MiB |                                |
|   * Total tree entries       |  29.7 k   |                                |
| * Blobs                      |           |                                |
|   * Count                    |  1.22 k   |                                |
|   * Total size               |  26.4 MiB |                                |
| * Annotated tags             |           |                                |
|   * Count                    |     0     |                                |
| * References                 |           |                                |
|   * Count                    |     2     |                                |
|     * Branches               |     1     |                                |
|     * Remote-tracking refs   |     1     |                                |
|                              |           |                                |
| Biggest objects              |           |                                |
| * Commits                    |           |                                |
|   * Maximum size         [1] |  1.97 KiB |                                |
|   * Maximum parents      [2] |     1     |                                |
| * Trees                      |           |                                |
|   * Maximum entries      [3] |   126     |                                |
| * Blobs                      |           |                                |
|   * Maximum size         [4] |  3.79 MiB |                                |
|                              |           |                                |
| History structure            |           |                                |
| * Maximum history depth      |   513     |                                |
| * Maximum tag depth          |     0     |                                |
|                              |           |                                |
| Biggest checkouts            |           |                                |
| * Number of directories  [5] |    25     |                                |
| * Maximum path depth     [6] |     5     |                                |
| * Maximum path length    [6] |    73 B   |                                |
| * Number of files        [7] |   281     |                                |
| * Total size of files    [8] |  20.6 MiB |                                |
| * Number of symlinks         |     0     |                                |
| * Number of submodules       |     0     |                                |

[1]  314be6877a8519aba4e703f2fdc7a9d540b441db
[2]  6a930f6bb128b4e023b5d40f4ec284650441cb19 (refs/heads/main)
[3]  70871672fc82c0697bb8a9e1d8ee78cc48940779 (723190f8c4bd0a25651123c2842438f544d46810:assets)
[4]  6e6f60ac463d1616bedcf2b9d3826c4e52d2b49f (refs/heads/main:assets/文件.pdf)
[5]  6612e646c5b1203be32186c76aa093852519f8f3 (12c0591edb5a3f6affe1dd5d001bfc2d4072d64f^{tree})
[6]  63264b7f5024765f195d69cca0a7d8734d9508f9 (refs/heads/main^{tree})
[7]  7ef042f07987acc492f5ca5f8cf3fb0c15c58264 (1424d4955f210f89f1f82117b18822ead85ae617^{tree})
[8]  78bdd67d7e37b0f4a8af0f6009236ef2270a7288 (f84cb9d396b1d2297dddea27dc72d6ed252f33cd^{tree})
```

## 输出解释

从 `git-sizer` 的输出中可以看出，你的 Git 仓库的整体大小和结构信息。以下是一些关键点的解释：

## 仓库整体大小
- Commits（提交）:
  - Count（数量）: 513
  - Total size（总大小）: 148 KiB

- Trees（树）:
  - Count（数量）: 1.09k
  - Total size（总大小）: 1.34 MiB
  - Total tree entries（总树条目）: 29.7k

- Blobs（文件对象）:
  - Count（数量）: 1.22k
  - Total size（总大小）: 26.4 MiB

- Annotated tags（注释标签）:
  - Count（数量）: 0

- References（引用）:
  - Count（数量）: 2
  - Branches（分支）: 1
  - Remote-tracking refs（远程跟踪引用）: 1

## 最大对象
- Commits（提交）:
  - Maximum size（最大大小）: 1.97 KiB
  - Maximum parents（最大父级数量）: 1

- Trees（树）:
  - Maximum entries（最大条目数）: 126

- Blobs（文件对象）:
  - Maximum size（最大大小）: 3.79 MiB

## 历史结构
- Maximum history depth（最大历史深度）: 513
- Maximum tag depth（最大标签深度）: 0

## 最大检出
- Number of directories（目录数量）: 25
- Maximum path depth（最大路径深度）: 5
- Maximum path length（最大路径长度）: 73 B
- Number of files（文件数量）: 281
- Total size of files（文件总大小）: 20.6 MiB
- Number of symlinks（符号链接数量）: 0
- Number of submodules（子模块数量）: 0

## 具体对象
- [1]: 最大提交大小的对象 ID 是 `314be6877a8519aba4e703f2fdc7a9d540b441db`
- [2]: 最大父级数量的提交 ID 是 `6a930f6bb128b4e023b5d40f4ec284650441cb19`（分支 `main`）
- [3]: 最大条目数的树对象 ID 是 `70871672fc82c0697bb8a9e1d8ee78cc48940779`
- [4]: 最大文件对象大小的 ID 是 `6e6f60ac463d1616bedcf2b9d3826c4e52d2b49f`（文件路径 `assets/文件.pdf`）
- [5]: 最大目录数量的树对象 ID 是 `6612e646c5b1203be32186c76aa093852519f8f3`
- [6]: 最大路径深度和路径长度的树对象 ID 是 `63264b7f5024765f195d69cca0a7d8734d9508f9`
- [7]: 最大文件数量的树对象 ID 是 `7ef042f07987acc492f5ca5f8cf3fb0c15c58264`
- [8]: 最大文件总大小的树对象 ID 是 `78bdd67d7e37b0f4a8af0f6009236ef2270a7288`

这些信息可以帮助你了解仓库的大小和结构，识别可能需要优化的部分。

## 哪些部分需要优化

根据 `git-sizer` 的输出，以下是一些可能需要优化的部分：

## 1. Blobs（文件对象）
- 最大文件对象大小: 3.79 MiB
  - 文件路径: `assets/文件.pdf`
  - 大文件可能会导致仓库克隆和操作变慢。你可以考虑将大文件移到 Git LFS（Large File Storage）或其他外部存储解决方案。

## 2. 总文件大小
- 文件总大小: 20.6 MiB
  - 如果仓库中有很多大文件，可能会影响性能。你可以检查哪些文件占用了大量空间，并考虑是否可以将它们移到外部存储。

## 3. 树对象
- 最大条目数: 126
  - 树对象中的条目数较多，可能会影响性能。你可以检查这些目录，看看是否可以简化目录结构或减少文件数量。

## 4. 提交历史
- 最大历史深度: 513
  - 提交历史较深，可能会影响性能。你可以考虑使用 `git rebase` 或 `git filter-branch` 来简化历史记录。

## 具体优化建议：

1. 使用 Git LFS:

- 对于大文件（如 PDF、图像、视频等），可以使用 Git LFS 来存储它们。这样可以减少仓库的大小，提高性能。

- 安装 Git LFS 并跟踪大文件：

```bash
git lfs install
git lfs track "*.pdf"
git add .gitattributes
git commit -m "Track PDF files with Git LFS"
```

2. 移除不必要的文件:

- 检查仓库中的大文件和不必要的文件，考虑将它们移到外部存储或删除。

- 使用以下命令查找大文件：

```bash
git rev-list --objects --all | sort -k 2 > allfileshas.txt
git gc && git verify-pack -v .git/objects/pack/pack-*.idx | sort -k 3 -n | tail -40
```

3. 简化提交历史:

- 使用 `git rebase` 或 `git filter-branch` 来简化提交历史，减少不必要的提交。

- 例如，使用 `git rebase` 合并提交：

```bash
git rebase -i HEAD~n  ## n 是你想要合并的提交数量
```

4. 优化目录结构:

- 检查目录结构，看看是否可以简化或减少文件数量。

- 例如，将相关文件合并到一个目录中，减少目录层级。

通过这些优化措施，你可以减少仓库的大小，提高操作性能。
