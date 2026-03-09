import enum
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
src = root / "src"
sys.path.insert(0, str(src))

import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch, call
from services.action_queue_service import ActionQueueService
from models.pending_action_model import PendingAction, ActionType, ActionStatus
from models.counter_model import Counter
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_resolve_action_window_no_counters(action_queue_service, mock_action_repo, mock_db_session, sample_pending_action):
    """Test resolving action window with no counters (should succeed)"""

    action_id = 1
    counter_count = 0

    sample_pending_action.counters = []

    mock_action_repo.get_by_id.return_value = sample_pending_action


    with patch.object(action_queue_service, '_emit_action_resolved', new_callable=AsyncMock) as mock_emit, \
         patch.object(action_queue_service, '_execute_resolved_action', new_callable=AsyncMock) as mock_execute:


        result = await action_queue_service.resolve_action_window(action_id)


        assert result == ActionStatus.RESOLVED
        mock_action_repo.resolve_action.assert_called_once_with(action_id, ActionStatus.RESOLVED)
        mock_db_session.flush.assert_called_once()
        mock_emit.assert_called_once_with(1, sample_pending_action, ActionStatus.RESOLVED, counter_count)
        mock_execute.assert_called_once_with(sample_pending_action)


@pytest.mark.asyncio
async def test_resolve_action_window_even_counters(action_queue_service, mock_action_repo, mock_db_session, sample_pending_action):
    """Test resolving action window with even number of counters (should succeed)"""

    action_id = 1
    counter_count = 2


    counter1 = MagicMock(spec=Counter)
    counter2 = MagicMock(spec=Counter)
    sample_pending_action.counters = [counter1, counter2]

    mock_action_repo.get_by_id.return_value = sample_pending_action



    with patch.object(action_queue_service, '_emit_action_resolved', new_callable=AsyncMock) as mock_emit, \
         patch.object(action_queue_service, '_execute_resolved_action', new_callable=AsyncMock) as mock_execute:


        result = await action_queue_service.resolve_action_window(action_id)


        assert result == ActionStatus.RESOLVED
        mock_action_repo.resolve_action.assert_called_once_with(action_id, ActionStatus.RESOLVED)
        mock_emit.assert_called_once_with(1, sample_pending_action, ActionStatus.RESOLVED, counter_count)
        mock_execute.assert_called_once_with(sample_pending_action)


@pytest.mark.asyncio
async def test_resolve_action_window_odd_counters(action_queue_service, mock_action_repo, mock_db_session, sample_pending_action):
    """Test resolving action window with odd number of counters (should be cancelled)"""

    action_id = 1
    counter_count = 1


    counter = MagicMock(spec=Counter)
    sample_pending_action.counters = [counter]

    mock_action_repo.get_by_id.return_value = sample_pending_action


    with patch.object(action_queue_service, '_emit_action_resolved', new_callable=AsyncMock) as mock_emit, \
         patch.object(action_queue_service, '_handle_cancelled_action', new_callable=AsyncMock) as mock_cancel:


        result = await action_queue_service.resolve_action_window(action_id)


        assert result == ActionStatus.CANCELLED
        mock_action_repo.resolve_action.assert_called_once_with(action_id, ActionStatus.CANCELLED)
        mock_emit.assert_called_once_with(1, sample_pending_action, ActionStatus.CANCELLED, counter_count)
        mock_cancel.assert_called_once_with(sample_pending_action)


@pytest.mark.asyncio
async def test_resolve_action_window_three_counters(action_queue_service, mock_action_repo, mock_db_session, sample_pending_action):
    """Test resolving action window with three counters (odd, should be cancelled)"""

    action_id = 1
    counter_count = 3


    counters = [MagicMock(spec=Counter) for _ in range(3)]
    sample_pending_action.counters = counters

    mock_action_repo.get_by_id.return_value = sample_pending_action


    with patch.object(action_queue_service, '_emit_action_resolved', new_callable=AsyncMock) as mock_emit, \
         patch.object(action_queue_service, '_handle_cancelled_action', new_callable=AsyncMock) as mock_cancel:


        result = await action_queue_service.resolve_action_window(action_id)


        assert result == ActionStatus.CANCELLED
        mock_action_repo.resolve_action.assert_called_once_with(action_id, ActionStatus.CANCELLED)
        mock_emit.assert_called_once_with(1, sample_pending_action, ActionStatus.CANCELLED, counter_count)
        mock_cancel.assert_called_once_with(sample_pending_action)


@pytest.mark.asyncio
async def test_resolve_action_window_action_not_found(action_queue_service, mock_action_repo):
    """Test resolving action window when action doesn't exist"""

    action_id = 999

    mock_action_repo.get_by_id.return_value = None


    with pytest.raises(ValueError, match="Action not found"):
        await action_queue_service.resolve_action_window(action_id)


@pytest.mark.asyncio
async def test_resolve_action_window_execution_failure(action_queue_service, mock_action_repo, mock_db_session, sample_pending_action):
    """Test handling execution failure during action resolution"""

    action_id = 1
    counter_count = 0

    sample_pending_action.counters = []

    mock_action_repo.get_by_id.return_value = sample_pending_action


    with patch.object(action_queue_service, '_emit_action_resolved', new_callable=AsyncMock) as mock_emit, \
         patch.object(action_queue_service, '_execute_resolved_action', new_callable=AsyncMock, side_effect=Exception("Execution failed")) as mock_execute:


        with pytest.raises(Exception, match="Execution failed"):
            await action_queue_service.resolve_action_window(action_id)


@pytest.mark.asyncio
async def test_resolve_action_window_cancellation_failure(action_queue_service, mock_action_repo, mock_db_session, sample_pending_action):
    """Test handling cancellation failure during action resolution"""

    action_id = 1
    counter_count = 1

    counter = MagicMock(spec=Counter)
    sample_pending_action.counters = [counter]

    mock_action_repo.get_by_id.return_value = sample_pending_action


    with patch.object(action_queue_service, '_emit_action_resolved', new_callable=AsyncMock) as mock_emit, \
         patch.object(action_queue_service, '_handle_cancelled_action', new_callable=AsyncMock, side_effect=Exception("Cancellation failed")) as mock_cancel:


        with pytest.raises(Exception, match="Cancellation failed"):
            await action_queue_service.resolve_action_window(action_id)