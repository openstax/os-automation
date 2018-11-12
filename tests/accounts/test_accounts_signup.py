"""Test the Accounts signup process."""

from pages.accounts.home import AccountsHome as Home
from pages.accounts.signup import Signup
from tests.markers import accounts, smoke_test, social, test_case
from utils.email import RestMail
from utils.utilities import Utility


@test_case('C195549')
@smoke_test
@accounts
def test_sign_up_as_a_student_user(accounts_base_url, selenium, student):
    """Test student user signup."""
    # GIVEN: a valid and accessible email address
    # AND: the Accounts Home page is loaded
    name = Utility.random_name()
    email = RestMail(
        '{first}.{last}.{tag}'
        .format(first=name[1], last=name[2], tag=Utility.random_hex(3))
        .lower()
    )
    email.empty()
    address = email.address
    password = student[1]
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
        email=address,
        password=password,
        _type='Student',
        provider='restmail',
        name=name,
        school='Automation',
        news=False)

    # THEN: the Account Profile page is loaded
    assert(page.current_url == accounts_base_url + '/profile'), \
        'Account profile not loaded'


@test_case('C205362')
@smoke_test
@accounts
def test_sign_up_as_an_instructor(accounts_base_url, selenium, teacher):
    """Test non-student user signup."""
    # GIVEN: a valid and accessible email address
    # AND: the Accounts Home page is loaded
    name = Utility.random_name()
    email = RestMail(
        '{first}.{last}.{tag}'
        .format(first=name[1], last=name[2], tag=Utility.random_hex(3))
        .lower()
    )
    email.empty()
    address = email.address
    password = teacher[1]
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
        email=address,
        password=password,
        _type='Instructor',
        provider='restmail',
        name=name,
        school='Automation',
        news=False,
        phone=Utility.random_phone(),
        webpage='https://openstax.org/',
        subjects=subject_list(2),
        students=10,
        use='Fully adopted and using it as the primary textbook')

    # THEN: the Account Profile page is loaded
    assert(page.current_url == accounts_base_url + '/profile'), \
        'Account profile not loaded'


@test_case('C195550')
@accounts
def test_sign_up_as_a_nonstudent_user(accounts_base_url, selenium, teacher):
    """Test non-student user signup."""
    # GIVEN: a valid and accessible email address
    # AND: the Accounts Home page is loaded
    name = Utility.random_name()
    email = RestMail(
        '{first}.{last}.{tag}'
        .format(first=name[1], last=name[2], tag=Utility.random_hex(3))
        .lower()
    )
    email.empty()
    address = email.address
    password = teacher[1]
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
        email=address,
        password=password,
        _type='Other',
        provider='restmail',
        name=name,
        school='Automation',
        news=False,
        phone=Utility.random_phone(),
        webpage='https://openstax.org/',
        subjects=subject_list(3))

    # THEN: the Account Profile page is loaded
    assert(page.current_url == accounts_base_url + '/profile'), \
        'Account profile not loaded'


@test_case('C200745')
@social
@accounts
def test_sign_up_as_a_facebook_user(
        accounts_base_url, selenium, facebook_signup, student):
    """Test signing up with a Facebook account."""
    # GIVEN: a valid Facebook that is not associated with a current account
    # AND: the Accounts Home page is loaded
    name = Utility.random_name()
    email = RestMail(
        '{first}.{last}.{tag}'
        .format(first=name[1], last=name[2], tag=Utility.random_hex(3))
        .lower()
    )
    email.empty()
    address = email.address
    password = student[1]
    page = Home(selenium, accounts_base_url).open()

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
    page = page.login.go_to_signup
    page = page.account_signup(
        email=address,
        password=password,
        _type='Student',
        provider='restmail',
        news=True,
        school='Automation',
        social='facebook',
        social_login=facebook_signup[0],
        social_password=facebook_signup[1]
    )

    # THEN: the account profile for the new student is displayed
    # AND: the name is the same as the Facebook user's name
    assert ('profile' in selenium.current_url)
    full_name = page.name.get_name_parts()
    for name in (full_name[1].lower().split() + full_name[2].lower().split()):
        assert(name in facebook_signup[0]), \
            '{missing} not in {signup}'.format(missing=name,
                                               signup=facebook_signup[0])

    # WHEN: the name field is changed
    # AND: a verified email is added to the profile
    # AND: the Profile page is reloaded
    # AND: a password log in option is added
    # AND: the email associated with the Facebook account is deleted
    # AND: the Facebook log in option is deleted
    name = Utility.random_name()
    page.name.open()
    page.name.first_name = name[1]
    page.name.last_name = name[2]
    page.name.confirm()
    username = name[1] + name[2] + str(Utility.random(100, 999))
    page.emails.add_email(username + '@restmail.net')
    password = student[1]
    page.login_method.add_password(password)
    page.login_method.get_active_options()[0].delete
    email = RestMail(username)
    email.get_mail()
    email.inbox[-1].confirm_email()
    page.reload()
    for email in page.emails.emails:
        if email.email_text == facebook_signup[0]:
            email.delete()
            break

    # THEN: the Facebook account is available for use


@test_case('C200746')
@social
@accounts
def test_sign_up_as_a_google_user(
        accounts_base_url, selenium, google_signup, student):
    """Test signing up with a Google account."""
    # GIVEN: a valid Google email that is not associated with a current account
    # AND: the Accounts Home page is loaded
    name = Utility.random_name()
    email = RestMail(
        '{first}.{last}.{tag}'
        .format(first=name[1], last=name[2], tag=Utility.random_hex(3))
        .lower()
    )
    email.empty()
    address = email.address
    password = student[1]
    page = Home(selenium, accounts_base_url).open()

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
    page = page.login.go_to_signup.account_signup(
        email=address,
        password=password,
        _type='Student',
        provider='restmail',
        news=True,
        school='Automation',
        social='google',
        social_login=google_signup[0],
        social_password=google_signup[1]
    )

    # THEN: the account profile for the new student is displayed
    # AND: the name is the same as the Google user's name
    assert ('profile' in selenium.current_url)
    full_name = page.name.get_name_parts()
    for name in (full_name[1].lower().split() + full_name[2].lower().split()):
        assert(name in google_signup[0]), \
            '{missing} not in {signup}'.format(missing=name,
                                               signup=google_signup[0])

    # WHEN: the name field is changed
    # AND: a verified email is added to the profile
    # AND: a password log in option is added
    # AND: the Google log in option is deleted
    # AND: the Profile page is reloaded
    # AND: the Gmail address is deleted
    name = Utility.random_name()
    page.name.open()
    page.name.first_name = name[1]
    page.name.last_name = name[2]
    page.name.confirm()
    username = name[1] + name[2] + str(Utility.random(100, 999))
    page.emails.add_email(username + '@restmail.net')
    password = student[1]
    page.login_method.add_password(password)
    page.login_method.get_active_options()[0].delete
    email = RestMail(username)
    email.get_mail()
    email.inbox[-1].confirm_email()
    page.reload()
    for email in page.emails.emails:
        if email.email_text == google_signup[0]:
            email.delete()
            break

    # THEN: the Google account is available for use


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
