from sqlalchemy.orm import Session
from models.set_model import SetPlay 
from repositories.game_cards_repository import GameCardsRepository

class SetRepository:
    def __init__(self, db: Session):
        self.db = db
        self.game_cards_repo = GameCardsRepository(db)

    def get_by_id(self, set_id: int):
        return (
             self.db.query(SetPlay).filter(SetPlay.id == set_id).first()
        )

    def get_by_game_id(self, game_id: int):
        return (
            self.db.query(SetPlay)
            .filter(SetPlay.game_id == game_id)
            .all()
        )
    
    def get_by_player_id(self, game_id: int, player_id: int):
        return (
            self.db.query(SetPlay)
            .filter(SetPlay.game_id == game_id, SetPlay.owner_id == player_id)
            .all()
        )

    def add_detective(self, player_id: int, set_id: int, game_card_id: int):
        sett = self.get_by_id(set_id)
        if not sett:
            return False
        detective_card = self.game_cards_repo.get_by_id(game_card_id)
        if not detective_card:
            return False
        detective_card.set_id = set_id
        detective_card.owner_id = player_id
        sett.cards.append(detective_card)
        self.db.commit()
        self.db.refresh(sett)
        return True

