"""Test of teacher on the preview course calendar."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_nag_in_preview_course_second(tutor_base_url, selenium, teacher):
    """Test 'Nag' in preview course - every 2nd assignment."""
    # GIVEN: logged in as a teacher account that doesn't
    #  already have any courses

    # WHEN: Go to Preview Course
    # AND: Make 2 assignments (HW, reading, or external)

    # THEN: Upon making the 2nd assignment, a Nag should pop up saying
    # "Remember -- this is just a preview course!"
    # and encouraging the user to "Create a Course"


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_nag_in_preview_course_expires(tutor_base_url, selenium, teacher):
    """Test 'Nag' in preview course - preview expires."""
    # GIVEN: logged in as a teacher account that doesn't
    # already have any courses
    # AND: Navigate to preview course
    # AND: Get course number/title
    # AND: Login as admin on separate browser
    # AND: Go to dropdown > Admin > Course Organization > Courses
    # AND: Search for and click on the specific preview course that
    # user found above (distinguishing by course no.)
    # AND: Click to edit
    # AND: Change the End Date to be soon (~1 or 2 min)
    # AND: Navigate back to teacher account

    # WHEN: Refresh after the new course End Date has passed

    # THEN: Nag should show up urging Tutor Adoption and saying
    # "Preview Course has expired"


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_nag_in_preview_course_launching(tutor_base_url,
                                         selenium, teacher):
    """Test 'Nag' in preview course - stop after launching full course."""
    # GIVEN: A logged in teacher user

    # WHEN: Navigate to Preview Course

    # THEN: the user should not see any "Create a Course" button on the
    # Navbar, nor any tutor adoption nags


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_nag_in_preview_course_create(tutor_base_url, selenium, teacher):
    """Test 'Nag' in preview course - create a course button."""
    # GIVEN: A logged in teacher user

    # WHEN: Navigate to preview course

    # THEN: User should see "Create a Course" button
    # on the Navbar at the top


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_setup_nag_appear(tutor_base_url, selenium, teacher):
    """Test teacher to setup now 'nag' appearing on first.

    initialization of preview course.
    """
    # GIVEN: A verified instructor account made at least
    # 4 hours before the test is conducted

    # WHEN: Four hours after the instructor account was created,
    # click on a preview course

    # THEN: User should see A "Nag" encouraging teachers to
    # create their own course
