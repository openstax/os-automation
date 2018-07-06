"""Tests the adopters webpage."""

from tests.markers import expected_failure, nondestructive, test_case, web


@test_case('')
@expected_failure
@nondestructive
@web
def test_view_our_impact(web_base_url, selenium):
    """Tests the ability to view adopters from the homepage."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click on "Our Impact" on the header
    # AND: Click "See a full list of institutions that have adopted openstax"
    # THEN: User views OpenStax Institutional Partners and Affiliate Schools
