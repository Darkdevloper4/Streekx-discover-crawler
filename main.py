import json
import threading
import time
import logging
from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    return "Streekx Discovery Backend is RUNNING 24/7! 🚀"

def run():
  # Port 8080 Replit ke liye standard hai
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Aapke existing crawler logic se pehle ise call karein
if __name__ == "__main__":
    print("Initializing 24/7 Heartbeat...")
    keep_alive()
    # Yahan aapka crawler start karne ka code aayega
    # example: start_crawler()

from crawler.url_frontier import URLFrontier
from crawler.fetcher import Fetcher
from crawler.parser import Parser
from crawler.indexer import Indexer

# System Logging
logging.basicConfig(level=logging.INFO, format='%(threadName)s: %(message)s')

class StreekxBeastCrawler:
    def __init__(self):
        with open('config.json', 'r') as f:
            self.config = json.load(f)
            
        self.frontier = URLFrontier(self.config['db_path'])
        self.fetcher = Fetcher(user_agent=self.config['user_agent'])
        self.indexer = Indexer(self.config['db_path'])
        self.parser = Parser()
        self.max_threads = self.config.get('max_concurrent_fetches', 3)
        self.active_threads = 0

    def worker(self):
        """Worker thread logic for high-speed crawling."""
        while True:
            target = self.frontier.get_next_url()
            if not target:
                break
                
            url, depth = target
            
            # Politeness & Throttling
            time.sleep(self.config['delay_per_domain'])
            
            logging.info(f"Fetching: {url}")
            html = self.fetcher.fetch(url)
            
            if html:
                # Mojeek-level parsing (Heuristics)
                data = self.parser.parse(html, url)
                
                # Indexing for Replit/Android App
                self.indexer.add_page(
                    url=url, 
                    title=data['title'], 
                    content=data['text'], 
                    link_count=data['link_count']
                )
                
                # Discovery
                if depth < self.config['max_depth']:
                    for link in data['links'][:25]: # Top 25 links only
                        self.frontier.add_url(link, depth=depth+1)
            
            self.frontier.mark_done(url)

    def run(self):
        logging.info("Streekx Discovery: BEAST MODE ACTIVATE")
        
        # Initial Seeds
        for url in self.config['seed_urls']:
            self.frontier.add_url(url, priority=10, depth=0)
            
        threads = []
        for i in range(self.max_threads):
            t = threading.Thread(target=self.worker, name=f"StreekxWorker-{i}")
            t.start()
            threads.append(t)
            
        for t in threads:
            t.join()

if __name__ == "__main__":
    import os
    if not os.path.exists('data'): os.makedirs('data')
    
    bot = StreekxBeastCrawler()
    bot.run()

