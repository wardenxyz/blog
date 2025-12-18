#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Development server with live reload.
Watches for changes in posts, templates, and static files,
rebuilds the site, and refreshes the browser.
"""

import sys
from pathlib import Path
from livereload import Server

# Ensure we can import static_gen from the same directory
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.append(str(SCRIPT_DIR))

import static_gen
import subprocess

def rebuild():
    """Rebuild the site."""
    print("\nDetected changes, rebuilding site...")
    try:
        # Run static_gen.py as a subprocess to ensure we use the latest code
        subprocess.run([sys.executable, str(SCRIPT_DIR / "static_gen.py")], check=True)
        print("Rebuild complete.")
    except Exception as e:
        print(f"Rebuild failed: {e}")

def main():
    # Initial build
    rebuild()

    server = Server()

    # Watch paths
    # Repo root
    repo_root = static_gen.REPO_ROOT
    
    # Watch markdown files in root
    server.watch(str(repo_root / "*.md"), rebuild)
    
    # Watch posts directory
    server.watch(str(repo_root / "posts" / "**" / "*.md"), rebuild)
    
    # Watch templates
    server.watch(str(static_gen.TEMPLATES / "**" / "*"), rebuild)
    
    # Watch static files
    server.watch(str(static_gen.STATIC / "**" / "*"), rebuild)
    
    # Watch the generator script itself
    server.watch(str(SCRIPT_DIR / "static_gen.py"), rebuild)

    # Serve the site
    print(f"\nStarting development server at http://127.0.0.1:8000")
    print("Press Ctrl+C to stop.")
    
    server.serve(root=str(static_gen.OUT), port=8000, open_url_delay=1)

if __name__ == "__main__":
    main()
