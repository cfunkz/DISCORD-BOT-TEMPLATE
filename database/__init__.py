from .database import execute_query

def init_db():
    """Initializes the database by creating necessary tables."""
    create_users_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        xp INTEGER DEFAULT 0,
        bank INTEGER DEFAULT 5000,
        inventory TEXT DEFAULT '{}',
        created_at TEXT NOT NULL
    );
    """
    
    # Create the users table if it doesn't exist
    execute_query(create_users_table_query)