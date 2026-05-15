from app import db, create_app
from app.models import *
from werkzeug.security import generate_password_hash

from datetime import datetime


# -------------------------
# SEED SCRIPT CONTEXT
# -------------------------
# Must run inside Flask app context
# -------------------------

app = create_app()
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

        # -------------------------
        # MAMBWE
        # -------------------------

        User(
            username="mambwe_admin",
            email="mambwe.admin@unireviews.com",
            password_hash=generate_password_hash("hash1"),
            role=UserRole.ADMIN
        ),

        User(
            username="mambwe_mod",
            email="mambwe.mod@unireviews.com",
            password_hash=generate_password_hash("hash2"),
            role=UserRole.MODERATOR
        ),

        User(
            username="mambwe_student",
            email="mambwe.student@unireviews.com",
            password_hash=generate_password_hash("hash3"),
            role=UserRole.STUDENT
        ),


        # -------------------------
        # KEITHLIN
        # -------------------------

        User(
            username="keithlin_admin",
            email="keithlin.admin@unireviews.com",
            password_hash=generate_password_hash("hash4"),
            role=UserRole.ADMIN
        ),

        User(
            username="keithlin_mod",
            email="keithlin.mod@unireviews.com",
            password_hash=generate_password_hash("hash5"),
            role=UserRole.MODERATOR
        ),

        User(
            username="keithlin_student",
            email="keithlin.student@unireviews.com",
            password_hash=generate_password_hash("hash6"),
            role=UserRole.STUDENT
        ),


        # -------------------------
        # BRONTE
        # -------------------------

        User(
            username="bronte_admin",
            email="bronte.admin@unireviews.com",
            password_hash=generate_password_hash("hash7"),
            role=UserRole.ADMIN
        ),

        User(
            username="bronte_mod",
            email="bronte.mod@unireviews.com",
            password_hash=generate_password_hash("hash8"),
            role=UserRole.MODERATOR
        ),

        User(
            username="bronte_student",
            email="bronte.student@unireviews.com",
            password_hash=generate_password_hash("hash9"),
            role=UserRole.STUDENT
        ),
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
            tags=["python"]
        ),

        Unit(
            code="CITS1501",
            name="Introduction to Programming with Python",
            level=1,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS1501",
            tags=["python"]
        ),

        Unit(
            code="CITS2002",
            name="Systems Programming",
            level=2,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS2002",
            tags=["c"]
        ),

        Unit(
            code="CITS2005",
            name="Object Oriented Programming",
            level=2,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS2005",
            tags=["java"]
        ),

        Unit(
            code="CITS2006",
            name="Defensive Cybersecurity",
            level=2,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS2006",
            tags=["security"]
        ),

        Unit(
            code="CITS2200",
            name="Data Structures and Algorithms",
            level=2,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS2200",
            tags=["java"]
        ),

        Unit(
            code="CITS2211",
            name="Discrete Structures",
            level=2,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS2211",
            tags=["mathematics"]
        ),

        Unit(
            code="CITS2401",
            name="Computer Analysis and Visualisation",
            level=2,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS2401",
            tags=["python"]
        ),

        Unit(
            code="CITS3001",
            name="Advanced Algorithms",
            level=3,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS3001",
            tags=["algorithms"]
        ),

        Unit(
            code="CITS3002",
            name="Computer Networks",
            level=3,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS3002",
            tags=["networking"]
        ),

        Unit(
            code="CITS3003",
            name="Graphics and Animation",
            level=3,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS3003",
            tags=["graphics"]
        ),

        Unit(
            code="CITS3005",
            name="Knowledge Representation",
            level=3,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS3005",
            tags=["ai"]
        ),

        Unit(
            code="CITS3007",
            name="Secure Coding",
            level=3,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS3007",
            tags=["security"]
        ),

        Unit(
            code="CITS3009",
            name="Computer Science WIL Internship",
            level=3,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS3009",
            tags=["industry"]
        ),

        Unit(
            code="CITS3011",
            name="Intelligent Agents",
            level=3,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS3011",
            tags=["ai"]
        ),

        Unit(
            code="CITS3402",
            name="High Performance Computing",
            level=3,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS3402",
            tags=["c"]
        ),

        Unit(
            code="CITS3403",
            name="Agile Web Development",
            level=3,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS3403",
            tags=["web"]
        ),

        Unit(
            code="CITS4001",
            name="Computer Science and Software Engineering Research Project Part 1",
            level=4,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS4001",
            tags=["research"]
        ),

        Unit(
            code="CITS4002",
            name="Computer Science and Software Engineering Research Project Part 2",
            level=4,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS4002",
            tags=["research"]
        ),

        Unit(
            code="CITS4010",
            name="Computer Science Honours Research Project Part 1",
            level=4,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS4010",
            tags=["research"]
        ),

        Unit(
            code="CITS4011",
            name="Computer Science Honours Research Project Part 2",
            level=4,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS4011",
            tags=["research"]
        ),

        Unit(
            code="CITS4012",
            name="Natural Language Processing",
            level=4,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS4012",
            tags=["python"]
        ),

        Unit(
            code="CITS4403",
            name="Computational Modelling",
            level=4,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS4403",
            tags=["python"]
        ),

        Unit(
            code="CITS4404",
            name="Artificial Intelligence and Adaptive Systems",
            level=4,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS4404",
            tags=["ai"]
        ),

        Unit(
            code="CITS4407",
            name="Open Source Tools and Scripting",
            level=4,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS4407",
            tags=["linux"]
        ),

        Unit(
            code="CITS4419",
            name="Mobile and Wireless Computing",
            level=4,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS4419",
            tags=["mobile"]
        ),

        Unit(
            code="CITS4505",
            name="Human Aspects of Cybersecurity",
            level=4,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS4505",
            tags=["security"]
        ),

        Unit(
            code="CITS5014",
            name="Data and Information Technologies Research Project Part 1",
            level=5,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS5014",
            tags=["research"]
        ),

        Unit(
            code="CITS5015",
            name="Data and Information Technologies Research Project Part 2",
            level=5,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS5015",
            tags=["research"]
        ),

        Unit(
            code="CITS5017",
            name="Deep Learning",
            level=5,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS5017",
            tags=["python"]
        ),

        Unit(
            code="CITS5206",
            name="Information Technology Capstone Project",
            level=5,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS5206",
            tags=["project"]
        ),

        Unit(
            code="CITS5503",
            name="Cloud Computing",
            level=5,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS5503",
            tags=["cloud"]
        ),

        Unit(
            code="CITS5505",
            name="Agile Web Development",
            level=5,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS5505",
            tags=["web"]
        ),

        Unit(
            code="CITS5506",
            name="The Internet of Things",
            level=5,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS5506",
            tags=["iot"]
        ),

        Unit(
            code="CITS5507",
            name="High Performance Computing",
            level=5,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS5507",
            tags=["c"]
        ),

        Unit(
            code="CITZ5101",
            name="Fundamentals of AI: Predictive AI to GenAI",
            level=5,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITZ5101",
            tags=["ai"]
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
            created_at=datetime.now(timezone.utc)
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
            created_at=datetime.now(timezone.utc),
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
            created_at=datetime.now(timezone.utc),
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