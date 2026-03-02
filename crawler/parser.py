from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

class Parser:
    def parse(self, html: str, base_url: str):
        soup = BeautifulSoup(html, 'lxml')
        
        # Meta Description & Title
        title = (soup.title.string or "No Title").strip()
        meta_desc = soup.find("meta", attrs={"name": "description"})
        desc = meta_desc["content"] if meta_desc else ""

        # Content Extraction (Heuristics: Remove scripts, styles, nav)
        for junk in soup(["script", "style", "nav", "footer", "header"]):
            junk.decompose()
        
        clean_text = ' '.join(soup.get_text().split())
        
        # Link Extraction
        links = []
        domain = urlparse(base_url).netloc
        for a in soup.find_all('a', href=True):
            link = urljoin(base_url, a['href'])
            # Only index http/s links
            if urlparse(link).scheme in ['http', 'https']:
                links.append(link)

        return {
            "title": title,
            "description": desc,
            "text": clean_text[:10000], # Mobile limit: 10kb text per page
            "links": links,
            "link_count": len(links)
        }
