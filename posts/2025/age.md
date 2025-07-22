---
title: age-note
date: 2025-07-22
tags: [age, 加密, 隐私]
category: [计算机]
---

# age-note

age 是一个简单的加密工具，旨在提供一种安全、易用的方式来加密文件和数据。它的设计理念是简洁和高效，适合需要快速加密和解密的场景。

- 生成密钥对

```bash
age-keygen -o key.txt
Public key: age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p
```

- 加密文件

```bash
age -r age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p secrets.txt > secrets.txt.age
```

- 解密文件

```bash
age -d -i key.txt secrets.txt.age > secrets.txt
```


- 使用密码加密

```bash
age -p secrets.txt > secrets.txt.age
```

- 解密时输入密码

```bash
age -d secrets.txt.age > secrets.txt
```

## 密钥对加解密

```bash
age -r age1t9xarklwwxyzcgftvc2m8s574lt4c0wl0ukgk7qmpl38ry3cruxs4f69r5 -o encrypted.age a.txt
age -d -i key.txt -o decrypted.txt encrypted.age
```

## 密码加解密

```bash
age --passphrase -o encrypt.age a.txt
age --decrypt -o a.txt encrypt.age
```
