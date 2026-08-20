# Analytics engine

Owns: Tenant business metrics, dashboard definitions, event facts, reports, and analytics connections.

This module follows the four-layer contract in `docs/01-architecture.md`. Other modules may use its declared application API or versioned events; they may not import its domain or infrastructure internals.
