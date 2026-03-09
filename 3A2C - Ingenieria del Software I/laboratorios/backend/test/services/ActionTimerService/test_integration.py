import sys
from pathlib import Path

root = Path(__file__).resolve().parents[3]
src = root / "src"
sys.path.insert(0, str(src))

import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from services.action_timer_service import ActionTimerService
from models.pending_action_model import PendingAction, ActionType, ActionStatus
from datetime import datetime, timedelta, timezone


@pytest.mark.asyncio
async def test_timer_service_integration_flow():
    """Integration test: timer service detects and resolves an expired action"""
    
    mock_db_session = MagicMock()
    mock_session_factory = MagicMock(return_value=mock_db_session)
    
    timer_service = ActionTimerService(mock_session_factory)
    
    expired_action = MagicMock(spec=PendingAction)
    expired_action.id = 1
    expired_action.game_id = 1
    expired_action.action_type = ActionType.PLAY_SET
    expired_action.status = ActionStatus.PENDING
    expired_action.expires_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    
    resolution_called = False
    
    async def mock_resolve_action(action_id):
        nonlocal resolution_called
        resolution_called = True
        assert action_id == 1
    
    with patch('services.action_timer_service.ActionRepository') as mock_repo_class, \
         patch('services.action_timer_service.ActionQueueService') as mock_service_class:
        
        mock_repo = MagicMock()
        mock_repo.get_expired_actions.side_effect = [[expired_action], [], []]
        mock_repo_class.return_value = mock_repo
        
        mock_action_service = AsyncMock()
        mock_action_service.resolve_action_window.side_effect = mock_resolve_action
        mock_service_class.return_value = mock_action_service
        
        await timer_service.start()
        
        await asyncio.sleep(1.5)
        
        await timer_service.stop()
        
        assert resolution_called is True


@pytest.mark.asyncio
async def test_timer_service_handles_concurrent_expirations():
    """Test that timer service can handle multiple actions expiring at once"""
    
    mock_db_session = MagicMock()
    mock_session_factory = MagicMock(return_value=mock_db_session)
    
    timer_service = ActionTimerService(mock_session_factory)
    
    expired_actions = []
    for i in range(1, 6):
        action = MagicMock(spec=PendingAction)
        action.id = i
        action.game_id = 1
        expired_actions.append(action)
    
    resolved_ids = set()
    
    async def mock_resolve_action(action_id):
        resolved_ids.add(action_id)
    
    with patch('services.action_timer_service.ActionRepository') as mock_repo_class, \
         patch('services.action_timer_service.ActionQueueService') as mock_service_class:
        
        mock_repo = MagicMock()
        mock_repo.get_expired_actions.side_effect = [expired_actions, []]
        mock_repo_class.return_value = mock_repo
        
        mock_action_service = AsyncMock()
        mock_action_service.resolve_action_window.side_effect = mock_resolve_action
        mock_service_class.return_value = mock_action_service
        
        await timer_service.start()
        
        await asyncio.sleep(1.5)
        
        await timer_service.stop()
        
        assert resolved_ids == {1, 2, 3, 4, 5}


@pytest.mark.asyncio
async def test_timer_service_continues_after_error():
    """Test that timer service continues running after encountering errors"""
    
    mock_db_session = MagicMock()
    mock_session_factory = MagicMock(return_value=mock_db_session)
    
    timer_service = ActionTimerService(mock_session_factory)
    
    action1 = MagicMock(spec=PendingAction)
    action1.id = 1
    
    action2 = MagicMock(spec=PendingAction)
    action2.id = 2
    
    resolved_actions = []
    
    async def mock_resolve_action(action_id):
        if action_id == 1:
            raise Exception("Simulated error")
        resolved_actions.append(action_id)
    
    with patch('services.action_timer_service.ActionRepository') as mock_repo_class, \
         patch('services.action_timer_service.ActionQueueService') as mock_service_class, \
         patch('services.action_timer_service.logger'):
        
        mock_repo = MagicMock()
        mock_repo.get_expired_actions.side_effect = [
            [action1, action2],
            [action2],
            []
        ]
        mock_repo_class.return_value = mock_repo
        
        mock_action_service = AsyncMock()
        mock_action_service.resolve_action_window.side_effect = mock_resolve_action
        mock_service_class.return_value = mock_action_service
        
        await timer_service.start()
        
        await asyncio.sleep(2.5)
        
        await timer_service.stop()
        
        assert 2 in resolved_actions


@pytest.mark.asyncio
async def test_timer_service_session_isolation():
    """Test that each timer check uses a fresh database session"""
    
    session_instances = []
    
    def mock_session_factory():
        session = MagicMock()
        session_instances.append(session)
        return session
    
    timer_service = ActionTimerService(mock_session_factory)
    
    with patch('services.action_timer_service.ActionRepository') as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo.get_expired_actions.return_value = []
        mock_repo_class.return_value = mock_repo
        
        await timer_service.start()
        
        await asyncio.sleep(2.5)
        
        await timer_service.stop()
        
        assert len(session_instances) >= 2
        
        for session in session_instances:
            session.close.assert_called()
