import sqlite3
from typing import Optional, Tuple

class URLFrontier:
    """Manages URL queue, priority, and deduplication using SQLite."""
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._prepare_db()

    def _prepare_db(self):
        # status: 'pending', 'processing', 'completed', 'failed'
        self.conn.execute('''CREATE TABLE IF NOT EXISTS queue 
            (url TEXT PRIMARY KEY, priority INTEGER, status TEXT, depth INTEGER)''')
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_status ON queue(status)")
        self.conn.commit()

    def add_url(self, url: str, priority: int = 1, depth: int = 0):
        try:
            self.conn.execute("INSERT INTO queue (url, priority, status, depth) VALUES (?, ?, 'pending', ?)", 
                             (url, priority, depth))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass  # URL already crawled or in queue

    def get_next_url(self) -> Optional[Tuple[str, int]]:
        cursor = self.conn.execute(
            "SELECT url, depth FROM queue WHERE status='pending' ORDER BY priority DESC LIMIT 1"
        )
        res = cursor.fetchone()
        if res:
            self.conn.execute("UPDATE queue SET status='processing' WHERE url=?", (res[0],))
            self.conn.commit()
        return res

    def mark_done(self, url: str):
        self.conn.execute("UPDATE queue SET status='completed' WHERE url=?", (url,))
        self.conn.commit()

    def mark_failed(self, url: str):
        self.conn.execute("UPDATE queue SET status='failed' WHERE url=?", (url,))
        self.conn.commit()

