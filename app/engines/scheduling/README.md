# Scheduling engine

Owns: Availability, resources, bookings, reservations, classes, waitlists, and recurrence.

This module follows the four-layer contract in `docs/01-architecture.md`. Other modules may use its declared application API or versioned events; they may not import its domain or infrastructure internals.
