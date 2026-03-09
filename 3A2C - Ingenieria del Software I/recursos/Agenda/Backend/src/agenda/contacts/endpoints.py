"""Defines contacts endpoints."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from agenda.contacts.models import Contact
from agenda.contacts.schemas import (
    ContactIn,
    ContactOut,
    ContactResponse,
    WSAddMessage,
    WSRemoveMessage,
)
from agenda.contacts.services import ContactService
from agenda.contacts.utils import db_contact_2_contact_out
from agenda.models.db import get_db
from agenda.tags.models import Tag
from agenda.websockets import manager

contacts_router = APIRouter()


@contacts_router.get(path="")
async def retrieve_contacts(
    db=Depends(get_db),
    name: Optional[str] = None,
    lastname: Optional[str] = None,
    email: Optional[str] = None,
) -> List[ContactOut]:
    (
        """
    retrieves contact information as a list filtering by name, 
    lastaname or email.

    Parameters
    ----------
    name : Optional[str], optional
        contact name, default None
    lastname : Optional[str], optional
        contact lastname, by default None
    email : Optional[str], optional
        contact email, by default None

    Returns
    -------
    List[ContactOut]
        A list of retrieved contacts
    """
        """"""
    )
    return [
        db_contact_2_contact_out(contact)
        for contact in ContactService(db).get_all(
            name=name, lastname=lastname, email=email
        )
    ]


@contacts_router.get(path="/{id}")
async def get_contact(id: int, db=Depends(get_db)) -> ContactOut:
    """
    Get a contact

    Parameters
    ----------
    id : int
        contact id

    Returns
    -------
    ContactOut
        Contact retrieved

    Raises
    ------
    HTTPException
        404 -> When contact is not found
    """
    db_contact = ContactService(db).get_by_id(id=id)
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {id} does not exist",
        )
    return db_contact_2_contact_out(db_contact=db_contact)


@contacts_router.post(path="", status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact_info: ContactIn, db=Depends(get_db)
) -> ContactResponse:
    """
    creates a new contact

    Parameters
    ----------
    contact_info : ContactIn
        Contact information

    Returns
    -------
    ContactResponse
        Contact identifier

    Raises
    ------
    HTTPException
        400 -> When email already exist or a tag id doesn't exist

    """
    try:
        created_contact = ContactService(db).create(contact_dto=contact_info.to_dto())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    ws_message = WSAddMessage(
        payload=db_contact_2_contact_out(db_contact=created_contact)
    )
    await manager.broadcast(ws_message.model_dump_json())
    return ContactResponse(id=created_contact.id)


@contacts_router.delete(path="/{id}")
async def delete_contact(id: int, db=Depends(get_db)) -> ContactResponse:
    """
    Delete contact with id.

    Parameters
    ----------
    id : int
        id of desidered contact

    Returns
    -------
    ContactResponse
        id of deleted contact

    Raises
    ------
    HTTPException
        404 -> When contact with id is not found
    """
    try:
        deleted_id = ContactService(db).delete(id=id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    ws_message = WSRemoveMessage(payload=deleted_id)
    await manager.broadcast(ws_message.model_dump_json())
    return ContactResponse(id=deleted_id)
