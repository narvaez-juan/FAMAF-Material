from sqlalchemy.orm import Session
from repositories.game_cards_repository import GameCardsRepository
from repositories.game_repository import GameRepository
from repositories.player_repository import PlayerRepository
from repositories.set_repository import SetRepository
from models.set_model import SetPlay, SetType, SetState, SetEffect
from models.card_model import CardType
from models.game_cards_model import GameCards, CardLocation
from models.game_action_model import GameAction, GameActionType
from realtime.sockets import sio
from services.secret_card_service import SecretService
from services.game_events import emit_action_event
from services.card_events import emit_player_sets, emit_all_sets, emit_player_hand, emit_set_effects
from fastapi import HTTPException
from services.exceptions import (
    GameNotFoundError,
    PlayerNotFoundError,
    PlayerNotInGameError,
    SetNotFoundError,
    badRequestError
)

def is_poirot_set(cards: list[GameCards]) -> bool:
    """Check if the set of cards matches the Hercule Poirot set criteria."""
    if len(cards) != 3:
        return False
    owners = {gc.owner_id for gc in cards}
    if len(owners) != 1:
        return False
    if not any(gc.card.image.startswith("07") for gc in cards):
        return False
    if not all(
        gc.card.image.startswith("07") or gc.card.image.startswith("14") for gc in cards
    ):
        return False
    if not all(gc.card.type == CardType.DET for gc in cards):
        return False

    return True


def is_marple_set(cards: list[GameCards]) -> bool:
    """Check if the set of cards matches the Miss Marple set criteria."""
    if len(cards) != 3:
        return False
    owners = {gc.owner_id for gc in cards}
    if len(owners) != 1:
        return False
    if not any(gc.card.image.startswith("08") for gc in cards):
        return False
    if not all(
        gc.card.image.startswith("08") or gc.card.image.startswith("14") for gc in cards
    ):
        return False
    if not all(gc.card.type == CardType.DET for gc in cards):
        return False

    return True


def is_satterthwaite_set(cards: list[GameCards]) -> bool:
    """Check if the set of cards matches the Satterthwaite set criteria."""
    if len(cards) != 2:
        return False
    owners = {gc.owner_id for gc in cards}
    if len(owners) != 1:
        return False
    if not any(gc.card.image.startswith("09") for gc in cards):
        return False
    if not all(
        gc.card.image.startswith("09") or gc.card.image.startswith("14") for gc in cards
    ):
        return False
    if not all(gc.card.type == CardType.DET for gc in cards):
        return False

    return True


def is_pyne_set(cards: list[GameCards]) -> bool:
    """Check if the set of cards matches the Pyne set criteria."""
    if len(cards) != 2:
        return False
    owners = {gc.owner_id for gc in cards}
    if len(owners) != 1:
        return False
    if not any(gc.card.image.startswith("10") for gc in cards):
        return False
    if not all(
        gc.card.image.startswith("10") or gc.card.image.startswith("14") for gc in cards
    ):
        return False
    if not all(gc.card.type == CardType.DET for gc in cards):
        return False

    return True


def is_brent_set(cards: list[GameCards]) -> bool:
    """Check if the set of cards matches the Brent set criteria."""
    if len(cards) != 2:
        return False
    owners = {gc.owner_id for gc in cards}
    if len(owners) != 1:
        return False
    if not any(gc.card.image.startswith("11") for gc in cards):
        return False
    if not all(
        gc.card.image.startswith("11") or gc.card.image.startswith("14") for gc in cards
    ):
        return False
    if not all(gc.card.type == CardType.DET for gc in cards):
        return False

    return True


def is_tommy_set(cards: list[GameCards]) -> bool:
    """Check if the set of cards matches the Tommy set criteria."""
    if len(cards) != 2:
        return False
    owners = {gc.owner_id for gc in cards}
    if len(owners) != 1:
        return False
    if not any(gc.card.image.startswith("12") for gc in cards):
        return False
    if not all(
        gc.card.image.startswith("12") or gc.card.image.startswith("13") or gc.card.image.startswith("14") for gc in cards
    ):
        return False
    if not all(gc.card.type == CardType.DET for gc in cards):
        return False

    return True


def is_tuppence_set(cards: list[GameCards]) -> bool:
    """Check if the set of cards matches the Tuppence set criteria."""
    if len(cards) != 2:
        return False
    owners = {gc.owner_id for gc in cards}
    if len(owners) != 1:
        return False
    if not any(gc.card.image.startswith("13") for gc in cards):
        return False
    if not all(
        gc.card.image.startswith("13") or gc.card.image.startswith("14") for gc in cards
    ):
        return False
    if not all(gc.card.type == CardType.DET for gc in cards):
        return False

    return True

def is_ariadne_set(cards: list[GameCards]) -> bool:
    """Check if the set of cards matches the Ariadne set criteria"""
    if len(cards) != 1:
        return False
    owners = {gc.owner_id for gc in cards}
    if len(owners) != 1:
        return False
    if not any(gc.card.image.startswith("15") for gc in cards):
        return False
    if not all(gc.card.image.startswith("15") for gc in cards):
        return False
    return True

class SetService:
    def __init__(self, db: Session):
        self._db = db
        self.repo_game_cards = GameCardsRepository(db)
        self.game_repo = GameRepository(db)
        self.player_repo = PlayerRepository(db)
        self.repo = SetRepository(db)
        self.secret_service = SecretService(db)
        self.sio = sio 

    def get_set_type(self, cards: list[GameCards]) -> SetType | None:
        """Determine the set type based on the provided cards."""
        if is_poirot_set(cards):
            return SetType.HERCULE_POIROT
        if is_marple_set(cards):
            return SetType.MISS_MARPLE
        if is_satterthwaite_set(cards):
            return SetType.MR_SATTERTHWAITE
        if is_pyne_set(cards):
            return SetType.PARKER_PYNE
        if is_brent_set(cards):
            return SetType.LADY_EILEEN_BUNDLE_BRENT
        if is_tommy_set(cards):
            return SetType.TOMMY_BERESFORD
        if is_tuppence_set(cards):
            return SetType.TUPPENCE_BERESFORD
        if is_ariadne_set(cards):
            return SetType.ARIADNE_OLIVER
        return None
    
    def get_set_effect(self, set_type: SetType, has_wildcard: bool) -> SetEffect:
        """Get the effect associated with a set type."""
        if set_type in {SetType.HERCULE_POIROT, SetType.MISS_MARPLE}:
            return SetEffect.REVEAL_BY_ACTOR
        elif set_type in {SetType.MR_SATTERTHWAITE} and has_wildcard:
            return SetEffect.STEAL
        elif set_type in {
            SetType.MR_SATTERTHWAITE,
            SetType.LADY_EILEEN_BUNDLE_BRENT,
            SetType.TOMMY_BERESFORD,
            SetType.TUPPENCE_BERESFORD,
            SetType.ARIADNE_OLIVER,
        }:
            return SetEffect.REVEAL_BY_TARGET
        elif set_type in {
            SetType.PARKER_PYNE,
        }:
            return SetEffect.HIDE
        return SetEffect.NONE
    
    def has_wildcard_card(self, cards: list[GameCards]) -> bool:
        """Check if the set contains the wildcard card (14-detective_quin.png)."""
        return any(card.card.image == "14-detective_quin.png" for card in cards)
    
    async def join_ariadne_to_set(
        self,
        game_id: int,
        ariadne_card_id: int,
        target_set_id: int,
        player_id: int,
    ):
        
        # Validar set objetivo
        target_set = self.repo.get_by_id(target_set_id)
        if not target_set:
            raise HTTPException(status_code=404, detail="Set objetivo no encontrado")

        # Validar carta de Ariadne
        card = self.repo_game_cards.get_by_id(ariadne_card_id)
        if not card or card.card.image != "15-detective_oliver.png":
            raise HTTPException(status_code=400, detail="La carta no es Ariadne o no existe")


        # Asociar la carta al set
        card.set_id = target_set.id
        card.location = CardLocation.SET
        self._db.add(card)
        self._db.commit()

        # Emitir evento para que el dueño del set revele una carta
        await self.sio.emit(
            "select_secret_request",
            {
                "game_id": game_id,
                "set_play_id": target_set.id,
                "requester_id": player_id,
                "target_player_id": target_set.owner_id,
                "steal": False,
                "effect": "REVEAL"
            },
            room=f"game:{game_id}",
        )

        await emit_player_sets(game_id, player_id, self._db)
        await emit_player_hand(game_id, player_id, self._db)
        await emit_all_sets(game_id, self._db)

    async def create_set(self, card_ids: list[int], owner_id: int, game_id: int) -> SetPlay:
        """Create a new set if the cards meet the criteria."""
        cards = self.repo_game_cards.get_cards_for_set(card_ids, owner_id, game_id)

        if len(cards) != len(card_ids):
            raise ValueError(
                "Some cards are invalid or do not belong to the specified owner in the given game."
            )

        set_type = self.get_set_type(cards)
        if not set_type:
            raise ValueError("The provided cards do not form a valid set.")

        has_wildcard = self.has_wildcard_card(cards)

        set_effect = self.get_set_effect(set_type, has_wildcard)
        if not set_effect:
            raise ValueError("Could not determine the effect for the set type.")
        
        if set_type == SetType.ARIADNE_OLIVER:
            await self.sio.emit(
                "choose_target_for_ariadne",
                {
                    "game_id": game_id,
                    "owner_id": owner_id,
                    "card_ids": card_ids,
                },
                room=f"game:{game_id}",
            )
            return None

        new_set = SetPlay(
            game_id=game_id,
            owner_id=owner_id,
            set_type=set_type,
            state=SetState.PENDING_SELECTION,
            effect=set_effect,
            wildcard=has_wildcard,
        )
        self._db.add(new_set)
        self._db.commit()
        self._db.refresh(new_set)

        for card in cards:
            card.set_id = new_set.id
            card.location = CardLocation.SET
            self._db.add(card)

        self._db.commit()

        await emit_player_sets(game_id, owner_id, self._db)
        await emit_all_sets(game_id, self._db)
        await emit_player_hand(game_id, owner_id, self._db)
        await emit_set_effects(new_set, game_id, card_ids)

        return new_set
    
    async def play_set(
        self,
        game_id: int,
        set_id: int,
        target_player_id: int,
        chosen_secret_id: int = None,
        chosen_set_id: int = None,
    ):    
        # Validation
        game = self.game_repo.get_by_id(game_id)
        if not game:
            raise GameNotFoundError("Game not found")

        target_player = self.player_repo.get_player_by_id(target_player_id)
        if not target_player:
            raise PlayerNotFoundError("Target player not found")

        if target_player.game_id != game_id:
            raise PlayerNotInGameError("Target player does not belong to the game")

        sett = self.repo.get_by_id(set_id)
        if not sett:
            raise SetNotFoundError("Set not found")

        set_type = sett.set_type

        def ok_response():
            return {"status": "ok", "set_play_id": set_id}

        def pending_response():
            return {
                "status": "pending_selection",
                "set_play_id": set_id,
                "message": "Waiting for target player to choose a secret",
            }

        # Poirot / Marple
        if set_type in {SetType.HERCULE_POIROT, SetType.MISS_MARPLE}:
            if not chosen_secret_id:
                raise badRequestError("chosen_secret_id is required for Poirot/Marple")
            await self.secret_service.update_secret_state_service(
                game_id, target_player_id, chosen_secret_id, "REVEAL"
            )
            await emit_action_event(
                db=self._db,
                game_id=game_id,
                actor_id=sett.owner_id,
                action_type=GameActionType.REVEAL_SECRET,
                description=f"{sett.owner.name} played {set_type.value} set to reveal a secret card from {target_player.name}",
                secret_id=chosen_secret_id,
            )
            return ok_response()

        # Parker Pyne
        if set_type == SetType.PARKER_PYNE:
            if not chosen_secret_id:
                raise badRequestError("chosen_secret_id is required for Parker Pyne")
            await self.secret_service.update_secret_state_service(
                game_id, target_player_id, chosen_secret_id, "HIDE"
            )
            await emit_action_event(
                db=self._db,
                game_id=game_id,
                actor_id=sett.owner_id,
                action_type=GameActionType.HIDE_SECRET,
                description=f"{sett.owner.name} played {set_type.value} set to hide a {target_player.name}'s secret card",
                secret_id=chosen_secret_id,
            )
            return ok_response()

        # Ariadne Oliver
        if set_type == SetType.ARIADNE_OLIVER:
            if not chosen_set_id:
                raise badRequestError("chosen_set_id is required for Ariadne Oliver")
            ariadne_game_card = next(
                (x for x in sett.cards if x.card.image == "15-detective_oliver.png"), None
            )
            if not ariadne_game_card:
                raise badRequestError("Ariadne card not present in the played set")
            # add to the target set (chosen_set_id)
            self.repo.add_detective(target_player_id, chosen_set_id, ariadne_game_card.id)
            await emit_all_sets(game_id, self._db)
            await self.sio.emit(
                "select_secret_request",
                {
                    "game_id": game_id,
                    "set_play_id": set_id,
                    "requester_id": sett.owner_id,
                    "target_player_id": target_player_id,
                    "steal": False,
                    "effect": "REVEAL"
                },
                room=f"game:{game_id}",
            )
            await emit_action_event(
                db=self._db,
                game_id=game_id,
                actor_id=sett.owner_id,
                action_type=GameActionType.JOIN_SET,
                description=f"{sett.owner.name} added {set_type.value} to a {target_player.name}'s set",
                secret_id=chosen_secret_id,
            )
            return pending_response()

        # Mr.Sarrerthwaite with Wildcard
        if set_type == SetType.MR_SATTERTHWAITE and sett.wildcard:
            # await SecretService(db).steal_secret(game_id, player_id: int, target_player_id, chosen_secret_id)
            await self.sio.emit(
                "select_secret_request",
                {
                    "game_id": game_id, 
                    "set_play_id": set_id, 
                    "requester_id": sett.owner_id, 
                    "target_player_id": target_player_id, 
                    "steal": True,
                    "effect": "REVEAL"
                },
                room=f"game:{game_id}",
            )

            await emit_action_event(
                db=self._db,
                game_id=game_id,
                actor_id=sett.owner_id,
                action_type=GameActionType.PLAY_SET,
                description=f"{sett.owner.name} played {set_type.value} + Harley Quinn Wildcard to steal a secret card from {target_player.name}",
            )
            return pending_response()

        # default (Lady Brent, Tommy, Tuppence)
        await self.sio.emit(
            "select_secret_request",
            {
                "game_id": game_id, 
                "set_play_id": set_id, 
                "requester_id": sett.owner_id, 
                "target_player_id": target_player_id, 
                "steal": False,
                "effect": "REVEAL"    
            },
            room=f"game:{game_id}",
        )

        await emit_action_event(
            db=self._db,
            game_id=game_id,
            actor_id=sett.owner_id,
            action_type=GameActionType.PLAY_SET,
            description=f"{sett.owner.name} played {set_type.value} targeting {target_player.name}, who must reveal a secret",
        )
        
        return pending_response()
    
    async def steal_set(
        self,
        game_id: int,
        player_id: int,
        chosen_set_id: int,
    ):

        game = self.game_repo.get_by_id(game_id)
        if not game:
            raise GameNotFoundError("Game not found")

        player = self.player_repo.get_player_by_id(player_id)
        if not player:
            raise PlayerNotFoundError("Player not found")

        sett = self.repo.get_by_id(chosen_set_id)
        if not sett:
            raise SetNotFoundError("Set not found")
        
        if sett.owner_id == player_id:
            raise badRequestError("Player cannot steal their own set")
        
        sett.owner_id = player_id
        self._db.commit()
        self._db.refresh(sett)

        await emit_player_sets(game_id, player_id, self._db)
        await emit_all_sets(game_id, self._db)

    async def join_detective_to_set(
            self,
            game_id: int,
            detective_card_id: int,
            target_set_id: int,
            player_id: int,
        ):
            WILDCARD_PREFIX = "14"


            target_set = self.repo.get_by_id(target_set_id)
            if not target_set:
                raise HTTPException(status_code=404, detail="Set not found")

            if target_set.game_id != game_id:
                raise HTTPException(status_code=400, detail="Set does not belong to this game")

            if target_set.owner_id != player_id:
                raise HTTPException(status_code=400, detail="Set does not belong to that player")


            card = self.repo_game_cards.get_by_id(detective_card_id)
            if not card:
                raise HTTPException(status_code=404, detail="Detective card not found")

            if card.owner_id != player_id or card.location != CardLocation.HAND:
                raise HTTPException(status_code=400, detail="Card does not belong to player or is not in their hand")


            set_cards = self.repo_game_cards.get_cards_in_set(target_set_id)
            if not set_cards:
                raise HTTPException(status_code=400, detail="Set has no cards")

            set_card_prefix = None
            set_has_wildcard = False
            for set_card in set_cards:
                img = getattr(set_card.card, "image", None)
                if not img:
                    continue
                prefix = img.split("-")[0]
                if prefix == WILDCARD_PREFIX:
                    set_has_wildcard = True
                    continue
                set_card_prefix = prefix
                break

            detective_img = getattr(card.card, "image", None)
            if not detective_img:
                raise HTTPException(status_code=400, detail="Detective card image metadata missing")
            new_card_prefix = detective_img.split("-")[0]

            if set_has_wildcard:
                if new_card_prefix != set_card_prefix:
                    raise HTTPException(status_code=400, detail="When a set used a wildcard, you must add the non-wildcard detective of the set type")
            else:
                if new_card_prefix != set_card_prefix and new_card_prefix != WILDCARD_PREFIX:
                    raise HTTPException(status_code=400, detail="Detective card does not match the set type")

            try:
                self.repo.add_detective(player_id, target_set_id, detective_card_id)
                self._db.refresh(target_set)

            except Exception:
                try:
                    self._db.rollback()
                except Exception:
                    raise HTTPException(status_code=500, detail="Failed to add detective to set")


            await emit_player_sets(game_id, player_id, self._db)
            await emit_player_hand(game_id, player_id, self._db)
            await emit_all_sets(game_id, self._db)

            return target_set