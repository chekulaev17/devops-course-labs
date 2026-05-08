import json
import pytest
from testlib.inputs import User

def _build_user(inputs, index):
    assert 'users' in inputs
    users = inputs['users']
    assert len(users) > index
    assert 'username' in users[index]
    assert 'password' in users[index]
    return User(users[index]['username'], users[index]['password'])

@pytest.fixture(scope='session')
def test_inputs():
    with open('inputs.json') as f:
        return json.load(f)

@pytest.fixture(scope='session')
def base_url(test_inputs):
    return test_inputs['base_url']

@pytest.fixture(scope='session')
def user(test_inputs):
    return _build_user(test_inputs, 0)

@pytest.fixture(scope='session')
def alt_user(test_inputs):
    return _build_user(test_inputs, 1)

@pytest.fixture
def catty_api():
    pytest.skip("playwright not available")
