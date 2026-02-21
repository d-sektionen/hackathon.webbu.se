import os
from datetime import datetime
from typing import NamedTuple
from uuid import UUID

import asyncpg
from asyncpg import Connection, Pool
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


class Project(NamedTuple):
    id: UUID
    name: str
    description: str
    github_url: str
    owner_user_id: UUID
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
    session: Session | None = await db.fetchrow(
        "SELECT * FROM sessions WHERE token = $1", token
    )
    return session

async def add_project(name: str, description: str, github_url: str | None, owner_user_id: UUID, db: Connection) -> Project:
    project: Project | None = await db.fetchrow(
        "INSERT INTO projects (name, description, github_url, owner_user_id) VALUES ($1, $2, $3, $4) RETURNING *",
        name,
        description,
        github_url,
        owner_user_id,
    )
    if project is None:
        raise Exception("Failed to create project")
    return project

async def get_all_projects(db: Connection) -> list[Project]:
    projects = await db.fetch("SELECT * FROM projects")
    return [Project(**project) for project in projects]

async def get_project_by_id(project_id: UUID, db: Connection) -> Project | None:
    project: Project | None = await db.fetchrow("SELECT * FROM projects WHERE id = $1", project_id)
    if project is None:
        return None
    return project
