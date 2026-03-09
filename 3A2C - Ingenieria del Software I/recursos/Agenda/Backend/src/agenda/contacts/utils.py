"""Contacts utilities."""

from agenda.contacts.models import Contact
from agenda.contacts.schemas import ContactOut
from agenda.tags.schemas import TagSchema


def db_contact_2_contact_out(db_contact: Contact) -> ContactOut:
    """
    Converts a Database contact into a response schema

    Parameters
    ----------
    db_contact : Contact
        Database contact

    Returns
    -------
    ContactOut
        Contact schema for response
    """

    return ContactOut(
        id=db_contact.id,
        name=db_contact.name,
        lastname=db_contact.lastname,
        email=db_contact.email,
        phone_main=db_contact.phone_main,
        phone_backup=db_contact.phone_backup,
        tags=[TagSchema(id=t.id, label=t.label) for t in db_contact.tags],
    )
