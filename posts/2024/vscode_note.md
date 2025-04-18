---
title: VSCode 高效使用指南
date: 2024-04-08
tags: [vscode]
category: [计算机]
---

# VSCode 高效使用指南

## 🔑 SSH 连接服务器配置

1. **生成密钥对**：本地执行 `ssh-keygen`，公钥路径 `C:\Users\用户\.ssh\id_rsa.pub`
2. **配置服务器**：

```bash
# 服务器操作
echo 公钥内容 >> ~/.ssh/authorized_keys
sudo passwd 用户名  # 重置密码
```

3. **本地配置** `~/.ssh/config`：

```bash
Host 服务器hostname  # 通过 hostname 命令获取
HostName 服务器IP
User 用户名
```

> 💡 提示：密钥认证可免密操作，首次连接需输入密码验证身份

## 🛠️ VSCodium 扩展源切换

修改 `安装根目录/resources/app/product.json` 文件中的 `extensionsGallery` 键对应的值如下：

```json
"extensionsGallery": {
    "serviceUrl": "https://marketplace.visualstudio.com/_apis/public/gallery",
    "itemUrl": "https://marketplace.visualstudio.com/items"
}
```

## ✨ 高效编辑技巧

### 多光标操作

- `Alt+单击`：任意位置添加光标
- `Ctrl+F2`：全选相同内容添加光标
- `Alt+↑/↓`：整行快速复制

### 批量注释

`Ctrl+/`：选中多行后切换注释状态（Mac：`Cmd+/`）

### 查找替换

- `Ctrl+F`：快速查找
- `Ctrl+H`：替换当前文件内容
- `Ctrl+Alt+Enter`：全部替换

## ⚠️ 注意事项

代码片段（snippets）在以下场景不生效：

- Markdown 数学公式块（`$$` 包裹区域）
- YAML 文档属性区块
