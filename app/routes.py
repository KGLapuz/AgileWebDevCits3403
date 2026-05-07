from models import Unit, Discussion, Project, User
from datetime import datetime
from fake_db import *
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = "dev"

@app.context_processor
def inject_globals():
    return dict(get_user=get_user)

# -------------------------
# setting logged-in user for testing purposes
# -------------------------
@app.route("/set_user", methods=["POST"])
def set_user():
    user_id = int(request.json.get("user_id"))
    session["user_id"] = user_id
    return jsonify({"success": True})

def get_current_user():
    return session.get("user_id", 1)  # default = 1

def get_current_user_obj():
    return get_user(get_current_user())

# -----------------------------------------------------------------------------------------------------
# MAMBWE trying out some functions in flask. DO NOT DELETE
@app.route("/")
def home():
    return render_template("home.html", units=units)  # pass units list to template

@app.route("/unit/<code>")
def unit_page(code):
    unit = get_unit(code)
    reviews = get_reviews_for_unit(code)
    discussions = get_discussions_for_unit(code)
    projects = get_projects_for_unit(code)

    return render_template(
        "unit_page.html",
        unit=unit,
        reviews=reviews,
        discussions=discussions,
        projects=projects
    )
    
@app.route("/discussion/<int:discussion_id>")
def discussion_thread(discussion_id):

    discussion = next(d for d in discussions if d.discussion_id == discussion_id)
    
    comments_tree = build_comment_tree(discussion.comments)
    
    unit = get_unit(discussion.unit_code)

    return render_template(
        "discussion_thread.html",
        discussion=discussion,
        unit=unit,
        comments=comments_tree,
        current_user_id=get_current_user()
    )
    
def build_comment_tree(comments):

    comment_map = {}

    # create lookup + clear replies
    for c in comments:
        c.replies = []
        comment_map[c.comment_id] = c

    root_comments = []

    for c in comments:

        # top-level comment
        if c.parent_comment_id is None:
            root_comments.append(c)

        else:
            parent = comment_map.get(c.parent_comment_id)

            # IMPORTANT: prevent self-reference
            if parent and parent.comment_id != c.comment_id:
                parent.replies.append(c)

    return root_comments

@app.route("/create_review/<unit_code>", methods=["POST"])
def create_review(unit_code):
    # This is just a placeholder to show how we might handle form submissions
    # In a real app, you'd get these from request.form and validate them
    author_id = get_current_user()
    rating = 5
    workload = 3
    content = "This is a great unit!"

    add_review(unit_code, author_id, rating, workload, content)

    return "Review added!"  # In reality, you'd redirect back to the unit page

# routing for comments and replies to comments
@app.route("/add_comment", methods=["POST"])
def add_comment_route():
    data = request.get_json()

    discussion_id = int(data.get("discussion_id"))
    content = data.get("content")
    parent_id = data.get("parent_id")
    
    # parent_id will be None for top-level comments, but if it's provided, we should convert it to int
    if parent_id is not None:
        parent_id = int(parent_id)

    discussion = next((d for d in discussions if d.discussion_id == discussion_id), None)

    if not discussion or not content:
        return jsonify({"error": "Invalid"}), 400

    new_comment = add_comment(discussion, get_current_user(), content, parent_id)

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

# route to specific static files (e.g. JS, CSS)
@app.route("/static/<path:filename>")
def serve_static(filename):
    return app.send_static_file(filename)
# -----------------------------------------------------------------------------------------------------