"""Scheduling domain exceptions."""

from app.core.errors import DomainError


class BookingConflictError(DomainError):
    pass


class BookingNotFoundError(DomainError):
    pass
