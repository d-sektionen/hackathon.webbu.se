import uuid
from contextlib import asynccontextmanager

import argon2

# from db import add_session, add_user, close_pool, create_pool, get_user_by_nameim
import db
from asyncpg import Connection, Pool
from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.create_pool(app)
    yield
    # Shutdown
    await db.close_pool(app)


# Dependency to get DB connection
async def get_db():
    async with app.state.pool.acquire() as connection:
        yield connection

async def verify_token(token: str, conn: Connection):
    session = await db.get_session_by_token(uuid.UUID(token), conn)
    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return session

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


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
    return {
        "status": "success",
        "token": session.token
    }

@app.post("/signup")
async def signup(name: str, password: str, conn: Connection = Depends(get_db)):
    ph = argon2.PasswordHasher()
    hashed_password = ph.hash(password)

    user = await db.add_user(name, hashed_password, conn)
    session = await db.add_session(user.id, conn)

    return {"status": "success", "token": session.token}
