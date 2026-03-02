from uuid import UUID

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from .db import schema, themes
from .deps import get_current_session, get_db

router = APIRouter()

class ThemeRequest(BaseModel):
    name: str

class ThemeListResponse(BaseModel):
    themes: list[schema.Theme]

class ThemeResponse(BaseModel):
    theme: schema.Theme

class VoteResponse(BaseModel):
    vote: schema.ThemeVote


@router.get("/themes")
async def list_themes(conn: Connection = Depends(get_db)) -> ThemeListResponse:
    theme_list = await themes.get_all(conn)

    return ThemeListResponse(themes=theme_list)

@router.post("/themes")
async def suggest_theme(
    theme_data: ThemeRequest,
    session: schema.Session = Depends(get_current_session),
    conn: Connection = Depends(get_db),
) -> ThemeResponse:
    if len(theme_data.name) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="the name of the theme must at least be 2 characters long"
        )

    theme = await themes.add(theme_data.name, session.user_id, conn)
    return ThemeResponse(theme=theme)

@router.post("/themes/{theme_id}/vote")
async def vote_theme(
    theme_id: UUID,
    session: schema.Session = Depends(get_current_session),
    conn: Connection = Depends(get_db),
) -> VoteResponse:
    theme = themes.get_by_id(theme_id, conn)
    if theme is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="no theme found with the provided id"
        )

    vote = await themes.add_vote(session.user_id, theme_id, conn)
    if vote is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="failed to cast vote"
        )

    return VoteResponse(vote=vote)
