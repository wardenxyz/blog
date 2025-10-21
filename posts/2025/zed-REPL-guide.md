---
title: 如何在 zed 中配置 REPL（python）
date: 2025-10-21
tags: [python, zed, REPL]
category: [计算机技术]
---

# 如何在 zed 中配置 REPL（python）

在 zed 的 settings.json 中写入

```json
"lsp": {
		"python": {
			"initialization_options": {
				"path": "D:\\Python\\Python313\\Lib\\site-packages" //这里是 pip install 的位置
			}
		}
	},
	"jupyter": {
		"kernel_selections": {
			"python": "ipykernel"
		}
	}
```

然后安装运行以下命令

```bash
pip install ipykernel
```

```bash
python -m ipykernel install --user
```
