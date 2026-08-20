# Portal engine

Owns: Customer-facing access spaces and visibility policies for records owned by other engines.

This module follows the four-layer contract in `docs/01-architecture.md`. Other modules may use its declared application API or versioned events; they may not import its domain or infrastructure internals.
