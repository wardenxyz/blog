#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Static site generator located under .github/site.

Content root: repo root (README.md, categories.md, tags.md, posts/..)
Output: repo_root/site
Assets (templates/static): alongside this file (.github/site)
"""

from __future__ import annotations

import os
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Tuple

import frontmatter
from markdown import Markdown
from bs4 import BeautifulSoup
from pymdownx.superfences import fence_div_format


SCRIPT_DIR = Path(__file__).parent.resolve()
# repo root is the parent of the .github directory; this file is under .github/script
REPO_ROOT = SCRIPT_DIR.parent.parent
SRC = REPO_ROOT
OUT = REPO_ROOT / "site"
# assets live in .github/templates and .github/static
TEMPLATES = SCRIPT_DIR.parent / "templates"
STATIC = SCRIPT_DIR.parent / "static"


@dataclass
class Page:
    src: Path
    out: Path
    title: str
    html: str
    toc: str
    base: str
    date: str = ""  # 添加日期字段
    tags: list[str] | None = None
    categories: list[str] | None = None


def clean_outdir():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)


def copy_static():
    if STATIC.exists():
        shutil.copytree(STATIC, OUT / "static")


def rel_base(path_under_out: Path) -> str:
    rel = path_under_out.relative_to(OUT)
    depth = len(rel.parents) - 1
    return "" if depth <= 0 else "../" * depth


def load_markdown_with_toc(text: str) -> Tuple[str, str]:
    # Enable TOC, fences, tables, lists, attrs, magiclink (autolink urls), and mermaid via superfences
    md = Markdown(
        extensions=[
            "toc",
            "fenced_code",
            "tables",
            "sane_lists",
            "attr_list",
            "pymdownx.magiclink",
            "pymdownx.superfences",
        ],
    extension_configs={
            # Superfences: convert ```mermaid fenced blocks into <div class="mermaid"> ... </div>
            "pymdownx.superfences": {
                "custom_fences": [
                    {
                        "name": "mermaid",
                        "class": "mermaid",
            # Pass the actual function object for programmatic API
            "format": fence_div_format,
                    }
                ]
            },
            # Magiclink: create clickable links for bare https:// URLs
            "pymdownx.magiclink": {
                "repo_url_shortener": False,
                "hide_protocol": False,
            },
        },
    )
    html = md.convert(text)
    toc_html = getattr(md, "toc", "") or ""
    return html, toc_html


def extract_title_from_text(text: str) -> str:
    for line in text.splitlines():
        m = re.match(r"^\s*#\s+(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return "Untitled"


def render_template(template_name: str, context: dict) -> str:
    tpl_path = TEMPLATES / template_name
    text = tpl_path.read_text(encoding="utf-8")
    def repl(s: str) -> str:
        for k, v in context.items():
            s = s.replace(f"{{{{ {k} }}}}", str(v))
        return s
    return repl(text)


def rewrite_md_links_to_html(html: str) -> str:
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception:
        return html
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href or href.startswith("#"):
            continue
        low = href.lower()
        # For external links, ensure they open in a new tab with safe rel attributes
        if low.startswith("http://") or low.startswith("https://"):
            # target
            a["target"] = "_blank"
            # merge rel values
            existing_rel = set((a.get("rel") or [])) if isinstance(a.get("rel"), list) else set(str(a.get("rel") or "").split())
            existing_rel.update({"noopener", "noreferrer"})
            if existing_rel:
                a["rel"] = " ".join(sorted(existing_rel))
            continue
        if low.startswith("mailto:") or low.startswith("tel:"):
            continue
        qpos = href.find("?")
        fpos = href.find("#")
        split_pos = None
        if qpos != -1 and fpos != -1:
            split_pos = min(qpos, fpos)
        elif qpos != -1:
            split_pos = qpos
        elif fpos != -1:
            split_pos = fpos
        path = href if split_pos is None else href[:split_pos]
        tail = "" if split_pos is None else href[split_pos:]
        if path.lower().endswith(".md"):
            a["href"] = path[:-3] + ".html" + tail
    try:
        return str(soup)
    except Exception:
        return html


def build_page(src_md: Path, out_html: Path) -> Page:
    post = frontmatter.load(src_md)
    body_md = post.content or src_md.read_text(encoding="utf-8")
    title = post.get("title") or extract_title_from_text(body_md)
    date = post.get("date", "")
    # 如果日期是 datetime 对象，转换为字符串
    if hasattr(date, 'strftime'):
        date = date.strftime('%Y-%m-%d')
    elif date:
        date = str(date)
    # 解析 tags 与 categories（兼容 category / categories 字段与字符串/列表）
    raw_tags = post.get("tags") or []
    if isinstance(raw_tags, (str, int, float)):
        tags: list[str] = [str(raw_tags)]
    else:
        tags = [str(t) for t in raw_tags]

    raw_cats = post.get("categories") if "categories" in post else post.get("category")
    if raw_cats is None:
        categories: list[str] = []
    elif isinstance(raw_cats, (str, int, float)):
        categories = [str(raw_cats)]
    else:
        categories = [str(c) for c in raw_cats]
    html, toc = load_markdown_with_toc(body_md)
    # Post-process links: convert .md to .html and set external links to open in new tab
    html = rewrite_md_links_to_html(html)
    base = rel_base(out_html)
    return Page(src=src_md, out=out_html, title=title, html=html, toc=toc, base=base, date=date, tags=tags, categories=categories)


def generate_sidebar(all_pages: list[Page], current: Page) -> str:
    items: dict[str, list[tuple[str, str, str]]] = {}  # 改为存储 (title, link, date)
    for p in all_pages:
        rel = os.path.relpath(p.out, start=current.out.parent)
        link = rel.replace(os.sep, "/")
        year = "Others"
        try:
            parts = p.src.relative_to(SRC).parts
            if len(parts) >= 3 and parts[0] == "posts" and parts[1].isdigit():
                year = parts[1]
        except Exception:
            pass
        items.setdefault(year, []).append((p.title, link, p.date))
    
    years = sorted(items.keys(), reverse=True)
    html_parts = ["<nav class=\"sidebar\" aria-label=\"所有文章\">"]
    for y in years:
        html_parts.append(f"<div class=\"sidebar-group\"><div class=\"sidebar-year\">{y}</div><ul>")
        # 按日期排序，最新的在上面，如果没有日期则排在后面
        sorted_items = sorted(items[y], key=lambda t: (t[2] if t[2] else "0000-00-00"), reverse=True)
        for title, link, date in sorted_items:
            active = ' class="active"' if link == os.path.relpath(current.out, start=current.out.parent).replace(os.sep, "/") else ""
            html_parts.append(f"<li><a href=\"{link}\"{active}>{title}</a></li>")
        html_parts.append("</ul></div>")
    html_parts.append("</nav>")
    return "".join(html_parts)


def write_page(page: Page, github_url: str, owner: str, sidebar_html: str):
    # 构建元信息区块 HTML（仅当存在任意一项时渲染）
    meta_parts: list[str] = []
    if page.date:
        meta_parts.append(f'<span class="meta-item meta-date" title="发布日期">📅 {page.date}</span>')
    if page.categories:
        cats = "".join(f'<span class="badge badge-cat">{c}</span>' for c in page.categories or [])
        if cats:
            meta_parts.append(f'<span class="meta-item" title="分类">📂 {cats}</span>')
    if page.tags:
        tgs = "".join(f'<span class="badge badge-tag">{t}</span>' for t in page.tags or [])
        if tgs:
            meta_parts.append(f'<span class="meta-item" title="标签">🏷️ {tgs}</span>')
    meta_html = ""
    if meta_parts:
        meta_html = '<div class="post-meta" aria-label="文章元信息">' + "".join(meta_parts) + "</div>"
    context = {
        "title": page.title,
        "content": page.html,
        "toc": page.toc,
        "year": datetime.now().year,
        "owner": owner,
        "github_url": github_url,
        "base": page.base,
        "sidebar": sidebar_html,
        "meta": meta_html,
    }
    out_html = render_template("base.html", context)
    page.out.parent.mkdir(parents=True, exist_ok=True)
    page.out.write_text(out_html, encoding="utf-8")


def write_search_index(pages: list[Page]):
    """Write a lightweight search index to OUT/search.json
    Include title, output path relative to site root, tags (if available), and plain text content.
    """
    import json
    from bs4 import BeautifulSoup

    items = []
    for p in pages:
        # Skip non-md or non-content pages if needed; here we include all.
        rel_path = p.out.relative_to(OUT).as_posix()
        # Extract text content from HTML
        try:
            soup = BeautifulSoup(p.html, "html.parser")
            text = soup.get_text(" ", strip=True)
        except Exception:
            text = ""
        # Try fetch tags from frontmatter by reloading quickly
        tags = []
        try:
            fm = frontmatter.load(p.src)
            tags = fm.get("tags") or []
        except Exception:
            pass
        items.append({
            "title": p.title,
            "path": rel_path,
            "tags": tags,
            "content": text[:2000]  # cap to keep file small
        })

    (OUT / "search.json").write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")


def iter_markdown_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*.md") if p.is_file()]


def copy_post_assets(posts_root: Path):
    exts = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".mp4", ".mp3", ".pdf"}
    if not posts_root.exists():
        return
    for p in posts_root.rglob("*"):
        if p.is_file() and p.suffix.lower() in exts:
            rel = p.relative_to(REPO_ROOT)
            dest = OUT / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)


def main():
    clean_outdir()
    copy_static()
    gh_repo = os.getenv("GITHUB_REPOSITORY", "")
    github_url = f"https://github.com/{gh_repo}" if gh_repo else "#"
    owner = os.getenv("GITHUB_REPOSITORY_OWNER") or os.getenv("USERNAME") or os.getenv("USER") or "Your Name"

    root_pages = [
        (SRC / "README.md", OUT / "index.html"),
        (SRC / "categories.md", OUT / "categories.html"),
        (SRC / "tags.md", OUT / "tags.html"),
    ]
    built_pages: list[Page] = []
    for src_md, out_html in root_pages:
        if src_md.exists():
            page = build_page(src_md, out_html)
            built_pages.append(page)

    posts_dir = SRC / "posts"
    count_posts = 0
    if posts_dir.exists():
        for md in iter_markdown_files(posts_dir):
            rel = md.relative_to(SRC)
            out_html = OUT / rel.with_suffix(".html")
            page = build_page(md, out_html)
            built_pages.append(page)
            count_posts += 1
        copy_post_assets(posts_dir)

    for p in built_pages:
        sidebar = generate_sidebar([bp for bp in built_pages if bp.src.as_posix().endswith('.md')], p)
        write_page(p, github_url, owner, sidebar)

    # write search index after all pages are built
    write_search_index(built_pages)

    print(f"Built pages: {len([p for p in [rp[0] for rp in root_pages] if p.exists()])}, posts: {count_posts}")


if __name__ == "__main__":
    main()
