# Identity context

Owns accounts, credentials and federated identities, sessions, tenant memberships, staff roles, permission grants, and identity audit history. Authentication primitives remain in `app/core/security.py`; identity business data and use cases belong here.

This platform context follows the same four-layer contract as an engine.
