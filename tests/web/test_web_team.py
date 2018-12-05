"""Test the OpenStax team and advisor page."""

from pages.web.home import WebHome
from tests.markers import nondestructive, test_case, web


@test_case('C210455')
@nondestructive
@web
def test_the_openstax_team_is_split_into_three_groups(web_base_url, selenium):
    """."""
    # GIVEN: a user viewing the team page
    home = WebHome(selenium, web_base_url).open()
    team = home.web_nav.openstax.view_team()

    # WHEN:

    # THEN: the "OpenStax Team", "Strategic Advisors", and
    #       "Faculty Advisory Board" are displayed
    assert(team.is_displayed())
    assert('team' in team.location)


@test_case('C210456')
@nondestructive
@web
def test_selecting_a_team_member_opens_their_bio(web_base_url, selenium):
    """."""
    # GIVEN: a user viewing the team page

    # WHEN: they click on an OpenStax team member

    # THEN: a pop out pane displays the team member's bio

    # WHEN: they click on the team member again

    # THEN: the pop out pane is closed


@test_case('C210457')
@nondestructive
@web
def test_strategic_advisors_are_listed_with_their_bio(web_base_url, selenium):
    """."""
    # GIVEN: a user viewing the team page

    # WHEN: they click on the "Strategic Advisors" tab

    # THEN: the strategic advisors are listed with their
    #       name and bio


@test_case('C210458')
@nondestructive
@web
def test_advisory_board_members_are_listed_with_their_school(
        web_base_url, selenium):
    """."""
    # GIVEN: a user viewing the team page

    # WHEN: they click on the "Faculty Advisory Board" tab

    # THEN: the advisory board members are listed with their
    #       photo and school


@test_case('C210459')
@nondestructive
@web
def test_mobile_users_are_presented_bard(web_base_url, selenium):
    """."""
    # GIVEN: a user viewing the team page
    # AND:  the screen width is 600 pixels

    # WHEN: they click on the "OpenStax Team" bar

    # THEN: the team member tiles are displayed

    # WHEN: they click on the "OpenStax Team" bar

    # THEN: the team member section is closed

    # WHEN: they click on the "Strategic Advisors" bar

    # THEN: the advisor tiles are displayed

    # WHEN: they click on the "Strategic Advisors" bar

    # THEN: the advisors section is closed

    # WHEN: they click on the "Faculty Advisory Board" bar

    # THEN: the board member tiles are displayed

    # WHEN: they click on the "Faculty Advisory Board" bar

    # THEN: the board section is closed
