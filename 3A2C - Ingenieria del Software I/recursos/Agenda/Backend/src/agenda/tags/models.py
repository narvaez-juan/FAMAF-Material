"""Tags models."""

from sqlalchemy import Column, Integer, String

from agenda.models.db import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

class Tag(Base):
    """Represents a Tag"""

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    label = Column(String, unique=True)
