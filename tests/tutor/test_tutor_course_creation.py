"""Test the Tutor teacher creating new course functions."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@test_case('')
@tutor
def test_create_a_new_course(tutor_base_url, selenium, teacher):
    """Create a new course."""
    # GIVEN: Logged into Tutor as a teacher

    # WHEN: From menu, click "create a course"
    # AND: Fill out the form

    # THEN: A new course is created
    # AND: User is taken to the course dashboard


@expected_failure
@test_case('')
@tutor
def test_copy_a_course_from_past_courses(tutor_base_url, selenium, teacher):
    """Copy a new course from a existing course."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Choose a course user want to copy, click "copy this course"
    # AND: Fill out the form

    # THEN: A new course is created
    # AND: User is taken to the course dashboard, old assignments are present


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_cancel_creating_a_new_course(tutor_base_url, selenium, teacher):
    """Cancel creating a new course."""
    # GIVEN: Logged into Tutor as a teacher

    # WHEN: From menu, click "create a course"
    # AND: Fill out the form
    # AND: Click "cancel"

    # THEN: User is taken back to course picker
    # AND: No course is created


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_cancel_copying_a_new_course(tutor_base_url, selenium, teacher):
    """Cancel copying a new course."""
    # GIVEN: Logged into Tutor as a teacher

    # WHEN: Choose a course user want to copy, then click "copy this course"
    # AND: Fill out the form
    # AND: Click "cancel"

    # THEN: User is taken back to course picker
    # AND: No course is created


@expected_failure
@test_case('')
@tutor
def test_create_new_course_with_empty_fields(
        tutor_base_url, selenium, teacher):
    """Attempt to create a new course without filling in required fields."""
    # GIVEN: Logged into Tutor as a teacher

    # WHEN: From menu, click "create a course"
    # AND: Fill out the form, leaving some of the fields blank

    # THEN: Course could not be created
    # AND: User is prompted to fill out the required fields


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_copy_course_with_empty_fields(tutor_base_url, selenium, teacher):
    """Attempt to copy a course without filling in required fields."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Choose a course user want to copy, click "copy this course"
    # AND: Fill out the form, leaving some of the fields blank

    # THEN: Course could not be created
    # AND: User is prompted to fill in the required fields


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_copy_course_with_old_version_textbook(tutor_base_url, selenium,
                                               teacher):
    """Attempt to copy a course with old version textbook should fail."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course with a old version textbook

    # WHEN: Choose a course with old version textbook, click "copy this course"
    # AND: Fill out the form

    # THEN: Course could not be created
    # AND: User should see massage: "the textbook is too old to be supported."
