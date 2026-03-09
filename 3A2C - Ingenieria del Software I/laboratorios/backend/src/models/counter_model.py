"""Counter Model for NSF Card Plays."""

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base
from datetime import datetime
from typing import TYPE_CHECKING


class Counter(Base):
    """
    Represents a single NSF card play against a pending action.
    Multiple counters create a chain.
    """
    __tablename__ = "counters"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    action_id: Mapped[int] = mapped_column(Integer, ForeignKey("pending_actions.id"), nullable=False)
    
    player_id: Mapped[int] = mapped_column(Integer, nullable=False)
    
    nsf_game_card_id: Mapped[int] = mapped_column(Integer, nullable=False)
    
    played_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    chain_position: Mapped[int] = mapped_column(Integer, nullable=False)
    
    action: Mapped["PendingAction"] = relationship("PendingAction", back_populates="counters")


if TYPE_CHECKING:
    from .pending_action_model import PendingAction
