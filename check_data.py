import sqlite3

def check():
    conn = sqlite3.connect('data/crawl_db.sqlite')
    cursor = conn.cursor()
    
    # Check total pages
    count = cursor.execute("SELECT count(*) FROM pages").fetchone()[0]
    print(f"✅ Total Pages Crawled: {count}")
    
    # Show last 5 titles
    print("\n--- Last 5 Indexed Pages ---")
    rows = cursor.execute("SELECT title, url FROM pages ORDER BY id DESC LIMIT 5").fetchall()
    for row in rows:
        print(f"Title: {row[0]}\nURL: {row[1]}\n")

if __name__ == "__main__":
    check()

