#!/usr/bin/env python3
"""
Usage:
  python3 scripts/test_selector_generic.py "https://example.com/path" \
      --selectors ".content,main,article" --out debug.html --timeout 15

What it does:
- Fetches URL with a browser-like User-Agent.
- Saves raw HTML to --out (if provided).
- Tests a list of selectors with lxml and html.parser and prints whether each selector is found and the text length.
"""
import argparse
import requests
from bs4 import BeautifulSoup

DEFAULT_SELECTORS = [".content", "main .content", "div.content", "main", "article", ".markdown-body"]

def try_parsers(html, selectors):
    parsers = ["lxml", "html.parser"]
    results = {}
    for p in parsers:
        try:
            soup = BeautifulSoup(html, p)
        except Exception as e:
            results[p] = ("error", str(e))
            continue
        results[p] = {}
        for sel in selectors:
            node = soup.select_one(sel)
            results[p][sel] = (node is not None, len(node.get_text(strip=True)) if node is not None else 0)
    return results

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url", help="Target URL to fetch")
    ap.add_argument("--selectors", default=",".join(DEFAULT_SELECTORS),
                    help="Comma-separated selectors to try (default common ones)")
    ap.add_argument("--out", default="debug_from_requests.html",
                    help="File to save raw HTML (default debug_from_requests.html)")
    ap.add_argument("--ua", default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36")
    ap.add_argument("--timeout", type=int, default=15)
    args = ap.parse_args()

    selectors = [s.strip() for s in args.selectors.split(",") if s.strip()]
    print("Fetching:", args.url)
    r = requests.get(args.url, headers={"User-Agent": args.ua}, timeout=args.timeout)
    print("Status:", r.status_code)
    html = r.text
    print("Body length:", len(html))
    print("Saving raw HTML ->", args.out)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)

    print("Trying selectors with available parsers...")
    res = try_parsers(html, selectors)
    for parser, info in res.items():
        if isinstance(info, tuple) and info[0] == "error":
            print("Parser:", parser, "error:", info[1])
            continue
        print("Parser:", parser)
        for sel, (exists, length) in info.items():
            print(f"  {sel:25} -> found={exists}, text_len={length}")
    print("\nIf selectors are found here but scrapper still skips, re-run scrapper with --verbose and check the saved debug HTML in the scrapper output debug/ folder.")
if __name__ == "__main__":
    main()
