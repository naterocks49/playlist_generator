import pytest
from app import app

@pytest.fixture
def app():
    app = app()
    return app

'''def test_index_authenticated():
    client = app.test_client()
    with client.session_transaction() as session:
        session['token_info'] = {'user_id': 123}
    response = client.get('/')
    assert response.status_code == 200
    assert b"Mac miller" in response.data
    assert b"J Cole" in response.data
    assert b"Kanye West" in response.data

def test_index_unauthenticated():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 302
    assert response.location.endswith('/login')'''