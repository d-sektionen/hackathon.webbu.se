import uuid
from contextlib import asynccontextmanager

import argon2
from asyncpg import Connection
from fastapi import Cookie, Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel

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


async def get_current_session(
    token: str | None = Cookie(default=None),
    conn: Connection = Depends(get_db)
):
    """Get and validate the current session from cookie token"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token"
        )

    try:
        session = await db.get_session_by_token(uuid.UUID(token), conn)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return session

class Login(BaseModel):
    name: str
    password: str

class Signup(BaseModel):
    name: str
    password: str

class CreateProject(BaseModel):
    name: str
    description: str
    github_url: str | None = None

@app.post("/login")
async def login(response: Response, login: Login | None = None, conn: Connection = Depends(get_db)):
    if login is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing username or password")

    user = await db.get_user_by_name(login.name, conn)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")

    ph = argon2.PasswordHasher()
    try:
        ph.verify(user.password, login.password)
    except argon2.exceptions.VerifyMismatchError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")

    session = await db.add_session(user.id, conn)

    # Set the token as a cookie
    response.set_cookie(
        key="token",
        value=str(session.token),
        httponly=True,
        samesite="lax"
    )

    return {"status": "success", "token": session.token}


@app.post("/signup")
async def signup(signup_data: Signup, response: Response, conn: Connection = Depends(get_db)):
    if len(signup_data.password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 characters long")

    previous_user = await db.get_user_by_name(signup_data.name, conn)
    if previous_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    ph = argon2.PasswordHasher()
    hashed_password = ph.hash(signup_data.password)

    user = await db.add_user(signup_data.name, hashed_password, conn)
    session = await db.add_session(user.id, conn)

    # Set the token as a cookie
    response.set_cookie(
        key="token",
        value=str(session.token),
        httponly=True,
        samesite="lax"
    )

    return {"status": "success", "token": session.token}

@app.post("/projects")
async def create_project(
    project_data: CreateProject,
    session = Depends(get_current_session),
    conn: Connection = Depends(get_db)
):
    project = await db.add_project(
        project_data.name,
        project_data.description,
        project_data.github_url,
        session.user_id,
        conn
    )
    return {"status": "success", "project": project}

@app.get("/projects")
async def list_projects(conn: Connection = Depends(get_db)):
    projects = await db.get_all_projects(conn)
    return {"status": "success", "projects": projects}

@app.get("/projects/{project_id}")
async def get_project(project_id: uuid.UUID, conn: Connection = Depends(get_db)):
    project = await db.get_project_by_id(project_id, conn)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return {"status": "success", "project": project}
