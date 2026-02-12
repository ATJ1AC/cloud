from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime, date

router = APIRouter()

# In-memory storage for calendar events (in real application, use database)
events_storage = []

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    reminder_enabled: bool = False

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    reminder_enabled: Optional[bool] = None

class Event(EventBase):
    id: str
    created_at: datetime
    updated_at: datetime

@router.post("/", response_model=Event)
async def create_event(event: EventCreate):
    event_id = str(uuid.uuid4())
    db_event = Event(
        id=event_id,
        title=event.title,
        description=event.description,
        start_time=event.start_time,
        end_time=event.end_time,
        location=event.location,
        reminder_enabled=event.reminder_enabled,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    events_storage.append(db_event)
    return db_event

@router.get("/{event_id}", response_model=Event)
async def get_event(event_id: str):
    for event in events_storage:
        if event.id == event_id:
            return event
    raise HTTPException(status_code=404, detail="Event not found")

@router.get("/", response_model=List[Event])
async def get_events(skip: int = 0, limit: int = 100, date_filter: Optional[date] = None):
    filtered_events = events_storage[skip:skip+limit]
    
    if date_filter:
        filtered_events = [
            event for event in filtered_events
            if event.start_time.date() == date_filter
        ]
    
    return filtered_events

@router.put("/{event_id}", response_model=Event)
async def update_event(event_id: str, event_update: EventUpdate):
    for i, event in enumerate(events_storage):
        if event.id == event_id:
            updated_data = event_update.dict(exclude_unset=True)
            for field, value in updated_data.items():
                setattr(events_storage[i], field, value)
            events_storage[i].updated_at = datetime.utcnow()
            return events_storage[i]
    raise HTTPException(status_code=404, detail="Event not found")

@router.delete("/{event_id}")
async def delete_event(event_id: str):
    for i, event in enumerate(events_storage):
        if event.id == event_id:
            del events_storage[i]
            return {"message": "Event deleted successfully"}
    raise HTTPException(status_code=404, detail="Event not found")