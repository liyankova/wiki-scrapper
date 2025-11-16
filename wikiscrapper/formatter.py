from bs4 import BeautifulSoup
from markdownify import markdownify as md
import re
from datetime import datetime

def clean_soup(soup):
    # Remove script, style, nav, footer, noscript tags
    for tag in soup(["script", "style", "noscript", "header", "footer", "aside", "form", "svg"]):
        tag.decompose()
    # Optionally remove elements with "hidden" or aria-hidden
    for tag in soup.select("[hidden], [aria-hidden='true']"):
        tag.decompose()
    return soup

def html_to_markdown(soup) -> str:
    """
    Convert a BeautifulSoup object (content area) to Markdown string.
    """
    clean = clean_soup(soup)
    # Convert selected node's HTML to markdown
    html = str(clean)
    md_text = md(html, heading_style="ATX")
    # Normalize whitespace & blank lines
    md_text = re.sub(r'\n{3,}', '\n\n', md_text).strip()
    return md_text

def html_to_text(soup) -> str:
    """
    Convert a BeautifulSoup object to plain text while preserving paragraphs and code blocks.
    """
    clean = clean_soup(soup)
    # Replace code/pre with fenced blocks
    for pre in clean.find_all(["pre", "code"]):
        text = pre.get_text()
        pre.replace_with("\n```\n" + text.strip() + "\n```\n")
    text = clean.get_text(separator="\n\n", strip=True)
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    return text

def make_frontmatter(url: str, title: str, selector: str):
    now = datetime.utcnow().isoformat() + "Z"
    fm = f"---\nsource_url: \"{url}\"\ntitle: \"{title}\"\ncrawl_date: \"{now}\"\nselector: \"{selector}\"\n---\n\n"
    return fm
