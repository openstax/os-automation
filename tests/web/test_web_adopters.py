"""Tests the adopters webpage."""

from tests.markers import nondestructive, skip_test, test_case, web


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_view_our_impact(web_base_url, selenium):
    """Tests the ability to view adopters from the homepage."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click on "Our Impact" on the header
    # AND: Click "See a full list of institutions that have adopted openstax"
    # THEN: User views OpenStax Institutional Partners and Affiliate Schools
