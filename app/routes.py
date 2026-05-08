from app import app, db
from app.models import *

from flask import (
    render_template,
    request,
    jsonify,
    session
)


# -------------------------------------------------
# GLOBAL TEMPLATE FUNCTIONS
# -------------------------------------------------

@app.context_processor
def inject_globals():

    return dict(
        current_user_id=get_current_user(),
        current_user=get_current_user_obj()
    )


# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------

def get_user(user_id):
    return User.query.get(user_id)


def get_current_user():
    return session.get("user_id", 1)


def get_current_user_obj():
    return User.query.get(get_current_user())


# -------------------------------------------------
# TEST LOGIN ROUTE
# -------------------------------------------------

@app.route("/set_user", methods=["POST"])
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
# HOME PAGE
# -------------------------------------------------

@app.route("/")
def home():

    units = Unit.query.order_by(Unit.code).all()

    return render_template(
        "home.html",
        units=units
    )


# -------------------------------------------------
# UNIT PAGE
# -------------------------------------------------

@app.route("/unit/<code>")
def unit_page(code):

    unit = Unit.query.get_or_404(code)

    return render_template(
        "unit_page.html",
        unit=unit,

        # Sort reviews, discussions, and projects by creation date (newest first)
        reviews = sorted(
            unit.reviews,
            key=lambda r: r.created_at,
            reverse=True
        ),

        discussions = sorted(
            unit.discussions,
            key=lambda d: d.created_at,
            reverse=True
        ),

        projects = sorted(
            unit.projects,
            key=lambda p: p.created_at,
            reverse=True
        )
    )


# -------------------------------------------------
# DISCUSSION THREAD
# -------------------------------------------------

@app.route("/discussion/<int:discussion_id>")
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


# -------------------------------------------------
# BUILD NESTED COMMENT TREE
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
# CREATE REVIEW
# -------------------------------------------------

@app.route("/create_review/<unit_code>", methods=["POST"])
def create_review(unit_code):

    unit = Unit.query.get_or_404(unit_code)

    author_id = get_current_user()

    # placeholder values
    rating = 5
    workload = 3
    content = "This is a great unit!"

    review = Review(
        unit_code=unit.code,
        author_id=author_id,
        rating=rating,
        workload=workload,
        content=content
    )

    db.session.add(review)

    db.session.commit()

    return jsonify({
        "success": True
    })


# -------------------------------------------------
# ADD COMMENT / REPLY
# -------------------------------------------------

@app.route("/add_comment", methods=["POST"])
def add_comment_route():

    data = request.get_json()

    discussion_id = int(
        data.get("discussion_id")
    )

    content = data.get("content")

    parent_id = data.get("parent_id")

    if parent_id is not None:
        parent_id = int(parent_id)

    discussion = Discussion.query.get(
        discussion_id
    )

    if not discussion or not content:

        return jsonify({
            "error": "Invalid"
        }), 400

    new_comment = Comment(
        discussion_id=discussion_id,
        comment_author_id=get_current_user(),
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
