import sys
from pathlib import Path

root = Path(__file__).resolve().parents[3]
src = root / "src"
sys.path.insert(0, str(src))

import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch, call
from services.action_timer_service import ActionTimerService
from models.pending_action_model import PendingAction, ActionType, ActionStatus
from datetime import datetime, timedelta, timezone


@pytest.mark.asyncio
async def test_check_expired_actions_with_no_expired():
    """Test checking for expired actions when there are none"""
    
    mock_db_session = MagicMock()
    mock_session_factory = MagicMock(return_value=mock_db_session)
    
    timer_service = ActionTimerService(mock_session_factory)
    
    with patch('services.action_timer_service.ActionRepository') as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo.get_expired_actions.return_value = []
        mock_repo_class.return_value = mock_repo
        
        await timer_service._check_and_resolve_expired_actions()
        
        mock_repo.get_expired_actions.assert_called_once()
        
        mock_db_session.close.assert_called_once()


@pytest.mark.asyncio
async def test_check_expired_actions_with_one_expired():
    """Test checking and resolving a single expired action"""
    
    mock_db_session = MagicMock()
    mock_session_factory = MagicMock(return_value=mock_db_session)
    
    timer_service = ActionTimerService(mock_session_factory)
    
    expired_action = MagicMock(spec=PendingAction)
    expired_action.id = 1
    expired_action.game_id = 1
    expired_action.action_type = ActionType.PLAY_SET
    expired_action.expires_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    
    with patch('services.action_timer_service.ActionRepository') as mock_repo_class, \
         patch('services.action_timer_service.ActionQueueService') as mock_service_class:
        
        mock_repo = MagicMock()
        mock_repo.get_expired_actions.return_value = [expired_action]
        mock_repo_class.return_value = mock_repo
        
        mock_action_service = AsyncMock()
        mock_service_class.return_value = mock_action_service
        
        await timer_service._check_and_resolve_expired_actions()
        
        mock_action_service.resolve_action_window.assert_called_once_with(1)
        
        mock_db_session.commit.assert_called_once()
        
        mock_db_session.close.assert_called_once()


@pytest.mark.asyncio
async def test_check_expired_actions_with_multiple_expired():
    """Test checking and resolving multiple expired actions"""
    
    mock_db_session = MagicMock()
    mock_session_factory = MagicMock(return_value=mock_db_session)
    
    timer_service = ActionTimerService(mock_session_factory)
    
    expired_action_1 = MagicMock(spec=PendingAction)
    expired_action_1.id = 1
    
    expired_action_2 = MagicMock(spec=PendingAction)
    expired_action_2.id = 2
    
    expired_action_3 = MagicMock(spec=PendingAction)
    expired_action_3.id = 3
    
    with patch('services.action_timer_service.ActionRepository') as mock_repo_class, \
         patch('services.action_timer_service.ActionQueueService') as mock_service_class:
        
        mock_repo = MagicMock()
        mock_repo.get_expired_actions.return_value = [expired_action_1, expired_action_2, expired_action_3]
        mock_repo_class.return_value = mock_repo
        
        mock_action_service = AsyncMock()
        mock_service_class.return_value = mock_action_service
        
        await timer_service._check_and_resolve_expired_actions()
        
        assert mock_action_service.resolve_action_window.call_count == 3
        mock_action_service.resolve_action_window.assert_any_call(1)
        mock_action_service.resolve_action_window.assert_any_call(2)
        mock_action_service.resolve_action_window.assert_any_call(3)
        
        assert mock_db_session.commit.call_count == 3
        
        mock_db_session.close.assert_called_once()


@pytest.mark.asyncio
async def test_check_expired_actions_handles_resolution_error():
    """Test that an error resolving one action doesn't stop processing others"""
    
    mock_db_session = MagicMock()
    mock_session_factory = MagicMock(return_value=mock_db_session)
    
    timer_service = ActionTimerService(mock_session_factory)
    
    expired_action_1 = MagicMock(spec=PendingAction)
    expired_action_1.id = 1
    
    expired_action_2 = MagicMock(spec=PendingAction)
    expired_action_2.id = 2
    
    with patch('services.action_timer_service.ActionRepository') as mock_repo_class, \
         patch('services.action_timer_service.ActionQueueService') as mock_service_class, \
         patch('services.action_timer_service.logger') as mock_logger:
        
        mock_repo = MagicMock()
        mock_repo.get_expired_actions.return_value = [expired_action_1, expired_action_2]
        mock_repo_class.return_value = mock_repo
        
        mock_action_service = AsyncMock()
        mock_action_service.resolve_action_window.side_effect = [
            Exception("Resolution failed"),
            None  
        ]
        mock_service_class.return_value = mock_action_service
        
        await timer_service._check_and_resolve_expired_actions()
        
        assert mock_action_service.resolve_action_window.call_count == 2
        
        mock_logger.error.assert_called()
        
        mock_db_session.rollback.assert_called()
        
        mock_db_session.commit.assert_called_once()
        
        mock_db_session.close.assert_called_once()


@pytest.mark.asyncio
async def test_check_expired_actions_handles_general_error():
    """Test that a general error in checking actions is caught"""
    
    mock_db_session = MagicMock()
    mock_session_factory = MagicMock(return_value=mock_db_session)
    
    timer_service = ActionTimerService(mock_session_factory)
    
    with patch('services.action_timer_service.ActionRepository') as mock_repo_class, \
         patch('services.action_timer_service.logger') as mock_logger:
        
        mock_repo_class.side_effect = Exception("Database connection failed")
        
        await timer_service._check_and_resolve_expired_actions()

        mock_db_session.rollback.assert_called_once()
        mock_db_session.close.assert_called_once()


@pytest.mark.asyncio
async def test_check_expired_actions_creates_new_session():
    """Test that each check creates a new database session"""
    
    mock_db_session = MagicMock()
    mock_session_factory = MagicMock(return_value=mock_db_session)
    
    timer_service = ActionTimerService(mock_session_factory)
    
    with patch('services.action_timer_service.ActionRepository') as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo.get_expired_actions.return_value = []
        mock_repo_class.return_value = mock_repo
        
        await timer_service._check_and_resolve_expired_actions()
        await timer_service._check_and_resolve_expired_actions()
        
        assert mock_session_factory.call_count == 2
        
        assert mock_db_session.close.call_count == 2
