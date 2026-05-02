from models import User, Unit, Review, Discussion, Comment, Project, UserRole
from datetime import datetime

# -------------------------
# "TABLES"
# -------------------------


# Users
users = [
    User(1, "michael", "m@example.com", "hash1", role=UserRole.STUDENT),
    User(2, "sarah", "s@example.com", "hash2", role=UserRole.STUDENT),
    User(3, "james", "j@example.com", "hash3", role=UserRole.MODERATOR),
    User(4, "admin", "admin@example.com", "hash4", role=UserRole.ADMIN),
    User(5, "alex", "alex@example.com", "hash5", role=UserRole.STUDENT),
]

# Units
units = [
    Unit(
        code="CITS1401",
        name="Computational Thinking with Python",
        level=1,
        rating=4.5,
        workload=3.0,
        handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS1401",
        tags=["python", "intro", "core"]
    ),
    Unit(
        code="CITS1402",
        name="Relational Database Management Systems",
        level=1,
        rating=4.2,
        workload=3.2,
        handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS1402",
        tags=["sql", "databases"]
    ),
    Unit(
        code="CITS2005",
        name="Object Oriented Programming",
        level=2,
        rating=4.0,
        workload=3.8,
        handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS2005",
        tags=["java", "oop", "core"]
    ),
    Unit(
        code="CITS3403",
        name="Agile Web Development",
        level=3,
        rating=4.7,
        workload=4.0,
        handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS3403",
        tags=["web", "flask", "group-project"]
    ),
]

# reviews
reviews = []

review_id = 1

def add_review(unit_code, author_id, rating, workload, content):
    global review_id
    reviews.append(
        Review(
            review_id=review_id,
            unit_code=unit_code,
            author_id=author_id,
            rating=rating,
            workload=workload,
            content=content,
            created_at=datetime.now()
        )
    )
    review_id += 1
    
    # CITS1401
add_review("CITS1401", 1, 5, 3, "Great intro unit, very beginner friendly.")
add_review("CITS1401", 2, 4, 3, "Good pacing, assignments were fair.")
add_review("CITS1401", 3, 5, 2, "Easy HD if you stay consistent.")
add_review("CITS1401", 4, 4, 3, "Lectures were clear.")
add_review("CITS1401", 5, 5, 3, "Loved learning Python here.")

    # CITS1402
for i in range(5):
    add_review("CITS1402", (i % 5) + 1, 4, 3, "Solid database fundamentals.")

    # CITS2005
for i in range(5):
    add_review("CITS2005", (i % 5) + 1, 4, 4, "Java OOP concepts are important.")

    # CITS3403
for i in range(5):
    add_review("CITS3403", (i % 5) + 1, 5, 4, "Great project-based unit.")

# discussions
discussions = []

# projects
projects = []

# comments
comments = []

# populating discussions and comments
discussion_id = 1
comment_id = 1

def create_discussion(unit_code, title, author_id, body):
    global discussion_id
    d = Discussion(
        discussion_id=discussion_id,
        unit_code=unit_code,
        title=title,
        author_id=author_id,
        created_at=datetime.now(),
        body=body,
        upvotes=10,
        downvotes=2
    )
    discussions.append(d)
    discussion_id += 1
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

def add_comment(discussion, author_id, content, parent_id=None):
    global comment_id
    c = Comment(
        comment_id=comment_id,
        author_id=author_id,
        content=content,
        created_at=datetime.now(),
        parent_comment_id=parent_id
    )
    discussion.comments.append(c)
    comment_id += 1
    return c

c1 = add_comment(d1, 2, "Group matters a LOT. Try to find proactive people.")
c2 = add_comment(d1, 3, "Start early and use Git properly.")
c3 = add_comment(d1, 4, "Communication is everything.")

# replies to c1
add_comment(d1, 5, "How do you find good teammates?", parent_id=c1.comment_id)
add_comment(d1, 2, "Usually through labs or Discord.", parent_id=c1.comment_id)

# replies to c2
add_comment(d1, 1, "Any Git tips?", parent_id=c2.comment_id)
add_comment(d1, 3, "Use branches + PRs always.", parent_id=c2.comment_id)

# more top-level
add_comment(d1, 5, "Don't leave frontend to last week.")
add_comment(d1, 2, "Test your APIs early.")

for d in discussions:
    for u in units:
        if u.code == d.unit_code:
            u.discussions.append(d.discussion_id)