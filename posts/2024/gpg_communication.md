---
title: GPG 在通信中的简单理解
date: 2024-04-08
tags: [GPG, 加密]
category: [计算机]
---

# GPG 在通信中的简单理解

```
+----------------+          +----------------+
| Alice生成密钥对 |          | Bob生成密钥对  |
| 公钥A | 私钥A   |          | 公钥B | 私钥B  |
+-------+--------+          +-------+--------+
        | 交换公钥 |                    |
        +--------->+<------------------+
                   |
+------------------|-------------------+
| 加密阶段：        | 解密阶段：         |
| Alice用公钥B加密  → 密文 → Bob用私钥B解密 |
+------------------|-------------------+
| 签名阶段：         | 验证阶段：         |
| Alice用私钥A签名 → 签名 → Bob用公钥A验证 |
+--------------------------------------+
```

## 核心概念

**非对称加密体系**：

- 公钥（Public Key）：可公开分发的加密钥匙
- 私钥（Private Key）：必须严格保密的解密钥匙
- 数学关系：公钥由私钥推导得出，但无法逆向反推

**数字签名三要素**：

1. 身份认证（Authentication） - 确认消息来源
2. 完整性验证（Integrity） - 确保内容未被篡改
3. 不可否认性（Non-repudiation） - 发送方无法否认发送行为

## 密钥管理流程

```bash
# 生成密钥对（4096位 RSA）
gpg --full-generate-key

# 导出公钥
gpg --armor --export alice@example.com > alice_pubkey.asc

# 导入他人公钥
gpg --import bob_pubkey.asc

# 查看密钥列表
gpg --list-keys
```

## 完整通信流程（Alice → Bob）

### 准备阶段

1. 双方生成密钥对
2. 交换公钥（通过密钥服务器/邮件/当面交换）
3. 互相签名验证公钥真实性

### 加密阶段

1. Alice 撰写原始消息 `message.txt`

2. 使用 Bob 的公钥加密：

```bash
gpg --encrypt --recipient bob@example.com message.txt
```

3. 生成数字签名：

```bash
gpg --sign --detach-sig message.txt.gpg
```

### 解密验证阶段

1. Bob 接收加密文件 `message.txt.gpg` 和签名文件 `message.sig`

2. 验证签名：

```bash
gpg --verify message.sig message.txt.gpg
```

3. 解密文件：

```bash
gpg --decrypt message.txt.gpg > decrypted_message.txt
```

## 安全机制解析

| 步骤       | 使用密钥     | 数学运算 | 安全目标            |
| ---------- | ------------ | -------- | ------------------- |
| 消息加密   | Bob 的公钥   | RSA 加密 | 机密性              |
| 生成哈希值 | SHA-256      | 哈希计算 | 完整性校验          |
| 签名加密   | Alice 的私钥 | RSA 加密 | 身份认证/不可否认性 |
| 签名验证   | Alice 的公钥 | RSA 解密 | 验证来源            |
| 消息解密   | Bob 的私钥   | RSA 解密 | 获取明文            |

## 典型应用场景

1. 安全电子邮件（Thunderbird + Enigmail）
2. 软件包签名验证（Linux 软件源）
3. Git commit 签名
4. 加密文件存储
5. SSH 认证（GPG 作为 SSH 密钥）

## 常见问题解答

Q：私钥泄露怎么办？
A：立即吊销密钥并重新生成：

```bash
gpg --gen-revoke [key-id]
```

Q：如何验证公钥真实性？
A：通过指纹校验（16位短指纹更易验证）：

```bash
gpg --fingerprint bob@example.com
```

Q：为什么需要交叉签名？
A：建立信任链，推荐做法：

1. 当面交换密钥指纹
2. 参加密钥签名聚会（Key Signing Party）
3. 使用 Web of Trust 信任网络

Q：GPG 与对称加密的区别？
A：对比表

| 特性     | GPG（非对称）     | AES（对称）      |
| -------- | ----------------- | ---------------- |
| 密钥数量 | 密钥对（2个）     | 单一密钥         |
| 加密速度 | 慢（适合小数据）  | 快（适合大数据） |
| 密钥交换 | 无需安全通道      | 需要安全通道     |
| 典型用途 | 数字签名/密钥交换 | 文件加密         |

---

[下载 gpg4win](https://gpg4win.org/index.html) | [GPG 官方手册](https://gnupg.org/documentation/)
