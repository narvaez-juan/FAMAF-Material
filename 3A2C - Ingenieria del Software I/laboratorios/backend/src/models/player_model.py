from sqlalchemy import Boolean, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from .game_model import Game
from db import Base
from typing import TYPE_CHECKING
from typing import List, TYPE_CHECKING


class Player(Base):
    
    __tablename__ = "players"
    __table_args__ = {"extend_existing": True}


    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    # Allow nullable birthdate for tests/fixtures
    birthdate: Mapped[str] = mapped_column(DateTime, nullable=False)
    role: Mapped[str] = mapped_column(
        String(50), nullable=True
    )  # e.g., 'murderer', 'detective', 'accomplice'
    social_disgrace: Mapped[bool] = mapped_column(Boolean, default=False)
    turn: Mapped[int] = mapped_column(Integer, default=0)
    game_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("games.id"), nullable=False
    )

    # relationship back to Game
    game: Mapped["Game"] = relationship("Game", back_populates="players")
    secrets = relationship("Secret", back_populates="player", cascade="all, delete-orphan")
    owned_sets: Mapped[List["SetPlay"]] = relationship("SetPlay", back_populates="owner")
    actions: Mapped[List["GameAction"]] = relationship("GameAction", back_populates="actor", cascade="all, delete-orphan")



if TYPE_CHECKING:
    from .game_model import Game
    from .set_model import SetPlay