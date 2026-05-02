from dataclasses import dataclass, field  # for simple data constructors
from typing import List, Optional # for type hints
from datetime import datetime # for timestamps
from enum import Enum # for role systems e.g. Student, Moderator, Admin


# -------------------------
# USER MODEL
# -------------------------
    # Role-based access control
@dataclass
class UserRole(Enum):
    STUDENT = "student"
    MODERATOR = "moderator"
    ADMIN = "admin"

@dataclass
class User:
    user_id: int
    username: str
    email: str
    role: 'UserRole' = UserRole.STUDENT # users are students by default
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
class Review:
    review_id: int
    unit_code: str
    author_id: int

    rating: float        #  1–5
    workload: float      #  1–5

    content: str
    created_at: datetime

@dataclass
class Unit:
    code: str
    name: str
    level: int
    handbook_link: str

    # Aggregated values
    review_count: int = 0
    rating: float = 0.0
    workload: float = 0.0

    reviews: List[int] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    tips: Optional[str] = None  # advisable prior study / get-ahead tips

    # Relationships (IDs reference other objects)
    discussions: List[int] = field(default_factory=list)
    projects: List[int] = field(default_factory=list)
    
    def calculate_rating(self, reviews: List[Review]) -> float:
        relevant = [r.rating for r in reviews if r.unit_code == self.code]
        return sum(relevant) / len(relevant) if relevant else 0.0
    
    def calculate_workload(self, reviews: List[Review]) -> float:
        relevant = [r.workload for r in reviews if r.unit_code == self.code]
        return sum(relevant) / len(relevant) if relevant else 0.0
    
    def increase_review_count(self):
        self.review_count += 1

# -------------------------
# DISCUSSION + COMMENTS
# -------------------------

@dataclass
class Comment:
    comment_id: int
    comment_author_id: int
    content: str
    created_at: datetime

    # For nested replies
    parent_comment_id: Optional[int] = None
    
    upvotes: int = 0
    downvotes: int = 0
    
    def score(self) -> int:
        return self.upvotes - self.downvotes
    
    def get_author_username(self, users: List["User"]) -> str:
        for user in users:
            if user.user_id == self.comment_author_id:
                return user.username
        return "Unknown"


@dataclass
class Discussion:
    discussion_id: int
    unit_code: str  # link back to Unit

    title: str
    author_id: int
    created_at: datetime
    body: str

    comments: List[Comment] = field(default_factory=list)
    
    upvotes: int = 0
    downvotes: int = 0
    voters: List[int] = field(default_factory=list)  # track users who voted

    def score(self) -> int:
        return self.upvotes - self.downvotes

    def reply_count(self) -> int:
        return len(self.comments)

    def get_author_username(self, users: List["User"]) -> str:
        for user in users:
            if user.user_id == self.author_id:
                return user.username
        return "Unknown"


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
    