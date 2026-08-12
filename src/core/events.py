"""Event bus for cross-engine communication"""
from typing import Callable, Any, Dict, List
import logging

logger = logging.getLogger(__name__)


class EventBus:
    """
    Simple in-process event bus for decoupling engines.
    Example: booking.created -> notifications sends confirmation, CRM logs conversion
    """

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event: str) -> Callable:
        """Decorator for subscribing to events"""
        def decorator(fn: Callable) -> Callable:
            self._subscribers.setdefault(event, []).append(fn)
            logger.info(f"Subscribed {fn.__name__} to event '{event}'")
            return fn
        return decorator

    async def publish(self, event: str, payload: Dict[str, Any]) -> None:
        """Publish event to all subscribers"""
        subscribers = self._subscribers.get(event, [])
        logger.info(f"Publishing event '{event}' to {len(subscribers)} subscribers")

        for fn in subscribers:
            try:
                await fn(payload)
            except Exception as e:
                logger.error(f"Error in subscriber {fn.__name__} for event '{event}': {e}")
                # Continue processing other subscribers

    def list_events(self) -> Dict[str, int]:
        """List all registered events and subscriber counts"""
        return {event: len(subscribers) for event, subscribers in self._subscribers.items()}


# Global event bus instance
event_bus = EventBus()
