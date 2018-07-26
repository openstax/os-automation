"""Test of admin console courses stats page."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_course_stats(tutor_base_url, selenium, admin):
    """Test admin to view course stats."""
    # GIVEN: logged in as admin
    # AND: At the Stats Page

    # WHEN: In the drop down click on ""Courses""

    # THEN: The course stats page is loaded
