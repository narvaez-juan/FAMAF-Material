from typing import List

from agenda.tags.models import Tag
from sqlalchemy.orm import Session


class TagService:
    def __init__(self, db: Session):
        self._db: Session = db

    def get_all(self) -> List[Tag]:
        return self._db.query(Tag).all()
    
    def get_by_label(self, label: str) -> Tag:
        return self._db.query(Tag).filter(Tag.label == label).first()
    
    def get_by_id(self, id: int) -> Tag:
        return self._db.query(Tag).filter(Tag.id == id).first()
    
    def create_tag(self, label: str):
        db_tag = self.get_by_label(label)
        if db_tag:
            raise ValueError(f"Tag {label} already exists")
        new_tag = Tag(label=label)
        self._db.add(new_tag)
        self._db.flush()
        self._db.commit()
        return new_tag.id