import re
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode, urljoin
from pathlib import Path
from bs4 import BeautifulSoup

def normalize_url(url: str) -> str:
    p = urlparse(url)
    scheme = p.scheme or "http"
    netloc = p.netloc.lower()
    path = p.path or "/"
    query = urlencode(sorted(parse_qsl(p.query)), doseq=True)
    return urlunparse((scheme, netloc, path, "", query, ""))

def is_same_domain(url: str, base_domain: str) -> bool:
    p = urlparse(url)
    return p.netloc.lower() == base_domain.lower()

def slugify_segment(segment: str, max_len: int = 120) -> str:
    seg = segment.strip()
    seg = re.sub(r'[^A-Za-z0-9\-_\.]', '-', seg)
    seg = re.sub(r'-{2,}', '-', seg)
    return seg.strip('-')[:max_len] or "segment"

def url_to_filepath(output_root: str, url: str, file_format: str) -> str:
    p = urlparse(url)
    host = slugify_segment(p.netloc)
    parts = [slugify_segment(s) for s in p.path.split('/') if s and s != '/']
    if not parts:
        filename = "index"
        dirpath = Path(output_root) / host
    else:
        filename = parts[-1]
        dirpath = Path(output_root) / host / Path("/".join(parts[:-1])) if len(parts) > 1 else Path(output_root) / host
    dirpath.mkdir(parents=True, exist_ok=True)
    return str((dirpath / f"{filename}.{file_format}").resolve())

def ensure_relative_link(base_url: str, href: str):
    return urljoin(base_url, href)

def detect_best_selector(html: str):
    """
    Heuristic selector detection:
    - Prefer <article>
    - Then <main>
    - Then classes that contain 'content', 'docs', 'markdown', 'container'
    - Return a list (ordered) of selectors to try.
    """
    soup = BeautifulSoup(html, "html.parser")
    selectors = []
    if soup.find("article"):
        selectors.append("article")
    if soup.find("main"):
        selectors.append("main")
    # class-based heuristics
    class_candidates = set()
    for el in soup.find_all(True, class_=True):
        for c in el.get("class", []):
            cname = c.lower()
            if any(k in cname for k in ("content", "docs", "markdown", "article", "container", "main")):
                class_candidates.add(c)
    # prefer shorter class names
    class_list = sorted(class_candidates, key=lambda s: (len(s), s))
    for c in class_list:
        selectors.append(f".{c}")
    # fallback
    selectors.extend(["div.content", "main > div", "body"])
    # dedupe while preserving order
    seen = set()
    ordered = []
    for s in selectors:
        if s not in seen:
            ordered.append(s)
            seen.add(s)
    return ordered
