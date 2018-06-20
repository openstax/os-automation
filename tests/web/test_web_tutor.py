from tests.markers import web, test_case, expected_failure, nondestructive

@test_case('')
@web
@expected_failure
@nondestructive
def test_view_tutor(web_base_url, selenium):
    """Tests ability to view tutor."""
    # GIVEN: On the OpenStax homepage

    # WHEN: Click "Technology"
    # AND: Click "About OpenStax Tutor"
    # AND: Click "Get Started"

    # THEN: User is on accounts if not logged in, tutor if logged in

