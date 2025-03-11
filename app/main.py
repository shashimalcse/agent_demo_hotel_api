from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import date
from .schemas import *
from .dependencies import TokenData, validate_token

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory data stores
hotels_data = {
    1: {
        "name": "Gardeo Saman Villa",
        "description": "Enjoy a luxurious stay at Gardeo Saman Villas in your suite, and indulge in a delicious breakfast and your choice of lunch or dinner from our daily set menus served at the restaurant. Access exquisite facilities, including the infinity pool, Sahana Spa, gymnasium and library, as you unwind in paradise.",
        "location": "Bentota, Sri Lanka",
        "rating": 4.5,
        "amenities": ["Infinity Pool", "Sahana Spa", "Gymnasium", "Library", "Restaurant", "Room Service"],
        "policies": [
            "Check-in: 2:00 PM",
            "Check-out: 12:00 PM", 
            "No pets allowed",
            "Non-smoking rooms"
        ],
        "roomTypes": ["deluxe", "super_deluxe"],
        "promotions": ["Early Bird 20% off", "Stay 3 nights get 1 free"]
    },
    2: {
        "name": "Gardeo Colombo Seven",
        "description": "Gardeo Colombo Seven is located in the heart of Colombo, the commercial capital of Sri Lanka and offers the discerning traveler contemporary accommodation and modern design aesthetic. Rising over the city landscape, the property boasts stunning views, a rooftop bar and pool, main restaurant, gym and spa services, as well as conference facilities.",
        "location": "Colombo 07, Sri Lanka", 
        "rating": 4.9,
        "amenities": ["Rooftop Pool", "Spa", "Gym", "Conference Facilities", "Restaurant", "Rooftop Bar"],
        "policies": [
            "Check-in: 3:00 PM",
            "Check-out: 11:00 AM",
            "No pets allowed", 
            "Non-smoking rooms"
        ],
        "roomTypes": ["studio", "super_deluxe"],
        "promotions": ["Business Package", "Weekend Special"]
    },
    3: {
        "name": "Gardeo Kandy Hills",
        "description": "Set amidst the misty hills of Kandy, Gardeo Kandy Hills offers breathtaking views of the surrounding mountains. This heritage property combines traditional Sri Lankan architecture with modern luxury, featuring an infinity pool overlooking the valley, authentic local cuisine, and a wellness center.",
        "location": "Kandy, Sri Lanka",
        "rating": 4.7,
        "amenities": ["Infinity Pool", "Wellness Center", "Heritage Restaurant", "Tea Lounge", "Mountain Biking", "Cultural Tours"],
        "policies": [
            "Check-in: 2:00 PM",
            "Check-out: 11:00 AM",
            "No pets allowed",
            "Non-smoking rooms"
        ],
        "roomTypes": ["deluxe", "studio"],
        "promotions": ["Cultural Experience Package", "Honeymoon Special"]
    },
    4: {
        "name": "Gardeo Beach Resort Galle",
        "description": "Located along the historic Galle coast, Gardeo Beach Resort offers direct beach access and stunning views of the Indian Ocean. The resort features colonial-era architecture, beachfront dining, water sports facilities, and a luxury spa.",
        "location": "Galle, Sri Lanka",
        "rating": 4.8,
        "amenities": ["Private Beach", "Water Sports", "Beachfront Dining", "Luxury Spa", "Infinity Pool", "Kids Club"],
        "policies": [
            "Check-in: 2:00 PM", 
            "Check-out: 12:00 PM",
            "No pets allowed",
            "Non-smoking rooms"
        ],
        "roomTypes": ["deluxe", "super_deluxe"],
        "promotions": ["Beach Getaway Package", "Family Fun Deal"]
    }
}

room_type_data = {
    "deluxe": {"description": "The spacious rooms are defined by king size beds commanding a modern yet minimal ambience, with amenities set in minimalist contours of elegance and efficiency with all the creature comforts a traveler needs."},
    "super_deluxe": {"description": "The super deluxe rooms are defined by king size beds commanding a modern yet minimal ambience, with a bathtub and amenities set in minimalist contours of elegance and efficiency with all the creature comforts a traveler needs."},
    "studio": {"description": "The 1 bedroom serviced apartments spacious living areas as well as a kitchen housing a cooker, fridge, washing machine and microwave. Rooms are defined by king size beds commanding a modern yet minimal ambience, with amenities set in minimalist contours of elegance and efficiency with all the creature comforts a traveller needs."},
    "standard": {"description": "The standard rooms are defined by king size beds commanding a modern yet minimal ambience, with amenities set in minimalist contours of elegance and efficiency with all the creature comforts a traveler needs."}
}

rooms_data = {
    1: {
        101: {
            "room_number": "101",
            "room_type": "standard",
            "price_per_night": 69.99,
            "occupancy": 2,
            "amenities": ["Air Conditioning", "Free WiFi", "Safe"],
            "cancellationPolicy": "Free cancellation up to 24 hours before check-in",
            "is_available": True
        },
        102: {
            "room_number": "102", 
            "room_type": "super_deluxe",
            "price_per_night": 149.50,
            "occupancy": 3,
            "amenities": ["Air Conditioning", "Mini Bar", "Free WiFi", "Safe", "Bathtub", "Sea View"],
            "cancellationPolicy": "Free cancellation up to 24 hours before check-in",
            "is_available": True
        },
        103: {
            "room_number": "103",
            "room_type": "deluxe",
            "price_per_night": 99.99,
            "occupancy": 2,
            "amenities": ["Air Conditioning", "Mini Bar", "Free WiFi", "Safe", "Garden View"],
            "cancellationPolicy": "Free cancellation up to 24 hours before check-in",
            "is_available": True
        }
    },
    2: {
        201: {
            "room_number": "201",
            "room_type": "studio",
            "price_per_night": 299.99,
            "occupancy": 4,
            "amenities": ["Air Conditioning", "Kitchen", "Free WiFi", "Safe", "Washing Machine", "City View"],
            "cancellationPolicy": "Free cancellation up to 48 hours before check-in",
            "is_available": True
        },
        202: {
            "room_number": "202",
            "room_type": "super_deluxe",
            "price_per_night": 199.50,
            "occupancy": 3,
            "amenities": ["Air Conditioning", "Mini Bar", "Free WiFi", "Safe", "Bathtub", "City View"],
            "cancellationPolicy": "Free cancellation up to 48 hours before check-in",
            "is_available": True
        },
        203: {
            "room_number": "203",
            "room_type": "standard",
            "price_per_night": 89.99,
            "occupancy": 4,
            "amenities": ["Air Conditioning", "Free WiFi"],
            "cancellationPolicy": "Free cancellation up to 24 hours before check-in", 
            "is_available": True
        }
    },
    3: {
        301: {
            "room_number": "301",
            "room_type": "deluxe",
            "price_per_night": 179.99,
            "occupancy": 2,
            "amenities": ["Air Conditioning", "Mini Bar", "Free WiFi", "Safe", "Mountain View"],
            "cancellationPolicy": "Free cancellation up to 24 hours before check-in",
            "is_available": True
        },
        302: {
            "room_number": "302",
            "room_type": "studio",
            "price_per_night": 259.99,
            "occupancy": 4,
            "amenities": ["Air Conditioning", "Kitchen", "Free WiFi", "Safe", "Washing Machine", "Valley View"],
            "cancellationPolicy": "Free cancellation up to 48 hours before check-in",
            "is_available": True
        },
        303: {
            "room_number": "303",
            "room_type": "deluxe",
            "price_per_night": 189.99,
            "occupancy": 2,
            "amenities": ["Air Conditioning", "Mini Bar", "Free WiFi", "Safe", "Garden View"],
            "cancellationPolicy": "Free cancellation up to 24 hours before check-in",
            "is_available": True
        }
    },
    4: {
        401: {
            "room_number": "401",
            "room_type": "deluxe",
            "price_per_night": 199.99,
            "occupancy": 2,
            "amenities": ["Air Conditioning", "Mini Bar", "Free WiFi", "Safe", "Ocean View"],
            "cancellationPolicy": "Free cancellation up to 24 hours before check-in",
            "is_available": True
        },
        402: {
            "room_number": "402",
            "room_type": "super_deluxe",
            "price_per_night": 299.50,
            "occupancy": 3,
            "amenities": ["Air Conditioning", "Mini Bar", "Free WiFi", "Safe", "Bathtub", "Ocean View", "Private Balcony"],
            "cancellationPolicy": "Free cancellation up to 48 hours before check-in",
            "is_available": True
        },
        403: {
            "room_number": "403",
            "room_type": "deluxe",
            "price_per_night": 209.99,
            "occupancy": 2,
            "amenities": ["Air Conditioning", "Mini Bar", "Free WiFi", "Safe", "Garden View"],
            "cancellationPolicy": "Free cancellation up to 24 hours before check-in",
            "is_available": True
        }
    }
}

bookings_data = {}

user_bookings_data = [
    {
        "hotel_id": 1,
        "hotel_name": "Gardeo Saman Villa",
        "user_id": "6dcec033-8117-49bb-8363-3c519bcdbb73",
        "room_id": 101,
        "room_type": "deluxe",
        "check_in": date(2024, 2, 12),
        "check_out": date(2024, 2, 15),
        "total_price": 299.97
    },
    {
        "hotel_id": 2,
        "hotel_name": "Gardeo Colombo Seven",
        "user_id": "6dcec033-8117-49bb-8363-3c519bcdbb73",
        "room_id": 201,
        "room_type": "studio",
        "check_in": date(2024, 3, 1),
        "check_out": date(2024, 3, 5),
        "total_price": 1199.96
    }
]
last_booking_id = 0

@app.get("/hotels", response_model=Hotels)
async def list_hotels(
    token_data: TokenData = Security(validate_token, scopes=["read_hotels"])
):
    return {
        "hotels": [
            HotelBasic(id=hid, **hotel_data)
            for hid, hotel_data in hotels_data.items()
        ]
    }

@app.get("/hotels/{hotel_id}", response_model=Hotel)
async def get_hotel(
    hotel_id: int,
    token_data: TokenData = Security(validate_token, scopes=["read_rooms"])
):
    if hotel_id not in hotels_data:
        raise HTTPException(status_code=404, detail="Hotel not found")
    
    hotel = hotels_data[hotel_id]
    rooms = [
        Room(id=rid, **room_data)
        for rid, room_data in rooms_data[hotel_id].items()
    ]
    
    return {
        "id": hotel_id,
        "name": hotel["name"],
        "description": hotel["description"],
        "location": hotel["location"],
        "rating": hotel["rating"],
        "amenities": hotel["amenities"],
        "policies": hotel["policies"],
        "roomTypes": hotel["roomTypes"],
        "promotions": hotel["promotions"],
        "rooms": rooms
    }
class Room(BaseModel):
    id: int
    room_number: str
    room_type: str
    price_per_night: float
    occupancy: int
    amenities: List[str]
    cancellationPolicy: str
    is_available: bool

@app.get("/rooms/{room_id}", response_model=Room)
async def get_room_details(
    room_id: int,
    token_data: TokenData = Security(validate_token, scopes=["read_rooms"])
):
    # Find the hotel that has this room
    room_data = None
    for hotel_rooms in rooms_data.values():
        if room_id in hotel_rooms:
            room_data = hotel_rooms[room_id]
            break
    
    if not room_data:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return {
        "id": room_id,
        "room_number": room_data["room_number"],
        "room_type": room_data["room_type"],
        "price_per_night": room_data["price_per_night"],
        "occupancy": room_data["occupancy"],
        "amenities": room_data["amenities"],
        "cancellationPolicy": room_data["cancellationPolicy"],
        "is_available": room_data["is_available"]
    }

@app.post("/bookings", response_model=Booking)
async def book_room(
    booking: BookingCreate,
    token_data: TokenData = Security(validate_token, scopes=["create_bookings"])
):
    global last_booking_id
    
    # Validate hotel exists
    if booking.hotel_id not in hotels_data:
        raise HTTPException(status_code=404, detail="Hotel not found")
    
    # Validate room exists
    if booking.room_id not in rooms_data.get(booking.hotel_id, {}):
        raise HTTPException(status_code=404, detail="Room not found")
    
    # # Check if room is available for the dates
    # for existing_booking in bookings_data.values():
    #     if (existing_booking["hotel_id"] == booking.hotel_id and 
    #         existing_booking["room_id"] == booking.room_id and 
    #         not (booking.check_out <= existing_booking["check_in"] or 
    #              booking.check_in >= existing_booking["check_out"])):
    #         raise HTTPException(status_code=400, detail="Room not available for these dates")
    
    # Get hotel and room data
    hotel = hotels_data[booking.hotel_id]
    room = rooms_data[booking.hotel_id][booking.room_id]
    
    # Calculate total price
    days = (booking.check_out - booking.check_in).days
    total_price = room["price_per_night"] * days
    
    # Create booking
    last_booking_id += 1
    bookings_data[last_booking_id] = {
        "id": last_booking_id,  # Add booking ID here
        "hotel_id": booking.hotel_id,
        "hotel_name": hotel["name"],
        "user_id": booking.user_id,
        "room_id": booking.room_id,
        "room_type": room["room_type"],
        "check_in": booking.check_in,
        "check_out": booking.check_out,
        "total_price": total_price
    }
    
    return Booking(**bookings_data[last_booking_id])

@app.get("/bookings/{booking_id}", response_model=Booking)
async def get_booking_details(
    booking_id: int,
    token_data: TokenData = Security(validate_token, scopes=["read_bookings"])
):
    if booking_id not in bookings_data:
        raise HTTPException(status_code=404, detail="Booking not found")
    return Booking(**bookings_data[booking_id])

@app.post("/bookings/preview", response_model=BookingPreview)
async def get_booking_preview(
    booking_preview_request: BookingPreviewRequest,
    token_data: TokenData = Security(validate_token, scopes=["read_rooms"])
):
    room_id = booking_preview_request.room_id
    check_in = booking_preview_request.check_in
    check_out = booking_preview_request.check_out

    # Find the hotel that has this room
    hotel_id = None
    room_data = None
    for hid, rooms in rooms_data.items():
        if room_id in rooms:
            hotel_id = hid
            room_data = rooms[room_id]
            break
    
    if not room_data:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Check room availability
    is_available = True
    # for booking in bookings_data.values():  # Fix: iterate over values
    #     if (booking["hotel_id"] == hotel_id and 
    #         booking["room_id"] == room_id and 
    #         not (check_out <= booking["check_in"] or check_in >= booking["check_out"])):
    #         is_available = False
    #         break
    
    # Calculate total price
    days = (check_out - check_in).days
    total_price = room_data["price_per_night"] * days
    
    # Get hotel and room type details
    hotel = hotels_data[hotel_id]
    room_type_details = room_type_data[room_data["room_type"]]
    
    return {
        "room_id": room_id,
        "room_number": room_data["room_number"],
        "room_type": room_data["room_type"],
        "room_type_description": room_type_details["description"],
        "price_per_night": room_data["price_per_night"],
        "total_price": total_price,
        "hotel_id": hotel_id,
        "hotel_name": hotel["name"],
        "hotel_description": hotel["description"],
        "hotel_rating": hotel["rating"],
        "is_available": is_available,
        "check_in": check_in,
        "check_out": check_out
    }


@app.get("/users/{user_id}/bookings", response_model=List[Booking])
async def get_user_bookings(
    user_id: str,
    token_data: TokenData = Security(validate_token, scopes=["read_bookings"])
):
    return [
        Booking(**booking)
        for booking in user_bookings_data
        if booking["user_id"] == user_id
    ]

@app.get("/users/{user_id}/loyalty", response_model=UserLoyalty)
async def get_user_loyalty(
    user_id: int,
    token_data: TokenData = Security(validate_token, scopes=["read_loyalty"])
):
    # Return mock loyalty data
    return {"user_id": user_id, "loyalty_points": 1200}
