import uuid
from contextlib import asynccontextmanager

import argon2
from asyncpg import Connection
from fastapi import Cookie, Depends, FastAPI, HTTPException

from . import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.create_pool(app)
    yield
    # Shutdown
    await db.close_pool(app)


app = FastAPI(lifespan=lifespan)


# Dependency to get DB connection
async def get_db():
    async with app.state.pool.acquire() as connection:
        yield connection


async def verify_token(token: str, conn: Connection):
    session = await db.get_session_by_token(uuid.UUID(token), conn)
    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return session


@app.post("/login")
async def login(name: str, password: str, conn: Connection = Depends(get_db)):
    user = await db.get_user_by_name(name, conn)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    ph = argon2.PasswordHasher()
    try:
        ph.verify(user.password, password)
    except argon2.exceptions.VerifyMismatchError:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    session = await db.add_session(user.id, conn)
    return {"status": "success", "token": session.token}


@app.post("/signup")
async def signup(name: str, password: str, conn: Connection = Depends(get_db)):
    ph = argon2.PasswordHasher()
    hashed_password = ph.hash(password)

    user = await db.add_user(name, hashed_password, conn)
    session = await db.add_session(user.id, conn)

    return {"status": "success", "token": session.token}

@app.post("/projects")
async def create_project(
    name: str,
    description: str,
    github_url: str,
    token: str | None = Cookie(default=None),
    conn: Connection = Depends(get_db)
):
    if token is None:
        raise HTTPException(status_code=401, detail="Missing token")

    session = await verify_token(token, conn)
    project = await db.add_project(name, description, github_url, session.user_id, conn)

    return {"status": "success", "project": project}

@app.get("/projects")
async def list_projects(conn: Connection = Depends(get_db)):
    projects = await db.get_all_projects(conn)
    return {"status": "success", "projects": projects}

@app.get("/projects/{project_id}")
async def get_project(project_id: uuid.UUID, conn: Connection = Depends(get_db)):
    project = await db.get_project_by_id(project_id, conn)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"status": "success", "project": project}

# @app.get("/projects/{project_id}/readme")
