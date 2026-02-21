import os
from datetime import datetime
from typing import NamedTuple
from uuid import UUID

import asyncpg
from asyncpg import Connection, Pool
from fastapi import FastAPI

DATABASE_URL = os.getenv("DATABASE_URL")


async def create_pool(app: FastAPI):
    app.state.pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)


async def close_pool(app: FastAPI):
    await app.state.pool.close()


class User(NamedTuple):
    id: UUID
    name: str
    password: str
    is_admin: bool
    created_at: datetime


class Session(NamedTuple):
    user_id: UUID
    token: UUID
    created_at: datetime


async def add_user(name: str, password: str, db: Connection) -> User:
    user: User | None = await db.fetchrow(
        "INSERT INTO users (name, password) VALUES ($1, $2) RETURNING *", name, password
    )
    if user is None:
        raise Exception("Failed to create user")
    return user


async def get_user_by_name(name: str, db: Connection) -> User | None:
    user: User | None = await db.fetchrow("SELECT * FROM users WHERE name = $1", name)
    return user


async def add_session(user_id: UUID, db: Connection) -> Session:
    session: Session | None = await db.fetchrow(
        "INSERT INTO sessions (user_id) VALUES ($1) RETURNING *", user_id
    )
    if session is None:
        raise Exception("Failed to create session")

    return session

async def get_session_by_token(token: UUID, db: Connection) -> Session | None:
    session: Session | None = await db.fetchrow("SELECT * FROM sessions WHERE token = $1", token)
    return session
