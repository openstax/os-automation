"""Test of teacher on the menu."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_course_setting_w_menu(tutor_base_url, selenium, teacher):
    """Test teacher use the user drop bar menu to view course setting."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click ""course setting"" in the menu""

    # THEN: User should be taken to the settings page


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_course_roaster_w_menu(tutor_base_url, selenium, teacher):
    """Test teacher use user drop bar menu to view course roaster."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click ""course roster"" from menu""

    # THEN: User should be taken to course roster page
