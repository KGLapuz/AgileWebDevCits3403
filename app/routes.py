from models import Unit, Discussion, Project, User
from datetime import datetime
from fake_db import get_unit, discussions, get_user
from flask import render_template

# -----------------------------------------------------------------------------------------------------
# MAMBWE trying out some functions in flask. DO NOT DELETE
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
    
# -----------------------------------------------------------------------------------------------------