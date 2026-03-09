"""Card Models."""
from typing import List, TYPE_CHECKING
import enum
from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped
from db import Base

class CardType(str,enum.Enum):
    NSF = "Not so Fast"
    DET = "Detective"
    DEV = "Devious"
    EVT = "Event"
    HLP = "Help"
    SCT = "Secret "

class Card(Base):
    __tablename__ = "cards"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(Enum(CardType))

    # Use string-based relationship to avoid circular imports
    games: Mapped[List["GameCards"]] = relationship("GameCards", back_populates="card")

# Move the TYPE_CHECKING import to the bottom
if TYPE_CHECKING:
    from .game_cards_model import GameCards