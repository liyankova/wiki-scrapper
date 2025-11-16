import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def make_session(retries: int = 3, backoff_factor: float = 0.5, timeout: int = 10):
    """
    Create a requests.Session configured with retry and reasonable timeouts.
    """
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.request_timeout = timeout  # attribute for callers to use
    return session

def fetch(session: requests.Session, url: str, headers: dict, timeout: int = None):
    """
    Fetch URL using the provided session; returns response object or raises requests exceptions.
    """
    t = timeout if timeout is not None else getattr(session, "request_timeout", 10)
    resp = session.get(url, headers=headers, timeout=t)
    resp.raise_for_status()
    return resp
