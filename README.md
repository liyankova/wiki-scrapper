# WikiScrapper

WikiScrapper is a CLI tool to scrape documentation and wiki pages and convert them into clean .txt or .md files suitable for LLM context.
no AI things here, this scrape just work without any weird API outthere
feed that wiki you scrape and feed it to your dumb AI

## What's it do?

- Crawls a site starting from any URL.
- Saves content as clean .txt or .md files.
- Keeps the original site's folder structure (so .../guides/auth becomes output_dir/guides/auth.md).
- Polite by default: adds a delay so you don't get IP-banned.
- Stamps each file with metadata (Source URL, date, etc.) so you (and your LLM) know where it came from.

### Big improvement refactor focuses on:
- Respecting robots.txt
- Robust network behavior (retries, timeouts)
- URL normalization & deduplication
- Safe file path generation
- Cleaner Markdown/Text output with YAML frontmatter
- Checkpointing for resume
- Optional JS-render mode using Playwright (opt-in)

## Installation

Requires Python 3.8+.

1. Clone repo:
```bash
git clone https://github.com/liyankova/wikiscrapper.git
cd wikiscrapper
```

2. Set up a virtual environment (trust me, it's good practice):
```bash
# only for macOS/linux with bash and zsh, other than that make sure to browse how to do
python -m venv venv
source venv/bin/activate
pip install -e .
```

3. (Optional) If you plan to use JS-render mode, install Playwright browsers:
```bash
# install Python package (already in dependencies if using pyproject)
pip install playwright

# install browser binaries (required)
playwright install
```

## Usage

```bash
# for knowing some of option and flag
wikiscrapper --help 

wikiscrapper run START_URL -s "article,.content" -d 1 -o ./out -v
```

Examples:
- Auto-detect selector, compact:
  wikiscrapper run https://wiki.example.com/es/get-started/ -o ./hypr -q

- Provide multiple selectors (fallback):
  wikiscrapper run https://example.com/docs -s "article,main,.content" -o ~/scrapes/dank -v

- Use Playwright to render JS-heavy sites:
  wikiscrapper run https://example-js-site --js -o ./out -v

- Start fresh and ignore checkpoint:
  wikiscrapper run https://example.com -F -o ./out -v

Debugging:
- If a page doesn't match selectors, raw HTML is saved to output/debug/*.html for inspection.
- Use -v for verbose to see per-file saved paths and debug messages.


Note: JS rendering tests will be automatically skipped if Playwright or browser binaries are not available.

## Notes & Limitations
- This tool targets static documentation pages by default. JS-heavy SPA sites may require `--js-render`.
- Playwright increases dependencies and resource usage; use only when necessary.
- Respect site Terms-of-Service and robots.txt rules.

MIT License
