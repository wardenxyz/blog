#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Static website generator for Markdown blog
"""

import os
import re
import shutil
import yaml
import json
import markdown
import datetime
from pathlib import Path
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension
from collections import defaultdict

# Configuration
SITE_TITLE = "随便写写"
SITE_DESCRIPTION = "A minimalist blog that uses pure markdown files"
SOURCE_DIR = Path(".")
OUTPUT_DIR = Path("site")
POSTS_DIR = Path("posts")
ASSETS_DIR = Path("assets")
CSS_FILE = "styles.css"
README_FILE = Path("README.md")  # 添加README文件路径配置

def extract_front_matter(content):
    """Extract front matter from markdown content."""
    front_matter = {}
    content_text = content

    # Check if the content starts with front matter
    if content.startswith('---'):
        end_index = content.find('---', 3)
        if end_index != -1:
            front_matter_text = content[3:end_index].strip()
            try:
                front_matter = yaml.safe_load(front_matter_text)
                content_text = content[end_index+3:].strip()
            except yaml.YAMLError:
                print("Error parsing front matter")

    return front_matter, content_text

def parse_markdown_file(file_path):
    """Parse a markdown file and return its front matter and HTML content."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    front_matter, content_text = extract_front_matter(content)

    # Process Mermaid diagrams - replace ```mermaid blocks with <div class="mermaid">
    content_text = re.sub(
        r'```mermaid\s*([\s\S]*?)```',
        r'<div class="mermaid">\1</div>',
        content_text
    )

    # 1. 先保护大代码块（三个反引号包裹的代码）
    code_blocks = []
    
    # Capture code blocks (```...```)
    def code_block_replace(match):
        lang = match.group(1).strip() if match.group(1) else ''
        code_content = match.group(2)
        code_blocks.append((lang, code_content))
        return f"CODE_BLOCK_PLACEHOLDER_{len(code_blocks) - 1}_"
    
    # 使用非贪婪匹配来避免匹配过多内容
    content_text = re.sub(r'```([^\n]*)\n([\s\S]*?)```', code_block_replace, content_text)

    # 2. 然后处理行内代码（单个反引号）
    inline_code = []
    
    # Capture inline code expressions (`...`)
    def inline_code_replace(match):
        inline_code.append(match.group(1))
        return f"INLINE_CODE_PLACEHOLDER_{len(inline_code) - 1}_"
    
    # 使用负向前视和负向后视断言确保不会匹配位于代码块内的反引号
    content_text = re.sub(r'(?<!`)`([^`]+?)`(?!`)', inline_code_replace, content_text)

    # 3. 最后保护数学表达式
    # Store all math expressions temporarily and replace with placeholders
    inline_math = []
    display_math = []

    # Capture inline math expressions ($...$)
    def inline_math_replace(match):
        inline_math.append(match.group(1))
        return f"INLINE_MATH_PLACEHOLDER_{len(inline_math) - 1}_"

    content_text = re.sub(r'\$([^\$]+?)\$', inline_math_replace, content_text)

    # Capture display math expressions ($$...$$)
    def display_math_replace(match):
        display_math.append(match.group(1))
        return f"DISPLAY_MATH_PLACEHOLDER_{len(display_math) - 1}_"

    content_text = re.sub(r'\$\$([^\$]+?)\$\$', display_math_replace, content_text)

    # Convert markdown to HTML
    html_content = markdown.markdown(
        content_text,
        extensions=[
            FencedCodeExtension(),
            TableExtension(),
            'nl2br',
            TocExtension(title='目录', permalink=True),
            'sane_lists'
        ]
    )

    # 1. 首先恢复代码块
    for i, (lang, code) in enumerate(code_blocks):
        code_html = f'<pre><code class="language-{lang}">{code}</code></pre>' if lang else f'<pre><code>{code}</code></pre>'
        html_content = html_content.replace(
            f"CODE_BLOCK_PLACEHOLDER_{i}_",
            code_html
        )

    # 2. 再恢复行内代码
    for i, code in enumerate(inline_code):
        html_content = html_content.replace(
            f"INLINE_CODE_PLACEHOLDER_{i}_",
            f"<code>{code}</code>"
        )

    # 3. 最后恢复数学表达式
    # Restore inline math expressions
    for i, math in enumerate(inline_math):
        html_content = html_content.replace(
            f"INLINE_MATH_PLACEHOLDER_{i}_",
            f"${math}$"
        )

    # Restore display math expressions
    for i, math in enumerate(display_math):
        html_content = html_content.replace(
            f"DISPLAY_MATH_PLACEHOLDER_{i}_",
            f"$${math}$$"
        )

    return front_matter, html_content

def generate_post_page(post_path, output_path, template):
    """Generate a HTML page for a post."""
    front_matter, html_content = parse_markdown_file(post_path)

    # Get metadata
    title = front_matter.get('title', os.path.basename(post_path).replace('.md', ''))
    date = front_matter.get('date', 'Unknown date')
    tags = front_matter.get('tags', [])
    category = front_matter.get('category', [])

    # Format date if it's a date object
    if isinstance(date, datetime.date):
        date = date.strftime('%Y-%m-%d')

    # Generate HTML
    html_output = template.replace('{{title}}', title)
    html_output = html_output.replace('{{date}}', str(date))
    html_output = html_output.replace('{{content}}', html_content)

    # Generate tags HTML
    tags_html = ''
    if tags:
        tags_html = '<div class="tags">标签: '
        tags_html += ', '.join(f'<a href="/tags.html#{tag}">{tag}</a>' for tag in tags)
        tags_html += '</div>'
    html_output = html_output.replace('{{tags}}', tags_html)

    # Generate category HTML
    category_html = ''
    if category:
        if isinstance(category, list):
            category_html = '<div class="category">分类: '
            category_html += ', '.join(f'<a href="/categories.html#{cat}">{cat}</a>' for cat in category)
            category_html += '</div>'
        else:
            category_html = f'<div class="category">分类: <a href="/categories.html#{category}">{category}</a></div>'
    html_output = html_output.replace('{{category}}', category_html)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write HTML to file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(html_output)

    # Return the HTML content for search index
    return html_content

def generate_index_page(posts_data, template):
    """Generate the main index page."""
    # Sort posts by date (newest first)
    sorted_posts = sorted(posts_data, key=lambda x: x['date'] if x['date'] != 'Unknown date' else '', reverse=True)

    # Group posts by year and month
    posts_by_year_month = defaultdict(lambda: defaultdict(list))

    for post in sorted_posts:
        if post['date'] != 'Unknown date' and isinstance(post['date'], str):
            try:
                date_obj = datetime.datetime.strptime(post['date'], '%Y-%m-%d')
                year = date_obj.year
                month = date_obj.month
                posts_by_year_month[year][month].append(post)
            except ValueError:
                posts_by_year_month['Unknown']['Unknown'].append(post)
        else:
            posts_by_year_month['Unknown']['Unknown'].append(post)

    # Generate HTML content for posts list
    content = '<h1>博客文章</h1>'

    # Process posts by year and month
    for year in sorted(posts_by_year_month.keys(), reverse=True):
        content += f'<h2>{year} 年</h2>'

        for month in sorted(posts_by_year_month[year].keys(), reverse=True):
            if month != 'Unknown':
                content += f'<h3>{month} 月</h3>'
            else:
                content += '<h3>日期未知</h3>'

            content += '<ul>'
            for post in posts_by_year_month[year][month]:
                content += f'<li><a href="{post["url"]}">{post["title"]}</a>'
                if post['date'] != 'Unknown date':
                    content += f' <span class="date">({post["date"]})</span>'
                content += '</li>'
            content += '</ul>'

    # Replace placeholders in the template
    html_output = template.replace('{{title}}', SITE_TITLE)
    html_output = html_output.replace('{{content}}', content)
    html_output = html_output.replace('{{date}}', '')
    html_output = html_output.replace('{{tags}}', '')
    html_output = html_output.replace('{{category}}', '')

    # Write HTML to file
    with open(OUTPUT_DIR / 'index.html', 'w', encoding='utf-8') as file:
        file.write(html_output)

def generate_tag_page(posts_data, template):
    """Generate the tags page."""
    # Group posts by tag
    posts_by_tag = defaultdict(list)

    for post in posts_data:
        for tag in post.get('tags', []):
            posts_by_tag[tag].append(post)

    # Sort tags alphabetically
    sorted_tags = sorted(posts_by_tag.keys())

    # Generate HTML content
    content = '<h1>标签</h1>'

    # Add a list of all tags at the top
    content += '<div class="tag-list">'
    for tag in sorted_tags:
        content += f'<a href="#tag-{tag}" class="tag-link">{tag}</a> '
    content += '</div>'

    # Add posts grouped by tag
    for tag in sorted_tags:
        content += f'<h2 id="tag-{tag}">{tag}</h2>'
        content += '<ul>'

        # Sort posts within each tag by date (newest first)
        sorted_posts = sorted(
            posts_by_tag[tag],
            key=lambda x: x['date'] if x['date'] != 'Unknown date' else '',
            reverse=True
        )

        for post in sorted_posts:
            content += f'<li><a href="{post["url"]}">{post["title"]}</a>'
            if post['date'] != 'Unknown date':
                content += f' <span class="date">({post["date"]})</span>'
            content += '</li>'

        content += '</ul>'

    # Replace placeholders in the template
    html_output = template.replace('{{title}}', 'Tags - ' + SITE_TITLE)
    html_output = html_output.replace('{{content}}', content)
    html_output = html_output.replace('{{date}}', '')
    html_output = html_output.replace('{{tags}}', '')
    html_output = html_output.replace('{{category}}', '')

    # Write HTML to file
    with open(OUTPUT_DIR / 'tags.html', 'w', encoding='utf-8') as file:
        file.write(html_output)

def generate_category_page(posts_data, template):
    """Generate the categories page."""
    # Group posts by category
    posts_by_category = defaultdict(list)

    for post in posts_data:
        categories = post.get('category', [])
        if not categories:
            continue

        if isinstance(categories, list):
            for category in categories:
                posts_by_category[category].append(post)
        else:
            posts_by_category[categories].append(post)

    # Sort categories alphabetically
    sorted_categories = sorted(posts_by_category.keys())

    # Generate HTML content
    content = '<h1>分类</h1>'

    # Add a list of all categories at the top
    content += '<div class="category-list">'
    for category in sorted_categories:
        content += f'<a href="#cat-{category}" class="category-link">{category}</a> '
    content += '</div>'

    # Add posts grouped by category
    for category in sorted_categories:
        content += f'<h2 id="cat-{category}">{category}</h2>'
        content += '<ul>'

        # Sort posts within each category by date (newest first)
        sorted_posts = sorted(
            posts_by_category[category],
            key=lambda x: x['date'] if x['date'] != 'Unknown date' else '',
            reverse=True
        )

        for post in sorted_posts:
            content += f'<li><a href="{post["url"]}">{post["title"]}</a>'
            if post['date'] != 'Unknown date':
                content += f' <span class="date">({post["date"]})</span>'
            content += '</li>'

        content += '</ul>'

    # Replace placeholders in the template
    html_output = template.replace('{{title}}', 'Categories - ' + SITE_TITLE)
    html_output = html_output.replace('{{content}}', content)
    html_output = html_output.replace('{{date}}', '')
    html_output = html_output.replace('{{tags}}', '')
    html_output = html_output.replace('{{category}}', '')

    # Write HTML to file
    with open(OUTPUT_DIR / 'categories.html', 'w', encoding='utf-8') as file:
        file.write(html_output)

def generate_search_page(template):
    """Generate the search page."""
    # Generate HTML content
    content = '''
    <h1>搜索</h1>
    <div class="search-container">
        <input type="text" id="search-input" class="search-input" placeholder="请输入搜索内容..." aria-label="搜索">
        <div id="loading-indicator" style="display: none; text-align: center; margin: 20px 0;">正在加载搜索数据...</div>
        <div class="search-keyboard-help">
            <small>键盘导航: 使用 <kbd>↑</kbd> <kbd>↓</kbd> 键选择结果, <kbd>Enter</kbd> 打开选中结果, <kbd>Esc</kbd> 返回搜索框</small>
        </div>
    </div>
    <div id="search-results" class="search-results"></div>
    <script src="/assets/search.js"></script>
    '''

    # Replace placeholders in the template
    html_output = template.replace('{{title}}', '搜索 - ' + SITE_TITLE)
    html_output = html_output.replace('{{content}}', content)
    html_output = html_output.replace('{{date}}', '')
    html_output = html_output.replace('{{tags}}', '')
    html_output = html_output.replace('{{category}}', '')

    # Write HTML to file
    with open(OUTPUT_DIR / 'search.html', 'w', encoding='utf-8') as file:
        file.write(html_output)

def generate_search_index(posts_data):
    """Generate a JSON search index file containing all posts' data."""
    search_index = []

    for post in posts_data:
        # Extract the plain content from the HTML content
        if 'content_html' in post:
            # Create a simplified version of the content for search purposes
            # Strip HTML tags but keep the text content
            plain_content = re.sub(r'<[^>]+>', ' ', post['content_html'])
            # Normalize whitespace
            plain_content = re.sub(r'\s+', ' ', plain_content).strip()

            # Format date if it's a date object to make it JSON serializable
            date = post['date']
            if isinstance(date, datetime.date):
                date = date.strftime('%Y-%m-%d')

            search_item = {
                'title': post['title'],
                'url': post['url'],
                'content': plain_content[:10000],  # Limit content length to avoid very large JSON
                'date': date,
                'tags': post.get('tags', []),
                'category': post.get('category', [])
            }
            search_index.append(search_item)

    # Write search index to JSON file
    with open(OUTPUT_DIR / 'search-index.json', 'w', encoding='utf-8') as file:
        json.dump(search_index, file, ensure_ascii=False, indent=2)

def copy_assets():
    """Copy assets to the output directory."""
    assets_src = SOURCE_DIR / ASSETS_DIR
    assets_dest = OUTPUT_DIR / ASSETS_DIR

    # Create assets directory if it doesn't exist
    if not assets_src.exists():
        assets_src.mkdir(parents=True)

    # Copy assets directory if it exists
    if assets_src.exists():
        if assets_dest.exists():
            shutil.rmtree(assets_dest)
        shutil.copytree(assets_src, assets_dest)

def create_assets():
    """Create necessary asset files if they don't exist."""
    assets_dir = SOURCE_DIR / ASSETS_DIR

    # Create assets directory if it doesn't exist
    if not assets_dir.exists():
        assets_dir.mkdir(parents=True)

    # Create CSS file if it doesn't exist
    css_file = assets_dir / CSS_FILE

def generate_readme_index_page(template):
    """Generate the main index page from README.md."""
    # Check if README.md exists
    if not (SOURCE_DIR / README_FILE).exists():
        print(f"Warning: {README_FILE} not found, falling back to generated index.")
        return False

    # Parse README.md
    front_matter, html_content = parse_markdown_file(SOURCE_DIR / README_FILE)

    # Process links in the HTML content to make them work in the static site
    # Convert relative links like [title](posts/2024/file.md) to [title](/posts/2024/file.html)
    html_content = re.sub(
        r'href="posts/(\d{4})/([^"]+)\.md"',
        r'href="/posts/\1/\2.html"',
        html_content
    )
    html_content = re.sub(
        r'href=\'posts/(\d{4})/([^\']+)\.md\'',
        r'href="/posts/\1/\2.html"',
        html_content
    )

    # Fix category and tags links
    html_content = re.sub(r'href="categories\.md"', r'href="/categories.html"', html_content)
    html_content = re.sub(r'href="tags\.md"', r'href="/tags.html"', html_content)

    # Replace placeholders in the template
    html_output = template.replace('{{title}}', SITE_TITLE)
    html_output = html_output.replace('{{content}}', html_content)
    html_output = html_output.replace('{{date}}', '')
    html_output = html_output.replace('{{tags}}', '')
    html_output = html_output.replace('{{category}}', '')

    # Write HTML to file
    with open(OUTPUT_DIR / 'index.html', 'w', encoding='utf-8') as file:
        file.write(html_output)

    return True

def main():
    """Generate the static website."""
    # Create output directory if it doesn't exist
    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir(parents=True)

    # Create necessary asset files
    create_assets()

    # Copy assets to output directory
    copy_assets()

    # Read the HTML template
    template_path = SOURCE_DIR / ".github/scripts/template.html"

    with open(template_path, 'r', encoding='utf-8') as file:
        template = file.read()

    # Find markdown files
    posts_data = []
    for year_dir in (SOURCE_DIR / POSTS_DIR).iterdir():
        if year_dir.is_dir() and re.match(r'^\d{4}$', year_dir.name):
            for post_file in year_dir.glob('*.md'):
                if post_file.is_file():
                    # Parse markdown file
                    front_matter, html_content = parse_markdown_file(post_file)

                    # Get metadata
                    title = front_matter.get('title', post_file.stem)
                    date = front_matter.get('date', 'Unknown date')
                    tags = front_matter.get('tags', [])
                    category = front_matter.get('category', [])

                    # Compute relative URL
                    rel_path = post_file.relative_to(SOURCE_DIR)
                    url = f"/{rel_path.with_suffix('.html')}"

                    # Compute output path
                    output_path = OUTPUT_DIR / rel_path.with_suffix('.html')

                    # Generate HTML
                    post_html_content = generate_post_page(post_file, output_path, template)

                    # Add to posts data
                    posts_data.append({
                        'title': title,
                        'date': date,
                        'tags': tags,
                        'category': category,
                        'url': url,
                        'content_html': post_html_content  # Store HTML content for search index
                    })

    # Generate index page from README.md
    readme_success = generate_readme_index_page(template)

    # Fall back to the original index generation if README processing failed
    if not readme_success:
        generate_index_page(posts_data, template)

    # Generate tags page
    generate_tag_page(posts_data, template)

    # Generate categories page
    generate_category_page(posts_data, template)

    # Generate search page
    generate_search_page(template)

    # Generate search index
    generate_search_index(posts_data)

if __name__ == '__main__':
    main()
    print(f"Static website generated at {OUTPUT_DIR}")
