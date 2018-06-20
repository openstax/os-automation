from tests.markers import web, test_case, expected_failure, nondestructive

@test_case('')
@web
@expected_failure
@nondestructive
def test_view_our_impact(web_base_url, selenium):
    """Tests ability to view our impact page."""
    # GIVEN: On the OpenStax homepage

    # WHEN: Click "Our Impact"

    # THEN: User is on our impact page


@test_case('')
@web
@expected_failure
@nondestructive
def test_view_insitutions(web_base_url, selenium):
    """Tests ability to view insitutions using openstax."""
    # GIVEN: On the OpenStax homepage

    # WHEN: Click on "Our Impact" on the header
    # AND: Click "See a full list of institutions that have adopted openstax"

    # THEN: User views OpenStax Institutional Partners and Affiliate Schools
