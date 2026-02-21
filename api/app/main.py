from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import db
from .auth import router as auth_router
from .projects import router as projects_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.create_pool(app)
    yield
    # Shutdown
    await db.close_pool(app)


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(projects_router)
