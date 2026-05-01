"""
API routes for Reservation management
"""
from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.models.reservation import Reservation, ReservationCreate, ReservationUpdate
from app.services.reservation_service import ReservationService

router = APIRouter()

@router.post("/", response_model=Reservation)
async def create_reservation(reservation: ReservationCreate):
    """Create a new reservation"""
    try:
        return await ReservationService.create_reservation(reservation)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Reservation])
async def list_reservations(skip: int = 0, limit: int = 100):
    """Get all reservations"""
    try:
        return await ReservationService.get_all_reservations(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{reservation_id}", response_model=Reservation)
async def get_reservation(reservation_id: int):
    """Get a specific reservation"""
    reservation = await ReservationService.get_reservation(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@router.put("/{reservation_id}", response_model=Reservation)
async def update_reservation(reservation_id: int, reservation_update: ReservationUpdate):
    """Update a reservation"""
    try:
        updated_reservation = await ReservationService.update_reservation(reservation_id, reservation_update)
        if not updated_reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")
        return updated_reservation
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{reservation_id}")
async def delete_reservation(reservation_id: int):
    """Delete a reservation"""
    success = await ReservationService.delete_reservation(reservation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"message": "Reservation deleted successfully"}

@router.get("/date/{date}", response_model=List[Reservation])
async def get_reservations_by_date(date: datetime):
    """Get reservations for a specific date"""
    try:
        return await ReservationService.get_reservations_by_date(date)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
