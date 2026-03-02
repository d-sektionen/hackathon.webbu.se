from uuid import UUID

from asyncpg import Connection, Record

from .schema import Project


async def add(
    name: str,
    description: str,
    github_url: str | None,
    owner_user_id: UUID,
    db: Connection,
) -> Project:
    project: Record | None = await db.fetchrow(
        "INSERT INTO projects (name, description, github_url, owner_user_id) VALUES ($1, $2, $3, $4) RETURNING *",
        name,
        description,
        github_url,
        owner_user_id,
    )
    if project is None:
        raise Exception("Failed to create project")
    return Project(**dict(project))


async def get_all(db: Connection) -> list[Project]:
    projects = await db.fetch("SELECT * FROM projects")
    return [Project(**project) for project in projects]


async def get_by_id(project_id: UUID, db: Connection) -> Project | None:
    project: Record | None = await db.fetchrow(
        "SELECT * FROM projects WHERE id = $1", project_id
    )
    if project is None:
        return None
    return Project(**dict(project))


async def update(
    project_id: UUID,
    name: str,
    description: str,
    github_url: str | None,
    db: Connection,
) -> Project:
    project: Record | None = await db.fetchrow(
        "UPDATE projects SET name = $1, description = $2, github_url = $3 WHERE id = $4 RETURNING *",
        name,
        description,
        github_url,
        project_id,
    )
    if project is None:
        raise Exception("Failed to update project")
    return Project(**dict(project))
