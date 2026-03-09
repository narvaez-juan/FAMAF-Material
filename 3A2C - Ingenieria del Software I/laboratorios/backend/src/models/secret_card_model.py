"""Modelo para representar cartas de tipo Secreto."""

from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from enum import Enum as PyEnum
from db import Base
from typing import Optional



class TipoSecreto(PyEnum):
    MURDERER = "Murderer"
    ACCOMPLICE = "Accomplice"
    OTRO= "Otro"


class Secret(Base):
    """
    Representa un secreto asignado a un jugador dentro de una partida.
    """

    __tablename__ = "secrets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    secret_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    secret_type = Column(Enum(TipoSecreto, values_callable=lambda e: [x.value for x in e]), nullable=False)
    revealed = Column(Boolean, default=False)
    image = Column(String, default="")

    player_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("players.id"), nullable=True)
    game_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("games.id"), nullable=True)

    # Relaciones con otras entidades
    player = relationship("Player", back_populates="secrets")
    game = relationship("Game", back_populates="secrets")