from typing import List, Optional

from agenda.contacts.dtos import ContactDTO
from agenda.contacts.models import Contact
from agenda.tags.services import TagService


class ContactService:
    def __init__(self, db):
        self._db = db
        self._tag_service = TagService(db)

    def get_all(
        self,
        name: Optional[str] = None,
        lastname: Optional[str] = None,
        email: Optional[str] = None,
    ) -> List[Contact]:
        query = self._db.query(Contact)
        if name:
            query = query.filter(Contact.name==name)
        if lastname:
            query = query.filter(Contact.lastname==lastname)
        if email:
            query = query.filter(Contact.email==email)
        return query.all()

    def get_by_id(self, id: int) -> Optional[Contact]:
        return self._db.query(Contact).filter(Contact.id == id).first()

    def get_by_email(self, email: str) -> Optional[Contact]:
        return self._db.query(Contact).filter(Contact.email == email).first()

    def create(self, contact_dto: ContactDTO) -> Contact:
        db_contact = self.get_by_email(email=contact_dto.email)
        if db_contact:
            raise ValueError(f"There is a contact registered with same email")
        tags = [db_tag for tag_id in contact_dto.tags if (db_tag := self._tag_service.get_by_id(tag_id)) is not None]
        new_contact = Contact(
            name=contact_dto.name,
            lastname=contact_dto.lastname,
            email=contact_dto.email,
            phone_main=contact_dto.phone_main,
            tags=tags,
        )
        if contact_dto.phone_backup:
            new_contact.phone_backup = contact_dto.phone_backup
        self._db.add(new_contact)
        self._db.flush()
        self._db.commit()
        return new_contact
    
    def delete(self, id: int) -> int:
        db_contact = self.get_by_id(id)
        if not db_contact:
            raise ValueError(f"Contact with id {id} does not exist")
        self._db.delete(db_contact)
        self._db.flush()
        self._db.commit()
        return id
