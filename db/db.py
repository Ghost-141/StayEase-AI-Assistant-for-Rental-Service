import time
from psycopg_pool import ConnectionPool
from core.config import settings
from core.logger import setup_logger

logger = setup_logger(__name__)

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
            timeout=30.0,
            # This checks if the connection is still alive before giving it to you
            check=ConnectionPool.check_connection,
            # Ensure the pooler connection string works correctly
            kwargs={"sslmode": "require"}
        )
        logger.info("Database connection pool initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database connection pool: {e}", exc_info=True)
else:
    logger.warning("DATABASE_URL not found in settings. Pool not initialized.")

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
