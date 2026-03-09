"""Game Action Model."""
from datetime import datetime
from typing import Optional, TYPE_CHECKING, List
from sqlalchemy import Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base
import enum

class GameActionType(str, enum.Enum):
    """Types of visible player actions for players."""
    PLAY_SET = "play_set"
    REVEAL_SECRET = "reveal_secret"
    HIDE_SECRET = "hide_secret"    
    STEAL_SECRET = "steal_secret"
    JOIN_SET = "join_set"
    DISCARD_CARDS = "discard_cards" 
    PLAY_EVENT = "play_event"
    CANCEL_ACTION = "cancel_action"
    OTHER = "other"             

class GameAction(Base):
    """
    Represents a visible action in the game, used to inform players.
    """
    __tablename__ = "game_actions"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    game_id: Mapped[int] = mapped_column(Integer, ForeignKey("games.id"), nullable=False)
    actor_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"), nullable=False)

    action_type: Mapped[GameActionType] = mapped_column(Enum(GameActionType), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

    card_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("game_cards.id"), nullable=True)
    secret_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("secrets.id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    game = relationship("Game", back_populates="actions")
    actor = relationship("Player", back_populates="actions")

# TYPE_CHECKING imports
if TYPE_CHECKING:
    from .game_model import Game
    from .player_model import Player
