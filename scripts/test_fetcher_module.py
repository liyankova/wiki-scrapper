#!/usr/bin/env python3
"""
Test what the package's fetcher + parser sees for the target URL.
This mimics core.run_scrape network + parsing stack.
"""
from wikiscrapper.fetcher import make_session, fetch
from bs4 import BeautifulSoup
from wikiscrapper.utils import normalize_url
from urllib.parse import urlparse
import sys, re

URL = "https://wiki.hypr.land/Hypr-Ecosystem/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
SELECTOR = ".content"

def main():
    print("Using wikiscrapper.fetcher.make_session + fetch to get the page (mimics core)...")
    session = make_session()
    headers = {"User-Agent": UA}
    try:
        resp = fetch(session, URL, headers)
    except Exception as e:
        print("Fetch failed:", e)
        sys.exit(2)
    print("Fetch OK. status_code:", getattr(resp, "status_code", "N/A"))
    b = resp.content
    print("resp.content length:", len(b))
    s = None
    try:
        # try lxml first if available
        soup = BeautifulSoup(b, "lxml")
        s = soup.select_one(SELECTOR)
        parser_used = "lxml"
    except Exception as e:
        soup = BeautifulSoup(b, "html.parser")
        s = soup.select_one(SELECTOR)
        parser_used = "html.parser"

    print("Parser used (tested):", parser_used)
    print(f"Selector '{SELECTOR}' found?:", bool(s))
    if s:
        text = s.get_text(" ", strip=True)
        print("Selector text length:", len(text))
        print("Selector sample (first 300 chars):")
        print(text[:300].replace("\n", " ").strip())
    else:
        # also test regex for class presence (class attribute containing 'content')
        raw = b.decode("utf-8", errors="replace")
        found_literal = bool(re.search(r'class=["\'][^"\']*\bcontent\b[^"\']*["\']', raw))
        print("Regex class=\"...content...\" present?:", found_literal)
        # try to locate first few occurrences of the word 'Hypr Ecosystem' to show surrounding HTML
        idx = raw.find("Hypr Ecosystem")
        if idx != -1:
            start = max(0, idx-200)
            end = min(len(raw), idx+200)
            print("HTML surrounding 'Hypr Ecosystem' (snippet):")
            print(raw[start:end])
        else:
            print("Did not find 'Hypr Ecosystem' literal in HTML.")
        # save debug for inspection
        with open("hypr_debug_from_module.html", "w", encoding="utf-8") as f:
            f.write(raw)
        print("Saved debug HTML -> hypr_debug_from_module.html")

if __name__ == "__main__":
    main()
