# 个人静态网页

- 网页生成脚本在 `.github/scripts`

- 静态资源在 `.github/static`

- 网页模板在 `.github/templates`

- 帖子在  posts 下按年份排列

- README.md 就是 index.html

- 运行 `uv run .github\scripts\static_gen.py` 来生成网页，预览命令是 `python -m http.server -d site`
