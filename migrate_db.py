"""
Database Migration Script
This script handles database schema updates for the Contract Generator.
Run this when the database schema changes.
"""

import os
from database import Base, engine

def migrate_database():
    """Recreate database with updated schema"""
    db_path = "contracts.db"
    
    # Backup old database if it exists
    if os.path.exists(db_path):
        backup_path = f"{db_path}.backup"
        if os.path.exists(backup_path):
            os.remove(backup_path)
        os.rename(db_path, backup_path)
        print(f"✅ Backed up old database to {backup_path}")
    
    # Create new database with updated schema
    Base.metadata.create_all(bind=engine)
    print("✅ Created new database with updated schema")
    print("\n⚠️  Note: Old contract data is in contracts.db.backup")
    print("   You can manually migrate data if needed.")

if __name__ == "__main__":
    migrate_database()
