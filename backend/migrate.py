#!/usr/bin/env python3
"""Database migration script"""

import os
import subprocess
import sys

def run_migrations():
    """Run Alembic migrations"""
    try:
        # Set database URL from environment
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            print("ERROR: DATABASE_URL environment variable not set")
            sys.exit(1)
        
        # Run migrations
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            env={**os.environ, "DATABASE_URL": db_url},
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Database migrations completed successfully")
        else:
            print(f"❌ Migration failed: {result.stderr}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Migration error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_migrations()