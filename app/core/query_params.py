"""Shared list-query parsing."""

from dataclasses import dataclass, field

from fastapi import HTTPException, Request


@dataclass
class ListParams:
    limit: int = 20
    cursor: str | None = None
    sort: str | None = None
    filters: dict[str, str] = field(default_factory=dict)


def make_list_params_dep(allowed_filters: set[str], allowed_sort: set[str]):
    def dep(request: Request) -> ListParams:
        q = request.query_params
        filters = {k: v for k, v in q.items() if k in allowed_filters}
        sort = q.get("sort")
        if sort and sort.lstrip("-") not in allowed_sort:
            raise HTTPException(422, f"Unsupported sort field: {sort}")
        return ListParams(
            limit=int(q.get("limit", 20)),
            cursor=q.get("cursor"),
            sort=sort,
            filters=filters,
        )

    return dep
