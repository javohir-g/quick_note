from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.noteservice import NoteService
from database.models import engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List
from datetime import datetime

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

router = APIRouter()


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/notes/", response_model=List[Note])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notes = NoteService.get_notes(db, skip=skip, limit=limit)
    return notes


@router.post("/notes/", response_model=Note)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    return NoteService.create_note(db=db, title=note.title, content=note.content)


@router.get("/notes/{note_id}", response_model=Note)
def read_note(note_id: int, db: Session = Depends(get_db)):
    note = NoteService.get_note(db, note_id=note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, note: NoteCreate, db: Session = Depends(get_db)):
    updated_note = NoteService.update_note(db=db, note_id=note_id, title=note.title, content=note.content)
    if updated_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note


@router.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = NoteService.delete_note(db=db, note_id=note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}