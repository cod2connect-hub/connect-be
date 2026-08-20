# Commerce engine

Owns: Carts, customer orders, inventory, fulfillment, delivery/pickup, returns, gift cards, and POS sync.

This module follows the four-layer contract in `docs/01-architecture.md`. Other modules may use its declared application API or versioned events; they may not import its domain or infrastructure internals.
