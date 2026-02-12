from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

router = APIRouter()

# In-memory storage for notes (in real application, use database)
notes_storage = []

class NoteBase(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

class Note(NoteBase):
    id: str
    created_at: datetime
    updated_at: datetime

@router.post("/", response_model=Note)
async def create_note(note: NoteCreate):
    note_id = str(uuid.uuid4())
    db_note = Note(
        id=note_id,
        title=note.title,
        content=note.content,
        tags=note.tags,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    notes_storage.append(db_note)
    return db_note

@router.get("/{note_id}", response_model=Note)
async def get_note(note_id: str):
    for note in notes_storage:
        if note.id == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")

@router.get("/", response_model=List[Note])
async def get_notes(skip: int = 0, limit: int = 100):
    return notes_storage[skip:skip+limit]

@router.put("/{note_id}", response_model=Note)
async def update_note(note_id: str, note_update: NoteUpdate):
    for i, note in enumerate(notes_storage):
        if note.id == note_id:
            updated_data = note_update.dict(exclude_unset=True)
            for field, value in updated_data.items():
                setattr(notes_storage[i], field, value)
            notes_storage[i].updated_at = datetime.utcnow()
            return notes_storage[i]
    raise HTTPException(status_code=404, detail="Note not found")

@router.delete("/{note_id}")
async def delete_note(note_id: str):
    for i, note in enumerate(notes_storage):
        if note.id == note_id:
            del notes_storage[i]
            return {"message": "Note deleted successfully"}
    raise HTTPException(status_code=404, detail="Note not found")