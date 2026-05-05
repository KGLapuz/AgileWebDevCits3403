from models import Unit, Discussion, Project, User
from datetime import datetime
from fake_db import *
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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
    unit = get_unit(discussion.unit_code)

    # fake logged-in user for now
    current_user = get_user(1)

    return render_template(
        "discussion_thread.html",
        discussion=discussion,
        unit=unit,
        get_user=get_user,   # pass function into Jinja
        current_user=current_user
    )

@app.route("/create_review/<unit_code>", methods=["POST"])
def create_review(unit_code):
    # This is just a placeholder to show how we might handle form submissions
    # In a real app, you'd get these from request.form and validate them
    author_id = 1  # fake logged-in user
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
    parent_id = data.get("parent_id")  # None for top-level

    # ⚠️ TEMP: hardcode logged-in user
    current_user_id = 8 # Mambwe is currently logged in as user_id=8, but you can change this to test with other users

    # find discussion
    discussion = next((d for d in discussions if d.discussion_id == discussion_id), None)

    if not discussion or not content:
        return jsonify({"error": "Invalid data"}), 400

    new_comment = add_comment(
        discussion,
        comment_author_id=current_user_id,
        content=content,
        parent_id=parent_id
    )

    return jsonify({
        "success": True,
        "comment_id": new_comment.comment_id,
        "author": get_user(current_user_id).username,
        "content": new_comment.content,
        "created_at": new_comment.created_at.isoformat(),
        "parent_id": new_comment.parent_comment_id
    })

# route to specific static files (e.g. JS, CSS)
@app.route("/static/<path:filename>")
def serve_static(filename):
    return app.send_static_file(filename)
# -----------------------------------------------------------------------------------------------------