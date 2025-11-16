# wikiscrapper/core.py
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from rich.console import Console

from .utils import get_and_prepare_filepath, is_valid_url

# We use rich.print for better terminal output
console = Console()

def scrape_page(url, headers, selector):
    """Scrapes a single page and returns its soup and text content."""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            console.print(f"[bold red]Failed:[/bold red] Status {response.status_code} on {url}")
            return None, None, None

        soup = BeautifulSoup(response.content, 'html.parser')
        content_area = soup.select_one(selector)
        
        if not content_area:
            console.print(f"[bold yellow]Warning:[/bold yellow] Selector '{selector}' not found on {url}. Skipping.")
            return None, None, None
            
        text_content = content_area.get_text(separator='\n\n', strip=True)
        page_title = soup.title.string.strip() if soup.title else "Scraped Page"
        
        return soup, text_content, page_title

    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error (Request):[/bold red] {e}")
        return None, None, None

def crawl_site(current_url, base_domain, output_dir, visited, depth, max_depth, selector, user_agent, delay, file_format):
    """
    The main recursive crawling function.
    """
    if depth > max_depth or current_url in visited:
        return

    visited.add(current_url)
    console.print(f"[{depth}/{max_depth}] Scraping: [cyan]{current_url}[/cyan]")

    headers = {'User-Agent': user_agent}
    soup, text_content, page_title = scrape_page(current_url, headers, selector)
    
    if not soup:
        return

    # --- Prepare Content ---
    metadata = f"""---
[LLM-Context-Metadata]
Source-URL: {current_url}
Scrape-Date: {datetime.now().isoformat()}
CSS-Selector-Used: {selector}
---

"""
    if file_format == "md":
        final_content = metadata + f"# {page_title}\n\n" + text_content
    else:
        final_content = metadata + text_content

    # --- Save File ---
    filepath = get_and_prepare_filepath(current_url, output_dir, file_format)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)
    except Exception as e:
        console.print(f"[bold red]Error writing file {filepath}:[/bold red] {e}")
        return # Don't crawl further if we can't write

    # --- Find Links and Recurse ---
    if depth < max_depth:
        time.sleep(delay) # Be polite *before* the next batch of requests
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            next_url = urljoin(current_url, href)
            next_url = next_url.split('#')[0] # Remove fragments

            if is_valid_url(next_url, base_domain) and next_url not in visited:
                crawl_site(
                    current_url=next_url,
                    base_domain=base_domain,
                    output_dir=output_dir,
                    visited=visited,
                    depth=depth + 1,
                    max_depth=max_depth,
                    selector=selector,
                    user_agent=user_agent,
                    delay=delay,
                    file_format=file_format
                )
