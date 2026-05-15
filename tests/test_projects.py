from app.models import Project
from tests.helpers import *

def test_submit_project(client, app):

    with app.app_context():

        user = create_test_user()
        unit = create_test_unit()

        login_user(client, user.user_id)

        response = client.post(
            "/CITS1401/create_project",
            data={
                "project_title": (
                    "This is a valid project title"
                ),
                "repo_link": (
                    "https://github.com/test/repo"
                ),
                "project_body": (
                    "This is a valid project description."
                )
            }
        )

        assert response.status_code == 302

        project = Project.query.first()

        assert project is not None