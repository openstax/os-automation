from tests.markers import web, test_case, expected_failure, nondestructive

@test_case('')
@web
@expected_failure
@nondestructive
def test_view_home(web_base_url, selenium):
    """Tests ability view homepage from other pages."""
    # GIVEN: On the OpenStax homepage

    # WHEN: Click "About Us"
    # AND: Click the OpenStax logo on the upper left corner

    # THEN: On homepage
