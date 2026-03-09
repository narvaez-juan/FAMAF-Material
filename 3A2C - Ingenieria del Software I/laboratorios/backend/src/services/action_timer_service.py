"""Background timer service for auto-resolving expired NSF actions."""

import asyncio
from sqlalchemy.orm import Session
from repositories.action_repository import ActionRepository
from services.action_queue_service import ActionQueueService
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ActionTimerService:
    """
    Background service that monitors pending actions and auto-resolves them
    when their counter window expires.
    
    Runs in an async loop, checking every second for expired actions.
    When found, resolves them through the ActionQueueService.
    """
    
    def __init__(self, db_session_factory):
        """
        Initialize the timer service.
        
        Parameters
        ----------
        db_session_factory : callable
            Factory function that creates new database sessions
            (e.g., SessionLocal from FastAPI)
        """
        self.db_session_factory = db_session_factory
        self._running = False
        self._task: Optional[asyncio.Task] = None
    
    async def start(self):
        """Start the background timer task."""
        if self._running:
            logger.warning("ActionTimerService is already running")
            return
        
        self._running = True
        self._task = asyncio.create_task(self._timer_loop())
        logger.info("ActionTimerService started")
    
    async def stop(self):
        """Stop the background timer task."""
        if not self._running:
            return
        
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        logger.info("ActionTimerService stopped")
    
    async def _timer_loop(self):
        """
        Main timer loop that runs every second.
        Checks for expired actions and resolves them.
        """
        while self._running:
            try:
                await self._check_and_resolve_expired_actions()
            except Exception as e:
                logger.error(f"Error in timer loop: {e}", exc_info=True)
            
            # Sleep for 1 second before next check
            await asyncio.sleep(1.0)
    
    async def _check_and_resolve_expired_actions(self):
        """
        Check for expired actions and resolve them.
        Creates a new DB session for each check to avoid stale data.
        """
        # Create new session for this check
        db = self.db_session_factory()
        try:
            action_repo = ActionRepository(db)
            expired_actions = action_repo.get_expired_actions()
            
            if not expired_actions:
                return
            
            logger.info(f"Found {len(expired_actions)} expired actions")
            
            # Resolve each expired action
            for action in expired_actions:
                try:
                    action_service = ActionQueueService(db)
                    await action_service.resolve_action_window(action.id)
                    # Commit this action's resolution (includes execution)
                    db.commit()
                    logger.info(f"Auto-resolved action {action.id}")
                except Exception as e:
                    logger.error(f"Failed to resolve action {action.id}: {e}", exc_info=True)
                    db.rollback()  # Rollback this action's changes, continue with others
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error checking expired actions: {e}", exc_info=True)
        finally:
            db.close()
    
    def is_running(self) -> bool:
        """Check if the timer service is currently running."""
        return self._running
