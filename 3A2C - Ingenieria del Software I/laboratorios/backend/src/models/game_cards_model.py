
from sqlalchemy import ForeignKey, Integer, Enum
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped
from db import Base
import enum 

class CardLocation(enum.Enum):
    DECK = "deck"
    HAND = "hand"
    DISCARD = "discardPile"
    DRAFT = "draft"
    SET = "set"
    REMOVED = "removed"

class GameCards(Base):
    __tablename__= "game_cards"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey("games.id"), nullable=False)
    card_id: Mapped[int] = mapped_column(Integer, ForeignKey("cards.id"), nullable=True)
    location: Mapped[CardLocation] = mapped_column(Enum(CardLocation), default=CardLocation.DECK)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"), nullable=True)
    # position can be null when a card is drawn (no position while in HAND)
    position: Mapped[int] = mapped_column(Integer, nullable=True)
    discard_order: Mapped[int] = mapped_column(Integer, nullable=True)
    set_id: Mapped[int] = mapped_column(Integer, ForeignKey("set_plays.id"), nullable=True)
    
    # Use string-based relationships
    game: Mapped["Game"] = relationship("Game", back_populates="cards")
    card: Mapped["Card"] = relationship("Card", back_populates="games")
    set: Mapped[int] = relationship("SetPlay", back_populates="cards")

# TYPE_CHECKING imports at the bottom
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_model import Game
    from .card_model import Card
    from .player_model import Player
