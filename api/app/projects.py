import uuid

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from . import utils
from .db import projects, schema
from .deps import get_current_session, get_db

router = APIRouter()

class ProjectRequest(BaseModel):
    name: str
    description: str
    github_url: str | None = None

class ProjectResponse(BaseModel):
    project: schema.Project

class ProjectListResponse(BaseModel):
    projects: list[schema.Project]

class ReadmeResponse(BaseModel):
    content: str

@router.post("/projects")
async def create_project(
    project_data: ProjectRequest,
    session: schema.Session = Depends(get_current_session),
    conn: Connection = Depends(get_db),
) -> ProjectResponse:
    if project_data.github_url is not None:
        try:
            utils.match_github_url(project_data.github_url)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid GitHub URL"
            )

    project = await projects.add(
        project_data.name,
        project_data.description,
        project_data.github_url,
        session.user_id,
        conn,
    )
    return ProjectResponse(project=project)


@router.get("/projects")
async def list_projects(conn: Connection = Depends(get_db)) -> ProjectListResponse:
    project_list = await projects.get_all(conn)

    return ProjectListResponse(projects=project_list)


@router.get("/projects/{project_id}")
async def get_project(project_id: uuid.UUID, conn: Connection = Depends(get_db)) -> ProjectResponse:
    project = await projects.get_by_id(project_id, conn)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    return ProjectResponse(project=project)


@router.put("/projects/{project_id}")
async def update_project(
    project_id: uuid.UUID,
    project_data: ProjectRequest,
    session: schema.Session = Depends(get_current_session),
    conn: Connection = Depends(get_db),
) -> ProjectResponse:
    project = await projects.get_by_id(project_id, conn)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    if project.owner_user_id != session.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this project",
        )

    if project_data.github_url is not None:
        try:
            utils.match_github_url(project_data.github_url)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid GitHub URL"
            )

    updated_project = await projects.update(
        project_id,
        project_data.name,
        project_data.description,
        project_data.github_url,
        conn,
    )

    return ProjectResponse(project=updated_project)


@router.get(
    "/projects/{project_id}/readme",
)
async def get_github_readme(project_id: uuid.UUID, conn: Connection = Depends(get_db)) -> ReadmeResponse:
    """Fetch the project README via the GitHub API.

    Args:
        project_id: Project UUID.

    Returns:
        Plain-text README content (text/plain; charset=utf-8).

    Raises:
        HTTPException: 204 if the project has no GitHub URL.
        HTTPException: 404 if the project is not found.
        HTTPException: 500 on GitHub fetch or decode errors.
    """
    project = await projects.get_by_id(project_id, conn)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    if not project.github_url:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Project does not have a GitHub URL",
        )

    readme_content = await utils.fetch_github_readme(project.github_url)

    return ReadmeResponse(content=readme_content)
