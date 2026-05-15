from unittest import TestCase
from app import create_app, db
from app.models import User, Unit, Review, Discussion, Comment, Project, UserRole


class Testing(TestCase):

    # =========== SETUP AND TEARDOWN ===========

    def setUp(self):
        # RUN BEFORE EACH TEST
        from config import TestingConfig
        test_app = create_app(TestingConfig)      # spin up app with in-memory SQLite
        self.app_context = test_app.app_context()
        self.app_context.push()
        self.client = test_app.test_client()
        db.create_all()                           # create all tables in test DB

        # Populate DB with baseline data for all sections
        self.add_users()
        self.add_units()
        self.add_reviews()
        self.add_discussions()
        self.add_comments()
        self.add_projects()

    def tearDown(self):
        # RUN AFTER EACH TEST — wipe the in-memory DB clean
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    # =========== HELPER FUNCTIONS ===========

    def add_users(self):
        mambwe = User(username="mambwe_test", email="mambwe.test@unireviews.com")
        mambwe.password_hash = "password_mambwe"

        bronte = User(username="bronte_test", email="bronte.test@unireviews.com")
        bronte.password_hash = "password_bronte"

        keithlin = User(username="keithlin_test", email="keithlin.test@unireviews.com")
        keithlin.password_hash = "password_keithlin"

        db.session.add_all([mambwe, bronte, keithlin])
        db.session.commit()

    def add_units(self):
        unit = Unit(
            code="CITS1401",
            name="Computational Thinking with Python",
            level=1,
            handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS1401",
            tags=["python"]
        )
        db.session.add(unit)
        db.session.commit()

    def add_reviews(self):
        mambwe = User.query.filter_by(username="mambwe_test").first()
        review = Review(
            unit_code="CITS1401",
            author_id=mambwe.user_id,
            rating=5,
            workload=3,
            content="Great intro unit, very beginner friendly.",
            get_ahead_tip="Learn basic Python syntax before semester starts."
        )
        db.session.add(review)
        db.session.commit()

    def add_discussions(self):
        mambwe = User.query.filter_by(username="mambwe_test").first()
        discussion = Discussion(
            unit_code="CITS1401",
            author_id=mambwe.user_id,
            title="How hard is the group project?",
            body="I'm worried about getting a bad group. Any advice?"
        )
        db.session.add(discussion)
        db.session.commit()

    def add_comments(self):
        bronte = User.query.filter_by(username="bronte_test").first()
        discussion = Discussion.query.first()
        comment = Comment(
            discussion_id=discussion.discussion_id,
            comment_author_id=bronte.user_id,
            content="Don't worry, the groups are usually fine!"
        )
        db.session.add(comment)
        db.session.commit()

    def add_projects(self):
        keithlin = User.query.filter_by(username="keithlin_test").first()
        project = Project(
            unit_code="CITS1401",
            author_id=keithlin.user_id,
            title="Sorting Algorithm Visualiser",
            description="A Python tool that visually demonstrates common sorting algorithms.",
            external_link="https://github.com/keithlin/sorting-vis"
        )
        db.session.add(project)
        db.session.commit()


    # =========== UNIT TEST FUNCTIONS ===========

    # ===================== SECTION 1: User model =====================

    # ----++++ Check that the password_hash property raises AttributeError when accessed ++++----
    def test_password_hash_cannot_be_viewed(self):
        user = User.query.filter_by(username="mambwe_test").first()
        with self.assertRaises(AttributeError):
            _ = user.password_hash

    # ----++++ Check that the stored hash is not equal to the original plaintext password ++++----
    def test_password_is_hashed_not_stored_as_plaintext(self):
        user = User.query.filter_by(username="mambwe_test").first()
        self.assertNotEqual(user._password_hash, "password_mambwe")

    # ----++++ Check that authenticate() returns True when given the correct password ++++----
    def test_authenticate_returns_true_on_correct_password(self):
        user = User.query.filter_by(username="mambwe_test").first()
        self.assertTrue(user.authenticate("password_mambwe"))

    # ----++++ Check that authenticate() returns False when given the wrong password ++++----
    def test_authenticate_returns_false_on_wrong_password(self):
        user = User.query.filter_by(username="mambwe_test").first()
        self.assertFalse(user.authenticate("definitely_wrong"))

    # ----++++ Check that a user's role defaults to STUDENT on creation ++++----
    def test_user_role_defaults_to_student(self):
        user = User.query.filter_by(username="mambwe_test").first()
        self.assertEqual(user.role, UserRole.STUDENT)

    # ----++++ Check that two users cannot share the same email address ++++----
    def test_duplicate_email_raises_exception(self):
        duplicate = User(username="other_user", email="mambwe.test@unireviews.com")
        duplicate.password_hash = "somepassword"
        db.session.add(duplicate)
        with self.assertRaises(Exception):  # IntegrityError from unique=True constraint
            db.session.commit()

    # ----++++ Check that username cannot be null ++++----
    def test_username_cannot_be_null(self):
        user = User(email="nonull@unireviews.com")
        user.password_hash = "somepassword"
        db.session.add(user)
        with self.assertRaises(Exception):  # IntegrityError from nullable=False
            db.session.commit()

    # ----++++ Check that updating the password invalidates the old one ++++----
    def test_password_update_invalidates_old_password(self):
        user = User.query.filter_by(username="mambwe_test").first()
        user.password_hash = "new_password"
        db.session.commit()
        self.assertTrue(user.authenticate("new_password"))
        self.assertFalse(user.authenticate("password_mambwe"))


    # ===================== SECTION 2: Unit model =====================

    # ----++++ Check that a unit can be retrieved by its primary key code ++++----
    def test_unit_can_be_retrieved_by_code(self):
        unit = Unit.query.get("CITS1401")
        self.assertIsNotNone(unit)
        self.assertEqual(unit.name, "Computational Thinking with Python")

    # ----++++ Check that unit.rating returns 0.0 when there are no reviews ++++----
    def test_unit_rating_is_zero_with_no_reviews(self):
        empty_unit = Unit(code="CITS9999", name="Empty Unit", level=1)
        db.session.add(empty_unit)
        db.session.commit()
        self.assertEqual(empty_unit.rating, 0.0)

    # ----++++ Check that unit.rating correctly averages across multiple reviews ++++----
    def test_unit_rating_averages_correctly(self):
        mambwe = User.query.filter_by(username="mambwe_test").first()
        bronte = User.query.filter_by(username="bronte_test").first()
        # Add a second review so we can test averaging (first review has rating=5)
        db.session.add(Review(
            unit_code="CITS1401",
            author_id=bronte.user_id,
            rating=3,
            workload=5,
            content="Decent unit but lectures were dry and hard to follow."
        ))
        db.session.commit()
        unit = Unit.query.get("CITS1401")
        self.assertAlmostEqual(unit.rating, 4.0)  # (5 + 3) / 2

    # ----++++ Check that unit name cannot be null ++++----
    def test_unit_name_cannot_be_null(self):
        unit = Unit(code="CITS0000", level=1)
        db.session.add(unit)
        with self.assertRaises(Exception):  # IntegrityError from nullable=False
            db.session.commit()

    # ----++++ Check that review_count returns the correct number of reviews ++++----
    def test_unit_review_count_is_correct(self):
        unit = Unit.query.get("CITS1401")
        self.assertEqual(unit.review_count, 1)


    # ===================== SECTION 3: Review model =====================

    # ----++++ Check that a review is persisted correctly after creation ++++----
    def test_review_exists_after_creation(self):
        review = Review.query.first()
        self.assertIsNotNone(review)

    # ----++++ Check that review content is unchanged after being written to the DB ++++----
    def test_review_content_is_unchanged_after_creation(self):
        review = Review.query.first()
        self.assertEqual(review.content, "Great intro unit, very beginner friendly.")

    # ----++++ Check that a review without a rating cannot be committed ++++----
    def test_review_rating_cannot_be_null(self):
        mambwe = User.query.filter_by(username="mambwe_test").first()
        review = Review(
            unit_code="CITS1401",
            author_id=mambwe.user_id,
            workload=4,
            content="No rating provided."
        )
        db.session.add(review)
        with self.assertRaises(Exception):  # IntegrityError from nullable=False
            db.session.commit()

    # ----++++ Check that get_ahead_tip is optional (nullable) ++++----
    def test_review_get_ahead_tip_is_optional(self):
        bronte = User.query.filter_by(username="bronte_test").first()
        review = Review(
            unit_code="CITS1401",
            author_id=bronte.user_id,
            rating=4,
            workload=5,
            content="Solid unit with great lab content and a reasonable workload."
        )
        db.session.add(review)
        db.session.commit()
        saved = Review.query.filter_by(author_id=bronte.user_id).first()
        self.assertIsNone(saved.get_ahead_tip)

    # ----++++ Check that review is linked to the correct unit and author ++++----
    def test_review_relationships_are_correct(self):
        review = Review.query.first()
        self.assertEqual(review.unit.code, "CITS1401")
        self.assertEqual(review.author.username, "mambwe_test")


    # ===================== SECTION 4: Discussion model =====================

    # ----++++ Check that a discussion is persisted correctly after creation ++++----
    def test_discussion_exists_after_creation(self):
        discussion = Discussion.query.first()
        self.assertIsNotNone(discussion)

    # ----++++ Check that discussion title is unchanged after creation ++++----
    def test_discussion_title_is_unchanged_after_creation(self):
        discussion = Discussion.query.first()
        self.assertEqual(discussion.title, "How hard is the group project?")

    # ----++++ Check that a discussion cannot be created without a title ++++----
    def test_discussion_title_cannot_be_null(self):
        mambwe = User.query.filter_by(username="mambwe_test").first()
        discussion = Discussion(
            unit_code="CITS1401",
            author_id=mambwe.user_id,
            body="Body without a title."
        )
        db.session.add(discussion)
        with self.assertRaises(Exception):  # IntegrityError from nullable=False
            db.session.commit()

    # ----++++ Check that reply_count reflects the number of comments correctly ++++----
    def test_discussion_reply_count_is_correct(self):
        discussion = Discussion.query.first()
        # setUp adds one comment to this discussion
        self.assertEqual(discussion.reply_count, 1)

    # ----++++ Check that discussion is linked to the correct unit ++++----
    def test_discussion_unit_relationship_is_correct(self):
        discussion = Discussion.query.first()
        self.assertEqual(discussion.unit.code, "CITS1401")


    # ===================== SECTION 5: Comment model =====================

    # ----++++ Check that a comment is persisted correctly after creation ++++----
    def test_comment_exists_after_creation(self):
        comment = Comment.query.first()
        self.assertIsNotNone(comment)

    # ----++++ Check that comment content is unchanged after creation ++++----
    def test_comment_content_is_unchanged_after_creation(self):
        comment = Comment.query.first()
        self.assertEqual(comment.content, "Don't worry, the groups are usually fine!")

    # ----++++ Check that a comment cannot be created without content ++++----
    def test_comment_content_cannot_be_null(self):
        bronte = User.query.filter_by(username="bronte_test").first()
        discussion = Discussion.query.first()
        comment = Comment(
            discussion_id=discussion.discussion_id,
            comment_author_id=bronte.user_id
            # content deliberately omitted
        )
        db.session.add(comment)
        with self.assertRaises(Exception):  # IntegrityError from nullable=False
            db.session.commit()

    # ----++++ Check that a reply is correctly linked to its parent comment ++++----
    def test_comment_reply_links_to_parent(self):
        mambwe = User.query.filter_by(username="mambwe_test").first()
        parent = Comment.query.first()
        reply = Comment(
            discussion_id=parent.discussion_id,
            comment_author_id=mambwe.user_id,
            content="Totally agree with this!",
            parent_comment_id=parent.comment_id
        )
        db.session.add(reply)
        db.session.commit()
        saved_reply = Comment.query.filter_by(content="Totally agree with this!").first()
        self.assertEqual(saved_reply.parent_comment_id, parent.comment_id)

    # ----++++ Check that a comment cannot be submitted without an author ++++----
    def test_comment_cannot_be_submitted_without_author(self):
        discussion = Discussion.query.first()
        comment = Comment(
            discussion_id=discussion.discussion_id,
            content="Anonymous comment attempt."
            # comment_author_id deliberately omitted
        )
        db.session.add(comment)
        with self.assertRaises(Exception):  # IntegrityError from nullable=False
            db.session.commit()


    # ===================== SECTION 6: Project model =====================

    # ----++++ Check that a project is persisted correctly after creation ++++----
    def test_project_exists_after_creation(self):
        project = Project.query.first()
        self.assertIsNotNone(project)

    # ----++++ Check that project title is unchanged after creation ++++----
    def test_project_title_is_unchanged_after_creation(self):
        project = Project.query.first()
        self.assertEqual(project.title, "Sorting Algorithm Visualiser")

    # ----++++ Check that a project cannot be created without a title ++++----
    def test_project_title_cannot_be_null(self):
        keithlin = User.query.filter_by(username="keithlin_test").first()
        project = Project(
            unit_code="CITS1401",
            author_id=keithlin.user_id,
            description="A project with no title."
            # title deliberately omitted
        )
        db.session.add(project)
        with self.assertRaises(Exception):  # IntegrityError from nullable=False
            db.session.commit()

    # ----++++ Check that external_link is optional (nullable) ++++----
    def test_project_external_link_is_optional(self):
        mambwe = User.query.filter_by(username="mambwe_test").first()
        project = Project(
            unit_code="CITS1401",
            author_id=mambwe.user_id,
            title="Private Project",
            description="No external link for this one."
            # external_link deliberately omitted
        )
        db.session.add(project)
        db.session.commit()
        saved = Project.query.filter_by(title="Private Project").first()
        self.assertIsNone(saved.external_link)

    # ----++++ Check that project is linked to the correct author and unit ++++----
    def test_project_relationships_are_correct(self):
        project = Project.query.first()
        self.assertEqual(project.author.username, "keithlin_test")
        self.assertEqual(project.unit.code, "CITS1401")