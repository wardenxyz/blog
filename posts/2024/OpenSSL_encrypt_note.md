---
title: OpenSSL 加解密速查笔记
date: 2024-10-06
tags: [OpenSSL, 加密]
category: [计算机]
---

# OpenSSL 加解密速查指南

## 核心加解密命令

### 文件加密

```bash
openssl enc -p -aes-256-cbc -pbkdf2 -iter 20000 -pass pass:密码明文 -in 输入文件 -out 输出文件.enc
```

### 文件解密

```bash
openssl enc -d -p -aes-256-cbc -pbkdf2 -iter 20000 -pass pass:密码明文 -in 加密文件.enc -out 解密文件
```

通用参数说明：

- `-p`：显示使用的盐值和密钥
- `-aes-256-cbc`：AES 256位 CBC模式
- `-pbkdf2`：使用PBKDF2密钥派生
- `-iter 20000`：迭代次数（建议>=10000）

---

## 文件密钥操作

### 使用密钥文件加密

```bash
openssl enc -aes-256-cbc -pbkdf2 -in 明文文件 -out 加密文件 -pass file:密钥文件
```

### 使用密钥文件解密

```bash
openssl enc -d -aes-256-cbc -pbkdf2 -in 加密文件 -out 解密文件 -pass file:密钥文件
```

---

## 实用工具命令

### 生成随机文件

生成1MB随机数据：

```bash
openssl rand -out random.bin 1048576
```

### 计算文件哈希值

SHA-256校验：

```bash
openssl dgst -sha256 文件名
```

### 生成RSA密钥对

```bash
# 生成私钥
openssl genpkey -algorithm RSA -out private.pem

# 提取公钥
openssl rsa -pubout -in private.pem -out public.pem
```

---

## 算法查询命令

| 命令                                  | 功能               |
| ------------------------------------- | ------------------ |
| `openssl list -cipher-algorithms`     | 查看对称加密算法   |
| `openssl list -public-key-algorithms` | 查看非对称加密算法 |
| `openssl list -digest-commands`       | 查看支持的哈希算法 |
