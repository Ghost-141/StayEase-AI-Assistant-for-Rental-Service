import json
from langchain.tools import tool
from pydantic import BaseModel, Field
from db.db import get_db_connection
from core.logger import setup_logger

logger = setup_logger(__name__)


# Pydantic Input Models for Tools

class SearchInput(BaseModel):
    """Input parameters for searching available properties."""

    location: str = Field(
        ...,
        description="The specific city, area, or tourist destination in Bangladesh (e.g., 'Cox's Bazar', 'Sylhet', 'Gulshan').",
    )
    check_in_date: str = Field(
        ..., 
        description="The guest's check-in date. MUST be in YYYY-MM-DD format."
    )
    nights: int = Field(
        ..., 
        ge=1, 
        description="The total number of nights the guest intends to stay. Must be an integer >= 1."
    )
    guests: int = Field(
        ..., 
        ge=1, 
        description="The total number of people staying in the property. Must be an integer >= 1."
    )


class ListingDetailsInput(BaseModel):
    """Input parameters for retrieving listing details."""

    listing_id: int = Field(
        ..., 
        description="The unique numeric ID of the property, usually found in search results."
    )


class BookingInput(BaseModel):
    """Input parameters for creating a booking."""

    listing_id: int = Field(
        ..., 
        description="The unique numeric ID of the property the user wants to book."
    )
    guest_name: str = Field(
        ..., 
        description="The full legal name of the primary guest making the reservation."
    )
    check_in_date: str = Field(
        ..., 
        description="The confirmed check-in date. MUST be in YYYY-MM-DD format."
    )
    nights: int = Field(
        ..., 
        ge=1, 
        description="The number of nights for the stay. Must be an integer >= 1."
    )


# Tool Functions

@tool(args_schema=SearchInput)
def search_available_properties(
    location: str, check_in_date: str, nights: int, guests: int
) -> str:
    """
    Search for available rental properties in a specific location within Bangladesh.

    Args:
        location: The specific city, area, or destination name (e.g. 'Cox's Bazar').
        check_in_date: The guest's check-in date in YYYY-MM-DD format.
        nights: The total number of nights for the stay.
        guests: The number of people staying.
    """
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
    """
    Retrieve deep-dive information about a specific property listing.

    Args:
        listing_id: The unique numeric identifier for the property.
    """
    logger.info(f"Retrieving details for listing ID: {listing_id}...")
    query = "SELECT name, location, price_per_night, details FROM listings WHERE id = %s;"
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (listing_id,))
                result = cur.fetchone()
                
                if not result:
                    logger.warning(f"Listing ID {listing_id} not found.")
                    return "Property not found. Please provide a valid Listing ID."
                
                name, loc, price, details = result
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
    """
    Finalize a reservation for a guest in the database.

    Args:
        listing_id: The unique numeric identifier for the property.
        guest_name: The full legal name of the primary guest.
        check_in_date: The confirmed check-in date in YYYY-MM-DD format.
        nights: The confirmed number of nights for the stay.
    """
    logger.info(f"Initiating booking for {guest_name} at listing ID: {listing_id}...")

    # Fetch price
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
                    return "Booking failed: The property you selected could not be found."
                
                price_per_night, listing_name = res
                total_price = price_per_night * nights
                
                # Create booking
                cur.execute(insert_booking_query, (listing_id, guest_name, check_in_date, nights, total_price))
                booking_id = cur.fetchone()[0]
                conn.commit()
                
                logger.info(f"Booking successful! ID: {booking_id}")
                return (
                    f"SUCCESS: Your booking for {listing_name} is confirmed!\n"
                    f"- Confirmation ID: {booking_id}\n"
                    f"- Guest: {guest_name}\n"
                    f"- Check-in: {check_in_date}\n"
                    f"- Total Nights: {nights}\n"
                    f"- Total Amount: {total_price} BDT"
                )
    except Exception as e:
        logger.error(f"Error creating booking for listing ID {listing_id}: {e}", exc_info=True)
        return f"Error creating booking: {str(e)}"
