from models.game_model import Game
from models.player_model import Player
from typing import Optional
from models.game_model import Game

class GameRepository:

    def __init__(self, db):
        self._db = db

    def get_by_name(self, name: str) -> Optional[Game]:
        return self._db.query(Game).filter(Game.name == name).first()

    def get_by_id(self, game_id: int) -> Optional[Game]:
        return self._db.query(Game).filter(Game.id == game_id).first()

    def get_players(self, game_id: int) -> list[Player]:
        return (
            self._db.query(Player)
            .filter(Player.game_id == game_id)
            .order_by(Player.turn)
            .all()
        )

    def get_games(self) -> list[Game]:
        return (
            self._db.query(Game)
            .filter(Game.in_game == False, Game.players_amount < Game.max_players)
            .all()
        )

