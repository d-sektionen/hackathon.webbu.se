from uuid import UUID

from asyncpg import Connection, Record

from .schema import Theme, ThemeVote


async def get_all(db: Connection) -> list[Theme]:
    themes = await db.fetch("SELECT * FROM themes ORDER BY created_at DESC")
    return [Theme(**theme) for theme in themes]

async def add(name: str, creator_id: UUID, db: Connection) -> Theme:
    project: Record | None = await db.fetchrow(
        "INSERT INTO themes (name, creator_id) VALUES ($1, $2) RETURNING *",
        name,
        creator_id
    )
    if project is None:
        raise Exception("Failed to create theme")
    return Theme(**dict(project))

async def get_by_id(theme_id: UUID, db: Connection) -> Theme | None:
    project: Record | None = await db.fetchrow(
        "SELECT * FROM themes WHERE id = $1", theme_id
    )
    if project is None:
        return None
    return Theme(**dict(project))

async def add_vote(user_id: UUID, theme_id: UUID, db: Connection) -> ThemeVote | None:
    vote: Record | None = await db.fetchrow(
        "INSERT INTO theme_votes (user_id, theme_id) VALUES ($1, $2) RETURNING *",
        user_id, theme_id
    )
    if vote is None:
        return None
    return ThemeVote(**dict(vote))

async def get_vote(user_id: UUID, theme_id: UUID, db: Connection) -> ThemeVote | None:
    vote: Record | None = await db.fetchrow(
        "SELECT * FROM theme_votes WHERE user_id = $1 AND theme_id = $2",
        user_id, theme_id
    )
    if vote is None:
        return None
    return ThemeVote(**dict(vote))

async def get_votes_by_user_id(user_id: UUID, db: Connection) -> list[ThemeVote]:
    votes = await db.fetch(
        "SELECT * FROM theme_votes WHERE user_id = $1",
        user_id
    )
    return [ThemeVote(**vote) for vote in votes]

async def remove_vote(user_id: UUID, theme_id: UUID, db: Connection) -> None:
    await db.execute(
        "DELETE FROM theme_votes WHERE user_id = $1 AND theme_id = $2",
        user_id, theme_id
    )
