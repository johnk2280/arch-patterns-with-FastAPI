from fastapi.testclient import TestClient

from demo.app import app

from tests.database import Session

client = TestClient(app)


def test_get_account():
    # arrange
    url = '/accounts/1'

    # act
    response = client.get(url)

    # assert
    assert response.status_code == 200
    assert response.json()['id'] == 1
