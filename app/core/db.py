"""Database pool and request-scoped transaction helpers."""

from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI, Request

from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await asyncpg.create_pool(
        dsn=settings.database_url,
        min_size=5,
        max_size=20,
        statement_cache_size=0,
    )
    yield
    await app.state.pool.close()


async def get_db(request: Request):
    async with request.app.state.pool.acquire() as conn:
        async with conn.transaction():
            tenant_id = getattr(request.state, "tenant_id", None)
            if tenant_id is not None:
                await conn.execute("select set_config('app.tenant_id', $1, true)", str(tenant_id))
            yield conn
