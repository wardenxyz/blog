---
title: git-crypt 官方文档中文翻译
date: 2024-07-01
tags: [git-crypt, git]
category: [计算机]
---

# git-crypt 官方文档中文翻译

## git-crypt - Git 中的透明文件加密

git-crypt 使 Git 仓库中的文件可以实现透明的加密和解密。您可以选择需要保护的文件，在提交时进行加密，在检出时进行解密。git-crypt 可以让您自由共享包含公共和私有内容的仓库。即使开发者没有密钥，git-crypt 也能让其实现克隆和提交含有加密文件的仓库。这样，您可以将秘密资料（如密钥或密码）存储在与代码相同的仓库中，而不需要锁定整个仓库。

git-crypt 是由 [Andrew Ayer](https://www.agwa.name)（ agwa@andrewayer.name ）编写的。
更多信息，请访问 https://www.agwa.name/projects/git-crypt。

## 构建 git-crypt

参考 [INSTALL.md](https://github.com/AGWA/git-crypt/blob/master/INSTALL.md) ​ 文件进行安装。

## 使用 git-crypt

配置仓库以使用 git-crypt：

```
cd repo
git-crypt init
```

通过创建 .gitattributes 文件来指定要加密的文件：

```
secretfile filter=git-crypt diff=git-crypt
*.key filter=git-crypt diff=git-crypt
secretdir/** filter=git-crypt diff=git-crypt
```

.gitattributes 文件跟 .gitignore 类似，可以匹配通配符，并且应该提交到仓库里。更多信息可以查看下方内容。请确认不要错误地加密了 .gitattributes 文件本身（或者其他 Git 文件，例如 .gitignore 或者 .gitmodules）。请确认你的 .gitattributes 规则已经生效*在提交敏感文件之前*，否则这些文件将不会被加密！

使用 GPG 分享仓库（给他人或自己）：

```
git-crypt add-gpg-user USER_ID
```

​ `USER_ID` ​ 可以是一个密钥 ID、完整指纹、电子邮件地址或
其他任何唯一标识 GPG 公钥的方式（参见 gpg 手册页中的 "HOW TO
SPECIFY A USER ID"）。注意：`git-crypt add-gpg-user` ​ 会
在仓库根目录的 .git-crypt 目录下添加并提交一个 GPG 加密的密钥文件。

另外，你可以导出一个对称密钥，安全地传递给协作者即可（无需 GPG，也不会在仓库中增加文件）：

```
git-crypt export-key /path/to/key
```

克隆包含加密文件的存储库后，使用 GPG 进行解密：

```
git-crypt unlock
```

或者使用对称密钥：

```
git-crypt unlock /path/to/key
```

这就是你需要做的全部工作——在 `git-crypt` ​ 配置完成后（无论是通过 `git-crypt init` ​ 还是 `git-crypt unlock` ​），你可以像往常一样使用 `git` ​。加密和解密过程会透明地进行。

## 当前状态

git-crypt 的最新版本是 [0.7.0](https://github.com/AGWA/git-crypt/blob/master/NEWS.md)，发布于
2022-04-21。git-crypt 旨在实现无缺陷且可靠，即它不应崩溃、失效或泄露您的机密数据。然而，它尚未成熟，即它的文档、功能丰富性或易用性尚未达到应有的水平。此外，在 1.0 版本之前，可能会引入不向后兼容的变更。

## 安全性

git-crypt 比其他透明的 git 加密系统更安全。
git-crypt 使用 AES-256 在 CTR 模式下加密文件，并使用从文件的 SHA-1 HMAC 派生的合成 IV。
这种操作模式在确定性选择明文攻击下被证明是语义安全的。
这意味着尽管加密是确定性的（这是必需的，以便 git 可以区分文件是否已更改），
但它不会泄露任何信息，只会暴露两个文件是否相同。
其他透明的 git 加密方案使用 ECB 或 CBC 模式和固定 IV。这些系统在语义上不安全，会泄露信息。

## 局限性

git-crypt 依赖于 git 过滤器，而这些过滤器并非为加密设计。因此，git-crypt 并非加密版本库中大多数或全部文件的最佳工具。git-crypt 真正擅长的是这样一种场景：你的版本库绝大多数内容是公开的，但其中有一些文件（可能是一组命名为*. key 的私钥，或是一个含有 API 凭证的文件）需要加密。如果需要加密整个版本库，考虑使用 [git-remote-gcrypt](https://spwhitton.name/tech/code/git-remote-gcrypt/) 这类工具。（注：本文不对 git-remote-gcrypt 的安全性作出评价。）

git-crypt 不会加密文件名、提交信息、符号链接目标、gitlink 或其他元数据。

git-crypt 无法隐藏文件是否发生更改、文件长度，或者两个文件完全相同这一事实（参见上方“安全性”部分）

git-crypt 并不支持撤销对之前已授予访问权限的加密仓库的访问。这既适用于多用户 GPG 模式（没有 del-gpg-user 命令来补充 add-gpg-user），也适用于对称密钥模式（不支持轮换密钥）。这是因为，在历史数据的背景下，这是一个固有的复杂问题。例如，即使某个时刻密钥被轮换了，拥有之前密钥的用户仍然可以访问之前的仓库历史。这个问题在 https://github.com/AGWA/git-crypt/issues/47 中有更详细的讨论。

使用 git-crypt 加密的文件无法被压缩。即使对加密文件做了最微小的改动，git 也得存储改动后的整个文件，而不是仅仅存储改动部分。

虽然 git-crypt 使用 SHA-1 HMAC 保护单个文件内容，但如果整个仓库没有做防篡改保护，git-crypt 就不能安全使用（如果攻击者可以篡改你的仓库，他们就可以修改你的. gitattributes 文件来禁用加密）。如果必要，可以使用 git 的特性，例如签名标签，而不是仅仅依靠 git-crypt 来保证完整性。

使用 git-crypt 加密的文件不能用 git-apply 打补丁，除非补丁本身也是加密的。要生成一个加密的补丁，可以使用命令 `git diff --no-textconv --binary` ​。或者，你也可以在 git 外部使用 patch 命令来打明文补丁。

git-crypt 在一些第三方 git 图形用户界面（GUI）上无法可靠工作，例如 [Atlassian SourceTree](https://jira.atlassian.com/browse/SRCTREE-2511) 和 GitHub for Mac。文件可能会保持未加密状态。

## Gitattributes 文件

.gitattributes 文件的文档位于 gitattributes (5) 手册页面中。文件匹配模式与. gitignore 中使用的格式相同，详情可参见 gitignore (5) 手册页面，但需要注意的是，仅指定一个目录（例如 `/dir/` ​）不足以对该目录下的所有文件进行加密。

另请注意，`dir/*` ​模式不会匹配 `dir` ​子目录下的文件。如果要加密整个 `dir` ​子树，请使用 `dir/**` ​：

```
dir/** filter=git-crypt diff=git-crypt
```

.gitattributes 文件不能被加密，因此请确保通配符不会意外地匹配到它。如有必要，你可以像这样将 .gitattributes 排除在加密之外：

```
.gitattributes !filter !diff
```




