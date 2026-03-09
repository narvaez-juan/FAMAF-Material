"""Contacts Models."""

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from typing import List
from sqlalchemy.orm import Mapped
from agenda.models.db import Base
from agenda.tags.models import Tag


contact_tag_association = Table(
    "contact_tag_association",
    Base.metadata,
    Column("contact_id", ForeignKey("contacts.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

class Contact(Base):
    """
    Represent a Contact

    """

    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True)
    name = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    phone_main = Column(String, nullable=True)
    phone_backup = Column(String, nullable=True)
    tags: Mapped[List[Tag]] = relationship(
        secondary=contact_tag_association
    )