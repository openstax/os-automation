"""Test the OpenStax team and advisor page."""

from pages.web.home import WebHome
from tests.markers import nondestructive, skip_test, test_case, web
from utils.utilities import Utility
from utils.web import Web


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
    for tab in team.tabs:
        assert(tab.name in Web.TEAM_GROUPS)


@test_case('C210456')
@nondestructive
@web
def test_selecting_a_team_member_opens_their_bio(web_base_url, selenium):
    """."""
    # GIVEN: a user viewing the team page
    home = WebHome(selenium, web_base_url).open()
    team = home.web_nav.openstax.view_team()

    # WHEN: they click on an OpenStax team member
    person = team.people[Utility.random(end=len(team.people) - 1)]
    person.select()

    # THEN: a pop out pane displays the team member's bio
    if person.has_bio:
        assert(person.bio)

    # WHEN: they click on the team member again
    person.select()

    # THEN: the pop out pane is closed
    assert(not person.bio_visible)


@test_case('C210457')
@nondestructive
@web
def test_strategic_advisors_are_listed_with_their_bio(web_base_url, selenium):
    """."""
    # GIVEN: a user viewing the team page
    home = WebHome(selenium, web_base_url).open()
    team = home.web_nav.openstax.view_team()

    # WHEN: they click on the "Strategic Advisors" tab
    team.tabs[Web.STRATEGIC_ADVISORS].select()

    # THEN: the strategic advisors are listed with their
    #       name and bio
    for advisor in team.advisors:
        assert(advisor.name)
        assert(advisor.bio)


@skip_test(reason='FAB not currently available')
@test_case('C210458')
@nondestructive
@web
def test_advisory_board_members_are_listed_with_their_school(
        web_base_url, selenium):
    """."""
    # GIVEN: a user viewing the team page
    home = WebHome(selenium, web_base_url).open()
    team = home.web_nav.openstax.view_team()

    # WHEN: they click on the "Faculty Advisory Board" tab
    team.tabs[Web.ADVISORY_BOARD].select()

    # THEN: the advisory board members are listed with their
    #       photo and school
    for advisor in team.fab:
        assert(advisor.name)
        assert(advisor.has_image)
        assert(advisor.school)


@test_case('C210459')
@nondestructive
@web
def test_mobile_users_are_presented_bard(web_base_url, selenium):
    """."""
    # GIVEN: a user viewing the team page
    # AND:  the screen width is 600 pixels
    home = WebHome(selenium, web_base_url)
    home.resize_window(width=600)
    home.open()
    team = home.web_nav.openstax.view_team()

    for position, group in enumerate(team.bar):
        # WHEN: they click on the "OpenStax Team" bar
        group.toggle()

        # THEN: the team member tiles are displayed
        assert(group.is_open)
        if position == Web.OPENSTAX_TEAM:
            assert(team.people[0].is_visible)
        elif position == Web.STRATEGIC_ADVISORS:
            assert(team.advisors[0].is_visible)
        elif position == Web.ADVISORY_BOARD:
            assert(team.fab[0].is_visible)
        else:
            assert(False), \
                '"{0}"" is not a recognized group'.format(group.name)

        # WHEN: they click on the "OpenStax Team" bar
        group.toggle()

        # THEN: the team member section is closed
        assert(not group.is_open)
