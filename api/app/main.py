import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import auth, db, projects, themes


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    await db.create_pool(app)
    yield
    # Shutdown
    await db.close_pool(app)


app = FastAPI(
    title="HackathIIn",
    summary="Hackathon API written in FastAPI",
    version="0.1.0",
    contact={
        "name": "WebbU",
        "url": "https://webbu.se/",
        "email": "webmaster@d-sektionen.se",
    },
    openapi_tags=[
        {
            "name": "auth",
            "description": "Endpoints for user authentication and session management",
        },
        {
            "name": "projects",
            "description": "Endpoints for creating and listing projects",
        },
        {
            "name": "themes",
            "description": "Endpoints for suggesting and voting on themes",
        },
    ],
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ALLOWED_ORIGIN") or ""],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(themes.router)
