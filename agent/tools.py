from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


# ============================================================================
# Pydantic Input/Output Models for Tools
# ============================================================================


class SearchInput(BaseModel):
    """Input parameters for searching available properties."""

    location: str = Field(
        ..., description="City or area name (e.g., 'Cox's Bazar', 'Dhaka', 'Sylhet')"
    )
    check_in_date: str = Field(..., description="Check-in date in YYYY-MM-DD format")
    nights: int = Field(..., ge=1, description="Number of nights (positive integer)")
    guests: int = Field(..., ge=1, description="Number of guests (positive integer)")


class ListingDetailsInput(BaseModel):
    """Input parameters for retrieving listing details."""

    listing_id: int = Field(..., description="The unique identifier of the property")


class BookingInput(BaseModel):
    """Input parameters for creating a booking."""

    listing_id: int = Field(..., description="The unique identifier of the property")
    check_in_date: str = Field(..., description="Check-in date in YYYY-MM-DD format")
    nights: int = Field(..., ge=1, description="Number of nights")
    guest_name: str = Field(..., description="Full name of the guest")
    guest_email: str = Field(..., description="Email address of the guest")
    guest_phone: str = Field(..., description="Phone number of the guest")


class SearchResult(BaseModel):
    """Output structure for a single search result."""

    id: int
    name: str
    location: str
    price_per_night: int
    rating: Optional[float] = None


class ListingDetails(BaseModel):
    """Output structure for detailed listing information."""

    id: int
    name: str
    location: str
    price_per_night: int
    host_name: str
    host_contact: str
    check_in_time: str
    check_out_time: str
    cancellation_policy: str
    available_dates: List[str] = Field(default_factory=list)


class BookingConfirmation(BaseModel):
    """Output structure for booking confirmation."""

    booking_id: str
    status: str
    listing_name: str
    check_in_date: str
    nights: int
    total_price: int
    confirmation_message: str
    payment_url: str
    cancellation_policy: str


# ============================================================================
# Tool Functions
# ============================================================================


@tool
def search_available_properties(
    location: str, check_in_date: str, nights: int, guests: int
) -> List[SearchResult]:
    """Search for available properties based on location, check-in date, number of nights, and guests."""
    return [
        SearchResult(
            id=1,
            name="Cozy Beachside Cottage",
            location=location,
            price_per_night=150,
            rating=4.5,
        ),
        SearchResult(
            id=2,
            name="Modern City Apartment",
            location=location,
            price_per_night=100,
            rating=4.0,
        ),
    ]


@tool
def get_listing_details(listing_id: int) -> Dict[str, Any]:
    return {
        "id": listing_id,
        "name": "Ocean View Resort",
        "location": "Cox's Bazar",
        "price_per_night": 5500,
        "host_name": "Ahmed Khan",
        "host_contact": "+8801812345678",
        "check_in_time": "14:00",
        "check_out_time": "12:00",
        "cancellation_policy": "Free cancellation up to 7 days before check-in",
        "available_dates": ["2026-05-01", "2026-05-02", "2026-05-03"],
    }


@tool
def create_booking(
    listing_id: int,
    check_in_date: str,
    nights: int,
    guest_name: str,
    guest_email: str,
    guest_phone: str,
) -> Dict[str, Any]:

    return {
        "booking_id": f"BOOK-2026-{listing_id}001",
        "status": "pending",
        "listing_name": "Ocean View Resort",
        "check_in_date": check_in_date,
        "nights": nights,
        "total_price": 5500 * nights + int(5500 * nights * 0.05),  # Add 5% tax
        "confirmation_message": f"Your booking is confirmed! Booking ID: BOOK-2026-{listing_id}001",
        "payment_url": f"https://stayease.com/payment/BOOK-2026-{listing_id}001",
        "cancellation_policy": "Free cancellation up to 7 days before check-in",
    }
