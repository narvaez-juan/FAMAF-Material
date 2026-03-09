"""Games Models."""
from typing import List, TYPE_CHECKING
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped, relationship
from db import Base

class Game(Base):
    """
    Represent a Game
    """
    __tablename__ = "games"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    min_players = Column(Integer, nullable=False)
    max_players = Column(Integer, nullable=False)
    players_amount = Column(Integer, nullable=False)
    in_game = Column(Boolean, default=False)
    current_turn: Mapped[int] = mapped_column(Integer, default=0) 

    
    # Use string-based relationship
    cards: Mapped[List["GameCards"]] = relationship("GameCards", back_populates="game") 
   
    players = relationship(
        "Player",
        back_populates="game",
        cascade="all, delete-orphan",
        order_by="Player.turn",
    )
    secrets = relationship("Secret", back_populates="game", cascade="all, delete-orphan")
    sets: Mapped[List["SetPlay"]] = relationship("SetPlay", back_populates="game")
    actions: Mapped[List["GameAction"]] = relationship("GameAction", back_populates="game", cascade="all, delete-orphan")


if TYPE_CHECKING:
    from .game_cards_model import GameCards
    from .player_model import Player  # Add this if Player is in a separate file
    from .set_model import SetPlay