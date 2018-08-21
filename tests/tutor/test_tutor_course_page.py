"""Test of teacher on course page."""

from tests.markers import nondestructive, skip_test, test_case, tutor


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_accessibility_infor(tutor_base_url, selenium, teacher):
    """Test teacher to use accessibility info page."""
    # GIVEN: A logged in teacher user

    # WHEN: Click "help"
    # AND: Click "accessibility statement"

    # THEN: User is directed to accessibility info page


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_online_support_form(tutor_base_url, selenium, teacher):
    """Test teacher to use online support form."""
    # GIVEN: A logged in teacher user

    # WHEN: Click "help"
    # AND: Click "chat with support"

    # THEN: User is taken to online support form


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_super_training_wheel(tutor_base_url, selenium, teacher):
    """Test under new teacher, super training.

    The wheel is triggered automatically during the first visit.
    """
    # GIVEN: logged in Tutor as new verified teacher

    # WHEN: Navigate to each of the following pages for the
    #       first time: My Courses, Preview Course Dashboard,
    #       Question Library, Add Reading

    # THEN: Going to My Courses, Preview Course Dashboard, Question Library,
    # Add Reading should have training wheel triggered


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_training_wheel_no_reappear(tutor_base_url, selenium, teacher):
    """Test training wheel doesn't reappear after teacher create a course."""
    # GIVEN: A logged in teacher user

    # WHEN: Check that the "Create a Course" training wheel pops up
    # AND: Navigate to another page
    # AND: Click back to the "My Courses" page

    # THEN: User is able to see "Create a Course" training wheel.


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_active_super_training_wheels(tutor_base_url, selenium, teacher):
    """Test teacher to activate super training wheels."""
    # GIVEN: A logged in teacher user

    # WHEN: Click on bottom left corner of window

    # THEN: User is in spy mode(as indicated by a pi symbol).


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_support_page(tutor_base_url, selenium, teacher):
    """Test teacher to go to OpenStax Support page."""
    # GIVEN: A logged in teacher user

    # WHEN: Click "help articles" from user menu

    # THEN: User is taken to OpenStax support page


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_open_guide_new_tab(tutor_base_url, selenium, teacher):
    """Test teacher to open 'Best Practices Guide' in a new tab."""
    # GIVEN: A logged in teacher user

    # WHEN: Click "best practices" from user menu

    # THEN: User is taken to the best practices page


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_nag_new_course(tutor_base_url, selenium, teacher):
    """Test 'Nag' teacher each time they create a new course."""
    # GIVEN: A logged in teacher user

    # WHEN: User creates a full Tutor course

    # THEN: User should see the Nag message pop up


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_nag_second_login(tutor_base_url, selenium, teacher):
    """Test 'Nag' teachers upon their second login/session."""
    # GIVEN: logged in Tutor as a new verified teacher

    # WHEN: Create a full tutor course
    # AND: Mess around in course a bit
    # AND: Leave the course
    # AND: Return to the course

    # THEN: User should see the Nag message pop up


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_nag_reappears(tutor_base_url, selenium, teacher):
    """Test 'Nag' reappears if user select 'I don't know yet' option."""
    # GIVEN: logged in Tutor as a new verified teacher

    # WHEN: Create full tutor course
    # AND: Answer with the "I don't know yet" option
    # AND: Log out from teacher
    # AND: Log back into teacher
    # AND: Click back on the same course user just made

    # THEN: User should see the Nag message pop up


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_nag_not_pop_up(tutor_base_url, selenium, teacher):
    """Test 'nag' survey does not pop up when answering.

    'I won't be using it'.
    """
    # GIVEN: logged in Tutor as a new verified teacher

    # WHEN: Create full tutor course
    # AND: Answer the "Nag" with the "I won't be using it" option

    # THEN: The survey does not show up


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_nag_not_reappear(tutor_base_url, selenium, teacher):
    """Test 'Nag' doesn't reappear if user don't select.

    'I don't know yet' option.
    """
    # GIVEN: logged in Tutor as a new verified teacher

    # WHEN: Create full tutor course
    # AND: Answer with any option BUT the "I don't know yet" option
    # AND: Log out from teacher
    # AND: Log back into teacher
    # AND: Click back on the same course user just made

    # THEN: The "Nag" should not pop back up


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_pop_up_for_unverified_instructor(tutor_base_url, selenium, teacher):
    """Test modal popup for unverified instructor.

    signing up for new tutor account.
    """
    # GIVEN: Be at the Tutor page

    # WHEN: Log into unverified teacher account

    # THEN: User should not see the Key value
    #       prop/product differentiators on the My Courses
    #       page for an unverified teacher


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_pop_up_for_verified_instructor(tutor_base_url, selenium, teacher):
    """Test modal popup for verified instructor.

    signing up for new tutor account.
    """
    # GIVEN: Be at the Tutor page

    # WHEN: Log into verified teacher account

    # THEN: User should see the Key value prop/product
    #       differentiators on the My Courses
    #       page for a verified teacher
