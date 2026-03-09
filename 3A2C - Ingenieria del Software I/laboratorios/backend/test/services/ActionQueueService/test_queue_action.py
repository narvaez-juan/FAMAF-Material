import enum
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
src = root / "src"
sys.path.insert(0, str(src))

import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from services.action_queue_service import ActionQueueService
from models.pending_action_model import PendingAction, ActionType, ActionStatus
from models.counter_model import Counter
from models.game_cards_model import CardLocation
from models.card_model import CardType
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_queue_action_success(action_queue_service, mock_action_repo, mock_db_session):
    """Test successful action queuing"""

    game_id = 1
    action_type = ActionType.PLAY_SET
    initiator_id = 1
    payload = {"set_id": 1, "target_player_id": 2}
    target_id = 2

    mock_action = MagicMock(spec=PendingAction)
    mock_action.id = 1
    mock_action.game_id = game_id
    mock_action.action_type = action_type
    mock_action.initiator_player_id = initiator_id
    mock_action.target_player_id = target_id

    mock_action_repo.create_pending_action.return_value = mock_action


    with patch.object(action_queue_service, '_emit_action_pending', new_callable=AsyncMock) as mock_emit:

        result = await action_queue_service.queue_action(
            game_id=game_id,
            action_type=action_type,
            initiator_player_id=initiator_id,
            action_payload=payload,
            target_player_id=target_id
        )


        assert result == mock_action
        mock_action_repo.create_pending_action.assert_called_once_with(
            game_id=game_id,
            action_type=action_type,
            initiator_player_id=initiator_id,
            action_payload=payload,
            target_player_id=target_id,
            parent_action_id=None
        )
        mock_db_session.commit.assert_called_once()
        mock_emit.assert_called_once_with(game_id, mock_action)


@pytest.mark.asyncio
async def test_queue_action_with_parent(action_queue_service, mock_action_repo, mock_db_session):
    """Test queuing action with parent action ID"""

    game_id = 1
    action_type = ActionType.STEAL_SET
    initiator_id = 2
    payload = {"set_id": 1}
    target_id = 1
    parent_id = 5

    mock_action = MagicMock(spec=PendingAction)
    mock_action.id = 2

    mock_action_repo.create_pending_action.return_value = mock_action

    with patch.object(action_queue_service, '_emit_action_pending', new_callable=AsyncMock):

        result = await action_queue_service.queue_action(
            game_id=game_id,
            action_type=action_type,
            initiator_player_id=initiator_id,
            action_payload=payload,
            target_player_id=target_id,
            parent_action_id=parent_id
        )


        mock_action_repo.create_pending_action.assert_called_once_with(
            game_id=game_id,
            action_type=action_type,
            initiator_player_id=initiator_id,
            action_payload=payload,
            target_player_id=target_id,
            parent_action_id=parent_id
        )