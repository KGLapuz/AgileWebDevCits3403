from tests.helpers import logout_user, create_test_unit

def test_login_page_loads(client):

    response = client.get("/login")

    assert response.status_code == 200
    
def test_logout_redirects(client):

    response = client.get("/logout")

    assert response.status_code == 302
    
def test_create_review_requires_login(client):
    
    create_test_unit()
        
    logout_user(client)
    
    response = client.get(
        "/CITS1401/create_review",
        follow_redirects=False
    )

    assert response.status_code == 302