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
import subprocess
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
    last_modified: str = ""  # 添加最后修改时间字段
    tags: list[str] | None = None
    categories: list[str] | None = None
    description: str = ""
    url: str = ""
    image: str = ""


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
            "pymdownx.highlight",
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
            # Highlight: 为代码块添加语言类名，供 Prism.js 使用
            "pymdownx.highlight": {
                "use_pygments": False,  # 不使用 Pygments，让 Prism.js 处理
                "auto_title": False,
                "anchor_linenums": False,
                "line_spans": "__span",
                "pygments_lang_class": True,
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


def extract_description_from_html(html: str, max_len: int = 180) -> str:
    try:
        soup = BeautifulSoup(html, "html.parser")
        # Prefer first paragraph's text
        p = soup.find("p")
        text = p.get_text(" ", strip=True) if p else soup.get_text(" ", strip=True)
        text = re.sub(r"\s+", " ", text)
        return text[:max_len]
    except Exception:
        return ""


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


def enhance_media_html(html: str) -> str:
    """Apply frontend-focused optimizations on generated HTML."""
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception:
        return html

    changed = False

    for img in soup.find_all("img"):
        if not img.get("loading"):
            img["loading"] = "lazy"
            changed = True
        if not img.get("decoding"):
            img["decoding"] = "async"
            changed = True
        if not img.get("referrerpolicy"):
            img["referrerpolicy"] = "no-referrer"
            changed = True

    for iframe in soup.find_all("iframe"):
        if not iframe.get("loading"):
            iframe["loading"] = "lazy"
            changed = True

    return str(soup) if changed else html


def get_git_last_modified(file_path: Path) -> str:
    """Get the last modified date of a file from git history."""
    try:
        # Use git log to get the last commit date
        # %cd: committer date
        # --date=format:...: format the date
        cmd = [
            "git",
            "log",
            "-1",
            "--format=%cd",
            "--date=format:%Y-%m-%d",
            str(file_path),
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=REPO_ROOT, check=False
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    return ""


def get_git_creation_date(file_path: Path) -> str:
    """Get the creation date of a file from git history (first commit)."""
    try:
        # Use git log to get the first commit date
        # --diff-filter=A: Select only added files
        cmd = [
            "git",
            "log",
            "--diff-filter=A",
            "--format=%cd",
            "--date=format:%Y-%m-%d",
            str(file_path),
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=REPO_ROOT, check=False
        )
        # The output might contain multiple lines if the file was added multiple times (e.g. deleted and re-added)
        # We take the last line which corresponds to the oldest commit in the log output?
        # Wait, git log outputs in reverse chronological order (newest first).
        # So the last line is the oldest commit.
        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().splitlines()
            if lines:
                return lines[-1]
    except Exception:
        pass
    return ""


def build_page(src_md: Path, out_html: Path, site_url: str = "") -> Page | None:
    post = frontmatter.load(src_md)
    if post.get("draft") is True:
        return None
    body_md = post.content or src_md.read_text(encoding="utf-8")
    title = post.get("title") or extract_title_from_text(body_md)
    date = post.get("date", "")
    # 如果日期是 datetime 对象，转换为字符串
    if hasattr(date, 'strftime'):
        date = date.strftime('%Y-%m-%d')
    elif date:
        date = str(date)
    
    # 如果没有日期，尝试从 git 获取创建日期
    if not date:
        date = get_git_creation_date(src_md)

    # 获取最后修改时间
    last_modified = get_git_last_modified(src_md)

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
    html = enhance_media_html(html)
    base = rel_base(out_html)
    # description
    description = extract_description_from_html(html)
    # canonical url
    rel_url = out_html.relative_to(OUT).as_posix()
    page_url = f"{site_url.rstrip('/')}/{rel_url}" if site_url else rel_url
    # optional featured image
    image = str(post.get("image", "")) if post.get("image") else ""
    return Page(
        src=src_md,
        out=out_html,
        title=title,
        html=html,
        toc=toc,
        base=base,
        date=date,
        last_modified=last_modified,
        tags=tags,
        categories=categories,
        description=description,
        url=page_url,
        image=image,
    )


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


def generate_breadcrumbs(page: Page) -> str:
    """Generate breadcrumb navigation HTML based on folder structure."""
    if page.out.name == "index.html":
        return ""

    # Base: Home
    crumbs = [("首页", page.base + "index.html")]

    # Middle: Folders
    try:
        # Calculate relative path from source root
        rel_path = page.src.relative_to(SRC)
        # Get parent folders (excluding filename)
        folder_parts = rel_path.parent.parts
        
        for part in folder_parts:
            # Skip 'posts' folder as it's the content root
            if part == "posts":
                continue
            # Add folder name as text (no link as folders don't have index pages)
            crumbs.append((part, ""))
    except Exception:
        pass
    
    # Current page
    crumbs.append((page.title, ""))

    # Render HTML
    html = '<nav class="breadcrumbs" aria-label="面包屑导航"><ol>'
    for i, (name, link) in enumerate(crumbs):
        is_last = (i == len(crumbs) - 1)
        if is_last:
            html += f'<li class="breadcrumb-item active" aria-current="page">{name}</li>'
        else:
            if link:
                html += f'<li class="breadcrumb-item"><a href="{link}">{name}</a></li>'
            else:
                html += f'<li class="breadcrumb-item">{name}</li>'
    html += '</ol></nav>'
    return html


def write_page(page: Page, github_url: str, owner: str, sidebar_html: str):
    # 构建元信息区块 HTML（仅当存在任意一项时渲染）
    meta_parts: list[str] = []
    
    # 1. 创建时间
    if page.date:
        meta_parts.append(f'<span class="meta-item meta-date" title="发布时间">📅发布时间: {page.date}</span>')
        
    # 2. 最后修改
    if page.last_modified:
        meta_parts.append(f'<span class="meta-item meta-date" title="最后修改">📝最后修改: {page.last_modified}</span>')

    # 3. 分类
    if page.categories:
        cats = "".join(f'<span class="badge badge-cat">{c}</span>' for c in page.categories or [])
        if cats:
            meta_parts.append(f'<span class="meta-item" title="分类">📂 {cats}</span>')
            
    # 4. 标签
    if page.tags:
        tgs = "".join(f'<span class="badge badge-tag">{t}</span>' for t in page.tags or [])
        if tgs:
            meta_parts.append(f'<span class="meta-item" title="标签">🏷️ {tgs}</span>')

    meta_html = ""
    if meta_parts:
        meta_html = '<div class="post-meta" aria-label="文章元信息">' + "".join(meta_parts) + "</div>"
    # SEO head block (meta/og/twitter/canonical/json-ld)
    seo_parts: list[str] = []
    if page.description:
        seo_parts.append(f'<meta name="description" content="{page.description}" />')
    if page.url:
        seo_parts.append(f'<link rel="canonical" href="{page.url}" />')
        # Open Graph
        seo_parts.append(f'<meta property="og:title" content="{page.title}" />')
        seo_parts.append(f'<meta property="og:description" content="{page.description}" />')
        seo_parts.append(f'<meta property="og:type" content="article" />')
        seo_parts.append(f'<meta property="og:url" content="{page.url}" />')
        if page.image:
            img = page.image.strip()
            # make absolute
            if img.startswith("http://") or img.startswith("https://"):
                abs_img = img
            else:
                # resolve relative to page url directory
                base_url = page.url.rsplit('/', 1)[0]
                sep = '' if img.startswith('/') else '/'
                abs_img = (base_url + sep + img).replace('///', '//')
            seo_parts.append(f'<meta property="og:image" content="{abs_img}" />')
            seo_parts.append(f'<meta name="twitter:image" content="{abs_img}" />')
        # Twitter
        seo_parts.append('<meta name="twitter:card" content="summary" />')
        seo_parts.append(f'<meta name="twitter:title" content="{page.title}" />')
        seo_parts.append(f'<meta name="twitter:description" content="{page.description}" />')
        # JSON-LD Article
        pub_date_iso = ""
        try:
            if page.date:
                # assume YYYY-MM-DD
                pub_date_iso = datetime.strptime(page.date, "%Y-%m-%d").isoformat()
        except Exception:
            pub_date_iso = ""
        json_ld = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": page.title,
            "datePublished": pub_date_iso or None,
            "url": page.url,
            "keywords": ",".join(page.tags or []) or None,
            "inLanguage": "zh-CN",
        }
        # remove None values
        json_ld = {k: v for k, v in json_ld.items() if v}
        import json as _json
        seo_parts.append('<script type="application/ld+json">' + _json.dumps(json_ld, ensure_ascii=False) + '</script>')

        # Add WebSite JSON-LD on homepage for Sitelinks Search
        try:
            if page.out.name == "index.html":
                website_ld = {
                    "@context": "https://schema.org",
                    "@type": "WebSite",
                    "url": page.url.rsplit('/index.html', 1)[0],
                    "potentialAction": {
                        "@type": "SearchAction",
                        "target": page.url.rsplit('/index.html', 1)[0] + "/index.html?q={search_term_string}",
                        "query-input": "required name=search_term_string"
                    }
                }
                seo_parts.append('<script type="application/ld+json">' + _json.dumps(website_ld, ensure_ascii=False) + '</script>')
        except Exception:
            pass

    seo_head = "\n".join(seo_parts)

    breadcrumbs_html = generate_breadcrumbs(page)

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
        "seo_head": seo_head,
        "breadcrumbs": breadcrumbs_html,
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
        if rel_path in {"index.html", "categories.html", "tags.html"}:
            continue
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
        # Append each page's entry to the index (bug fix: previously appended only once outside the loop)
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


def write_sitemap(pages: list[Page], site_url: str):
    """Generate sitemap.xml in OUT.
    """
    if not site_url:
        return
    import xml.etree.ElementTree as ET
    urlset = ET.Element("urlset", attrib={"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"})
    for p in pages:
        if not p.url:
            continue
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = p.url
        if p.date:
            try:
                d = datetime.strptime(p.date, "%Y-%m-%d").date()
                ET.SubElement(url, "lastmod").text = d.isoformat()
            except Exception:
                pass
    tree = ET.ElementTree(urlset)
    (OUT / "sitemap.xml").write_text(
        ET.tostring(urlset, encoding="unicode", method="xml"), encoding="utf-8"
    )


def write_robots_txt(site_url: str):
    if not site_url:
        return
    txt = """User-agent: *
Allow: /

Sitemap: {site}/sitemap.xml
""".format(site=site_url.rstrip('/'))
    (OUT / "robots.txt").write_text(txt, encoding="utf-8")


def write_rss_feed(pages: list[Page], site_url: str, title: str = "My Blog", description: str = ""):
    """Generate a minimal RSS 2.0 feed: feed.xml"""
    if not site_url:
        return
    import email.utils as eut
    from xml.sax.saxutils import escape
    site = site_url.rstrip('/')
    items = []
    # sort by date desc when available
    def sort_key(p: Page):
        return p.date or "0000-00-00"
    for p in sorted(pages, key=sort_key, reverse=True)[:50]:
        pub_date_http = ""
        try:
            if p.date:
                dt = datetime.strptime(p.date, "%Y-%m-%d")
                pub_date_http = eut.format_datetime(dt)
        except Exception:
            pub_date_http = ""
        items.append(f"""
    <item>
      <title>{escape(p.title)}</title>
      <link>{escape(p.url)}</link>
      <guid>{escape(p.url)}</guid>
      {f'<pubDate>{pub_date_http}</pubDate>' if pub_date_http else ''}
      <description>{escape(p.description or '')}</description>
    </item>
""")
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{escape(title)}</title>
    <link>{escape(site)}</link>
    <description>{escape(description or title)}</description>
    {''.join(items)}
  </channel>
</rss>
"""
    (OUT / "feed.xml").write_text(rss, encoding="utf-8")


def write_404():
    html = """
<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>页面未找到 - 404</title>
  <meta name=\"robots\" content=\"noindex\" />
</head>
<body>
  <h1>404 - 页面未找到</h1>
  <p>你访问的页面不存在。请返回 <a href=\"/index.html\">首页</a>。</p>
</body>
</html>
"""
    (OUT / "404.html").write_text(html, encoding="utf-8")


def main():
    clean_outdir()
    copy_static()
    gh_repo = os.getenv("GITHUB_REPOSITORY", "")
    github_url = f"https://github.com/{gh_repo}" if gh_repo else "#"
    owner = os.getenv("GITHUB_REPOSITORY_OWNER") or os.getenv("USERNAME") or os.getenv("USER") or "Your Name"

    # site url inference, allow override via env SITE_URL
    site_url = os.getenv("SITE_URL", "").strip()
    if not site_url:
        # If deploying to wardenxyz.github.io, the site root is https://wardenxyz.github.io
        repo_url_env = os.getenv("TARGET_PAGES_REPO", "wardenxyz/wardenxyz.github.io")
        # prefer explicit owner from env
        pages_owner = os.getenv("PAGES_OWNER") or (gh_repo.split("/")[0] if gh_repo else "wardenxyz")
        site_url = f"https://{pages_owner}.github.io"

    root_pages = [
        (SRC / "README.md", OUT / "index.html"),
        (SRC / "categories.md", OUT / "categories.html"),
        (SRC / "tags.md", OUT / "tags.html"),
    ]
    built_pages: list[Page] = []
    for src_md, out_html in root_pages:
        if src_md.exists():
            page = build_page(src_md, out_html, site_url)
            if page:
                built_pages.append(page)

    posts_dir = SRC / "posts"
    count_posts = 0
    if posts_dir.exists():
        for md in iter_markdown_files(posts_dir):
            rel = md.relative_to(SRC)
            out_html = OUT / rel.with_suffix(".html")
            page = build_page(md, out_html, site_url)
            if page:
                built_pages.append(page)
                count_posts += 1
        copy_post_assets(posts_dir)

    for p in built_pages:
        sidebar = generate_sidebar([bp for bp in built_pages if bp.src.as_posix().endswith('.md')], p)
        write_page(p, github_url, owner, sidebar)

    # write search index after all pages are built
    write_search_index(built_pages)

    # SEO artifacts
    write_sitemap(built_pages, site_url)
    write_robots_txt(site_url)
    # Feed title: use owner for now
    write_rss_feed(built_pages, site_url, title=f"{owner} Blog", description="技术与笔记")
    write_404()

    print(f"Built pages: {len([p for p in [rp[0] for rp in root_pages] if p.exists()])}, posts: {count_posts}")


if __name__ == "__main__":
    main()
