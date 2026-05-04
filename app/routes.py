from models import Unit, Discussion, Project, User
from datetime import datetime
from fake_db import *
from flask import Flask, render_template


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
# -----------------------------------------------------------------------------------------------------