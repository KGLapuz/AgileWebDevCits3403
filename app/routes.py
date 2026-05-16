from . import db
from .models import *
from .controllers import user_registration, verify_login

from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from .log_in_page import (
    RegistrationForm,
    LoginForm,
    User
)

from datetime import datetime

# import os


main = Blueprint('main', __name__)


# -------------------------------------------------
# GLOBAL TEMPLATE FUNCTIONS
# -------------------------------------------------

@main.context_processor
def inject_globals():

    return dict(
        current_user_id=get_current_user(),
        current_user=get_current_user_obj(),
        greeting=get_greeting()
    )


# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------

def get_user(user_id):
    return User.query.get(user_id)


def get_current_user():
    return session.get("user_id")


def get_current_user_obj():
    user_id = get_current_user()

    if not user_id:
        return None

    return User.query.get(get_current_user())


# -------------------------------------------------
# GREETING HELPER FUNCTION
# -------------------------------------------------

def get_greeting():
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        return "Good Morning"

    elif 12 <= current_hour < 17:
        return "Good Afternoon"

    elif 17 <= current_hour < 21:
        return "Good Evening"

    else:
        return "Good Night"


# -------------------------------------------------
# COMMENT TREE HELPER FUNCTIONS
# -------------------------------------------------

def build_comment_tree(comments):

    comment_map = {}

    # Clear temporary replies lists
    for comment in comments:

        comment.replies_cache = []

        comment_map[comment.comment_id] = comment

    root_comments = []

    for comment in comments:

        if comment.parent_comment_id is None:

            root_comments.append(comment)

        else:

            parent = comment_map.get(
                comment.parent_comment_id
            )

            # Prevent self-reference
            if (
                parent and
                parent.comment_id != comment.comment_id
            ):
                parent.replies_cache.append(comment)

    return root_comments


# -------------------------------------------------
# TEST / DEVELOPMENT ROUTES
# -------------------------------------------------

@main.route("/set_user", methods=["POST"])
def set_user():

    user_id = int(request.json.get("user_id"))

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    session["user_id"] = user_id

    return jsonify({
        "success": True
    })


# -------------------------------------------------
# HOME ROUTES
# -------------------------------------------------

@main.route('/')
def index():
    return render_template('home_page.html')
# -------------------------------------------------
# AUTHENTICATION ROUTES
# -------------------------------------------------

@main.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm()
    signup_form = RegistrationForm()

    # This handles the signup post
    if signup_form.submit_signup.data and signup_form.validate_on_submit():

        user_registration(signup_form)

        return redirect(url_for('main.login'))
    
    if signup_form.errors:
        flash(
            'Please correct the errors in the sign up form',
            'error'
        )

    # This handles the login post
    if login_form.submit_login.data and login_form.validate_on_submit():

        user = verify_login(
            login_form.email.data,
            login_form.password.data
        )

        if user:
            session['user_id'] = user.user_id
            return redirect(url_for('main.index'))

        flash(
            'Login Unsuccessful. Please Check email and password',
            'error'
        )

    return render_template(
        'log_in_page.html',
        login_form=login_form,
        signup_form=signup_form
    )


@main.route('/logout')
def logout():

    session.pop('user_id', None)

    return redirect(url_for('main.login'))


# -------------------------------------------------
# UNIT ROUTES
# -------------------------------------------------

@main.route("/units")
def units():

    search = request.args.get("search", "").strip()

    query = Unit.query

    if search:
        query = query.filter(
            db.or_(
                Unit.code.ilike(f"%{search}%"),
                Unit.name.ilike(f"%{search}%")
            )
        )

    units = query.order_by(
        Unit.code.asc()
    ).all()

    return render_template(
        "unit_list.html",
        units=units
    )


@main.route("/unit/<code>")
def unit_page(code):

    unit = Unit.query.get_or_404(code)

    return render_template(
        "unit_page.html",
        unit=unit,

        # Sort reviews, discussions, and projects by creation date (newest first)
        reviews=sorted(
            unit.reviews,
            key=lambda r: r.created_at,
            reverse=True
        ),

        discussions=sorted(
            unit.discussions,
            key=lambda d: d.created_at,
            reverse=True
        ),

        projects=sorted(
            unit.projects,
            key=lambda p: p.created_at,
            reverse=True
        )
    )


# -------------------------------------------------
# DISCUSSION ROUTES
# -------------------------------------------------

@main.route("/discussion/<int:discussion_id>")
def discussion_thread(discussion_id):

    discussion = Discussion.query.get_or_404(
        discussion_id
    )

    comments_tree = build_comment_tree(
        discussion.comments
    )

    return render_template(
        "discussion_thread.html",
        discussion=discussion,
        unit=discussion.unit,
        comments=comments_tree,
        current_user_id=get_current_user()
    )


@main.route("/<unit_code>/discussions")
def unit_discussions(unit_code):

    unit = Unit.query.get_or_404(unit_code)

    search = request.args.get("search", "")

    query = Discussion.query.filter_by(
        unit_code=unit_code
    )

    if search:
        query = query.filter(
            db.or_(
                Discussion.title.ilike(f"%{search}%"),
                Discussion.body.ilike(f"%{search}%")
            )
        )

    discussions = query.order_by(
        Discussion.created_at.desc()
    ).all()

    return render_template(
        "content_list.html",
        unit=unit,
        items=discussions,
        content_type="discussions",
        page_title=f"{unit.code} Discussions"
    )


# -------------------------------------------------
# CREATE DISCUSSION ROUTES
# -------------------------------------------------

@main.route("/<unit_code>/create_discussion", methods=["GET"])
def create_discussion_page(unit_code):
    """Render the create-discussion form."""

    unit = Unit.query.get_or_404(unit_code)

    # Only logged-in users should reach this page
    if not get_current_user():

        flash(
            "You must be logged in to start a discussion.",
            "error"
        )

        return redirect(url_for("main.login"))

    return render_template(
        "create_discussion.html",
        unit=unit
    )


@main.route("/<unit_code>/create_discussion", methods=["POST"])
def create_discussion(unit_code):
    """Handle discussion form submission, save to DB, redirect to discussion list."""

    unit = Unit.query.get_or_404(unit_code)

    author_id = get_current_user()

    if not author_id:

        flash(
            "You must be logged in to start a discussion.",
            "error"
        )

        return redirect(url_for("main.login"))

    title = request.form.get("title", "").strip()
    body = request.form.get("body", "").strip()

    # Basic server-side validation
    if not title or len(title) < 10:

        flash(
            "Title must be at least 10 characters.",
            "error"
        )

        return render_template(
            "create_discussion.html",
            unit=unit
        )

    if not body or len(body) < 15:

        flash(
            "Description must be at least 15 characters.",
            "error"
        )

        return render_template(
            "create_discussion.html",
            unit=unit
        )

    discussion = Discussion(
        unit_code=unit.code,
        author_id=author_id,
        title=title,
        body=body,
    )

    db.session.add(discussion)
    db.session.commit()

    flash(
        "Discussion posted successfully!",
        "success"
    )

    return redirect(
        url_for(
            "main.unit_discussions",
            unit_code=unit.code
        )
    )


# -------------------------------------------------
# COMMENT / REPLY ROUTES
# -------------------------------------------------

@main.route("/add_comment", methods=["POST"])
def add_comment_route():
    comment_author=get_current_user()
     
    data = request.get_json()

    discussion_id = int(data.get("discussion_id"))
    
    if not comment_author:
        return jsonify({
            "error": "unauthenticated"
        }), 401
       
    content = data.get("content")
    parent_id = data.get("parent_id")

    if parent_id is not None:
        parent_id = int(parent_id)

    discussion = Discussion.query.get(discussion_id)

    if not discussion or not content:

        return jsonify({
            "error": "Invalid"
        }), 400

    new_comment = Comment(
        discussion_id=discussion_id,
        comment_author_id=comment_author,
        content=content,
        parent_comment_id=parent_id
    )

    db.session.add(new_comment)
    db.session.commit()

    # Set up an empty replies cache for the new comment so jinja renders correctly
    new_comment.replies_cache = []

    html = render_template(
        "partials/comment.html",
        comment=new_comment,
        current_user_id=get_current_user()
    )

    return jsonify({
        "success": True,
        "html": html,
        "parent_id": parent_id
    })


# -------------------------------------------------
# REVIEW ROUTES
# -------------------------------------------------

@main.route("/<unit_code>/reviews")
def unit_reviews(unit_code):

    unit = Unit.query.get_or_404(unit_code)

    search = request.args.get("search", "")

    query = Review.query.filter_by(
        unit_code=unit_code
    )

    if search:
        query = query.filter(
            Review.content.ilike(f"%{search}%")
        )

    reviews = query.order_by(
        Review.created_at.desc()
    ).all()

    return render_template(
        "content_list.html",
        unit=unit,
        items=reviews,
        content_type="reviews",
        page_title=f"{unit.code} Reviews"
    )


# -------------------------------------------------
# CREATE REVIEW ROUTES
# -------------------------------------------------

@main.route("/<unit_code>/create_review", methods=["GET"])
def create_review_page(unit_code):
    """Render the write-a-review form."""

    unit = Unit.query.get_or_404(unit_code)

    if not get_current_user():

        flash(
            "You must be logged in to write a review.",
            "error"
        )

        return redirect(url_for("main.login"))

    return render_template(
        "create_review.html",
        unit=unit
    )


@main.route("/<unit_code>/create_review", methods=["POST"])
def submit_review(unit_code):
    """Validate and save a new review, then redirect to the unit's review list."""

    unit = Unit.query.get_or_404(unit_code)

    author_id = get_current_user()

    if not author_id:

        flash(
            "You must be logged in to write a review.",
            "error"
        )

        return redirect(url_for("main.login"))

    # --- collect form values ---
    content = request.form.get(
        "content",
        ""
    ).strip()

    get_ahead = request.form.get(
        "get_ahead_tip",
        ""
    ).strip()

    try:

        rating = float(
            request.form.get("rating", 0)
        )

        workload = float(
            request.form.get("workload", 0)
        )

    except (TypeError, ValueError):

        flash(
            "Invalid rating or workload value.",
            "error"
        )

        return render_template(
            "create_review.html",
            unit=unit
        )

    # --- server-side validation ---
    if not (1 <= rating <= 5):

        flash(
            "Please select a star rating.",
            "error"
        )

        return render_template(
            "create_review.html",
            unit=unit
        )

    if not (1 <= workload <= 20):

        flash(
            "Workload must be between 1 and 20 hours.",
            "error"
        )

        return render_template(
            "create_review.html",
            unit=unit
        )

    if len(content) < 30:

        flash(
            "Review must be at least 30 characters.",
            "error"
        )

        return render_template(
            "create_review.html",
            unit=unit
        )

    if len(get_ahead) > 200:

        flash(
            "Get Ahead tip must be 200 characters or fewer.",
            "error"
        )

        return render_template(
            "create_review.html",
            unit=unit
        )

    review = Review(
        unit_code=unit.code,
        author_id=author_id,
        rating=rating,
        workload=workload,
        content=content,
        get_ahead_tip=get_ahead or None
    )

    db.session.add(review)
    db.session.commit()

    flash(
        "Review submitted - thanks for helping your fellow students!",
        "success"
    )

    return redirect(
        url_for(
            "main.unit_reviews",
            unit_code=unit.code
        )
    )


@main.route("/<unit_code>/get_ahead_tips")
def get_ahead_tips(unit_code):

    unit = Unit.query.get_or_404(unit_code)

    search = request.args.get("search", "")

    query = Review.query.filter(
        Review.unit_code == unit_code,
        Review.get_ahead_tip.is_not(None)
    )

    if search:
        query = query.filter(
            Review.content.ilike(f"%{search}%"),
            Review.get_ahead_tip.is_not(None)
        )

    tips = query.order_by(
        Review.created_at.desc()
    ).all()

    return render_template(
        "content_list.html",
        unit=unit,
        items=tips,
        content_type="tips",
        page_title=f"{unit.code} Get-Ahead tips"
    )


# -------------------------------------------------
# PROJECT ROUTES
# -------------------------------------------------

@main.route("/<unit_code>/projects")
def unit_project(unit_code):

    unit = Unit.query.get_or_404(unit_code)

    search = request.args.get("search", "")

    query = Project.query.filter_by(
        unit_code=unit_code
    )

    if search:
        query = query.filter(
            db.or_(
                Project.title.ilike(f"%{search}%"),
                Project.description.ilike(f"%{search}%")
            )
        )

    projects = query.order_by(
        Project.created_at.desc()
    ).all()

    return render_template(
        "content_list.html",
        unit=unit,
        items=projects,
        content_type="projects",
        page_title=f"{unit.code} Projects"
    )


@main.route("/projects/<int:project_id>")
def project_detail(project_id):

    project = Project.query.get_or_404(project_id)

    unit = project.unit

    return render_template(
        "project_detail.html",
        project=project,
        unit=unit
    )


# -------------------------------------------------
# CREATE PROJECT ROUTES
# -------------------------------------------------

@main.route("/<unit_code>/create_project", methods=["GET"])
def create_project(unit_code):
    """Render the create-project form."""

    unit = Unit.query.get_or_404(unit_code)

    # Only logged-in users should reach this page
    if not get_current_user():

        flash(
            "You must be logged in to submit project.",
            "error"
        )

        return redirect(url_for("main.login"))

    return render_template(
        "create_project.html",
        unit=unit
    )


@main.route("/<unit_code>/create_project", methods=["POST"])
def submit_project(unit_code):

    unit = Unit.query.get_or_404(unit_code)

    author_id = get_current_user()

    if not author_id:

        flash(
            "You must be logged in to submit a project.",
            "error"
        )

        return redirect(url_for("main.login"))

    title = request.form.get(
        "project_title",
        ""
    ).strip()

    repo_link = request.form.get(
        "repo_link",
        ""
    ).strip()

    project_body = request.form.get(
        "project_body",
        ""
    ).strip()

    if not title or len(title) < 10:

        flash(
            "Title must be at least 10 characters.",
            "error"
        )

        return render_template(
            "create_project.html",
            unit=unit
        )

    if not project_body or len(project_body) < 15:

        flash(
            "Description must be at least 15 characters.",
            "error"
        )

        return render_template(
            "create_project.html",
            unit=unit
        )

    project = Project(
        unit_code=unit.code,
        author_id=author_id,
        title=title,
        external_link=repo_link,
        description=project_body,
    )

    db.session.add(project)
    db.session.commit()

    flash(
        "Project posted successfully!",
        "success"
    )

    return redirect(
        url_for(
            "main.unit_project",
            unit_code=unit.code
        )
    )


# -------------------------------------------------
# UNIT SEARCH ROUTES
# -------------------------------------------------

@main.route("/units/search")
def search_units():

    search = request.args.get(
        "search",
        ""
    ).strip()

    query = Unit.query

    if search:
        query = query.filter(
            db.or_(
                Unit.code.ilike(f"%{search}%"),
                Unit.name.ilike(f"%{search}%")
            )
        )

    units = query.order_by(
        Unit.code.asc()
    ).all()

    return render_template(
        "partials/unit_search_results.html",
        units=units
    )


# -------------------------------------------------
# REVIEW SEARCH ROUTES
# -------------------------------------------------

@main.route("/<unit_code>/reviews/search")
def search_reviews(unit_code):

    unit = Unit.query.get_or_404(unit_code)

    search = request.args.get("search", "")

    query = Review.query.filter_by(
        unit_code=unit_code
    )

    if search:
        query = query.filter(
            Review.content.ilike(f"%{search}%")
        )

    reviews = query.order_by(
        Review.created_at.desc()
    ).all()

    return render_template(
        "partials/content_search_results.html",
        unit=unit,
        items=reviews,
        content_type="reviews"
    )


# -------------------------------------------------
# GET-AHEAD TIP SEARCH ROUTES
# -------------------------------------------------

@main.route("/<unit_code>/get_ahead_tips/search")
def search_get_ahead_tips(unit_code):

    unit = Unit.query.get_or_404(unit_code)

    search = request.args.get("search", "")

    query = Review.query.filter_by(
        unit_code=unit_code
    )

    if search:
        query = query.filter(
            Review.get_ahead_tip.ilike(f"%{search}%"),
            Review.get_ahead_tip.is_not(None)
        )

    tips = query.order_by(
        Review.created_at.desc()
    ).all()

    return render_template(
        "partials/content_search_results.html",
        unit=unit,
        items=tips,
        content_type="tips"
    )


# -------------------------------------------------
# PROJECT SEARCH ROUTES
# -------------------------------------------------

@main.route("/<unit_code>/projects/search")
def search_unit_projects(unit_code):

    unit = Unit.query.get_or_404(unit_code)

    search = request.args.get("search", "")

    query = Project.query.filter_by(
        unit_code=unit_code
    )

    if search:
        query = query.filter(
            db.or_(
                Project.title.ilike(f"%{search}%"),
                Project.description.ilike(f"%{search}%")
            )
        )

    projects = query.order_by(
        Project.created_at.desc()
    ).all()

    return render_template(
        "partials/content_search_results.html",
        unit=unit,
        items=projects,
        content_type="projects"
    )


# -------------------------------------------------
# DISCUSSION SEARCH ROUTES
# -------------------------------------------------

@main.route("/<unit_code>/discussions/search")
def search_unit_discussions(unit_code):

    unit = Unit.query.get_or_404(unit_code)

    search = request.args.get("search", "")

    query = Discussion.query.filter_by(
        unit_code=unit_code
    )

    if search:
        query = query.filter(
            db.or_(
                Discussion.title.ilike(f"%{search}%"),
                Discussion.body.ilike(f"%{search}%")
            )
        )

    discussions = query.order_by(
        Discussion.created_at.desc()
    ).all()

    return render_template(
        "partials/content_search_results.html",
        unit=unit,
        items=discussions,
        content_type="discussions"
    )


# -------------------------------------------------
# DUPLICATE PROJECT SEARCH ROUTE
# -------------------------------------------------

# @main.route("/<unit_code>/projects/search")
# def search_projects(unit_code):

#     unit = Unit.query.get_or_404(unit_code)

#     search = request.args.get("search", "")

#     query = Project.query.filter_by(
#         unit_code=unit_code
#     )

#     if search:
#         query = query.filter(
#             Project.title.ilike(f"%{search}%"),
#             Project.description.ilike(f"%{search}%")
#         )

#     projects = query.order_by(
#         Project.created_at.desc()
#     ).all()

#     return render_template(
#         "partials/content_search_results.html",
#         unit=unit,
#         items=projects,
#         content_type="projects"
#     )