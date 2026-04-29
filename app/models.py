from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


# -------------------------
# USER MODEL
# -------------------------

@dataclass
class User:
    user_id: int
    username: str
    email: str
    # Temporary feature: we will implement proper authentication later
    password_hash: str  # never store raw passwords

    # Optional / dynamic fields
    recently_viewed_units: List[str] = field(default_factory=list)
    recently_viewed_discussions: List[int] = field(default_factory=list)
    recently_viewed_projects: List[int] = field(default_factory=list)
    study_plan: List[str] = field(default_factory=list)  # unit codes
    bookmarks: List[str] = field(default_factory=list)   # could be URLs or IDs


# -------------------------
# UNIT MODEL
# -------------------------

@dataclass
class Unit:
    code: str
    name: str
    level: int

    # Aggregated values
    review_count: int = 0
    rating: float = 0.0
    workload: float = 0.0

    prerequisites: List[str] = field(default_factory=list)
    tips: Optional[str] = None  # advisable prior study / get-ahead tips

    # Relationships (IDs reference other objects)
    discussions: List[int] = field(default_factory=list)
    projects: List[int] = field(default_factory=list)


# -------------------------
# DISCUSSION + COMMENTS
# -------------------------

@dataclass
class Comment:
    comment_id: int
    author_id: int
    content: str
    created_at: datetime

    # For nested replies
    parent_comment_id: Optional[int] = None


@dataclass
class Discussion:
    discussion_id: int
    unit_code: str  # link back to Unit

    title: str
    author_id: int
    created_at: datetime
    body: str

    comments: List[Comment] = field(default_factory=list)

    def reply_count(self) -> int:
        return len(self.comments)


# -------------------------
# PROJECT MODEL
# -------------------------

@dataclass
class Project:
    project_id: int
    unit_code: str

    title: str
    author_id: int
    created_at: datetime
    year: int

    description: str
    external_link: Optional[str] = None  # GitHub or other resource