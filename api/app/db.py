import os
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

import asyncpg
from asyncpg import Connection, Record
from fastapi import FastAPI


async def create_pool(app: FastAPI):
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


async def close_pool(app: FastAPI):
    await app.state.pool.close()


@dataclass
class User:
    id: UUID
    email: str
    password: str
    is_admin: bool
    created_at: datetime


@dataclass
class Session:
    user_id: UUID
    token: UUID
    created_at: datetime


@dataclass
class Project:
    id: UUID
    name: str
    description: str
    github_url: str
    owner_user_id: UUID
    created_at: datetime


async def add_user(email: str, password: str, db: Connection) -> User:
    user: Record | None = await db.fetchrow(
        "INSERT INTO users (email, password) VALUES ($1, $2) RETURNING *", email, password
    )
    if user is None:
        raise Exception("Failed to create user")
    return User(**dict(user))


async def get_user_by_email(email: str, db: Connection) -> User | None:
    user: Record | None = await db.fetchrow("SELECT * FROM users WHERE email = $1", email)

    if user is None:
        return None
    return User(**dict(user))

async def get_user_by_id(id: UUID, db: Connection) -> User | None:
    user: Record | None = await db.fetchrow("SELECT * FROM users WHERE id = $1", id)
    
    if user is None:
       return None
    return User(**dict(user)) 

async def add_session(user_id: UUID, db: Connection) -> Session:
    session: Record | None = await db.fetchrow(
        "INSERT INTO sessions (user_id) VALUES ($1) RETURNING *", user_id
    )
    if session is None:
        raise Exception("Failed to create session")

    return Session(**dict(session))


async def get_session_by_token(token: UUID, db: Connection) -> Session | None:
    session: Record | None = await db.fetchrow(
        "SELECT * FROM sessions WHERE token = $1", token
    )
    if session is None:
        return None
    return Session(**dict(session))


async def add_project(
    name: str,
    description: str,
    github_url: str | None,
    owner_user_id: UUID,
    db: Connection,
) -> Project:
    project: Record | None = await db.fetchrow(
        "INSERT INTO projects (name, description, github_url, owner_user_id) VALUES ($1, $2, $3, $4) RETURNING *",
        name,
        description,
        github_url,
        owner_user_id,
    )
    if project is None:
        raise Exception("Failed to create project")
    return Project(**dict(project))


async def get_all_projects(db: Connection) -> list[Project]:
    projects = await db.fetch("SELECT * FROM projects")
    return [Project(**project) for project in projects]


async def get_project_by_id(project_id: UUID, db: Connection) -> Project | None:
    project: Record | None = await db.fetchrow(
        "SELECT * FROM projects WHERE id = $1", project_id
    )
    if project is None:
        return None
    return Project(**dict(project))


async def update_project(
    project_id: UUID,
    name: str,
    description: str,
    github_url: str | None,
    db: Connection,
) -> Project:
    project: Record | None = await db.fetchrow(
        "UPDATE projects SET name = $1, description = $2, github_url = $3 WHERE id = $4 RETURNING *",
        name,
        description,
        github_url,
        project_id,
    )
    if project is None:
        raise Exception("Failed to update project")
    return Project(**dict(project))
