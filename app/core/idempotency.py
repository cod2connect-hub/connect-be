"""Idempotency helpers for mutating requests."""

import hashlib
from dataclasses import dataclass

import asyncpg
from fastapi import Depends, Header, HTTPException, Request

from .db import get_db


@dataclass
class IdempotencyContext:
    key: str
    request_hash: str


class ShortCircuitResponse(Exception):
    def __init__(self, status: int, body: dict):
        self.status = status
        self.body = body


def _hash_body(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


async def idempotent(
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
    request: Request = None,
    conn: asyncpg.Connection = Depends(get_db),
) -> IdempotencyContext | None:
    if idempotency_key is None:
        return None

    request_hash = _hash_body(await request.body())
    existing = await conn.fetchrow(
        "select response_status, response_body, request_hash from idempotency_keys "
        "where tenant_id = $1 and key = $2 and endpoint = $3",
        request.state.tenant_id,
        idempotency_key,
        request.url.path,
    )
    if existing and existing["request_hash"] != request_hash:
        raise HTTPException(422, "Idempotency-Key reused with a different request body")
    if existing:
        raise ShortCircuitResponse(existing["response_status"], existing["response_body"])
    return IdempotencyContext(key=idempotency_key, request_hash=request_hash)


async def save_idempotent_response(
    conn: asyncpg.Connection,
    tenant_id,
    ctx: IdempotencyContext,
    endpoint: str,
    status: int,
    body: dict,
) -> None:
    await conn.execute(
        "insert into idempotency_keys (tenant_id, key, endpoint, request_hash, response_status, "
        "response_body, expires_at) values ($1,$2,$3,$4,$5,$6, now() + interval '24 hours')",
        tenant_id,
        ctx.key,
        endpoint,
        ctx.request_hash,
        status,
        body,
    )
