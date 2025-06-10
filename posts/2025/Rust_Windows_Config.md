---
title: 在 Windows 上配置 Rust 环境
date: 2025-03-16
tags: [Rust]
category: [计算机]
---

# 在 Windows 上配置 Rust 环境

起因：想编译 Zed 的 Windows 版，但不想下载 visual studio

视频：https://www.bilibili.com/video/BV12RDhYPE7M/?share_source=copy_web&vd_source=7a8cdea3693bb45fc81a5ee43e70eaa3

## 准备工作

### 配置 gcc 环境

在 [mingw](https://github.com/niXman/mingw-builds-binaries/releases) 网页下下载 `x86_64-15.1.0-release-win32-seh-ucrt-rt_v12-rev0.7z
`，其中 `x86_64` 是 64 位的，`seh` 是异常处理方式，`ucrt` 是 C 运行时库，`rt_v12-rev0` 是版本号，15.1.0 是 GCC 的版本号。

解压后把 `bin` 路径放到环境变量中

检测

```ps
gcc -v

Using built-in specs.
COLLECT_GCC=D:\workspace\mingw64\bin\gcc.exe
COLLECT_LTO_WRAPPER=D:/workspace/mingw64/bin/../libexec/gcc/x86_64-w64-mingw32/15.1.0/lto-wrapper.exe
Target: x86_64-w64-mingw32
Configured with: ../../../src/gcc-15.1.0/configure --host=x86_64-w64-mingw32 --build=x86_64-w64-mingw32 --target=x86_64-w64-mingw32 --prefix=/mingw64 --with-sysroot=/c/buildroot/x86_64-1510-win32-seh-ucrt-rt_v12-rev0/mingw64 --enable-host-shared --disable-multilib --enable-languages=c,c++,fortran,lto --enable-libstdcxx-time=yes --enable-threads=win32 --enable-libstdcxx-threads=yes --enable-libgomp --enable-libatomic --enable-lto --enable-graphite --enable-checking=release --enable-mingw-wildcard --enable-fully-dynamic-string --enable-version-specific-runtime-libs --enable-libstdcxx-filesystem-ts=yes --disable-libssp --disable-libstdcxx-pch --disable-libstdcxx-debug --enable-bootstrap --disable-rpath --disable-win32-registry --disable-nls --disable-werror --disable-symvers --with-gnu-as --with-gnu-ld --with-arch=nocona --with-tune=core2 --with-libiconv --with-system-zlib --with-gmp=/c/buildroot/prerequisites/x86_64-w64-mingw32-static --with-mpfr=/c/buildroot/prerequisites/x86_64-w64-mingw32-static --with-mpc=/c/buildroot/prerequisites/x86_64-w64-mingw32-static --with-isl=/c/buildroot/prerequisites/x86_64-w64-mingw32-static --with-pkgversion='x86_64-win32-seh-rev0, Built by MinGW-Builds project' --with-bugurl=https://github.com/niXman/mingw-builds LD_FOR_TARGET=/c/buildroot/x86_64-1510-win32-seh-ucrt-rt_v12-rev0/mingw64/bin/ld.exe --with-boot-ldflags='-pipe -fno-ident -L/c/buildroot/x86_64-1510-win32-seh-ucrt-rt_v12-rev0/mingw64/opt/lib -L/c/buildroot/prerequisites/x86_64-zlib-static/lib -L/c/buildroot/prerequisites/x86_64-w64-mingw32-static/lib  -Wl,--disable-dynamicbase -static-libstdc++ -static-libgcc'
Thread model: win32
Supported LTO compression algorithms: zlib
gcc version 15.1.0 (x86_64-win32-seh-rev0, Built by MinGW-Builds project)
```

### 下载 Rust

这里下载 [Rust](https://www.rust-lang.org/zh-CN/learn/get-started)，32 位和 64 位两种，根据实际情况选取

### 配置 Rust Toolchain 镜像源

- 中科大镜像源：https://mirrors.ustc.edu.cn/help/rust-static.html#rust-toolchain

```powershell
$env:RUSTUP_DIST_SERVER="https://mirrors.ustc.edu.cn/rust-static"
$env:RUSTUP_UPDATE_ROOT="https://mirrors.ustc.edu.cn/rust-static/rustup"
```

- Rsproxy 源：https://rsproxy.cn/#getStarted

```powershell
export RUSTUP_DIST_SERVER="https://rsproxy.cn"
export RUSTUP_UPDATE_ROOT="https://rsproxy.cn/rustup"
```

上面两个二选一

配置好的用户变量：

```
变量                                值
RUSTUP_DIST_SERVER                 https://rsproxy.cn
RUSTUP_UPDATE_ROOT                 https://rsproxy.cn/rustup
```

### 配置安装位置

在 D 盘下创建两个文件夹

```
D:\Rust\rustup
D:\Rust\cargo
```

把这两个文件夹加入到用户变量中去

```
变量                                值
RUSTUP_HOME                        D:\Rust\rustup
CARGO_HOME                         D:\Rust\cargo
```

## 安装

点击下载的 `rustup-init.exe`，运行开启一个终端，如下

```powershell
Rust Visual C++ prerequisites

Rust requires a linker and Windows API libraries but they don't seem to beavailable.

These components can be acquired through a Visual Studio installer.

1) Quick install via the Visual Studio Community installer
(free for individuals,academic uses, and open source).

2) Manually install the prerequisites
(for enterprise and advanced users).

3) Don't install the prerequisites
(if you're targeting the GNU ABI)

>2                  <----------------------------------------------------- 这里选第 2 个

You can acquire the build tools by installing Hicrosoft Visual Studio.

		https://visualstudio.microsoft.com/downloads

Check the box for "Desktop development with C++" which will ensure that the needed components are installed.If your locale language is not Englishthen additionally check the box for English under Language packs.

For more details see:

		https://rust-lang.github.io/rustup/installation/windows-msvc.html

Install the C++ build tools before proceeding.

If you will be targeting the GNU ABI or otherwise know what you are
doing then it is fine to continue installation without the build
tools, but otherwise, install the C++ build tools before proceeding.

Continue?(y/N)
y                 <----------------------------------------------------------------- Yes

The Cargo home directory is located at:

		D:\Rust\cargo

This can be modified with the CARGO_HOME environment variable.

The cargo, rustc, rustup and other commands will be added to Cargo's bin directory, located at:

		D:\Rust\cargo\bin

This path will then be added to your PATH environment variable by
modifying the HKEY_CURRENT_USER/Environment/PATH registry key.

You can uninstall at any time with rustup self uninstall and these changes will be reverted.

Current installation options:

		default host triple: x86_64-pc-windows-msvc
			default toolchain: stable(default)
								profile: default
	 modify PATH variable: yes

1) Proceed with standard installation(default - just press enter)

2) Customize installation

3) Cancel installation
>2                    <------------------------------------------------------------------- 选第 2 个

I'm going to ask you the value of each of these installation options.
You may simply press the Enter key to leave unchanged.

Default host triple? [x86_64-pc-windows-msvc]
x86_64-pc-windows-gnu            <------------------------------------ 输入 x86_64-pc-windows-gnu

Default toolchain?(stable/beta/nightly/none) [stable]
        <----------------------------------------------- 回车

Profile (which tools and data to install)?(minimal/default/complete) [default]
        <----------------------------------------------- 回车

Modify PATH variable?(Y/n)
y             <----------------------------------------------------------------------- Yes

Current installation options:

		default host triple: x86_64-pc-windows-gnu
			default toolchain: table
								profile: default
	 modify PATH variable: yes

1) Proceed with selected options(default - just press enter)
2) Customize installation
3) Cancel installation
>1                   <--------------------------------------------------------------- 选第 1 个

info: profile set to 'default'
info: setting default host triple to x86_64-pc-windows-gnu
info: syncing channel updates for 'stable-x86_64-pc-windows-gnu'
info: latest update on 2024-10-17, rust version 1.82.0(f6e511eec 2024-10-15)
info:downloading component 'cargo'
	10.3 MiB/  10.3MiB (100%)   4.8MiB/s in  2s  ETA: 0S
info: downloading component 'clippy'
	 4.1 MiB/   4.1MiB (100%)   4.1MiB/s in  1s  ETA: 0s
info: downloading component 'rust-docs'
	16.3 MiB/  16.3MiB (100%)   1.7MiB/s in  9s  ETA: 0s
info: downloading component 'rust-mingw'
	 4.7 MiB/   4.7MiB (100%)   2.3MiB/s in  2s  ETA: 0s
info: downloading component 'rust-std'
	23.7 MiB/  23.7MiB (100%)   3.7MiB/s in  8s  ETA: 0s
info: downloading component 'rustc'
	79.2 MiB/  79.2MiB (100%)   3.7MiB/s in 21s  ETA: 0s
info: downloading component 'rustfmt'
info: installing component 'cargo'
info: installing component 'clippy'
info: installing component 'rust-docs'
	16.3 MiB/  16.3MiB (100%)   3.2MiB/s in  5s  ETA: 0s
info: installing component 'rust-mingw'
info: installing component'rust-std'
	23.7 MiB/  23.7MiB (100%)  14.3MiB/s in  1S  ETA: 0s
info: installing component 'rustc'
	79.2 MiB/  79.2MiB (100%)  14.2MiB/s in  5s  ETA: 0s
info: installing component 'rustfmt'
info: default toolchain set to 'stable-x86_64-pc-windows-gnu'

		stable-x86_64-pc-windows-gnu installed - rustc 1.82.0(f6e511eec 2024-10-15)

Rust is installed now. Great!

To get started you may need to restart your current shell
This would reload its PATH environment variable to include
Cargo's bin directory(D:Rust\cargo\bin)
Press the Enter key to continue.
```

一共八步

检测

```ps
rustup --version

rustup 1.28.1 (f9edccde0 2025-03-05)
info: This is the version for the rustup toolchain manager, not the rustc compiler.
info: The currently active `rustc` version is `rustc 1.85.0 (4d91de4e4 2025-02-17)`
```

```ps
cargo --version

cargo 1.85.0 (d73d2caf9 2024-12-31)
```

## 配置 cargo 镜像源

这里选择中科大镜像源：https://mirrors.ustc.edu.cn/help/crates.io-index.html

在 `D:\Rust\cargo\config.toml` 中添加如下内容

```toml
[source.crates-io]
replace-with = 'ustc'

[source.ustc]
registry = "sparse+https://mirrors.ustc.edu.cn/crates.io-index/"

[registries.ustc]
index = "sparse+https://mirrors.ustc.edu.cn/crates.io-index/"
```
