"""Test of admin console."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_navbar_elements_present(tutor_base_url, selenium, admin):
    """Test admin console navbar elements present."""
    # GIVEN: Logged in as admin
    # AND: At the Tutor admin console

    # WHEN:

    # THEN: User is able to see the navbar with the following elements:
    # "Tutor Admin Console", "Course Organization", "Content",
    # "Legal", "Stats", "Users", "Job", "Payments", "Research Data",
    # "Salesforce", "System Setting".


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_student(tutor_base_url, selenium, admin):
    """Test to view students in a course."""
    # GIVEN: at Tutor admin console
    # AND: Click on "Course Organization"
    # AND: In the drop down click on "Courses"

    # WHEN: Click the ""List Students"" button next to one of the courses

    # THEN: A list of students in the course is displayed
