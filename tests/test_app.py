import app

def test_home_page():
    tester = app.app.test_client()
    response = tester.get('/')
    assert response.status_code == 200
    assert b'Inventory' in response.data

