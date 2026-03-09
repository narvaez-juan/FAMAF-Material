"""Pending Action Model for NSF Counter System."""


from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base
from datetime import datetime
import enum
from typing import Optional, TYPE_CHECKING


class ActionType(str, enum.Enum):
    """Types of counterable actions"""
    PLAY_SET = "play_set"
    PROCESS_SET = "process_set"
    STEAL_SECRET = "steal_secret"
    STEAL_SET = "steal_set"
    ARIADNE_JOIN = "ariadne_join"
    UPDATE_SECRET = "update_secret"
    DEAD_CARD_FOLLY = "dead_card_folly"


class ActionStatus(str, enum.Enum):
    """Status of pending action"""
    PENDING = "pending"                  
    COUNTER_PENDING = "counter_pending"  
    RESOLVED = "resolved"                
    CANCELLED = "cancelled"              
    EXPIRED = "expired"                  


class PendingAction(Base):
    """
    Represents an action that can be countered by NSF cards.
    Enters 5-second window where any player with NSF can interrupt.
    """
    __tablename__ = "pending_actions"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(Integer, nullable=False)
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    
    initiator_player_id: Mapped[int] = mapped_column(Integer, nullable=False)
    
    target_player_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    action_payload: Mapped[str] = mapped_column(JSON, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    parent_action_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    counters: Mapped[list["Counter"]] = relationship(
        "Counter", 
        back_populates="action", 
        cascade="all, delete-orphan"
    )

if TYPE_CHECKING:
    from .counter_model import Counter
