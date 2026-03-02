from uuid import UUID

from asyncpg import Connection, Record

from .schema import Session


async def add(user_id: UUID, db: Connection) -> Session:
    session: Record | None = await db.fetchrow(
        "INSERT INTO sessions (user_id) VALUES ($1) RETURNING *", user_id
    )
    if session is None:
        raise Exception("Failed to create session")

    return Session(**dict(session))


async def get_by_token(token: UUID, db: Connection) -> Session | None:
    session: Record | None = await db.fetchrow(
        "SELECT * FROM sessions WHERE token = $1", token
    )
    if session is None:
        return None
    return Session(**dict(session))
