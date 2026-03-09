"""Service for managing NSF action queue and counter resolution."""

from sqlalchemy.orm import Session
from repositories.action_repository import ActionRepository
from repositories.game_cards_repository import GameCardsRepository
from models.pending_action_model import PendingAction, ActionType, ActionStatus
from models.counter_model import Counter
from models.game_cards_model import CardLocation
from models.card_model import CardType
from services.exceptions import GameServiceError
from realtime.sockets import sio
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from services.set_services import SetService
from services.card_events import (
    emit_player_hand,
    emit_discard_pile,
    emit_all_sets,
    emit_dead_card_folly_event,
    emit_set_effects,
)


class ActionCancelledException(GameServiceError):
    """Raised when an action is cancelled by NSF"""
    pass


class ActionQueueService:
    def __init__(self, db: Session):
        self._db = db
        self.action_repo = ActionRepository(db)
        self.game_cards_repo = GameCardsRepository(db)
        self.sio = sio
    
    async def queue_action(
        self,
        game_id: int,
        action_type: ActionType,
        initiator_player_id: int,
        action_payload: dict,
        target_player_id: Optional[int] = None,
        parent_action_id: Optional[int] = None
    ) -> PendingAction:
        action = self.action_repo.create_pending_action(
            game_id=game_id,
            action_type=action_type,
            initiator_player_id=initiator_player_id,
            action_payload=action_payload,
            target_player_id=target_player_id,
            parent_action_id=parent_action_id
        )
        
        self._db.commit()
        
        await self._emit_action_pending(game_id, action)
        
        return action
    
    async def play_counter(
        self,
        action_id: int,
        player_id: int,
        nsf_game_card_id: int,
        game_id: int
    ) -> Dict[str, Any]:
        action = self.action_repo.get_by_id(action_id)
        if not action:
            raise ValueError("Action not found")
        
        if action.game_id != game_id:
            raise ValueError("Action does not belong to this game")
        
        if action.status not in [ActionStatus.PENDING.value, ActionStatus.COUNTER_PENDING.value]:
            raise ValueError("Action is no longer counterable")
        
        if action.expires_at < datetime.utcnow():
            raise ValueError("Counter window has expired")
        
        nsf_card = self.game_cards_repo.get_by_id(nsf_game_card_id)
        if not nsf_card:
            raise ValueError("NSF card not found")
        
        if nsf_card.owner_id != player_id:
            raise ValueError("NSF card does not belong to player")
        
        if nsf_card.location != CardLocation.HAND:
            raise ValueError("NSF card is not in player's hand")
        
        if nsf_card.card.type != CardType.NSF:
            raise ValueError("Card is not a 'Not So Fast' card")
        
        # Check if player played the last counter in the chain
        existing_counters = self.action_repo.get_counters_for_action(action_id)
        if existing_counters:
            last_counter = existing_counters[-1]
            if player_id == last_counter.player_id:
                raise ValueError("Cannot counter your own counter")
        else:
            # If no counters exist yet, check if player is the action initiator
            if player_id == action.initiator_player_id:
                raise ValueError("Cannot counter your own action")
        
        counter = self.action_repo.add_counter(
            action_id=action_id,
            player_id=player_id,
            nsf_game_card_id=nsf_game_card_id
        )
        
        nsf_card.location = CardLocation.DISCARD
        nsf_card.owner_id = None
        next_order = self._get_next_discard_order(game_id)
        nsf_card.discard_order = next_order
        
        self._db.commit()
        
        await self._emit_counter_played(game_id, action, counter)
        
        return {
            "counter_id": counter.id,
            "chain_position": counter.chain_position,
            "new_expires_at": action.expires_at.isoformat()
        }
    
    async def resolve_action_window(self, action_id: int) -> ActionStatus:

        action = self.action_repo.get_by_id(action_id)
        if not action:
            raise ValueError("Action not found")
        
  
        
        counter_count = len(action.counters)
        
        
        if counter_count == 0:
            final_status = ActionStatus.RESOLVED
        elif counter_count % 2 == 0:
            final_status = ActionStatus.RESOLVED
        else:
            final_status = ActionStatus.CANCELLED
                
        self.action_repo.resolve_action(action_id, final_status)
        self._db.flush() 
        
        await self._emit_action_resolved(action.game_id, action, final_status, counter_count)
        
        if final_status == ActionStatus.RESOLVED:
            await self._execute_resolved_action(action)
        elif final_status == ActionStatus.CANCELLED:
            await self._handle_cancelled_action(action)
        
        
        return final_status
    
    async def _execute_resolved_action(self, action: PendingAction):
        try:
            if action.action_type == ActionType.PLAY_SET.value:
                await self._execute_play_set(action)
            elif action.action_type == ActionType.PROCESS_SET.value:
                await self._execute_process_set(action)
            elif action.action_type == ActionType.STEAL_SECRET.value:
                await self._execute_steal_secret(action)
            elif action.action_type == ActionType.STEAL_SET.value:
                await self._execute_steal_set(action)
            elif action.action_type == ActionType.DEAD_CARD_FOLLY.value:
                await self._execute_dead_card_folly(action)
            
        except Exception as e:
            print(f"Failed to execute action {action.id}: {e}")
    
    async def _execute_play_set(self, action: PendingAction):
        """Execute a PLAY_SET action."""
        payload = action.action_payload or {}
        set_service = SetService(self._db)
        
        await set_service.play_set(
            game_id=action.game_id,
            set_id=payload.get("set_id"),
            target_player_id=payload.get("target_player_id"),
            chosen_secret_id=payload.get("chosen_secret_id"),
            chosen_set_id=payload.get("chosen_set_id")
        )
    
    async def _execute_process_set(self, action: PendingAction):
        from models.set_model import SetPlay

        payload = action.action_payload or {}
        set_id = payload.get("set_id")
        
        
        if not set_id:
            raise ValueError("set_id missing from PROCESS_SET payload")
        
        set_service = SetService(self._db)
        sett = set_service.repo.get_by_id(set_id)
        
        if not sett:
            raise ValueError(f"Set {set_id} not found")
        
        
        card_ids = payload.get("card_ids", [])
        await emit_set_effects(sett, action.game_id, card_ids, action_id=action.id)
    
    async def _execute_steal_secret(self, action: PendingAction):
        """Execute a STEAL_SECRET action."""
        # TODO: Implement when steal_secret is integrated
        pass
    
    async def _execute_steal_set(self, action: PendingAction):
        """Execute a STEAL_SET action."""
        # TODO: Implement when steal_set is integrated
        pass
    
    async def _execute_dead_card_folly(self, action: PendingAction):
        from services.effect_cards_events import CardsEventsEffects
        


        payload = action.action_payload or {}
        player_id = payload.get("player_id")
        direction = payload.get("direction")
        cards_to_pass = payload.get("cards_to_pass", [])
        id_dead_card_folly = payload.get("id_dead_card_folly")
        
        
        service = CardsEventsEffects(self._db)
        
        dead_card_folly = self.game_cards_repo.get_card_by_id(id_dead_card_folly)
        if dead_card_folly:
            dead_card_folly.location = CardLocation.DISCARD
        
        cards_to_pass = [pair for pair in cards_to_pass if len(pair) > 1]
        
        participants = service.get_participants(action.game_id, cards_to_pass)
        
        if len(participants) < 2:
            self._db.flush()
            await emit_discard_pile(action.game_id, self._db)
            return
        
        
        new_owners = service.calculate_destination_of_the_card(
            participants, cards_to_pass, direction
        )
        
        
        for card_id, new_owner_id in new_owners.items():
            card = self.game_cards_repo.get_card_by_id(card_id)
            if card and card.location == CardLocation.HAND:
                old_owner = card.owner_id
                card.owner_id = new_owner_id
            else:
                print(f"[_execute_dead_card_folly] Card {card_id} not found or not in hand, skipping")
        self._db.flush()
        
        for player_id_iter in participants:
            await emit_player_hand(action.game_id, player_id_iter, self._db)
        
        await emit_discard_pile(action.game_id, self._db)
        
        await emit_dead_card_folly_event(action.game_id, player_id, direction)
        
    
    async def _handle_cancelled_action(self, action: PendingAction):

        try:
            if action.action_type == ActionType.PROCESS_SET.value:
                await self._cancel_process_set(action)
            elif action.action_type == ActionType.STEAL_SECRET.value:
                await self._cancel_steal_secret(action)
            elif action.action_type == ActionType.STEAL_SET.value:
                await self._cancel_steal_set(action)
            elif action.action_type == ActionType.DEAD_CARD_FOLLY.value:
                await self._cancel_dead_card_folly(action)
            
            await self._discard_counter_cards(action)
            
        except Exception as e:
            print(f"Failed to cancel action {action.id}: {e}", exc_info=True)
    
    async def _cancel_process_set(self, action: PendingAction):
        from models.set_model import SetPlay
        from models.game_cards_model import GameCards, CardLocation
        
        
        payload = action.action_payload or {}
        set_id = payload.get("set_id")
        
        if not set_id:
            return  
        
        sett = self._db.query(SetPlay).filter(SetPlay.id == set_id).first()
        if not sett:
            return  
        
        owner_id = sett.owner_id
        
        set_cards = (
            self._db.query(GameCards)
            .filter(
                GameCards.game_id == action.game_id,
                GameCards.set_id == set_id
            )
            .all()
        )
        
        for card in set_cards:
            card.location = CardLocation.HAND
            card.set_id = None
            card.discard_order = None
        
        self._db.delete(sett)
        self._db.flush()
        
        await emit_player_hand(action.game_id, owner_id, self._db)
        await emit_all_sets(action.game_id, self._db)
    
    async def _cancel_steal_secret(self, action: PendingAction):
        """Cancel a STEAL_SECRET action."""
        # TODO: Implement when steal_secret is integrated
        pass
    
    async def _cancel_steal_set(self, action: PendingAction):
        """Cancel a STEAL_SET action."""
        # TODO: Implement when steal_set is integrated
        pass
    
    async def _cancel_dead_card_folly(self, action: PendingAction):
        
        
        payload = action.action_payload or {}
        player_id = payload.get("player_id")
        id_dead_card_folly = payload.get("id_dead_card_folly")
        
        
        dead_card_folly = self.game_cards_repo.get_card_by_id(id_dead_card_folly)
        if dead_card_folly:
            dead_card_folly.location = CardLocation.DISCARD
        
        self._db.flush()
        
        await emit_player_hand(action.game_id, player_id, self._db)
        
        await emit_discard_pile(action.game_id, self._db)
        
    
    async def _discard_counter_cards(self, action: PendingAction):

        from models.game_cards_model import GameCards, CardLocation
        
        if not action.counters:
            return
        
        players_updated = set()
        
        for counter in action.counters:
            nsf_card = (
                self._db.query(GameCards)
                .filter(GameCards.id == counter.nsf_game_card_id)
                .first()
            )
            
            if nsf_card:
                nsf_card.location = CardLocation.DISCARD
                nsf_card.discard_order = self._get_next_discard_order(action.game_id)
                players_updated.add(counter.player_id)
        
        self._db.flush()
        
        for player_id in players_updated:
            await emit_player_hand(action.game_id, player_id, self._db)
    
    def _get_next_discard_order(self, game_id: int) -> int:
        """Get next discard pile order number."""
        from models.game_cards_model import GameCards
        
        last_discard = (
            self._db.query(GameCards)
            .filter(
                GameCards.location == CardLocation.DISCARD,
                GameCards.game_id == game_id
            )
            .order_by(GameCards.discard_order.desc())
            .first()
        )
        return last_discard.discard_order + 1 if last_discard and last_discard.discard_order else 1
    
    
    async def _emit_action_pending(self, game_id: int, action: PendingAction):

        from models.game_cards_model import GameCards
        
        nsf_cards = (
            self._db.query(GameCards)
            .filter(
                GameCards.game_id == game_id,
                GameCards.location == CardLocation.HAND
            )
            .join(GameCards.card)
            .filter(GameCards.card.has(type=CardType.NSF))
            .all()
        )
        
        nsf_player_ids = list(set(
            card.owner_id for card in nsf_cards 
            if card.owner_id is not None and card.owner_id != action.initiator_player_id
        ))
        
        payload = {
            "action_id": action.id,
            "action_type": action.action_type,
            "initiator_id": action.initiator_player_id,
            "target_id": action.target_player_id,
            "expires_at": action.expires_at.isoformat(),
            "countdown_seconds": 5,
            "eligible_players": nsf_player_ids,
            "action_description": self._get_action_description(action)
        }
        
        await self.sio.emit("action_pending", payload, room=f"game:{game_id}")
    
    async def _emit_counter_played(self, game_id: int, action: PendingAction, counter: Counter):
        """
        Notify everyone that a counter was played.
        
        This updates the counter chain display on all clients
        and resets the countdown timer.
        """
        payload = {
            "action_id": action.id,
            "counter_id": counter.id,
            "player_id": counter.player_id,
            "chain_position": counter.chain_position,
            "new_expires_at": action.expires_at.isoformat(),
            "countdown_reset": True
        }
        
        await self.sio.emit("counter_played", payload, room=f"game:{game_id}")
    
    async def _emit_action_resolved(
        self,
        game_id: int,
        action: PendingAction,
        final_status: ActionStatus,
        counter_count: int
    ):
        """
        Notify everyone about final resolution.
        
        This tells all clients whether the action succeeded or was cancelled.
        """
        payload = {
            "action_id": action.id,
            "status": final_status.value,
            "counter_count": counter_count,
            "action_type": action.action_type,
            "message": "Action succeeded" if final_status == ActionStatus.RESOLVED else "Action cancelled"
        }
        
        await self.sio.emit("action_resolved", payload, room=f"game:{game_id}")
    
    def _get_action_description(self, action: PendingAction) -> str:
        """
        Generate human-readable description for frontend display.
        
        Used in the counter window notification to tell players
        what action they can counter.
        """
        descriptions = {
            ActionType.PLAY_SET.value: "play a detective set",
            ActionType.PROCESS_SET.value: "apply set effect",
            ActionType.STEAL_SECRET.value: "steal a secret",
            ActionType.STEAL_SET.value: "steal a set",
            ActionType.ARIADNE_JOIN.value: "add Ariadne to a set",
            ActionType.UPDATE_SECRET.value: "reveal/hide a secret",
            ActionType.DEAD_CARD_FOLLY.value: "pass cards between players"
        }
        
        if action.action_type == ActionType.DEAD_CARD_FOLLY.value:
            payload = action.action_payload or {}
            direction = payload.get("direction", "unknown")
            cards_count = len(payload.get("cards_to_pass", []))
            return f"pass {cards_count} cards {direction}"
        
        return descriptions.get(action.action_type, "perform an action")
