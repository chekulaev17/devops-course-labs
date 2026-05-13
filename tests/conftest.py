"""
This module provides fixtures for testing.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import json
import pytest

from playwright.sync_api import Playwright
from testlib.inputs import User


# --------------------------------------------------------------------------------
# Private Functions
# --------------------------------------------------------------------------------

def _build_user(inputs, index):
    assert 'users' in inputs
    users = inputs['users']

    assert len(users) > index

    assert 'username' in users[index]
    assert 'password' in users[index]

    return User(
        users[index]['username'],
        users[index]['password']
    )


# --------------------------------------------------------------------------------
# Input Fixtures
# --------------------------------------------------------------------------------

@pytest.fixture(scope='session')
def test_inputs():
    with open('inputs.json') as inputs_json:
        return json.load(inputs_json)


@pytest.fixture(scope='session')
def base_url(test_inputs):
    return test_inputs['base_url']


@pytest.fixture(scope='session')
def user(test_inputs):
    return _build_user(test_inputs, 0)


@pytest.fixture(scope='session')
def alt_user(test_inputs):
    return _build_user(test_inputs, 1)


# --------------------------------------------------------------------------------
# Playwright Fixtures
# --------------------------------------------------------------------------------

@pytest.fixture
def catty_api(playwright: Playwright, base_url: str):
    return playwright.request.new_context(base_url=base_url)
