"""Test case for student id."""

from tests.markers import expected_failure, test_case, tutor


@test_case('')
@expected_failure
@tutor
def test_change_student_id(tutor_base_url, selenium, student):
    """Test the changing student id."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user clicks on "Change Student ID"

    # AND: The user enters new student id to the input box

    # THEN: User is able to change student section

    # AND: User is able to enter new digits to the student id


@test_case('')
@expected_failure
@tutor
def test_change_id_to_dashboard(tutor_base_url, selenium, student):
    """Test student can go back to dashnoard from changing id page."""
    # GIVEN: Logged into Tutor as a student

    # AND: Is on a class dashboard

    # WHEN: The user clicks on "Change Student ID"

    # AND: The user clicks on "Cancel"

    # THEN: Navigated back to the dashboard of the class


@test_case('')
@expected_failure
@tutor
def test_save_student_id(tutor_base_url, selenium, student):
    """Test the changed student id is saved."""
    # GIVEN: Logged into Tutor as a student

    # AND: Is on a class dashboard

    # WHEN: The user clicks on "Change Student ID"

    # AND: The user enter the new student id number

    # AND: The user clicks "Save"

    # THEN: Student ID saved and navigatde back to the dashboard
