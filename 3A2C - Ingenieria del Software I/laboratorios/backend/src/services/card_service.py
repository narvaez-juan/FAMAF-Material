from repositories.game_repository import GameRepository
from repositories.player_repository import search_player_by_id
from repositories.card_repository import get_next_discard_order
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schemas.card_schema import DiscardActionResponse
from schemas.game_schema import PlayerTurnInfo
from .card_events import emit_player_hand, emit_discard_pile
from models.card_model import Card
from models.game_cards_model import GameCards, CardLocation
from .game_events import emit_turn_info_event
from .effect_cards_events import CardsEventsEffects

class CardService:
    def __init__(self, db: Session):
        self._db = db
        self.GameRepo = GameRepository(db)
        self.CardEventsEffects = CardsEventsEffects(db)

    async def discard_card(
        self, cards_ids: list[int], player_id: int, game_id: int
    ) -> DiscardActionResponse:

        db_game = self.GameRepo.get_by_id(game_id)
        if not db_game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Game not found"
            )

        if not db_game.in_game:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="The game has not started yet"
            )

        if not cards_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="No cards were provided to discard"
            )

        player = search_player_by_id(self._db, player_id, game_id)

        if player.turn != db_game.current_turn:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="It is not your turn"
            )

        # Obtener el próximo orden de descarte
        next_order = get_next_discard_order(self._db, game_id)

        discarded_cards = []
        for cid in cards_ids:
            game_card = (
                self._db.query(GameCards)
                .filter(GameCards.id == cid, GameCards.owner_id == player_id)
                .first()
            )
            if not game_card:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="The card was not founded or the card is not yours"
                )

            if game_card.card.image == "24-event_earlytrain.png":
                await self.CardEventsEffects.play_early_train_to_paddington(
                    game_id=game_id,
                    player_id=player_id,
                    event_card_id=game_card.id
                )
                continue

            game_card.location = CardLocation.DISCARD
            game_card.owner_id = None
            game_card.discard_order = next_order
            next_order += 1
            discarded_cards.append(game_card.id)    

        self._db.commit()

        # Obtener mano actualizada
        updated_hand = (
            self._db.query(GameCards)
            .filter(GameCards.owner_id == player_id, GameCards.location == CardLocation.HAND.value)
            .all()
        )
        updated_hand_ids = [gc.card_id for gc in updated_hand]

        # Emitir eventos
        await emit_player_hand(game_id, player_id, self._db)
        await emit_discard_pile(game_id, self._db)

        return DiscardActionResponse(
            game_id=game_id,
            player_id=player_id,
            discarded_cards=discarded_cards,
            updated_hand=updated_hand_ids
        )

    def get_last_discarded(self, game_id: int) -> GameCards | None:
        return (
            self._db.query(GameCards)
            .filter(GameCards.location == CardLocation.DISCARD, GameCards.game_id == game_id)
            .order_by(GameCards.discard_order.desc())
            .first()
        )
