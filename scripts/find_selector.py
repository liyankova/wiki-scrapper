#!/usr/bin/env python3
"""
Usage:
  python3 scripts/find_selector_generic.py debug_from_requests.html

What it does:
- Loads HTML file (or URL if you pass http(s)://...).
- Finds large text-bearing elements (article, main, section, div).
- Prints element path, classes, and a short text sample to help pick a selector.
"""
import sys
import requests
from bs4 import BeautifulSoup

def element_path(el):
    parts = []
    while el and el.name:
        part = el.name
        if el.get("id"):
            part += f"#{el.get('id')}"
        elif el.get("class"):
            part += "." + ".".join(el.get("class")[:2])
        parts.append(part)
        el = el.parent
    return " > ".join(reversed(parts))

def find_candidates(html_text, top_n=20):
    soup = BeautifulSoup(html_text, "html.parser")
    candidates = []
    tags = ["article", "main", "div", "section"]
    for tag in tags:
        for el in soup.find_all(tag):
            text = el.get_text(separator=" ", strip=True)
            length = len(text)
            if length > 50:
                candidates.append((length, el))
    candidates.sort(reverse=True, key=lambda x: x[0])
    return candidates[:top_n]

def main():
    if len(sys.argv) < 2:
        print("Usage: find_selector_generic.py <html-file-or-url>")
        sys.exit(2)
    src = sys.argv[1]
    if src.startswith("http://") or src.startswith("https://"):
        r = requests.get(src, timeout=15, headers={"User-Agent":"Mozilla/5.0"})
        html = r.text
    else:
        html = open(src, "r", encoding="utf-8").read()
    candidates = find_candidates(html)
    for l, el in candidates:
        print(f"len={l}  path: {element_path(el)[:200]}")
        cls = el.get("class")
        if cls:
            print("  classes:", cls)
        print("  sample:", el.get_text()[:200].replace('\\n',' ').strip())
        print("-" * 60)

if __name__ == "__main__":
    main()
