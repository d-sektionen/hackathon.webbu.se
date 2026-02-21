import uuid

from asyncpg import Connection
from fastapi import Cookie, Depends, HTTPException, Request, status

from . import db


async def get_db(request: Request):
    async with request.app.state.pool.acquire() as connection:
        yield connection


async def get_current_session(
    token: str | None = Cookie(default=None), conn: Connection = Depends(get_db)
):
    """Get and validate the current session from cookie token"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
        )

    try:
        session = await db.get_session_by_token(uuid.UUID(token), conn)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format"
        )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )

    return session
