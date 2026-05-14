from tests.helpers import create_test_unit

def test_home_redirect(client):

    response = client.get("/")

    assert response.status_code == 302


def test_units_page_loads(client):

    response = client.get("/units")

    assert response.status_code == 200


def test_unit_page_exists(client, app):

    with app.app_context():

        create_test_unit()

        response = client.get("/unit/CITS1401")

        assert response.status_code == 200