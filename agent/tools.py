import json
from langchain.tools import tool
from pydantic import BaseModel, Field
from db.db import get_db_connection
from core.logger import setup_logger

logger = setup_logger(__name__)


# ============================================================================
# Pydantic Input Models for Tools
# ============================================================================


class SearchInput(BaseModel):
    """Input parameters for searching available properties."""

    location: str = Field(
        ...,
        description="City or area name in Bangladesh (e.g., 'Cox's Bazar', 'Dhaka', 'Sylhet')",
    )
    check_in_date: str = Field(..., description="Check-in date in YYYY-MM-DD format")
    nights: int = Field(..., ge=1, description="Number of nights to stay")
    guests: int = Field(..., ge=1, description="Number of guests to stay")


class ListingDetailsInput(BaseModel):
    """Input parameters for retrieving listing details."""

    listing_id: int = Field(..., description="The unique ID of the property listing")


class BookingInput(BaseModel):
    """Input parameters for creating a booking."""

    listing_id: int = Field(..., description="The ID of the property to book")
    guest_name: str = Field(..., description="Full name of the guest")
    check_in_date: str = Field(..., description="Check-in date (YYYY-MM-DD)")
    nights: int = Field(..., ge=1, description="Number of nights")


# ============================================================================
# Tool Functions
# ============================================================================


@tool(args_schema=SearchInput)
def search_available_properties(
    location: str, check_in_date: str, nights: int, guests: int
) -> str:
    """Search for available properties in a specific location for given dates and guests."""
    logger.info(f"Searching for properties in {location} for {guests} guests...")
    query = """
    SELECT id, name, price_per_night 
    FROM listings 
    WHERE location ILIKE %s AND available = TRUE
    LIMIT 5;
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (f"%{location}%",))
                results = cur.fetchall()
                
                if not results:
                    logger.info(f"No properties found in {location}.")
                    return f"I'm sorry, I couldn't find any available properties in {location} for those criteria."
                
                logger.info(f"Found {len(results)} properties in {location}.")
                response = f"Found {len(results)} properties in {location}:\n"
                for r in results:
                    response += f"- {r[1]}: {r[2]} BDT/night (ID: {r[0]})\n"
                return response
    except Exception as e:
        logger.error(f"Error searching properties: {e}", exc_info=True)
        return f"Error searching properties: {str(e)}"


@tool(args_schema=ListingDetailsInput)
def get_listing_details(listing_id: int) -> str:
    """Retrieve detailed information about a specific property by its ID."""
    logger.info(f"Retrieving details for listing ID: {listing_id}...")
    query = "SELECT name, location, price_per_night, details FROM listings WHERE id = %s;"
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (listing_id,))
                result = cur.fetchone()
                
                if not result:
                    logger.warning(f"Listing ID {listing_id} not found.")
                    return "Property not found."
                
                name, loc, price, details = result
                # details is a dict (JSONB)
                amenities = ", ".join(details.get("amenities", []))
                policy = details.get("policy", "Standard cancellation policy applies.")
                
                logger.info(f"Successfully retrieved details for {name}.")
                return (
                    f"Details for {name} (ID: {listing_id}):\n"
                    f"- Location: {loc}\n"
                    f"- Price: {price} BDT/night\n"
                    f"- Amenities: {amenities}\n"
                    f"- Policy: {policy}"
                )
    except Exception as e:
        logger.error(f"Error retrieving listing details for ID {listing_id}: {e}", exc_info=True)
        return f"Error retrieving listing details: {str(e)}"


@tool(args_schema=BookingInput)
def create_booking(
    listing_id: int, guest_name: str, check_in_date: str, nights: int
) -> str:
    """Create a booking for a property and save it to the database."""
    logger.info(f"Initiating booking for {guest_name} at listing ID: {listing_id}...")
    # 1. Fetch price to calculate total
    get_price_query = "SELECT price_per_night, name FROM listings WHERE id = %s;"
    insert_booking_query = """
    INSERT INTO bookings (listing_id, guest_name, check_in, nights, total_price)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id;
    """
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Get price
                cur.execute(get_price_query, (listing_id,))
                res = cur.fetchone()
                if not res:
                    logger.warning(f"Booking failed: Listing ID {listing_id} not found.")
                    return "Booking failed: Listing not found."
                
                price_per_night, listing_name = res
                total_price = price_per_night * nights
                
                # Create booking
                cur.execute(insert_booking_query, (listing_id, guest_name, check_in_date, nights, total_price))
                booking_id = cur.fetchone()[0]
                conn.commit()
                
                logger.info(f"Booking successful! ID: {booking_id}")
                return (
                    f"SUCCESS: Booking confirmed for {guest_name} at {listing_name}!\n"
                    f"- Booking ID: {booking_id}\n"
                    f"- Check-in: {check_in_date}\n"
                    f"- Nights: {nights}\n"
                    f"- Total Price: {total_price} BDT"
                )
    except Exception as e:
        logger.error(f"Error creating booking for listing ID {listing_id}: {e}", exc_info=True)
        return f"Error creating booking: {str(e)}"
