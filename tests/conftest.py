import sys
sys.path.append('.')        ## googlekaap에 있는거 가져올때는 이코드를 넣어줘야 좋다.

from googlekaap.configs import TestingConfig
from googlekaap import create_app, db
import pytest
from googlekaap.models.user import User as UserModel



## dummy data 만들기
@pytest.fixture
def user_data():
    yield dict(
        user_id = 'tester',
        user_name = 'tester',
        password = 'tester'
    )

## 만든 dummy data를 sqlite에 넣어주자
@pytest.fixture
def app(user_data):
    app = create_app(TestingConfig())
    with app.app_context():
        db.drop_all()   ## db 초기화
        db.create_all() ## flask가 업데이트 된것처럼 db생성해준다.
        db.session.add(UserModel(**user_data))  ## model에 넣어준다.
        db.session.commit()
    yield app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client