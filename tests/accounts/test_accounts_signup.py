"""Test the Accounts signup process."""
import os

import pytest
from pytest_testrail.plugin import pytestrail

from pages.accounts.signup import Signup
from pages.utils.utilities import Utility


@pytestrail.case('C195549')
@pytest.mark.xfail
def test_student_account_signup(base_url, selenium):
    """Test student user signup."""
    page = Signup(selenium, base_url).open()

    page.account_signup(
        os.getenv('EMAIL_BASE').format(Utility.random_hex(5)),
        os.getenv('STUDENT_PASSWORD'),
        'student'
    )
    assert('profile' in selenium.current_url), \
        'Not logged in as a new student'


@pytestrail.case('C195550')
@pytest.mark.xfail
def test_non_student_account_signup(base_url, selenium):
    """Test non-student user signup."""
    page = Signup(selenium, base_url).open()
    # collect the account options besides the initial value and student
    options = [
        ('instructor', 'Instructor'),
        ('administrator', 'Administrator'),
        ('librarian', 'Librarian'),
        ('designer', 'Instructional Designer'),
        ('other', 'Other'),
    ]
    # select the type randomly to test each type over time
    choice = Utility.random(0, 5)
    (account_type, account_title) = options[choice]

    page.account_signup(
        os.getenv('EMAIL_BASE').format(Utility.random_hex(5)),
        os.getenv('TEACHER_PASSWORD'),
        account_type
    )
    assert('profile' in selenium.current_url), \
        'Not logged in as a new {0}'.format(account_type)
