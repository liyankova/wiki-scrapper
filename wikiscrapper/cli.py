# wikiscrapper/cli.py
import typer
from typing_extensions import Annotated
from rich.console import Console
from urllib.parse import urlparse
import os

from . import core

# Ini adalah aplikasi Typer utama
app = typer.Typer(
    name="wikiscrapper",
    help="A professional CLI tool to scrape documentation sites for LLM context.",
    add_completion=False
)
console = Console()

# --- Definisi Opsi (Flags) ---
# Kita gunakan Annotated untuk dokumentasi CLI yang lebih kaya
OptOutput = Annotated[str, typer.Option("--output", "-o", help="Output root directory.")]
OptDepth = Annotated[int, typer.Option("--depth", "-d", help="Recursion depth (how many links deep).")]
OptSelector = Annotated[str, typer.Option("--selector", "-s", help="CSS selector for the main content.")]
OptFormat = Annotated[str, typer.Option("--format", "-f", help="Output format (txt or md).")]
OptDelay = Annotated[float, typer.Option("--delay", help="Delay (in seconds) between requests.")]
OptUserAgent = Annotated[str, typer.Option("--user-agent", help="User-Agent string for requests.")]


# --- Perintah (Command) Utama: scrape ---
@app.command()
def scrape(
    # Argumen: URL yang wajib diisi
    url: Annotated[str, typer.Argument(help="The starting URL to scrape.", metavar="START_URL")],
    
    # Opsi (Flags) dengan nilai default
    output: OptOutput = "llm_docs",
    depth: OptDepth = 1,
    selector: OptSelector = "main",
    file_format: OptFormat = "txt",
    delay: OptDelay = 1.0,
    user_agent: OptUserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...", # (Disingkat)
):
    """
    Scrape a documentation website starting from START_URL.
    """
    
    # --- Validasi & Setup ---
    if file_format not in ['txt', 'md']:
        console.print(f"[bold red]Error:[/bold red] --format must be 'txt' or 'md'.")
        raise typer.Exit(code=1)
        
    try:
        base_domain = urlparse(url).netloc
        if not base_domain:
            console.print(f"[bold red]Error:[/bold red] Invalid URL provided: {url}")
            raise typer.Exit(code=1)
    except Exception:
        console.print(f"[bold red]Error:[/bold red] Could not parse URL: {url}")
        raise typer.Exit(code=1)
        
    os.makedirs(output, exist_ok=True)
    visited = set()

    # --- Tampilan Awal (UX) ---
    console.print(f"--- [bold green]Starting WikiScrapper[/bold green] ---")
    console.print(f"[bold]Target URL:[/bold] {url}")
    console.print(f"[bold]Base Domain:[/bold] {base_domain}")
    console.print(f"[bold]Output Dir:[/bold]  {output}")
    console.print(f"[bold]Selector:[/bold]    '{selector}'")
    console.print(f"[bold]Depth:[/bold]       {depth}")
    console.print(f"[bold]Delay:[/bold]       {delay}s")
    console.print(f"[bold]Format:[/bold]      {file_format}")
    console.print("-----------------------------")

    # --- Mulai Proses Inti ---
    try:
        core.crawl_site(
            current_url=url,
            base_domain=base_domain,
            output_dir=output,
            visited=visited,
            depth=0, # Mulai dari 0
            max_depth=depth,
            selector=selector,
            user_agent=user_agent,
            delay=delay,
            file_format=file_format
        )
        console.print("-----------------------------")
        console.print(f"[bold green]Scraping complete![/bold green] Files are in ./{output}")
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Scraping interrupted by user.[/bold yellow]")
        raise typer.Exit(code=130)

# --- Perintah (Command) Lain ---
# Anda bisa menambahkan perintah lain di sini, misal:
@app.command()
def config():
    """
    (Placeholder) Configure default settings for wikiscrapper.
    """
    console.print("[bold yellow]Fitur 'config' belum diimplementasikan.[/bold yellow]")
