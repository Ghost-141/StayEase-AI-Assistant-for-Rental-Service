import time
from psycopg_pool import ConnectionPool
from core.config import settings

# Initialize the connection pool using the DATABASE_URL from settings
# We use a synchronous pool as the current graph implementation uses sync invoke.
# Neon suggests using the -pooler connection string for serverless environments.

pool = None

if settings.DATABASE_URL:
    try:
        pool = ConnectionPool(
            conninfo=settings.DATABASE_URL,
            min_size=1,
            max_size=10,
            # wait_timeout is how long to wait for a connection before raising an error
            timeout=30.0,
        )
        print("Database connection pool initialized successfully.")
    except Exception as e:
        print(f"Error initializing database connection pool: {e}")
else:
    print("DATABASE_URL not found in settings. Pool not initialized.")

def get_db_connection():
    """
    Acquire a connection from the pool.
    Usage:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(...)
    """
    if pool is None:
        raise ConnectionError("Database connection pool is not initialized. Check your DATABASE_URL.")
    return pool.connection()
