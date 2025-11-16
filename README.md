# WikiScrapper

WikiScrapper is a CLI tool to scrape documentation and wiki pages and convert them into clean .txt or .md files suitable for LLM context.
no AI things here, this scrape just work without any weird API outthere
feed that wiki you scrape and feed it to your dumb AI

This refactor focuses on:
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

2. Install in editable mode:
```bash
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
- Use --verbose to see per-file saved paths and debug messages.


## Local testing

Basic tests are included under `tests/`. To run tests:

1. Install test deps (pytest is not required as dependency, install separately if needed):
```bash
pip install pytest
```

2. If you want to run JS-render tests, ensure Playwright and browsers are installed:
```bash
pip install playwright
playwright install
```

3. Run tests:
```bash
pytest -q
```

Note: JS rendering tests will be automatically skipped if Playwright or browser binaries are not available.

## Notes & Limitations
- This tool targets static documentation pages by default. JS-heavy SPA sites may require `--js-render`.
- Playwright increases dependencies and resource usage; use only when necessary.
- Respect site Terms-of-Service and robots.txt rules.

MIT License
