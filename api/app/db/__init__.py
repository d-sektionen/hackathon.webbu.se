import os

import asyncpg
from fastapi import FastAPI


async def create_pool(app: FastAPI) -> None:
    database_user = os.getenv("DATABASE_USER")
    if database_user is None:
        raise Exception("DATABASE_USER environment variable is not set")

    database_name = os.getenv("DATABASE_NAME")
    if database_name is None:
        raise Exception("DATABASE_NAME environment variable is not set")

    database_password = os.getenv("DATABASE_PASSWORD")
    if database_password is None:
        raise Exception("DATABASE_PASSWORD environment variable is not set")

    database_url = f"postgresql://{database_user}:{database_password}@postgres:5432/{database_name}"
    app.state.pool = await asyncpg.create_pool(database_url, min_size=1, max_size=10)

async def close_pool(app: FastAPI) -> None:
    await app.state.pool.close()
