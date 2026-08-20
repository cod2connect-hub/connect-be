"""Scheduling application ports."""

from typing import Protocol

from pydantic import BaseModel


class EventPublisher(Protocol):
    async def publish(self, event: str, payload: BaseModel) -> None: ...
