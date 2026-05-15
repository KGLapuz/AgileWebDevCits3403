from datetime import datetime, timezone
from enum import Enum

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property


# -------------------------------------------------
# USER ROLE ENUM
# -------------------------------------------------

class UserRole(Enum):
    STUDENT = "student"
    MODERATOR = "moderator"
    ADMIN = "admin"


# -------------------------------------------------
# USER MODEL
# -------------------------------------------------

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    _password_hash = db.Column(
        db.String(256),
        nullable=False
    )

    role = db.Column(
        db.Enum(UserRole),
        default=UserRole.STUDENT,
        nullable=False
    )

    # Relationships
    reviews = db.relationship(
        "Review",
        back_populates="author",
        cascade="all, delete-orphan",
        order_by="desc(Review.created_at)"
    )

    discussions = db.relationship(
        "Discussion",
        back_populates="author",
        cascade="all, delete-orphan",
        order_by="desc(Discussion.created_at)"
    )

    comments = db.relationship(
        "Comment",
        back_populates="author",
        cascade="all, delete-orphan",
        order_by="desc(Comment.created_at)"
    )

    projects = db.relationship(
        "Project",
        back_populates="author",
        cascade="all, delete-orphan",
        order_by="desc(Project.created_at)"
    )

    # -------------------------------------------------
    # PASSWORD — hybrid property, setter, authenticator
    # -------------------------------------------------

    @property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed.")

    @password_hash.setter
    def password_hash(self, plaintext):
        self._password_hash = generate_password_hash(plaintext)

    def authenticate(self, plaintext):
        return check_password_hash(self._password_hash, plaintext)

    def __repr__(self):
        return f"<User {self.username}>"


# -------------------------------------------------
# UNIT MODEL
# -------------------------------------------------

class Unit(db.Model):
    __tablename__ = "units"

    code = db.Column(
        db.String(16),
        primary_key=True
    )

    name = db.Column(
        db.String(255),
        nullable=False
    )

    level = db.Column(
        db.Integer,
        nullable=False
    )

    handbook_link = db.Column(db.String(500))

    tags = db.Column(db.JSON, default=list)

    # Relationships
    reviews = db.relationship(
        "Review",
        back_populates="unit",
        cascade="all, delete-orphan",
        order_by="desc(Review.created_at)"
    )

    discussions = db.relationship(
        "Discussion",
        back_populates="unit",
        cascade="all, delete-orphan",
        order_by="desc(Discussion.created_at)"
    )

    projects = db.relationship(
        "Project",
        back_populates="unit",
        cascade="all, delete-orphan",
        order_by="desc(Project.created_at)"
    )

    @property
    def review_count(self):
        return len(self.reviews)

    @property
    def rating(self):
        if not self.reviews:
            return 0.0
        return sum(r.rating for r in self.reviews) / len(self.reviews)

    @property
    def workload(self):
        if not self.reviews:
            return 0.0
        return sum(r.workload for r in self.reviews) / len(self.reviews)

    def __repr__(self):
        return f"<Unit {self.code}>"


# -------------------------------------------------
# REVIEW MODEL
# -------------------------------------------------

class Review(db.Model):
    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, primary_key=True)

    unit_code = db.Column(
        db.String(16),
        db.ForeignKey("units.code"),
        nullable=False
    )

    author_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False
    )

    rating = db.Column(db.Float, nullable=False)
    workload = db.Column(db.Float, nullable=False)

    content = db.Column(db.Text, nullable=False)

    get_ahead_tip = db.Column(db.String(200), nullable=True)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    unit = db.relationship(
        "Unit",
        back_populates="reviews"
    )

    author = db.relationship(
        "User",
        back_populates="reviews"
    )

    def __repr__(self):
        return f"<Review {self.review_id}>"


# -------------------------------------------------
# DISCUSSION MODEL
# -------------------------------------------------

class Discussion(db.Model):
    __tablename__ = "discussions"

    discussion_id = db.Column(
        db.Integer,
        primary_key=True
    )

    unit_code = db.Column(
        db.String(16),
        db.ForeignKey("units.code"),
        nullable=False
    )

    author_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    body = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    unit = db.relationship(
        "Unit",
        back_populates="discussions"
    )

    author = db.relationship(
        "User",
        back_populates="discussions"
    )

    comments = db.relationship(
        "Comment",
        back_populates="discussion",
        cascade="all, delete-orphan",
        order_by="desc(Comment.created_at)"
    )

    @property
    def reply_count(self):
        return len(self.comments)

    def __repr__(self):
        return f"<Discussion {self.title}>"


# -------------------------------------------------
# COMMENT MODEL
# -------------------------------------------------

class Comment(db.Model):
    __tablename__ = "comments"

    comment_id = db.Column(
        db.Integer,
        primary_key=True
    )

    discussion_id = db.Column(
        db.Integer,
        db.ForeignKey("discussions.discussion_id"),
        nullable=False
    )

    comment_author_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    parent_comment_id = db.Column(
        db.Integer,
        db.ForeignKey("comments.comment_id"),
        nullable=True
    )

    # Relationships
    discussion = db.relationship(
        "Discussion",
        back_populates="comments"
    )

    author = db.relationship(
        "User",
        back_populates="comments"
    )

    # Self-referential relationship
    replies = db.relationship(
        "Comment",
        backref=db.backref(
            "parent",
            remote_side=[comment_id]
        ),
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Comment {self.comment_id}>"


# -------------------------------------------------
# PROJECT MODEL
# -------------------------------------------------

class Project(db.Model):
    __tablename__ = "projects"

    project_id = db.Column(
        db.Integer,
        primary_key=True
    )

    unit_code = db.Column(
        db.String(16),
        db.ForeignKey("units.code"),
        nullable=False
    )

    author_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    external_link = db.Column(db.String(500))

    # Relationships
    unit = db.relationship(
        "Unit",
        back_populates="projects"
    )

    author = db.relationship(
        "User",
        back_populates="projects"
    )

    def __repr__(self):
        return f"<Project {self.title}>"