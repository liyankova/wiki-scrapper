import re
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode, urljoin
from pathlib import Path

def normalize_url(url: str) -> str:
    """
    Normalize a URL for deduplication:
    - ensure scheme exists
    - lowercase scheme & host
    - remove fragment
    - sort query params
    """
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
    """
    Convert URL to safe filepath under output_root.
    Example: https://example.com/docs/intro -> output_root/example.com/docs/intro.md
    """
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
    """
    Resolve relative hrefs to absolute URL using base_url.
    """
    return urljoin(base_url, href)
