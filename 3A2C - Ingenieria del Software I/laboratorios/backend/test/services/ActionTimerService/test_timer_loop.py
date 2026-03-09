import sys
from pathlib import Path

root = Path(__file__).resolve().parents[3]
src = root / "src"
sys.path.insert(0, str(src))

import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from services.action_timer_service import ActionTimerService


@pytest.mark.asyncio
async def test_timer_loop_runs_periodically():
    """Test that the timer loop calls check method periodically"""
    
    mock_session_factory = MagicMock()
    timer_service = ActionTimerService(mock_session_factory)
    
    check_count = 0
    
    async def mock_check():
        nonlocal check_count
        check_count += 1
    
    with patch.object(timer_service, '_check_and_resolve_expired_actions', side_effect=mock_check):
        await timer_service.start()
        
        await asyncio.sleep(2.2)
        
        await timer_service.stop()
        
        assert check_count >= 2


@pytest.mark.asyncio
async def test_timer_loop_handles_exceptions():
    """Test that exceptions in the check method don't crash the loop"""
    
    mock_session_factory = MagicMock()
    timer_service = ActionTimerService(mock_session_factory)
    
    call_count = 0
    
    async def mock_check_with_error():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise Exception("Test error")
    
    with patch.object(timer_service, '_check_and_resolve_expired_actions', side_effect=mock_check_with_error), \
         patch('services.action_timer_service.logger') as mock_logger:
        
        await timer_service.start()
        
        await asyncio.sleep(1.5)
        
        await timer_service.stop()
        
        assert call_count >= 2
        
        mock_logger.error.assert_called()


@pytest.mark.asyncio
async def test_timer_loop_stops_when_service_stops():
    """Test that the timer loop stops when the service is stopped"""
    
    mock_session_factory = MagicMock()
    timer_service = ActionTimerService(mock_session_factory)
    
    check_count = 0
    
    async def mock_check():
        nonlocal check_count
        check_count += 1
    
    with patch.object(timer_service, '_check_and_resolve_expired_actions', side_effect=mock_check):
        await timer_service.start()
        
        await asyncio.sleep(1.2)
        
        await timer_service.stop()
        
        checks_after_stop = check_count
        
        await asyncio.sleep(1.5)
        
        assert check_count <= checks_after_stop + 1


@pytest.mark.asyncio
async def test_timer_loop_respects_one_second_interval():
    """Test that the timer loop waits approximately 1 second between checks"""
    
    mock_session_factory = MagicMock()
    timer_service = ActionTimerService(mock_session_factory)
    
    timestamps = []
    
    async def mock_check():
        import time
        timestamps.append(time.time())
    
    with patch.object(timer_service, '_check_and_resolve_expired_actions', side_effect=mock_check):
        await timer_service.start()
        
        await asyncio.sleep(3.5)
        
        await timer_service.stop()
        
        assert len(timestamps) >= 3
        
        for i in range(1, len(timestamps)):
            interval = timestamps[i] - timestamps[i-1]
            assert 0.9 <= interval <= 1.3


@pytest.mark.asyncio
async def test_timer_loop_task_cancellation():
    """Test that the timer loop task can be cancelled properly"""
    
    mock_session_factory = MagicMock()
    timer_service = ActionTimerService(mock_session_factory)
    
    with patch.object(timer_service, '_check_and_resolve_expired_actions', new_callable=AsyncMock):
        await timer_service.start()
        
        task = timer_service._task
        assert task is not None
        assert not task.done()
        
        await timer_service.stop()
        
        assert task.done()
