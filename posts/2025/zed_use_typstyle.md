---
title: 在 zed 上配置 typstyle
date: 2025-03-21
tags: [zed, Typst]
category: [计算机]
---

# 在 zed 上配置 typstyle

在 Zed 上配置 Typst 的格式化工具，在 settings.json 中写入以下即可

```json
"languages": {
"Typst": {
			"show_edit_predictions": false,
			"format_on_save": "on",
			"formatter": {
				"external": {
					"command": "typstyle"
				}
			}
		}
}
```

Zed Typst 插件：https://github.com/weethet/typst.zed
