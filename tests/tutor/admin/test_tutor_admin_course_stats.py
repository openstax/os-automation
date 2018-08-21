"""Test of admin console courses stats page."""

from tests.markers import nondestructive, skip_test, test_case, tutor


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_view_course_stats(tutor_base_url, selenium, admin):
    """Test admin to view course stats."""
    # GIVEN: logged in as admin
    # AND: At the Stats Page

    # WHEN: In the drop down click on ""Courses""

    # THEN: The course stats page is loaded
