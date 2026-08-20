"""Tenant scope assertions."""


class MissingTenantScopeError(Exception):
    """Raised when a query executes without tenant scoping."""


def assert_scoped(tenant_id, *, context: str) -> None:
    if tenant_id is None:
        raise MissingTenantScopeError(f"Unscoped query in {context}")
