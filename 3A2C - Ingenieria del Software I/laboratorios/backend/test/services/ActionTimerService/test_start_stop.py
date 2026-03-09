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
async def test_start_timer_service():
    """Test that the timer service starts correctly"""
    
    mock_session_factory = MagicMock()
    
    timer_service = ActionTimerService(mock_session_factory)
    
    assert timer_service.is_running() is False
    
    await timer_service.start()
    
    assert timer_service.is_running() is True
    assert timer_service._task is not None
    
    await timer_service.stop()


@pytest.mark.asyncio
async def test_stop_timer_service():
    """Test that the timer service stops correctly"""
    
    mock_session_factory = MagicMock()
    timer_service = ActionTimerService(mock_session_factory)
    
    await timer_service.start()
    assert timer_service.is_running() is True
    
    await timer_service.stop()
    
    assert timer_service.is_running() is False
    
    await asyncio.sleep(0.1)




@pytest.mark.asyncio
async def test_is_running_status():
    """Test that is_running returns the correct status"""
    
    mock_session_factory = MagicMock()
    timer_service = ActionTimerService(mock_session_factory)
    
    assert timer_service.is_running() is False
    
    await timer_service.start()
    assert timer_service.is_running() is True
    
    await timer_service.stop()
    assert timer_service.is_running() is False
