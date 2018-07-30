"""Test the Accounts signup process."""

from pages.accounts.home import AccountsHome as Home
from pages.utils.email import RestMail
from pages.accounts.signup import Signup
from pages.utils.utilities import Utility
from tests.markers import accounts, expected_failure, social, test_case


@test_case('C195549')
@accounts
def test_sign_up_as_a_student_user(accounts_base_url, selenium):
    """Test student user signup."""
    # GIVEN: a valid and accessible email address
    # AND: the Accounts Home page is loaded
    name = Utility.random_hex()
    email = RestMail(name)
    email.empty()
    address = name + '@restmail.net'
    password = 'staxly16'
    page = Home(selenium, accounts_base_url).open()

    # WHEN: the user clicks the "Sign up here." link
    # AND: selects "Student" from the drop down menu
    # AND: enters the email address
    # AND: clicks the "NEXT" button
    # AND: enters the supplied PIN
    # AND: clicks the "CONFIRM" button
    # AND: enters the password in both input boxes
    # AND: clicks "SUBMIT"
    # AND: enters data in the profile boxes
    # AND: clicks the checkbox next to "I agree to the Terms of Use and the
    #      Privacy Policy."
    # AND: clicks the "CREATE ACCOUNT" button

    page.login.go_to_signup.account_signup(
        address, password,
        _type='Student', 
        provider='restmail',
        name=['', name, name, ''],
        school='staxly',
        news=False)

    # THEN: the Account Profile page is loaded
    assert(page.current_url == accounts_base_url + '/profile'),\
        'Account profile not loaded'


@test_case('C205362')
@accounts
def test_sign_up_as_an_instructor(accounts_base_url, selenium, teacher):
    """Test non-student user signup."""
    # GIVEN: a valid and accessible email address
    # AND: the Accounts Home page is loaded
    name = Utility.random_hex()
    email = RestMail(name)
    email.empty()
    address = name + '@restmail.net'
    password = 'staxly16'
    page = Home(selenium, accounts_base_url).open()

    # WHEN: the user clicks the "Sign up here." link
    # AND: selects "Instructor" from the drop down menu
    # AND: enters the email address
    # AND: clicks the "NEXT" button (a second click may be required if the
    #      email does not end in ".edu")
    # AND: enters the supplied PIN
    # AND: clicks the "CONFIRM" button
    # AND: enters the password in both input boxes
    # AND: clicks "SUBMIT"
    # AND: enters data in the various user and course profile boxes
    # AND: clicks the checkbox next to "I agree to the Terms of Use and the
    #      Privacy Policy."
    # AND: clicks the "CREATE ACCOUNT" button
    # AND: clicks the "OK" button

    page.login.go_to_signup.account_signup(
        address, password,
        _type='Instructor', 
        provider='restmail',
        name=['', name, name, ''],
        school='staxly',
        news=False,
        phone=Utility.random_phone(),
        webpage='https://openstax.org/',
        subjects=['accounting', 'astronomy'],
        students=10,
        use='Fully adopted and using it as the primary textbook')

    # THEN: the Account Profile page is loaded
    assert(page.current_url == accounts_base_url + '/profile'),\
        'Account profile not loaded'


@test_case('C195550')
@social
@accounts
def test_sign_up_as_a_nonstudent_user(accounts_base_url, selenium, teacher):
    """Test non-student user signup."""
    # GIVEN: a valid and accessible email address
    # AND: the Accounts Home page is loaded
    name = Utility.random_hex()
    email = RestMail(name)
    email.empty()
    address = name + '@restmail.net'
    password = 'staxly16'
    page = Home(selenium, accounts_base_url).open()

    # WHEN: the user clicks the "Sign up here." link
    # AND: selects an option other than "Student" or "Instructor" from the drop
    #      down menu
    # AND: enters the email address
    # AND: clicks the "NEXT" button (a second click may be required if the
    #      email does not end in ".edu")
    # AND: enters the supplied PIN
    # AND: clicks the "CONFIRM" button
    # AND: enters the password in both input boxes
    # AND: clicks "SUBMIT"
    # AND: enters data in the various user profile boxes
    # AND: clicks the checkbox next to "I agree to the Terms of Use and the
    #      Privacy Policy."
    # AND: clicks the "CREATE ACCOUNT" button
    # AND: clicks the "OK" button

    page.login.go_to_signup.account_signup(
        address, password,
        _type='Other', 
        provider='restmail',
        name=['', name, name, ''],
        school='staxly',
        news=False,
        phone=Utility.random_phone(),
        webpage='https://openstax.org/',
        subjects=['accounting', 'astronomy'],)

    # THEN: the Account Profile page is loaded
    assert(page.current_url == accounts_base_url + '/profile'),\
        'Account profile not loaded'


@test_case('C200745')
@expected_failure
@social
@accounts
def test_sign_up_as_a_facebook_user(accounts_base_url, selenium, facebook):
    """Test signing up with a Facebook account."""
    # GIVEN: a valid Facebook that is not associated with a current account
    # AND: the Accounts Home page is loaded

    # WHEN: the user clicks the "Sign up here." link
    # AND: selects "Student" from the drop down menu
    # AND: enters the email address associated with the Facebook account
    # AND: enters the PIN code from the Accounts verification email
    # AND: clicks the "CONFIRM" button
    # AND: clicks the "Sign up with Google or Facebook instead." link
    # AND: clicks the "Facebook" button
    # AND: logs into Facebook
    # AND: enters a school name in the School input box
    # AND: clicks the checkbox next to "I agree to the Terms of Use and the
    #      Privacy Policy."
    # AND: clicks the "CREATE ACCOUNT" button

    # THEN: the account profile for the new student is displayed
    # AND: the name is the same as the Facebook user's name

    # WHEN: the name field is changed
    # AND: a verified email is added to the profile
    # AND: the Profile page is reloaded
    # AND: a password log in option is added
    # AND: the email associated with the Facebook account is deleted
    # AND: the Facebook log in option is deleted

    # THEN: the Facebook account is available for use
    assert(False), 'Test script missing'


@test_case('C200746')
@expected_failure
@accounts
def test_sign_up_as_a_google_user(accounts_base_url, selenium, google):
    """Test signing up with a Google account."""
    # GIVEN: a valid Google email that is not associated with a current account
    # AND: the Accounts Home page is loaded

    # WHEN: the user clicks the "Sign up here." link
    # AND: selects "Student" from the drop down menu
    # AND: enters the Gmail address
    # AND: enters the PIN code from the Accounts verification email
    # AND: clicks the "CONFIRM" button
    # AND: clicks the "Sign up with Google or Facebook instead." link
    # AND: clicks the "Google" button
    # AND: logs into Google
    # AND: enters a school name in the School input box
    # AND: clicks the checkbox next to "I agree to the Terms of Use and the
    #      Privacy Policy."
    # AND: clicks the "CREATE ACCOUNT" button

    # THEN: the account profile for the new student is displayed
    # AND: the name is the same as the Facebook user's name

    # WHEN: the name field is changed
    # AND: a verified email is added to the profile
    # AND: the Profile page is reloaded
    # AND: a password log in option is added
    # AND: the Gmail address is deleted
    # AND: the Google log in option is deleted

    # THEN: the Google account is available for use
    assert(False), 'Test script missing'


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
