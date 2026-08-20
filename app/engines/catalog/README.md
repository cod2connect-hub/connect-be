# Catalog engine

Owns: Reusable listings, offerings, products, services, profiles, categories, and variants.

This module follows the four-layer contract in `docs/01-architecture.md`. Other modules may use its declared application API or versioned events; they may not import its domain or infrastructure internals.
