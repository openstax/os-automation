"""Test the Accounts signup process."""

import os

from pages.accounts.signup import Signup
from pages.utils.email import GuerrillaMail
from pages.utils.utilities import Utility
from tests.markers import accounts, test_case


@test_case('C195549')
@accounts
def test_student_account_signup(accounts_base_url, selenium):
    """Test student user signup."""
    page = GuerrillaMail(selenium).open()
    email = page.header.email
    page = Signup(selenium, accounts_base_url).open()
    page.account_signup(
        email=email,
        password=os.getenv('STUDENT_PASSWORD'),
        _type=Signup.STUDENT,
        provider='guerrilla',
        kwargs={
            'name': Utility.random_name(),
            'school': 'OpenStax Automation',
            'news': False,
        }
    )
    assert('org/profile' in selenium.current_url), \
        'Not logged in as a new student'


@test_case('C205362')
@accounts
def test_instructor_account_signup(accounts_base_url, selenium, teacher):
    """Test non-student user signup."""
    page = GuerrillaMail(selenium).open()
    email = page.header.email
    page = Signup(selenium, accounts_base_url).open()
    subjects = subject_list(Utility.random(1, 5))
    page.account_signup(
        email=email,
        password=teacher[1],
        _type=Signup.INSTRUCTOR,
        provider='guerrilla',
        kwargs={
            'name': Utility.random_name(),
            'news': False,
            'phone': Utility.random_phone(),
            'school': 'OpenStax Automation',
            'students': 40,
            'subjects': subjects,
            'use': Signup.INTEREST,
            'webpage': 'http://openstax.org'
        }
    )
    assert('profile' in selenium.current_url), \
        'Not logged in as a new instructor'


@test_case('C195550')
@accounts
def test_non_student_account_signup(accounts_base_url, selenium, teacher):
    """Test non-student user signup."""
    page = GuerrillaMail(selenium).open()
    email = page.header.email
    page = Signup(selenium, accounts_base_url).open()
    # collect the options besides the initial value, student and teacher
    options = [
        ('administrator', Signup.ADMINISTRATOR),
        ('librarian', Signup.LIBRARIAN),
        ('designer', Signup.DESIGNER),
        ('other', Signup.OTHER),
    ]
    # select the type randomly to test each type over time
    choice = Utility.random(0, len(options) - 1)
    (account_type, account_title) = options[choice]
    subjects = subject_list(Utility.random(1, 5))
    page.account_signup(
        email=email,
        password=teacher[1],
        _type=account_title,
        provider='guerrilla',
        kwargs={
            'name': Utility.random_name(),
            'news': False,
            'phone': Utility.random_phone(),
            'school': 'OpenStax Automation',
            'students': 40,
            'subjects': subjects,
            'use': Signup.INTEREST,
            'webpage': 'http://openstax.org'
        }
    )
    assert('profile' in selenium.current_url), \
        'Not logged in as a new {0}'.format(account_type)


def subject_list(size=1):
    """Return a list of subjects for an elevated signup."""
    subjects = len(Signup.SUBJECTS)
    if size > subjects:
        size = subjects
    book = ''
    group = []
    while len(group) < size:
        book = (Signup.SUBJECTS[Utility.random(0, subjects - 1)])[1]
        if book not in group:
            group.append(book)
    return group
