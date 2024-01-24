from fastapi.testclient import TestClient

from demo.app import app
from demo.database import Account
from demo.database import Base
from demo.database import get_session
from tests.database import engine
from tests.database import get_session as get_test_session
from tests.database import Session

client = TestClient(app)


def test_get_account():
    # arrange
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_session] = get_test_session

    url = '/accounts/1'
    # with Session() as session:
    #     session.add(
    #         Account(
    #             email='tes@email.com',
    #             password='qwerty',
    #             username='test_user',
    #         )
    #     )
    #     session.commit()

    # act
    response = client.get(url)

    # assert
    assert response.status_code == 200
    assert response.json()['id'] == 1
