"""Repository for managing pending actions and counters."""

from sqlalchemy.orm import Session
from models.pending_action_model import PendingAction, ActionType, ActionStatus
from models.counter_model import Counter
from datetime import datetime, timedelta, timezone
from typing import Optional, List


class ActionRepository:
    """Repository for CRUD operations on PendingAction and Counter models."""
    
    def __init__(self, db: Session):
        self._db = db
    
    def create_pending_action(
        self,
        game_id: int,
        action_type: ActionType,
        initiator_player_id: int,
        action_payload: dict,
        target_player_id: Optional[int] = None,
        parent_action_id: Optional[int] = None,
        countdown_seconds: int = 5
    ) -> PendingAction:
        """Create a new pending action that enters the counter window."""
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(seconds=countdown_seconds)
        
        action = PendingAction(
            game_id=game_id,
            action_type=action_type.value,
            status=ActionStatus.PENDING.value,
            initiator_player_id=initiator_player_id,
            target_player_id=target_player_id,
            action_payload=action_payload,
            created_at=now,
            expires_at=expires_at,
            parent_action_id=parent_action_id
        )
        
        self._db.add(action)
        self._db.flush()
        return action
    
    def get_by_id(self, action_id: int) -> Optional[PendingAction]:
        """Get a pending action by ID."""
        return self._db.query(PendingAction).filter(PendingAction.id == action_id).first()
    
    def get_pending_actions_by_game(self, game_id: int) -> List[PendingAction]:
        """Get all actions still in counter window for a game."""
        return (
            self._db.query(PendingAction)
            .filter(
                PendingAction.game_id == game_id,
                PendingAction.status.in_([ActionStatus.PENDING.value, ActionStatus.COUNTER_PENDING.value])
            )
            .all()
        )
    
    def add_counter(
        self,
        action_id: int,
        player_id: int,
        nsf_game_card_id: int
    ) -> Counter:
        """Add a counter to an action: create Counter, update action status and reset timer."""
        action = self.get_by_id(action_id)
        if not action:
            raise ValueError(f"Action {action_id} not found")
        
        if action.status not in [ActionStatus.PENDING.value, ActionStatus.COUNTER_PENDING.value]:
            raise ValueError(f"Action {action_id} is not in a counterable state (status: {action.status})")
        
        existing_counters = self._db.query(Counter).filter(Counter.action_id == action_id).count()
        chain_position = existing_counters + 1
        
        counter = Counter(
            action_id=action_id,
            player_id=player_id,
            nsf_game_card_id=nsf_game_card_id,
            played_at=datetime.now(timezone.utc),
            chain_position=chain_position
        )
        
        self._db.add(counter)
        
    
        action.status = ActionStatus.COUNTER_PENDING.value
        action.expires_at = datetime.now(timezone.utc) + timedelta(seconds=5)
        
        self._db.flush()
        return counter
    
    def resolve_action(self, action_id: int, final_status: ActionStatus):
        """Mark action as resolved/cancelled/expired."""
        action = self.get_by_id(action_id)
        if action:
            action.status = final_status.value
            action.resolved_at = datetime.now(timezone.utc)
            self._db.flush()
    
    def get_expired_actions(self) -> List[PendingAction]:
        """Get actions whose counter window has expired."""
        now = datetime.now(timezone.utc)
        return (
            self._db.query(PendingAction)
            .filter(
                PendingAction.status.in_([
                    ActionStatus.PENDING.value, 
                    ActionStatus.COUNTER_PENDING.value
                ]),
                PendingAction.expires_at < now
            )
            .all()
        )
    
    def get_counters_for_action(self, action_id: int) -> List[Counter]:
        """Get all counters for a specific action, ordered by chain position."""
        return (
            self._db.query(Counter)
            .filter(Counter.action_id == action_id)
            .order_by(Counter.chain_position)
            .all()
        )
