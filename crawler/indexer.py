import sqlite3

class Indexer:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._setup()

    def _setup(self):
        # Main storage table
        self.conn.execute('''CREATE TABLE IF NOT EXISTS pages 
            (id INTEGER PRIMARY KEY, url TEXT UNIQUE, title TEXT, 
             description TEXT, content TEXT, rank_score REAL)''')
        
        # FTS5 for fast search queries
        self.conn.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS pages_search 
            USING fts5(title, description, content, content='pages', content_rowid='id')''')
        
        # Trigger to keep FTS updated with main table
        self.conn.execute('''CREATE TRIGGER IF NOT EXISTS pages_ai AFTER INSERT ON pages BEGIN
            INSERT INTO pages_search(rowid, title, description, content) VALUES (new.id, new.title, new.description, new.content);
            END;''')
        self.conn.commit()

    def add_page(self, url: str, title: str, description: str, content: str, link_count: int):
        # Basic PageRank-like score: More links on page = higher authority
        rank_score = 1.0 + (link_count * 0.1)
        
        try:
            self.conn.execute(
                "INSERT OR REPLACE INTO pages (url, title, description, content, rank_score) VALUES (?, ?, ?, ?, ?)",
                (url, title, description, content, rank_score)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Indexer Error: {e}")
