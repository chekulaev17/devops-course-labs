"""
This module contains Web UI tests for the Catty app.
"""

import re

from playwright.sync_api import Page, expect
from testlib.inputs import User


def test_successful_login(page: Page, user: User):

    # Given
    page.goto('/login')
    page.wait_for_load_state('networkidle')

    # When
    page.locator('[name="username"]').fill(user.username)
    page.locator('[name="password"]').fill(user.password)

    with page.expect_navigation():
        page.get_by_text('Login').click()

    # Then
    expect(page).to_have_title('Reminders | Catty reminders app')

    expect(page).to_have_url(
        re.compile(re.escape('/') + 'reminders')
    )

    expect(page.locator('id=catty-logo')).to_be_visible()

    expect(page.locator('id=catty-title')).to_have_text('Catty')

    expect(
        page.get_by_role('button', name='Logout')
    ).to_be_visible()

    expect(
        page.locator('id=reminders-message')
    ).to_have_text(
        f'Reminders for {user.username}'
    )
