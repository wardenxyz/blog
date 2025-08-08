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
    md = Markdown(extensions=[
        "toc",
        "fenced_code",
        "tables",
        "sane_lists",
        "attr_list",
    ])
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
        if low.startswith("http://") or low.startswith("https://") or low.startswith("mailto:") or low.startswith("tel:"):
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
    html, toc = load_markdown_with_toc(body_md)
    html = rewrite_md_links_to_html(html)
    base = rel_base(out_html)
    return Page(src=src_md, out=out_html, title=title, html=html, toc=toc, base=base, date=date)


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
    context = {
        "title": page.title,
        "content": page.html,
        "toc": page.toc,
        "year": datetime.now().year,
        "owner": owner,
        "github_url": github_url,
        "base": page.base,
        "sidebar": sidebar_html,
    }
    out_html = render_template("base.html", context)
    page.out.parent.mkdir(parents=True, exist_ok=True)
    page.out.write_text(out_html, encoding="utf-8")


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

    print(f"Built pages: {len([p for p in [rp[0] for rp in root_pages] if p.exists()])}, posts: {count_posts}")


if __name__ == "__main__":
    main()
