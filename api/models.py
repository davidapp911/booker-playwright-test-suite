from typing import Optional

from pydantic import BaseModel


class BookingDates(BaseModel):
    checkin: str
    checkout: str


class BookingResponse(BaseModel):
    bookingid: int
    roomid: int
    firstname: str
    lastname: str
    email: Optional[str] = None
    phone: Optional[str] = None
    bookingdates: BookingDates
    depositpaid: bool


class BookingListResponse(BaseModel):
    bookings: list[BookingResponse]


class BookingUpdateResponse(BaseModel):
    bookingid: int
    booking: BookingResponse
