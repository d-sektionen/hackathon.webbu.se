from asyncpg import Connection

from .schema import Theme


async def get_all(db: Connection) -> list[Theme]:
    themes = await db.fetch("SELECT * FROM themes")
    return [Theme(**theme) for theme in themes]
