import urllib.robotparser
from urllib.parse import urljoin, urlparse
from functools import lru_cache

class RobotsCache:
    """
    Cache RobotFileParser per origin.
    """
    def __init__(self):
        self._cache = {}

    def allowed(self, user_agent: str, url: str) -> bool:
        parsed = urlparse(url)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        rp = self._cache.get(origin)
        if rp is None:
            rp = urllib.robotparser.RobotFileParser()
            robots_txt = urljoin(origin, "/robots.txt")
            try:
                rp.set_url(robots_txt)
                rp.read()
            except Exception:
                # If robots.txt cannot be fetched/parsed, be conservative: allow
                pass
            self._cache[origin] = rp
        try:
            return rp.can_fetch(user_agent, url)
        except Exception:
            return True
