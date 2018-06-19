from test.markers import web, test_case, expected_failure, nondestructive

@test_case('')
@web
@expected_failure
@nondestructive
def test_view_technology_options(web_base_url, selenium):
    """Tests ability to view to technology options page."""
    # GIVEN: On the OpenStax homepage

    # WHEN: Click "Technology"
    # AND: Click "Technology Options"

    # THEN: User can view the technology options page
    
