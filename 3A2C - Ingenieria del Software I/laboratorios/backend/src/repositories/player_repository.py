from models.player_model import Player
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload

class PlayerRepository:
    def __init__(self, db):
        self._db = db

    def get_player_by_id(self, player_id: int)-> Player:
        return self._db.query(Player).filter(Player.id == player_id).first()

    # Función global (se importa directo desde el módulo)
def search_player_by_id(db, player_id: int, game_id: int) -> Player:
    player = (
        db.query(Player)
        .options(joinedload(Player.game))
        .filter(Player.id == player_id, Player.game_id == game_id)
        .first()
    )
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="the player does not exist",
        )
    return player
    
