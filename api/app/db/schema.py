from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    id: UUID
    email: str
    password: str
    is_admin: bool
    created_at: datetime


@dataclass
class Session:
    user_id: UUID
    token: UUID
    created_at: datetime


@dataclass
class Project:
    id: UUID
    name: str
    description: str
    github_url: str
    owner_user_id: UUID
    created_at: datetime

@dataclass
class Theme:
    id: UUID
    name: str
    creator_id: UUID
    is_selected: bool
    created_at: datetime

@dataclass
class ThemeVote:
    user_id: UUID
    theme_id: UUID
    created_at: datetime
