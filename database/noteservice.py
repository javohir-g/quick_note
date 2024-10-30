from sqlalchemy.orm import Session
from . import models
from datetime import datetime


class NoteService:
    @staticmethod
    def get_notes(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Note).offset(skip).limit(limit).all()

    @staticmethod
    def get_note(db: Session, note_id: int):
        return db.query(models.Note).filter(models.Note.id == note_id).first()

    @staticmethod
    def create_note(db: Session, title: str, content: str):
        note = models.Note(title=title, content=content)
        db.add(note)
        db.commit()
        db.refresh(note)
        return note

    @staticmethod
    def update_note(db: Session, note_id: int, title: str, content: str):
        note = db.query(models.Note).filter(models.Note.id == note_id).first()
        if note:
            note.title = title
            note.content = content
            note.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(note)
        return note

    @staticmethod
    def delete_note(db: Session, note_id: int):
        note = db.query(models.Note).filter(models.Note.id == note_id).first()
        if note:
            db.delete(note)
            db.commit()
        return note
