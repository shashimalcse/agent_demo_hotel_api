from pydantic import BaseModel
from datetime import date
from typing import Dict, List, Optional

class Room(BaseModel):
    id: int
    room_number: str
    room_type: str
    price_per_night: float
    occupancy: int
    amenities: List[str]
    cancellationPolicy: str
    is_available: bool

class RoomBasic(BaseModel):
    id: int
    room_number: str
    room_type: str
    price_per_night: float
    occupancy: int
    is_available: bool    

class Hotel(BaseModel):
    id: int
    name: str
    description: str
    location: str
    rating: float
    amenities: List[str]
    policies: List[str]
    roomTypes: List[str]
    promotions: List[str]
    rooms: List[RoomBasic]

class HotelBasic(BaseModel):
    id: int
    name: str
    description: str
    location: str
    rating: float
    roomTypes: List[str]

class Hotels(BaseModel):
    hotels: List[HotelBasic]    

class Rooms(BaseModel):
    rooms: List[RoomBasic]    
class BookingCreate(BaseModel):
    user_id: str
    hotel_id: int
    room_id: int
    check_in: date
    check_out: date

class Booking(BaseModel):
    id: int
    user_id: str
    hotel_id: int
    hotel_name: str
    room_id: int
    room_type: str
    check_in: date
    check_out: date
    total_price: float

class UserLoyalty(BaseModel):
    user_id: str
    loyalty_points: int

class RoomSearchResult(BaseModel):
    room_id: int
    hotel_id: int
    hotel_name: str
    hotel_rating: float
    hotel_description: str
    room_number: str
    room_type: str
    room_type_description: str
    price_per_night: float

class BookingPreviewRequest(BaseModel):
    room_id: int
    check_in: date
    check_out: date    

class BookingPreview(BaseModel):
    room_id: int
    room_number: str
    room_type: str
    room_type_description: str
    price_per_night: float
    total_price: float
    hotel_id: int
    hotel_name: str
    hotel_description: str
    hotel_rating: float
    is_available: bool
    check_in: date
    check_out: date
