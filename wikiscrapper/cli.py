import typer
from typing_extensions import Annotated
from rich.console import Console
from urllib.parse import urlparse
from pathlib import Path

from . import core

app = typer.Typer(name="wikiscrapper", help="Scrape documentation sites (compact CLI)", add_completion=False)
console = Console()

# Compact flags:
OptOut = Annotated[str, typer.Option("-o", "--output", help="Output directory (default: ./llm_docs)")]
OptDepth = Annotated[int, typer.Option("-d", "--depth", help="Depth (0=start only).")]
OptSelector = Annotated[str, typer.Option("-s", "--selector", help="CSS selector (comma-separated). If omitted, auto-detect.)")]
OptFormat = Annotated[str, typer.Option("-f", "--format", help="Output format: md or txt")]
OptJs = Annotated[bool, typer.Option("-j", "--js", help="Enable JS render (Playwright, opt-in)")]
OptFresh = Annotated[bool, typer.Option("-F", "--fresh", help="Ignore existing checkpoint and start fresh")]
OptQuiet = Annotated[bool, typer.Option("-q", "--quiet", help="Quiet mode (compact progress)")]
OptVerbose = Annotated[bool, typer.Option("-v", "--verbose", help="Verbose mode (show saved paths and warnings)")]
OptMode = Annotated[str, typer.Option("--mode", help="Preset mode: 'docs' (default) or 'site')")]
# Hidden/opt-in: ignore robots.txt (use responsibly). Not documented in README.
OptNoRobots = Annotated[bool, typer.Option("--no-robots", help="Ignore robots.txt (use responsibly).")]  # hidden gem (opt-in)

@app.command()
def run(
    url: Annotated[str, typer.Argument(..., metavar="START_URL")],
    output: OptOut = "llm_docs",
    depth: OptDepth = 1,
    selector: OptSelector = None,
    file_format: OptFormat = "md",
    delay: float = 1.0,
    ua: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    js: OptJs = False,
    fresh: OptFresh = False,
    quiet: OptQuiet = False,
    verbose: OptVerbose = False,
    mode: OptMode = "docs",
    checkpoint: str = "wikiscrapper-checkpoint.json",
    no_robots: OptNoRobots = False,
):
    """
    Compact CLI: fewer flags. Example:
      wikiscrapper run https://example.com/docs -s "article,.content" -d 1 -o ./out -v
    """
    if file_format not in ("md", "txt"):
        console.print("[red]--format must be 'md' or 'txt'[/red]")
        raise typer.Exit(1)

    parsed = urlparse(url)
    if not parsed.netloc:
        console.print(f"[red]Invalid URL: {url}[/red]")
        raise typer.Exit(1)

    out_path = Path(output).expanduser().resolve()
    out_path.mkdir(parents=True, exist_ok=True)

    # mode presets
    if mode not in ("docs", "site"):
        console.print(f"[yellow]Unknown mode '{mode}', defaulting to 'docs'[/yellow]")
        mode = "docs"

    # Show compact startup summary
    console.print(f"--- [green]WikiScrapper v2[/green] ---")
    console.print(f"URL: {url}  Mode: {mode}  Out: {out_path}")
    console.print(f"Selector: {selector or '(auto)'}  Depth: {depth}  Format: {file_format}  JS: {js}")
    console.print(f"Fresh: {fresh}  Checkpoint: {checkpoint}  Quiet: {quiet}  Verbose: {verbose}")
    # Keep the no-robots flag output minimal (hidden gem). Only warn if set.
    if no_robots:
        console.print("[yellow]Warning: running with --no-robots (ignoring robots.txt). Use responsibly.[/yellow]")
    console.print("-----------------------------")

    core.run_scrape(
        start_url=url,
        output_dir=str(out_path),
        selector=selector,
        max_depth=depth,
        user_agent=ua,
        delay=delay,
        file_format=file_format,
        same_host=(mode == "docs"),
        max_pages=0,
        checkpoint_path=checkpoint,
        js_render=js,
        ignore_checkpoint=fresh,
        quiet=quiet,
        verbose=verbose,
        no_robots=no_robots,
    )
