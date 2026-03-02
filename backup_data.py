import shutil
import os
import time

def backup_db():
    source = 'data/crawl_db.sqlite'
    if not os.path.exists('backups'):
        os.makedirs('backups')
        
    if os.path.exists(source):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        destination = f'backups/crawl_db_backup_{timestamp}.sqlite'
        shutil.copy2(source, destination)
        print(f"✅ Backup created: {destination}")
    else:
        print("❌ Database not found. Run the crawler first.")

if __name__ == "__main__":
    backup_db()

