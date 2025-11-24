---
title: Docker Desktop 学习笔记
date: 2025-11-24
tags: [docker]
category: [计算机]
---

# Docker Desktop 学习笔记

## 基础配置

先安装 [WSL2](install_wsl2_and_to_d_disk.md)

然后去 docker 官网下载 [docker desktop](https://www.docker.com)

安装好之后修改配置：

---

1. 修改拉取的镜像位置

settings ——> Advanced ——> Resources ——> Disk image location

这里修改为 `D:\docker\DockerDesktopWSL`，

---

2. 修改文件共享位置

settings ——> Resources ——> File sharing

这里修改为 `D:\docker\file sharing`

---

3. 修改 docker hub 镜像

settings ——> Docker Engine

这里是 docker hub 镜像位置，去[华为云镜像中心](https://console.huaweicloud.com/swr/?region=cn-southwest-2#/swr/mirror)右上角的镜像加速器那儿复制镜像网址，让后填入其中

---

## 概念讲解

使用 vaultwarden 的 docker 部署命令来解释

```bash
docker pull vaultwarden/server:latest
docker run --detach --name vaultwarden \
  --env DOMAIN="https://vw.domain.tld" \
  --volume D:/workspace/vaultwarden_backupdata:/data/ \
  --restart unless-stopped \
  --publish 127.0.0.1:8000:80 \
  vaultwarden/server:latest
```

查看是否挂载成功的命令

```bash
docker exec -it vaultwarden ls -l /data
```

### 镜像

从 docker hub 拉取下来就是镜像，例如 `docker pull vaultwarden/server:latest` 命令，就是拉取了 vaultwarden 的最新版本

存储位置是 `Disk image location` 下的 vhdx 文件中，我已经把 `Disk image location` 修改为了 `D:\docker\DockerDesktopWSL`，所以是存储在这个路径下

### 容器

创建一个容器来运行镜像，例如

```bash
docker run --detach --name vaultwarden
```

- `docker run`：创建并运行一个容器
- `--detach`：后台运行
- `--name vaultwarden`：容器名是 vaultwarden

存储位置也是 `Disk image location` 下的 vhdx 文件中，我已经把 `Disk image location` 修改为了 `D:\docker\DockerDesktopWSL`，所以是存储在这个路径下

### 卷

这个目录是存储服务器持久化数据的地方，也是 Windows 宿主机所在路径

`--volume D:/docker/DockerDesktopWSL/:/data/` 就是卷所在目录，冒号之前的就是自定义路径，冒号之后的得翻阅文档才能确定

卷的路径需要在运行容器时自定义，不想前两个可以全局化配置

| 类型                       | 示例                             | 位置                        | 适用场景       |
| -------------------------- | -------------------------------- | --------------------------- | -------------- |
| **Docker 管理的 Volume**   | `docker volume create mydata`    | 存在 WSL2 的 docker/volumes | 最稳定、性能好 |
| **绑定挂载（Bind Mount）** | `D:/your-vaultwarden-data:/data` | 你本地 Windows 文件夹       | 方便查看和备份 |

容器的文件系统是 临时的：

- 删除容器 → 数据也删除
- 升级镜像 → 数据丢失
- 重建容器 → 空空如也

为了让重要数据 不跟着容器一起消失，Docker 提供了 Volume。

我使用的是 bind mount。

对于 Vaultwarden，它完全适合使用 bind mount，因为方便你在 Windows 上备份和同步。

Volume 就是用来存“容器生命周期之外仍要保存的数据”

比如数据库内容、上传文件、配置、密钥等

容器删了没关系，Volume 里的数据还在

### `--env DOMAIN="https://vw.domain.tld"`

给容器里的程序设置一个环境变量。

容器内能看到：

```ini
DOMAIN=https://vw.domain.tld
```

### `--publish 127.0.0.1:8000:80`

端口映射：

- 容器内 Vaultwarden 监听的是端口 80
- 映射到 宿主机的 127.0.0.1:8000

所以在 Windows 打开：

http://localhost:8000

如果想要让同局域网下的其它设备访问的话就去除 `127.0.0.1:` 字段，只保留 `--publish 8000:80`，意思是映射到 8000 端口

然后在同局域网下的其它设备访问 `http://<你的WindowsIP地址>:<宿主机端口>`，其中 Windows IP 地址是打开 pwsh，输入 `ipconfig` 就可查看 ip 地址

### `--restart unless-stopped`

自动重启策略：

- 宿主机重启后 → 自动启动
- 手动停止后 → 不自动启动

容器和镜像存储在 Disk image location 下，服务器持久化数据存储在 volume 下

## docker 删除缓存

### 构建缓存（Build Cache）

当你用 docker build 时，会产生很多分层缓存，用来加速下次 build。

特点：

- 不在运行的容器使用
- 不包含运行时数据
- 删了最多就是下次 build 会变慢一点

```bash
docker builder prune -a
```

### 未使用的镜像（unused image）

包括：

- 没容器在使用的镜像
- 被替换下来的老版本镜像
- 下载但没用过的镜像

```bash
docker image prune -a
```

### 停止的容器（stopped containers）

停止的容器不是在运行，也没有用处。

```bash
docker container prune
```

### 未使用的网络（unused networks）

只是 Docker 创建但容器没有使用的网络。

```bash
docker network prune
```

### 安全清理的一键命令

它会清理：

- build 缓存
- 停止的容器
- 未使用的镜像
- unused networks

**不删 volumes，所以很安全。**

```bash
docker system prune -a
```

### 清除 volumes 的命令要极度小心

```bash
docker volume prune
```

## docker 的通俗理解

| 真实含义                      | 类比                        | 存放位置                    | 删除会丢失吗？                |
| ----------------------------- | --------------------------- | --------------------------- | ----------------------------- |
| **镜像（Image）**             | VSCode 安装包/程序本体      | Disk image location（vhdx） | 删除不会影响 volume           |
| **容器本体（容器的 rootfs）** | VSCode 进程运行时的临时数据 | Disk image location（vhdx） | 删除不会影响 volume           |
| **Volume（持久化数据）**      | VSCode 打开的项目文本文件   | Windows 本地磁盘            | ✔ 永远不会因容器删除而丢失   |
| **Bind mount（你用的方式）**  | Windows 上的真实文件夹      | Windows 本地磁盘            | ✔ 永远不会因 Docker 行为丢失 |
