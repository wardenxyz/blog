---
title: SOPS:Secrets OPerationS
date: 2025-07-23
tags: [sops, 加密, age, gpg]
category: [计算机]
---

# SOPS:Secrets OPerationS

安装

https://github.com/getsops/sops

## 使用

创建 `.sops.yaml` 文件

```yaml
creation_rules:
  - age: 'age1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #age 公钥
#   - pgp: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #PGP 公钥
```

age 使用笔记：[age-note](/posts/2025/age.md)

gpg 使用笔记：[gpg-note](/posts/2024/gen_GPG_key.md)

## sops 加密二进制文件

```bash
sops --encrypt --input-type binary --output secret.json secret.bin
```

```bash
sops --decrypt --output-type binary --output secret.bin secret.json
```

## sops 加密文本文件

- 原地加密

```bash
sops -e -i secrets.txt
```

- 加密到新文件

```bash
sops --encrypt --output secrets.enc.txt secrets.txt
```

- 查看或编辑加密文件

```bash
sops secrets.enc.txt
```

- 解密文件（终端输出）

```bash
sops --decrypt a.txt
```

- 解密到新文件

```bash
sops --decrypt --output secrets.decrypted.txt secrets.enc.txt
```