"""Tests the about us webpage."""

from tests.markers import nondestructive, skip_test, test_case, web


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_view_about_us(web_base_url, selenium):
    """Tests ability go to about us page."""
    # GIVEN: On the OpenStax homepage.

    # WHEN: Click "About Us".

    # THEN: User is on the about us page.


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_view_about_us_hyperlinks(web_base_url, selenium):
    """Tests hyperlinks are present in about us page."""
    # GIVEN: On About Us Page
    # WHEN: On About Us Page
    # THEN: Hyperlinks in about us are present


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_view_team_members(web_base_url, selenium):
    """Tests ability to view team members."""
    # GIVEN: On About Us Page
    # WHEN: Scroll down to find Our Team and Strategic
    # Advisors with all the members in photo
    # THEN: Click a team member photo, a window
    # will appear on top with the introduction
    # AND: Click the x and the window introduction will close


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_view_homepage(web_base_url, selenium):
    """Tests ability to view homepage."""
    # GIVEN: On the OpenStax homepage
    # WHEN: At the About Us page
    # AND: Click the openstax logo on the upper left corner
    # THEN: On homepage
