from test.markers import web, test_case, expected_failure, nondestructive

@test_case('')
@web
@expected_failure
@nondestructive
def test_view_openstax_partners(web_base_url, selenium):
    """Tests ability to view openstax partners page."""
    # GIVEN: On the OpenStax homepage

    # WHEN: Click "Technology"
    # AND: Click "OpenStax Partners"

    # THEN: User is navigated to the OpenStax partners page
