from app import db, app
from app.models import *

from datetime import datetime


# -------------------------
# SEED SCRIPT CONTEXT
# -------------------------
# Must run inside Flask app context
# -------------------------

with app.app_context():

    # -------------------------
    # RESET DATABASE 
    # -------------------------
    db.drop_all()
    db.create_all()


    # -------------------------
    # USERS
    # -------------------------
    users = [
        User(username="michael", email="m@example.com", password_hash="hash1", role=UserRole.STUDENT),
        User(username="sarah", email="s@example.com", password_hash="hash2", role=UserRole.STUDENT),
        User(username="james", email="j@example.com", password_hash="hash3", role=UserRole.MODERATOR),
        User(username="admin", email="admin@example.com", password_hash="hash4", role=UserRole.ADMIN),
        User(username="alex", email="alex@example.com", password_hash="hash5", role=UserRole.STUDENT),
        User(username="bronte", email="bronte@unireviews.com", password_hash="hash6", role=UserRole.ADMIN),
        User(username="keithlin", email="keithlin@unireviews.com", password_hash="hash7", role=UserRole.MODERATOR),
        User(username="mambwe", email="mambwe@unireviews.com", password_hash="hash8", role=UserRole.STUDENT),
    ]

    db.session.add_all(users)
    db.session.commit()


    # -------------------------
    # UNITS
    # -------------------------
    units = [
        Unit(
            code="CITS1401",
            name="Computational Thinking with Python",
            level=1,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS1401",
            tags=["python", "intro", "core"]
        ),
        Unit(
            code="CITS1402",
            name="Relational Database Management Systems",
            level=1,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS1402",
            tags=["sql", "databases", "Data Science"]
        ),
        Unit(
            code="CITS2005",
            name="Object Oriented Programming",
            level=2,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS2005",
            tags=["java", "oop", "core"]
        ),
        Unit(
            code="CITS3403",
            name="Agile Web Development",
            level=3,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS3403",
            tags=["web", "flask", "group-project"]
        ),
    ]

    db.session.add_all(units)
    db.session.commit()


    # -------------------------
    # REVIEWS
    # -------------------------
    def add_review(unit_code, author_id, rating, workload, content):

        review = Review(
            unit_code=unit_code,
            author_id=author_id,
            rating=rating,
            workload=workload,
            content=content,
            created_at=datetime.utcnow()
        )

        db.session.add(review)


    add_review("CITS1401", 1, 5, 3, "Great intro unit, very beginner friendly.")
    add_review("CITS1401", 2, 4, 3, "Good pacing, assignments were fair.")
    add_review("CITS1401", 3, 5, 2, "Easy HD if you stay consistent.")
    add_review("CITS1401", 4, 4, 3, "Lectures were clear.")
    add_review("CITS1401", 5, 5, 3, "Loved learning Python here.")

    for i in range(5):
        add_review("CITS1402", (i % 5) + 1, 4, 3, "Solid database fundamentals.")

    for i in range(5):
        add_review("CITS2005", (i % 5) + 1, 4, 4, "Java OOP concepts are important.")

    for i in range(5):
        add_review("CITS3403", (i % 5) + 1, 5, 4, "Great project-based unit.")


    db.session.commit()


    # -------------------------
    # DISCUSSIONS
    # -------------------------
    def create_discussion(unit_code, title, author_id, body):

        d = Discussion(
            unit_code=unit_code,
            title=title,
            author_id=author_id,
            body=body,
            created_at=datetime.utcnow(),
            upvotes=10,
            downvotes=2
        )

        db.session.add(d)
        return d


    d1 = create_discussion(
        "CITS3403",
        "How hard is the group project?",
        1,
        "I'm worried about getting a bad group. Any advice?"
    )

    d2 = create_discussion(
        "CITS3403",
        "Best tech stack to use?",
        2,
        "Flask vs Node?"
    )

    d3 = create_discussion(
        "CITS3403",
        "How to prepare before semester?",
        3,
        "What should I learn early?"
    )

    db.session.commit()


    # -------------------------
    # COMMENTS
    # -------------------------
    def add_comment(discussion_id, author_id, content, parent_id=None):

        c = Comment(
            discussion_id=discussion_id,
            comment_author_id=author_id,
            content=content,
            created_at=datetime.utcnow(),
            parent_comment_id=parent_id
        )

        db.session.add(c)
        return c


    c1 = add_comment(d1.discussion_id, 2, "Group matters a LOT. Try to find proactive people.")
    c2 = add_comment(d1.discussion_id, 3, "Start early and use Git properly.")
    c3 = add_comment(d1.discussion_id, 4, "Communication is everything.")

    add_comment(d1.discussion_id, 5, "How do you find good teammates?", parent_id=c1.comment_id)
    add_comment(d1.discussion_id, 2, "Usually through labs or Discord.", parent_id=c1.comment_id)

    add_comment(d1.discussion_id, 1, "Any Git tips?", parent_id=c2.comment_id)
    add_comment(d1.discussion_id, 3, "Use branches + PRs always.", parent_id=c2.comment_id)

    add_comment(d1.discussion_id, 5, "Don't leave frontend to last week.")
    add_comment(d1.discussion_id, 2, "Test your APIs early.")

    db.session.commit()

    print("Database seeded successfully!")