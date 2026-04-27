from langchain.tools import tool
from pydantic import BaseModel, Field


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
    # Mocked response
    return (
        f"Found 2 properties in {location} for {check_in_date}:\n"
        "1. Ocean View Resort - 5,500 BDT/night (ID: 101)\n"
        "2. Beachside Haven - 4,200 BDT/night (ID: 102)"
    )


@tool(args_schema=ListingDetailsInput)
def get_listing_details(listing_id: int) -> str:
    """Retrieve detailed information about a specific property by its ID."""
    # Mocked response
    details = {
        101: "Ocean View Resort: Located at Kolatoli Beach. Amenities: AC, Wifi, Breakfast. Policy: Free cancellation.",
        102: "Beachside Haven: Cozy room near the beach. Amenities: Wifi, Balcony. Policy: Non-refundable.",
    }
    return details.get(listing_id, "Property not found.")


@tool(args_schema=BookingInput)
def create_booking(
    listing_id: int, guest_name: str, check_in_date: str, nights: int
) -> str:
    """Create a booking for a property."""
    # Mocked response
    return (
        f"SUCCESS: Booking created for {guest_name} at Property ID {listing_id}.\n"
        f"Check-in: {check_in_date} for {nights} nights.\n"
        f"Booking ID: SE-{listing_id}-999"
    )
