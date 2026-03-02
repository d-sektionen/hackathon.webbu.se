from uuid import UUID

from asyncpg import Connection, Record

from .schema import User


async def add(email: str, password: str, db: Connection) -> User:
    user: Record | None = await db.fetchrow(
        "INSERT INTO users (email, password) VALUES ($1, $2) RETURNING *", email, password
    )
    if user is None:
        raise Exception("Failed to create user")
    return User(**dict(user))


async def get_by_email(email: str, db: Connection) -> User | None:
    user: Record | None = await db.fetchrow("SELECT * FROM users WHERE email = $1", email)

    if user is None:
        return None
    return User(**dict(user))

async def get_by_id(id: UUID, db: Connection) -> User | None:
    user: Record | None = await db.fetchrow("SELECT * FROM users WHERE id = $1", id)

    if user is None:
       return None
    return User(**dict(user))
