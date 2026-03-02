import httpx
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from typing import Optional

class Fetcher:
    def __init__(self, user_agent: str):
        self.user_agent = user_agent
        self.robots_cache = {}

    def is_allowed(self, url: str) -> bool:
        parsed = urlparse(url)
        domain = f"{parsed.scheme}://{parsed.netloc}"
        if domain not in self.robots_cache:
            rp = RobotFileParser()
            try:
                # 10s timeout for robots.txt
                with httpx.Client(timeout=10.0) as client:
                    resp = client.get(f"{domain}/robots.txt")
                    if resp.status_code == 200:
                        rp.parse(resp.text.splitlines())
                    else:
                        return True
                self.robots_cache[domain] = rp
            except:
                return True
        return self.robots_cache[domain].can_fetch(self.user_agent, url)

    def fetch(self, url: str) -> Optional[str]:
        if not self.is_allowed(url):
            return None
        
        try:
            with httpx.Client(headers={"User-Agent": self.user_agent}, timeout=15.0, follow_redirects=True) as client:
                resp = client.get(url)
                if resp.status_code == 200 and "text/html" in resp.headers.get("Content-Type", ""):
                    return resp.text
        except Exception:
            pass
        return None
