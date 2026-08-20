"""In-process event bus and publisher abstraction."""

from typing import Callable

from pydantic import BaseModel


class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable]] = {}

    def subscribe(self, event: str):
        def decorator(fn):
            self._subscribers.setdefault(event, []).append(fn)
            return fn

        return decorator

    async def publish(self, event: str, payload: BaseModel) -> None:
        for fn in self._subscribers.get(event, []):
            await fn(payload)


event_bus = EventBus()


class InProcessEventPublisher:
    async def publish(self, event: str, payload: BaseModel) -> None:
        await event_bus.publish(event, payload)
