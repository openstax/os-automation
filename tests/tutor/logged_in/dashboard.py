"""Test case for main page of tutor with all the courses."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@test_case('')
@expected_failure
@nondestructive
@tutor
def test_tutor_dashboard_page(tutor_base_url, selenium, student):
    """Test the tutor dashboard page."""
    # GIVEN: The Tutor page logged in as a student

    # AND: The student has enrolled in a course

    # WHEN: The user clicks on a enrolled Tutor course card

    # THEN: The Dashboard page for that course loads


@test_case('')
@expected_failure
@tutor
def test_join_trial_course(tutor_base_url, selenium, student):
    """Test the tutor 14 days trial."""
    # GIVEN: Logged into Tutor as a student with a expired trial course

    # WHEN: The user trying to get into the course from course picker

    # THEN: a screen confirming "User's free trial is activated," should pop up


@test_case('')
@expected_failure
@tutor
def test_expired_course(tutor_base_url, selenium, student):
    """Test the expired course."""
    # GIVEN: Logged into Tutor as an student with a expired trial course

    # WHEN: The user clicks on the expired course

    # THEN: Modal pops up and student should be denied access to the course


@test_case('')
@expected_failure
@tutor
def test_access_user_course(tutor_base_url, selenium, student):
    """Test the access user"s course button."""
    # GIVEN: Logged into Tutor as a student with a free trial course

    # WHEN: Get to screen confirming "User's free trial is activated,"

    # AND: The user clicks "Access User's course"

    # THEN: Brought to the course dashboard


@test_case('')
@expected_failure
@tutor
def test_trial_course_access(tutor_base_url, selenium, student):
    """Test access to the trial course."""
    # GIVEN: Logged into Tutor as a student

    # AND: Enrolled in a class with 14 days trial mode

    # WHEN: The user navigates to a course while the 14 day grace period is
    # still in effect

    # THEN: Dashboard of that course is successfully loaded


@test_case('')
@expected_failure
@tutor
def test_enrollment_url(tutor_base_url, selenium, student):
    """Test the enrollment url for the student and the teacher works."""
    # GIVEN:  Logged into Tutor as teacher that has paid course

    # AND: Has gotten enrollment url

    # AND: Log out of teacher account and log in as a student

    # WHEN: The user enters the enrollment url as a student

    # AND: Click past modal(optional)

    # AND: Agree to Terms and Privacy Policy

    # THEN: Student is enrolled in the course


@test_case('')
@expected_failure
@tutor
def test_teacher_dashboard(tutor_base_url, selenium, teacher):
    """Test the teacher dashboard."""
    # GIVEN: Logged into Tutor as a teacher

    # WHEN: The user logs in as teacher

    # THEN: On the dashboard can see their all existing course's card with
    # information


@test_case('')
@expected_failure
@tutor
def test_preview_course(tutor_base_url, selenium, teacher):
    """Test the preview course section."""
    # GIVEN: Logged into Tutor as a teacher

    # WHEN: The user goes to the course picker page

    # THEN: Preview courses are present


@test_case('')
@expected_failure
@tutor
def test_copy_course_page(tutor_base_url, selenium, teacher):
    """Test the copy course page."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # WHEN: The user hovers over a course card

    # AND: Click "copy this course" button

    # THEN: User should be taken to the copy course page
