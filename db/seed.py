import uuid
from db.db import get_db_connection
from db.db import pool
from core.logger import setup_logger

logger = setup_logger(__name__)


def create_tables():
    """Create the initial database schema."""
    logger.info("Creating database tables...")
    queries = [
        "DROP TABLE IF EXISTS conversations CASCADE;", # Force recreation to update UUID to TEXT
        """
        CREATE TABLE IF NOT EXISTS listings (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            price_per_night INTEGER NOT NULL,
            details JSONB,
            available BOOLEAN DEFAULT TRUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS bookings (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            listing_id INTEGER REFERENCES listings(id),
            guest_name TEXT NOT NULL,
            check_in DATE NOT NULL,
            nights INTEGER NOT NULL,
            total_price INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            history JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
    ]

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            for query in queries:
                cur.execute(query)
            conn.commit()
    logger.info("Tables created successfully.")


def seed_data():
    """Inject dummy data into the listings table."""
    logger.info("Seeding dummy data into listings table...")

    listings = [
        (
            "Ocean View Resort",
            "Cox's Bazar",
            5500,
            '{"amenities": ["AC", "Wifi", "Breakfast"], "policy": "Free cancellation"}',
        ),
        (
            "Beachside Haven",
            "Cox's Bazar",
            4200,
            '{"amenities": ["Wifi", "Balcony"], "policy": "Non-refundable"}',
        ),
        (
            "Green Hill Tea Resort",
            "Sylhet",
            4800,
            '{"amenities": ["Garden View", "Wifi", "Restaurant"], "policy": "7-day cancellation"}',
        ),
        (
            "Modern City Apartment",
            "Dhaka",
            3500,
            '{"amenities": ["Gym", "Security", "Parking"], "policy": "Moderate cancellation"}',
        ),
        (
            "Royal Tulip Sea Pearl",
            "Cox's Bazar",
            8500,
            '{"amenities": ["Pool", "Spa", "Sea View", "Breakfast"], "policy": "Free cancellation", "rating": 4.5}',
        ),
        (
            "Hotel Noorjahan Grand",
            "Sylhet",
            6200,
            '{"amenities": ["Pool", "Gym", "Wifi"], "policy": "24-hour cancellation", "rating": 4.2}',
        ),
        (
            "Six Seasons Hotel",
            "Dhaka",
            9000,
            '{"amenities": ["Rooftop Pool", "Spa", "Fine Dining"], "policy": "Flexible cancellation", "rating": 4.6}',
        ),
        (
            "Hotel Agrabad",
            "Chattogram",
            5000,
            '{"amenities": ["Business Center", "Wifi", "Parking"], "policy": "Moderate cancellation", "rating": 4.0}',
        ),
        (
            "Nazimgarh Resort",
            "Sylhet",
            7500,
            '{"amenities": ["Hill View", "Private Villa", "Pool"], "policy": "3-day cancellation", "rating": 4.4}',
        ),
        (
            "Long Beach Hotel",
            "Cox's Bazar",
            6800,
            '{"amenities": ["Beach Access", "Gym", "Restaurant"], "policy": "Free cancellation", "rating": 4.3}',
        ),
        (
            "Hotel Sarina",
            "Dhaka",
            7200,
            '{"amenities": ["Airport Shuttle", "Pool", "Gym"], "policy": "Flexible cancellation", "rating": 4.2}',
        ),
        (
            "The Peninsula Chittagong",
            "Chattogram",
            6100,
            '{"amenities": ["Spa", "Restaurant", "Wifi"], "policy": "Moderate cancellation", "rating": 4.1}',
        ),
        (
            "Grand Sultan Tea Resort",
            "Moulvibazar",
            9500,
            '{"amenities": ["Luxury Spa", "Golf", "Pool"], "policy": "Strict cancellation", "rating": 4.7}',
        ),
        (
            "Hotel Sea Crown",
            "Cox's Bazar",
            3900,
            '{"amenities": ["Sea View", "Wifi"], "policy": "Non-refundable", "rating": 3.9}',
        ),
    ]

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Clear existing listings to avoid duplicates
            cur.execute("TRUNCATE listings RESTART IDENTITY CASCADE;")

            cur.executemany(
                "INSERT INTO listings (name, location, price_per_night, details) VALUES (%s, %s, %s, %s)",
                listings,
            )
            conn.commit()
    logger.info(f"Seeded {len(listings)} listings successfully.")


if __name__ == "__main__":
    try:
        logger.info("Starting database initialization...")
        create_tables()
        seed_data()
        logger.info("Database initialized successfully with dummy data.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}", exc_info=True)
    finally:
        if pool:
            logger.info("Closing database connection pool...")
            pool.close()
            logger.info("Pool closed.")
