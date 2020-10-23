"""Test the Accounts signup process."""

from random import sample

from pages.accounts.home import AccountsHome as Home
from tests.markers import accounts, skip_test, smoke_test, social, test_case
from utils.accounts import Accounts
from utils.email import RestMail
from utils.utilities import Utility
from utils.web import Web


@test_case('C195549')
@smoke_test
@accounts
def test_sign_up_as_a_student_user(accounts_base_url, selenium):
    """Test student user signup."""
    # SETUP:
    name = Utility.random_name()
    email = RestMail((f'{name[Accounts.FIRST]}.{name[Accounts.LAST]}.'
                      f'{Utility.random_hex(3)}').lower())
    email.empty()
    address = email.address
    password = Utility.random_hex(20)

    # GIVEN: a user with a valid email address viewing the home page
    home = Home(selenium, accounts_base_url).open()

    # WHEN: they click the "Sign up" tab
    # AND:  click the "Student" box
    # AND:  enter their first name, last name, email address and password,
    #       click the "I agree to the Terms of Use and Privacy Policy",
    #       checkbox, click the "Continue" button
    # AND:  enter the confirmation PIN number and click the "Confirm my
    #       account" button
    # AND:  click the "Finish" button
    sign_up = home.content.view_sign_up()

    student_sign_up = sign_up.content.sign_up_as_a_student().content

    student_sign_up.first_name = name[Accounts.FIRST]
    student_sign_up.last_name = name[Accounts.LAST]
    student_sign_up.email = address
    student_sign_up.password = password
    student_sign_up.i_agree()
    confirm_email = student_sign_up._continue().content

    pin = email.wait_for_mail()[-1].pin
    confirm_email.pin = pin
    complete_sign_up = confirm_email.confirm_my_account().content

    profile = complete_sign_up.finish()

    # THEN: their new account profile is displayed
    full_name = profile.content.name.full_name
    addresses = [entry.email for entry in profile.content.emails.emails]
    assert('profile' in profile.location), \
        'account profile not displayed'
    assert(name[Accounts.FIRST] in full_name), \
        'first name does not match sign up'
    assert(name[Accounts.LAST] in full_name), \
        'last name does not match sign up'
    assert(address in addresses), \
        'sign up email not found'


@test_case('C205362')
@smoke_test
@accounts
def test_sign_up_as_an_instructor(accounts_base_url, selenium):
    """Test non-student user signup."""
    # SETUP:
    from pages.accounts.profile import Profile as profile
    name = Utility.random_name()
    email = RestMail((f'{name[Accounts.FIRST]}.{name[Accounts.LAST]}.'
                      f'{Utility.random_hex(4)}').lower())
    email.empty()
    address = email.address
    password = Utility.random_hex(20)
    school = 'Rice University (Houston, TX)'

    # GIVEN: a user with a valid email address viewing the home page
    home = Home(selenium, accounts_base_url).open()

    # WHEN: they click the "Sign up" tab
    # AND:  click the "Educator" box
    # AND:  selects "Instructor" from the drop down menu
    # AND:  enters the email address
    # AND:  clicks the "NEXT" button (a second click may be required if the
    #       email does not end in ".edu")
    # AND:  enters the supplied PIN
    # AND:  clicks the "CONFIRM" button
    # AND:  enters the password in both input boxes
    # AND:  clicks "SUBMIT"
    # AND:  enters data in the various user and course profile boxes
    # AND:  clicks the checkbox next to "I agree to the Terms of Use and the
    #       Privacy Policy."
    # AND:  clicks the "CREATE ACCOUNT" button
    # AND:  clicks the "OK" button
    sign_up = home.content.view_sign_up()

    educator = sign_up.content.sign_up_as_an_educator()

    profile = educator.sign_up(
        first=name[1],
        last=name[2],
        email=email,
        password=password,
        phone=Utility.random_phone(),
        school=school,
        role=Web.ROLE_INSTRUCTOR,
        choice_by=sample(Web.TEXTBOOK_CHOICE_OPTIONS, 1)[0],
        using=sample(Web.USING_OPTIONS, 1)[0],
        students=Utility.random(1, 200),
        books=sample(Web.BOOK_SELECTION, Utility.random(1, 4)),
        page=profile,
        base_url=accounts_base_url)

    # THEN: their new account profile is displayed
    full_name = profile.content.name.full_name
    addresses = [entry.email for entry in profile.content.emails.emails]
    assert('profile' in profile.location), \
        'account profile not displayed'
    assert(name[Accounts.FIRST] in full_name), \
        'first name does not match sign up'
    assert(name[Accounts.LAST] in full_name), \
        'last name does not match sign up'
    assert(address in addresses), \
        'sign up email not found'


@test_case('C195550')
@accounts
def test_sign_up_as_a_nonstudent_user(accounts_base_url, selenium):
    """Test non-student user signup."""
    # SETUP:
    from pages.accounts.profile import Profile as profile
    name = Utility.random_name()
    email = RestMail((f'{name[Accounts.FIRST]}.{name[Accounts.LAST]}.'
                      f'{Utility.random_hex(5)}').lower())
    email.empty()
    address = email.address
    password = Utility.random_hex(20)
    school = 'Rice University (Houston, TX)'
    roles = [Web.ROLE_ADMINISTRATOR, Web.ROLE_OTHER_EDUCATIONAL_STAFF]
    role = roles[Utility.random(0, 1)]
    other = 'Other role' if role == Web.ROLE_OTHER_EDUCATIONAL_STAFF else None

    # GIVEN: a user with a valid email address viewing the home page
    home = Home(selenium, accounts_base_url).open()

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
    sign_up = home.content.view_sign_up()

    educator = sign_up.content.sign_up_as_an_educator()

    profile = educator.sign_up(
        first=name[1],
        last=name[2],
        email=email,
        password=password,
        phone=Utility.random_phone(),
        school=school,
        role=role,
        other=other,
        choice_by=sample(Web.TEXTBOOK_CHOICE_OPTIONS, 1)[0],
        using=sample(Web.USING_OPTIONS, 1)[0],
        students=Utility.random(1, 200),
        books=sample(Web.BOOK_SELECTION, Utility.random(1, 4)),
        page=profile,
        base_url=accounts_base_url)

    # THEN: their new account profile is displayed
    full_name = profile.content.name.full_name
    addresses = [entry.email for entry in profile.content.emails.emails]
    assert('profile' in profile.location), \
        'account profile not displayed'
    assert(name[Accounts.FIRST] in full_name), \
        'first name does not match sign up'
    assert(name[Accounts.LAST] in full_name), \
        'last name does not match sign up'
    assert(address in addresses), \
        'sign up email not found'


@skip_test(reason='bypass social test')
@test_case('C200745')
@social
@accounts
def test_sign_up_as_a_facebook_user(
        accounts_base_url, selenium, facebook_signup):
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


@skip_test(reason='bypass social test')
@social
@accounts
def test_sign_up_as_a_google_user(
        accounts_base_url, selenium, google_signup):
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
    # AND: the name is the same as the Google user's name

    # WHEN: the name field is changed
    # AND: a verified email is added to the profile
    # AND: a password log in option is added
    # AND: the Google log in option is deleted
    # AND: the Profile page is reloaded
    # AND: the Gmail address is deleted

    # THEN: the Google account is available for use


def subject_list(size=1):
    """Return a list of subjects for an elevated signup."""
    subjects = len(Accounts.SUBJECTS)
    if size > subjects:
        size = subjects
    book = ''
    group = [] if Accounts.accounts_old else {}
    while len(group) < size:
        book = (Accounts.SUBJECTS[Utility.random(0, subjects - 1)])[1]
        if book not in group:
            if Accounts.accounts_old:
                group.append(book)
            else:
                group[book] = {
                    'status': Accounts.randomized_use(),
                    'students': Utility.random(), }
    return group
