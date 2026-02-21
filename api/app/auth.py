import argon2
from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel

from . import db
from .deps import get_db

router = APIRouter()


class Login(BaseModel):
    name: str
    password: str


class Signup(BaseModel):
    name: str
    password: str


class AuthResponse(BaseModel):
    status: str
    token: str


@router.post("/login")
async def login(
    response: Response,
    login: Login | None = None,
    conn: Connection = Depends(get_db)
) -> AuthResponse:
    if login is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing username or password"
        )

    user = await db.get_user_by_name(login.name, conn)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    ph = argon2.PasswordHasher()
    try:
        ph.verify(user.password, login.password)
    except argon2.exceptions.VerifyMismatchError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    session = await db.add_session(user.id, conn)

    response.set_cookie(
        key="token",
        value=str(session.token),
        httponly=True,
        samesite="lax"
    )

    return AuthResponse(status="success", token=str(session.token))


@router.post("/signup")
async def signup(
    signup_data: Signup,
    response: Response,
    conn: Connection = Depends(get_db)
) -> AuthResponse:
    if len(signup_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )

    previous_user = await db.get_user_by_name(signup_data.name, conn)
    if previous_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    ph = argon2.PasswordHasher()
    hashed_password = ph.hash(signup_data.password)

    user = await db.add_user(signup_data.name, hashed_password, conn)
    session = await db.add_session(user.id, conn)

    response.set_cookie(
        key="token",
        value=str(session.token),
        httponly=True,
        samesite="lax"
    )

    return AuthResponse(status="success", token=str(session.token))
