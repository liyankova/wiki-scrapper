import time
from datetime import datetime
from collections import deque
from urllib.parse import urlparse
from rich.console import Console
from pathlib import Path
import re

from .fetcher import make_session, fetch
from .robots import RobotsCache
from .utils import normalize_url, is_same_domain, url_to_filepath, ensure_relative_link, detect_best_selector
from .formatter import html_to_markdown, html_to_text, make_frontmatter
from .storage import save_checkpoint, load_checkpoint
from bs4 import BeautifulSoup
import requests

console = Console()

def _choose_parser():
    try:
        import lxml
        return "lxml"
    except Exception:
        return "html.parser"

def _slugify(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9\-_\.]", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    return s.strip("-")[:120] or "page"

def run_scrape(
    start_url: str,
    output_dir: str,
    selector: str = None,
    max_depth: int = 1,
    user_agent: str = None,
    delay: float = 1.0,
    file_format: str = "txt",
    same_host: bool = True,
    max_pages: int = 0,
    checkpoint_path: str = "wikiscrapper-checkpoint.json",
    js_render: bool = False,
    ignore_checkpoint: bool = False,
    quiet: bool = False,
    verbose: bool = False,
    no_robots: bool = False,  # <-- new param to ignore robots.txt when True
):
    session = make_session()
    headers = {"User-Agent": user_agent or "wikiscrapper/0.2 (+https://github.com/liyankova/wiki-scrapper)"}
    robots = RobotsCache()
    parser = _choose_parser()

    start_norm = normalize_url(start_url)
    base_domain = urlparse(start_url).netloc

    visited, queue = (set(), [])
    if not ignore_checkpoint:
        visited, queue = load_checkpoint(checkpoint_path)
        if visited or queue:
            console.print(f"[yellow]Resuming from checkpoint:[/yellow] visited={len(visited)}, queued={len(queue)}")

    if not visited and not queue:
        queue = deque([(start_norm, 0)])
        visited = set()
    else:
        queue = deque(queue)

    pages_saved = 0
    pages_fetched = 0
    skipped = 0

    # Prepare selectors: either user-provided (comma-separated) or None (auto)
    if selector:
        selectors = [s.strip() for s in selector.split(",") if s.strip()]
    else:
        selectors = None  # will auto-detect on first page

    def print_summary(newline=False):
        summary = f"Fetched: {pages_fetched}  Saved: {pages_saved}  Skipped: {skipped}  Queue: {len(queue)}"
        end_char = "\n" if newline else "\r"
        if quiet:
            console.print(summary, end=end_char)
        else:
            console.print(summary, end=end_char)

    print_summary()

    auto_detected_once = False
    # If user explicitly passed no_robots, show a subtle confirmation in verbose
    if no_robots and verbose:
        console.print("[yellow]Note: robots.txt checks are disabled for this run (--no-robots).[/yellow]")

    while queue:
        current, depth = queue.popleft()
        if current in visited:
            continue
        if max_depth is not None and depth > max_depth:
            continue
        if max_pages and pages_saved >= max_pages:
            if verbose:
                console.print("[yellow]Reached max-pages limit.[/yellow]")
            break

        # robots check (skippable with no_robots)
        if not no_robots:
            if not robots.allowed(headers.get("User-Agent", "*"), current):
                if verbose:
                    console.print(f"[yellow]Skipping (robots): {current}[/yellow]")
                visited.add(current)
                print_summary()
                continue
        else:
            # when ignoring robots, we may optionally log minimally if verbose
            if verbose:
                console.print(f"[yellow]Ignoring robots.txt for: {current}[/yellow]")

        pages_fetched += 1
        if verbose:
            console.print(f"[{depth}/{max_depth}] Fetching: {current}")

        # fetch (with optional js renderer)
        try:
            if js_render:
                try:
                    from .renderer import render_page
                except Exception as re_imp:
                    console.print(f"[red]Playwright renderer import failed:[/red] {re_imp} — falling back to simple fetch.")
                    resp = fetch(session, current, headers)
                else:
                    try:
                        timeout_ms = int(getattr(session, "request_timeout", 10) * 1000)
                        html = render_page(current, timeout=timeout_ms, user_agent=headers.get("User-Agent"))
                        class DummyResp:
                            def __init__(self, content):
                                self.content = content.encode("utf-8")
                        resp = DummyResp(html)
                    except RuntimeError as re:
                        console.print(f"[red]JS render failed:[/red] {re} — falling back to simple fetch.")
                        resp = fetch(session, current, headers)
            else:
                resp = fetch(session, current, headers)
        except requests.RequestException as e:
            if verbose:
                console.print(f"[red]Request failed:[/red] {e} (url={current})")
            visited.add(current)
            print_summary()
            time.sleep(delay)
            continue

        # parse HTML
        try:
            soup = BeautifulSoup(resp.content, parser)
        except Exception:
            soup = BeautifulSoup(resp.content, "html.parser")

        # if selectors not set, auto-detect from first page
        if selectors is None and not auto_detected_once:
            candidates = detect_best_selector(resp.content.decode("utf-8", errors="ignore"))
            selectors = candidates if candidates else ["main", "article", "div.content"]
            auto_detected_once = True
            if verbose:
                console.print(f"[blue]Auto-detected selectors:[/blue] {selectors}")

        # try selectors in order
        content_node = None
        used_sel = None
        for sel in selectors:
            node = soup.select_one(sel)
            if node:
                content_node = node
                used_sel = sel
                break

        if content_node is None:
            skipped += 1
            # save debug HTML
            try:
                debug_dir = Path(output_dir) / "debug"
                debug_dir.mkdir(parents=True, exist_ok=True)
                fn = debug_dir / f"{_slugify(urlparse(current).netloc + urlparse(current).path)}.html"
                with fn.open("wb") as fh:
                    fh.write(resp.content)
                if verbose:
                    console.print(f"[yellow]No selector match on {current}; saved debug: {fn}[/yellow]")
            except Exception as e:
                if verbose:
                    console.print(f"[red]Failed saving debug HTML:[/red] {e}")
            visited.add(current)
            print_summary()
            time.sleep(delay)
            continue

        # build output content
        title = soup.title.string.strip() if soup.title and soup.title.string else "Scraped Page"
        front = make_frontmatter(current, title, used_sel or selectors[0])
        if file_format == "md":
            body = html_to_markdown(content_node)
            final = front + "# " + title + "\n\n" + body
        else:
            body = html_to_text(content_node)
            final = front + body

        filepath = url_to_filepath(output_dir, current, file_format)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(final)
            pages_saved += 1
            if verbose:
                console.print(f"[green]Saved:[/green] {filepath}")
            else:
                # compact feedback
                console.print(f"[green]Saved {pages_saved}[/green]", end="\r")
        except Exception as e:
            console.print(f"[red]Failed to write file:[/red] {e}")

        visited.add(current)
        print_summary()
        time.sleep(delay)

        # enqueue links
        if depth < max_depth:
            for a in soup.find_all("a", href=True):
                href = a["href"].strip()
                if href.startswith(("mailto:", "tel:", "javascript:")):
                    continue
                next_url = ensure_relative_link(current, href)
                next_norm = normalize_url(next_url)
                if next_norm in visited:
                    continue
                if same_host and not is_same_domain(next_norm, base_domain):
                    continue
                queue.append((next_norm, depth + 1))

        # checkpoint save
        if pages_saved % 10 == 0:
            save_checkpoint(checkpoint_path, visited, list(queue))

    # final checkpoint + summary
    save_checkpoint(checkpoint_path, visited, list(queue))
    print_summary(newline=True)
    console.print(f"[bold green]Done. Fetched: {pages_fetched}, Saved: {pages_saved}, Skipped: {skipped}[/bold green]")
