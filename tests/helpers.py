from app import db
from app.models import User, Unit

def create_test_user():

    user = User(
        username="testuser",
        email="test@test.com",
        password_hash="hashedpassword"
    )

    db.session.add(user)
    db.session.commit()

    return user

def create_test_unit():

    unit = Unit(
        code="CITS1401",
        name="Computational Thinking with Python",
        level="1",
        handbook_link="https://www.handbooks.uwa.edu.au/unitdetails?code=CITS1401",
        tags=["python"],
        tips='test tips'
    )

    db.session.add(unit)
    db.session.commit()

    return unit

def login_user(client, user_id=1):

    with client.session_transaction() as sess:
        sess["user_id"] = user_id


def logout_user(client):

    with client.session_transaction() as sess:
        sess.pop("user_id", None)
        