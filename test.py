from app import app

def test_one():
	response = app.test_client().get('/')
	assert response.status_code == 200