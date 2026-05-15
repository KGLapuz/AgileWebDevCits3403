from app import db
from app.models import Review

from tests.helpers import *


def test_submit_review(client, app):

    with app.app_context():

        user = create_test_user()
        unit = create_test_unit()

        login_user(client, user.user_id)

        response = client.post(
            "/CITS1401/create_review",
            data={
                "rating": 5,
                "workload": 10,
                "content": (
                    "This is a valid review "
                    "that is definitely longer than "
                    "30 characters."
                ),
                "get_ahead_tip": "Start early bcs I got cooked"
            }
        )

        assert response.status_code == 302

        review = Review.query.first()

        assert review is not None