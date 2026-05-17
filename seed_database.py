from app import db, create_app
from app.models import *
from datetime import datetime, timezone


# -------------------------------------------------
# APP CONTEXT
# -------------------------------------------------

app = create_app()

with app.app_context():

    # -------------------------------------------------
    # RESET DATABASE
    # -------------------------------------------------

    db.drop_all()
    db.create_all()


     # -------------------------------------------------
    # USERS
    # -------------------------------------------------

    users = []

    user_data = [

        # -------------------------
        # MAMBWE
        # -------------------------

        {
            "username": "mambwe_admin",
            "email": "mambwe.admin@unireviews.com",
            "password": "hash1",
            "role": UserRole.ADMIN
        },

        {
            "username": "mambwe_mod",
            "email": "mambwe.mod@unireviews.com",
            "password": "hash2",
            "role": UserRole.MODERATOR
        },

        {
            "username": "mambwe_student",
            "email": "mambwe.student@unireviews.com",
            "password": "hash3",
            "role": UserRole.STUDENT
        },

        # -------------------------
        # KEITHLIN
        # -------------------------

        {
            "username": "keithlin_admin",
            "email": "keithlin.admin@unireviews.com",
            "password": "hash4",
            "role": UserRole.ADMIN
        },

        {
            "username": "keithlin_mod",
            "email": "keithlin.mod@unireviews.com",
            "password": "hash5",
            "role": UserRole.MODERATOR
        },

        {
            "username": "keithlin_student",
            "email": "keithlin.student@unireviews.com",
            "password": "hash6",
            "role": UserRole.STUDENT
        },

        # -------------------------
        # BRONTE
        # -------------------------

        {
            "username": "bronte_admin",
            "email": "bronte.admin@unireviews.com",
            "password": "hash7",
            "role": UserRole.ADMIN
        },

        {
            "username": "bronte_mod",
            "email": "bronte.mod@unireviews.com",
            "password": "hash8",
            "role": UserRole.MODERATOR
        },

        {
            "username": "bronte_student",
            "email": "bronte.student@unireviews.com",
            "password": "hash9",
            "role": UserRole.STUDENT
        },
    ]

    for data in user_data:
        user = User(
            username=data["username"],
            email=data["email"],
            role=data["role"]
        )

        # Call the hybrid-property setter
        user.password_hash = data["password"]
        users.append(user)

    db.session.add_all(users)


    # -------------------------------------------------
    # UNITS
    # -------------------------------------------------

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


# -------------------------------------------------
    # DATABASE HELPER ARCHITECTURE (With .flush())
    # -------------------------------------------------
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

    def add_project(unit_code, title, description, author_id, link_url=None):
        p = Project(
            unit_code=unit_code,
            title=title,
            description=description,
            author_id=author_id,
            external_link=link_url,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(p)

# --- CITS1401 REVIEWS ---
    add_review("CITS1401", 1, 5, 3, "Great intro unit, very beginner friendly.")
    add_review("CITS1401", 2, 4, 3, "Good pacing, assignments were fair.")
    add_review("CITS1401", 3, 5, 2, "Easy HD if you stay consistent.")
    add_review("CITS1401", 4, 4, 3, "Lectures were clear.")
    add_review("CITS1401", 5, 5, 3, "Loved learning Python here.")

# --- CITS2005 REVIEWS ---
    add_review("CITS2005", 1, 5, 4, "The lectures are so engaging, and really good to go to in person. For anyone taking it, I highly recommend actually attending the lab sessions, super helpful before exams!!")
    add_review("CITS2005", 2, 3, 4, "It's a alright unit, takes up so much time during the entire sem. Contents pretty interesting.")
    add_review("CITS2005", 3, 5, 5, "Plan your time wisely, do not leave project to the night before! You will regret it!!")
    add_review("CITS2005", 4, 2, 5, "All the reviews are inaccurate. Horrible unit, don't take it if you want any social life.")
    add_review("CITS2005", 5, 3, 3, "Great resources on LMS better than most other CS units so take advantage of it.")

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
        db.session.flush()
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
# DISCUSSIONS (CITS2005)
# -------------------------

    d4 = create_discussion(
        "CITS2005",
        "Does everyone use Latex for this or is there a better editor?", 
        4, 
        "I'm using Latex for the project but it feels a bit buggy, any suggestions please?"
    )

    d5 = create_discussion(
        "CITS2005",
        "Anyone know a tutor for this that's not like $1000 an hour!!?",
        5, 
        "Struggling!! Let me know if you have a good contact"
    )

    d6 = create_discussion(
        "CITS2005", 
        "Hey anyone taking this unit sem 1 2026, if so drop a reply for any questions we can help each other with!",
        6,
        "lmk :P"
    )

    d7 = create_discussion(
        "CITS2005",
        "Anyone know what concepts are in the exam",
        7, 
        "They haven't mentioned in lectures and its getting close."
    )

    d8 = create_discussion(
        "CITS2005",
        "Kinda interested in this as an elective, is workload too hard. I can't really gage from the quick review graph on the other page.", 
        8, 
        " I'm willing to put some time in so not really worried about workload, but is it worth it. If you have already taken, what did you get out of it? Cheers"
    )

    d9 = create_discussion(
        "CITS2005",
        " Anyone retaking this in sem 2?? lmk",
        3,
        "Failed just on exam, what should i do next sem to pass?"
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
        db.session.flush()
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

    # -------------------------
    # COMMENTS Discussion 4
    # -------------------------
    c4 = add_comment(d4.discussion_id, 1, "Nah stick with it, or go to a lab and get them to help.")
    c5 = add_comment(d4.discussion_id, 2, "I used Overleaf and it was fine.")
    c6 = add_comment(d4.discussion_id, 5, "Get the latex extension on VS, has better UI.")

    add_comment(d4.discussion_id, 3, "Overleaf is where its at!", parent_id=c5.comment_id)
    add_comment(d4.discussion_id, 4, "I had some weird issues with Overleaf but it was generally good.", parent_id=c5.comment_id)

    db.session.commit()

    # -------------------------
    # COMMENTS Discussion 5
    # -------------------------
    c7 = add_comment(d5.discussion_id,2,"Sorry bro you're on your own")
    c8 = add_comment(d5.discussion_id,1,"Yep email my student id 32412399!!")
    c9 = add_comment(d5.discussion_id,3,"email the UC she will respond with a list")

    add_comment(d5.discussion_id, 3, "email the uc!!", parent_id=c7.comment_id)
    add_comment(d5.discussion_id,4,"ill email you too", parent_id=c8.comment_id)

    db.session.commit()

    # -------------------------
    # COMMENTS Discussion 6
    # -------------------------

    c10 = add_comment(d6.discussion_id,1,"me!!!")
    c11 = add_comment(d6.discussion_id,2,"i am, msg me on instagram @citscitscits")
    
    db.session.commit()

    # -------------------------
    # COMMENTS Discussion 7
    # -------------------------

    c12 = add_comment(d7.discussion_id,1,"its really similiar to practise ones")
    c13 = add_comment(d7.discussion_id,2,"i know!!! could they wait longer")
    c14 = add_comment(d7.discussion_id,3,"likely just weeks 7-12 because of midsem")
    c15 = add_comment(d7.discussion_id,4,"i know im stressed!")

    add_comment(d7.discussion_id,4,"me too, glad to know someone else is", parent_id=c15.comment_id)
    
    db.session.commit()
    
    # -------------------------
    # COMMENTS Discussion 8
    # -------------------------

    c16 = add_comment(d8.discussion_id,4,"all i can say is no")
    c17 = add_comment(d8.discussion_id,3,"hell no bro")
    c18 = add_comment(d8.discussion_id,2,"needed a good laugh today. thanks")

    add_comment(d8.discussion_id,1," i love how everyones just roasting them",parent_id=c16.comment_id)
   
    db.session.commit()

    # -------------------------
    # COMMENTS Discussion 9 
    # -------------------------

    c19 = add_comment(d9.discussion_id,1,"no but all the best")
    c20 = add_comment(d9.discussion_id,2,"you got this")

    db.session.commit()


    # -------------------------
    # PROJECTS (CITS2005)
    # -------------------------
    add_project(
        unit_code="CITS2005",
        title="Group Project 2026",
        description="Major project for the sem: OOP design in Java.",
        author_id=5,
        link_url="https://github.com/KGLapuz/AgileWebDevCits3403.git"
    )

    add_project(
        unit_code="CITS2005",
        title="OOP assignment: Java",
        description="Lots of definitions and theory if you need something to compare to",
        author_id=6,
        link_url="https://github.com/KGLapuz/AgileWebDevCits3403.git"
    )

    add_project(
        unit_code="CITS2005",
        title="Lab 5",
        description="Weekly lab exercises are optional, check out what I made with it .",
        author_id=9,
        link_url="https://github.com/KGLapuz/AgileWebDevCits3403.git"
    )

    add_project(
        unit_code="CITS2005",
        title="Mid-sem online ",
        description="This has screenshots from the 24 hour assignment online and what I was able to create, to give you an idea of how much you'll be able to complete!",
        author_id=3,
        link_url="https://github.com/KGLapuz/AgileWebDevCits3403.git"
    )

    db.session.commit()
    
    print("Database seeded successfully!")
    print(f"Seeded {len(users)} users")
    print(f"Seeded {len(units)} units")
