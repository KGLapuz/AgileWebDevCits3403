from app.models import User, Unit, Discussion
from app import db
from tests.helpers import *

def test_create_discussion(client, app):

    with app.app_context():

        user = User(
            username="testuser",
            email="test@test.com",
            password_hash="hashed"
        )

        unit = create_test_unit()

        db.session.add(user)
        db.session.add(unit)
        db.session.commit()

        login_user(client, user.user_id)

        response = client.post(
            "/CITS1401/create_discussion",
            data={
                "title": "This is a valid discussion title",
                "body": "This is a valid discussion body content"
            },
            follow_redirects=True
        )

        assert response.status_code == 200

        discussion = Discussion.query.first()

        assert discussion is not None