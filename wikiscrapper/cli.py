import typer
from typing_extensions import Annotated
from rich.console import Console
from urllib.parse import urlparse
import os
from pathlib import Path
import sys

from . import core

app = typer.Typer(
    name="wikiscrapper",
    help="A professional CLI tool to scrape documentation sites for LLM context.",
    add_completion=False
)
console = Console()

OptOutput = Annotated[str, typer.Option("--output", "-o", help="Output root directory.")]
OptDepth = Annotated[int, typer.Option("--depth", "-d", help="Recursion depth (how many links deep).")]
OptSelector = Annotated[str, typer.Option("--selector", "-s", help="CSS selector for the main content.")]
OptFormat = Annotated[str, typer.Option("--format", "-f", help="Output format (txt or md).")]
OptDelay = Annotated[float, typer.Option("--delay", help="Delay (in seconds) between requests.")]
OptUserAgent = Annotated[str, typer.Option("--user-agent", help="User-Agent string for requests.")]
OptSameHost = Annotated[bool, typer.Option("--same-host/--allow-external", help="Restrict crawling to the starting host.")]
OptMaxPages = Annotated[int, typer.Option("--max-pages", help="Maximum number of pages to fetch (0 = unlimited).")]
OptCheckpoint = Annotated[str, typer.Option("--checkpoint", help="Path to checkpoint file for resume/save state.")]
OptJsRender = Annotated[bool, typer.Option("--js-render", help="Enable JS rendering (uses Playwright).", show_default=False)]
OptIgnoreCheckpoint = Annotated[bool, typer.Option("--ignore-checkpoint", help="Ignore any existing checkpoint file and start fresh.")]
OptQuiet = Annotated[bool, typer.Option("--quiet", "-q", help="Quiet mode: show only compact progress summary.")]
OptVerbose = Annotated[bool, typer.Option("--verbose", "-v", help="Verbose mode: show saved file paths and warnings.")]


def _is_inside_package_dir(path: Path) -> bool:
    """
    Return True if path is inside the installed package directory where this code resides.
    We want to avoid writing output into the package source tree by accident.
    """
    pkg_dir = Path(__file__).resolve().parents[1]  # repo/wikiscrapper
    try:
        return path.resolve().is_relative_to(pkg_dir)
    except AttributeError:
        # Python <3.9 fallback
        try:
            path.resolve().relative_to(pkg_dir)
            return True
        except Exception:
            return False


@app.command()
def scrape(
    url: Annotated[str, typer.Argument(help="The starting URL to scrape.", metavar="START_URL")],
    output: OptOutput = "llm_docs",
    depth: OptDepth = 1,
    selector: OptSelector = "main",
    file_format: OptFormat = "txt",
    delay: OptDelay = 1.0,
    user_agent: OptUserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    same_host: OptSameHost = True,
    max_pages: OptMaxPages = 0,
    checkpoint: OptCheckpoint = "wikiscrapper-checkpoint.json",
    js_render: OptJsRender = False,
    ignore_checkpoint: OptIgnoreCheckpoint = False,
    quiet: OptQuiet = False,
    verbose: OptVerbose = False,
):
    if file_format not in ['txt', 'md']:
        console.print(f"[bold red]Error:[/bold red] --format must be 'txt' or 'md'.")
        raise typer.Exit(code=1)

    parsed = urlparse(url)
    base_domain = parsed.netloc
    if not base_domain:
        console.print(f"[bold red]Error:[/bold red] Invalid URL provided: {url}")
        raise typer.Exit(code=1)

    # Resolve output dir to absolute path
    out_path = Path(output).expanduser().resolve()
    # Warn if output dir is inside package source directory
    if _is_inside_package_dir(out_path):
        console.print("[bold yellow]Warning:[/bold yellow] The output directory appears to be inside the package source directory.")
        console.print("This can interfere with pip/setuptools or be accidentally committed. Please choose a directory outside the project.")
        console.print(f"Suggested: use './{out_path.name}' outside the package or an absolute path like '/tmp/{out_path.name}'.")
        console.print("Use --output to specify a different location, or rerun with --force to continue (not implemented).")
        raise typer.Exit(code=2)

    out_path.mkdir(parents=True, exist_ok=True)

    console.print(f"--- [bold green]Starting WikiScrapper[/bold green] ---")
    console.print(f"[bold]Target URL:[/bold] {url}")
    console.print(f"[bold]Base Domain:[/bold] {base_domain}")
    console.print(f"[bold]Output Dir:[/bold]  {out_path}")
    console.print(f"[bold]Selector:[/bold]    '{selector}'")
    console.print(f"[bold]Depth:[/bold]       {depth}")
    console.print(f"[bold]Delay:[/bold]       {delay}s")
    console.print(f"[bold]Format:[/bold]      {file_format}")
    console.print(f"[bold]Same-host only:[/bold] {same_host}")
    console.print(f"[bold]Max pages:[/bold]   {max_pages if max_pages>0 else 'unlimited'}")
    console.print(f"[bold]Checkpoint:[/bold]  {checkpoint}")
    console.print(f"[bold]JS-render:[/bold]    {js_render}")
    console.print(f"[bold]Ignore-checkpoint:[/bold] {ignore_checkpoint}")
    console.print(f"[bold]Quiet:[/bold]        {quiet}")
    console.print(f"[bold]Verbose:[/bold]      {verbose}")
    console.print("-----------------------------")

    try:
        core.run_scrape(
            start_url=url,
            output_dir=str(out_path),
            selector=selector,
            max_depth=depth,
            user_agent=user_agent,
            delay=delay,
            file_format=file_format,
            same_host=same_host,
            max_pages=max_pages,
            checkpoint_path=checkpoint,
            js_render=js_render,
            ignore_checkpoint=ignore_checkpoint,
            quiet=quiet,
            verbose=verbose,
        )
        console.print("-----------------------------")
        console.print(f"[bold green]Scraping complete![/bold green] Files are in ./{out_path}")
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Scraping interrupted by user.[/bold yellow]")
        raise typer.Exit(code=130)
