import enum
from typing import List
from sqlalchemy import Integer, Enum, ForeignKey, Boolean
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped
from db import Base


class SetType(str, enum.Enum):
    HERCULE_POIROT = "Hercule Poirot"
    MISS_MARPLE = "Miss Marple"
    MR_SATTERTHWAITE = "Mr. Satterthwaite"
    PARKER_PYNE = "Parker Pyne"
    LADY_EILEEN_BUNDLE_BRENT = "Lady Eileen 'Bundle' Brent"
    ARIADNE_OLIVER = "Ariadne Oliver"
    TOMMY_BERESFORD = "Tommy Beresford"
    TUPPENCE_BERESFORD = "Tuppence Beresford"


class SetState(str, enum.Enum):
    PENDING_SELECTION = "Pending Selection"
    RESOLVED = "Resolved"
    FAILED = "Failed"
    CANCELLED = "Cancelled"


class SetEffect(str, enum.Enum):
    REVEAL_BY_ACTOR = "Reveal by Actor"
    REVEAL_BY_TARGET = "Reveal by Target"
    HIDE = "Hide"
    STEAL = "Steal"


class SetPlay(Base):
    __tablename__ = "set_plays"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("games.id"), nullable=False
    )
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("players.id"), nullable=False
    )
    set_type: Mapped[SetType] = mapped_column(Enum(SetType), nullable=False)
    state: Mapped[SetState] = mapped_column(
        Enum(SetState), default=SetState.PENDING_SELECTION
    )
    effect: Mapped[SetEffect] = mapped_column(Enum(SetEffect), nullable=False)
    wildcard: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    game: Mapped["Game"] = relationship("Game", back_populates="sets")
    owner = relationship(
        "Player", foreign_keys=[owner_id], back_populates="owned_sets"
    )
    cards: Mapped[List["GameCards"]] = relationship(
        "GameCards", back_populates="set"
    )

# TYPE_CHECKING imports at the bottom
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_model import Game
    from .game_cards_model import GameCards