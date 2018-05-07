"""Test the Accounts signup process."""
import pytest
from pytest_testrail.plugin import testrail

from pages.accounts.signup import Signup


@testrail('')
@pytest.mark.destructive
def test_student_signup(base_url, selenium):
    """Sign up as a student."""
    page = Signup(selenium, base_url).open()
    assert(page)


@testrail('')
@pytest.mark.destructive
def test_nonstudent_signup(base_url, selenium):
    """Sign up as a non-student."""
    page = Signup(selenium, base_url).open()
    assert(page)
