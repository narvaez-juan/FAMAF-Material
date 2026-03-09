"""Contacts Schemas."""

from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from agenda.contacts.dtos import ContactDTO
from agenda.tags.schemas import TagSchema


class ContactIn(BaseModel):
    """
    Schema for representing a inbound contact
    """

    name: str
    lastname: str
    email: EmailStr
    phone_main: str
    phone_backup: Optional[str] = None
    tags: List[int] = Field(default_factory=list)

    def to_dto(self) -> ContactDTO:
        return ContactDTO(
            name=self.name,
            lastname=self.lastname,
            email=self.email,
            phone_main=self.phone_main,
            phone_backup=self.phone_backup,
            tags=self.tags,
        )


class ContactResponse(BaseModel):
    """Class for retriving Contact creation response."""

    id: int


class ContactOut(BaseModel):
    """
    Schema for representing a  contact
    """

    id: int
    name: str
    lastname: str
    email: EmailStr
    phone_main: str
    phone_backup: Optional[str] = None
    tags: List[TagSchema] = Field(default_factory=list)


class WSAddMessage(BaseModel):
    type: str = "contactAdd"
    payload: ContactOut


class WSRemoveMessage(BaseModel):
    type: str = "contactRemove"
    payload: int
