# 个人静态网页

- 网页生成脚本在 `.github/scripts`

- 静态资源在 `.github/static`

- 网页模板在 `.github/templates`

- 帖子在  posts 下按年份排列

- README.md 就是 index.html

## 启动命令如下

```bash
uv venv
```

```bash
.venv\Scripts\activate
```

```bash
uv pip install -r requirements.txt
```

```bash
uv run .github\scripts\static_gen.py
```

```bash
python -m http.server -d site
```
