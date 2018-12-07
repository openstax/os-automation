"""Test the research page."""

from pages.web.home import WebHome
from tests.markers import nondestructive, test_case, web
from utils.utilities import Utility
from utils.web import Web


@test_case('C210449')
@nondestructive
@web
def test_research_mission_statement_is_shown(web_base_url, selenium):
    """The research statement is displayed."""
    # GIVEN: a user viewing the research page
    home = WebHome(selenium, web_base_url).open()
    research = home.web_nav.openstax.view_research()

    # WHEN:

    # THEN: the mission statement is shown
    assert(research.is_displayed())
    assert('research' in research.location)
    assert(research.mission)


@test_case('C210450')
@nondestructive
@web
def test_current_research_projects_are_outlined(web_base_url, selenium):
    """Current research projects are outlined in page tiles."""
    # GIVEN: a user viewing the research page
    home = WebHome(selenium, web_base_url).open()
    research = home.web_nav.openstax.view_research()

    # WHEN:

    # THEN: project tiles are listed
    for project in research.projects:
        assert(project.topic)
        assert(project.summary)


@test_case('C210451')
@nondestructive
@web
def test_researchers_are_split_between_past_present_and_external_groups(
        web_base_url, selenium):
    """Researchers are split between past, current, and external groups."""
    # GIVEN: a user viewing the research page
    home = WebHome(selenium, web_base_url).open()
    research = home.web_nav.openstax.view_research()

    for position, group in enumerate(research.tabs):
        print(position, group.name)
        # WHEN: they click on a tab
        group.select()

        # THEN: the researchers are displayed
        assert(group.is_open)
        if position == Web.ALUMNI:
            members = research.alumni
        elif position == Web.CURRENT_MEMBERS:
            members = research.team
        elif position == Web.EXTERNAL_COLLABORATORS:
            members = research.external
        else:
            assert(False), '{0} not an expected group'.format(group.name)
        for place, member in enumerate(members):
            assert(member.name), \
                'Member #{0} is missing their name'.format(place)
            if group.name == Web.CURRENT_MEMBERS:
                assert(member.photo_is_visible), \
                    "{0}'s photo is missing.".format(member.name)
            assert(member.role), "{0}'s role is missing.".format(member.name)


@test_case('C210452')
@nondestructive
@web
def test_mobile_users_are_presented_bars(web_base_url, selenium):
    """On mobile, group tabs are replaced by accordion menus."""
    # GIVEN: a user viewing the research page
    # AND:  the screen width is 600 pixels
    home = WebHome(selenium, web_base_url)
    home.resize_window(width=600)
    home.open()
    home.web_nav.meta.toggle_menu()
    research = home.web_nav.openstax.view_research()

    for position, group in enumerate(research.bars):
        print(position, group.name)
        # WHEN: they click on the group bar
        group.toggle()

        # THEN: the team member tiles are displayed
        assert(group.is_open)
        if position == Web.ALUMNI:
            person = Utility.random(end=len(research.alumni) - 1)
            research.alumni[person].view()
            assert(research.alumni[person].is_visible)
        elif position == Web.CURRENT_MEMBERS:
            person = Utility.random(end=len(research.team) - 1)
            research.team[person].view()
            assert(research.team[person].is_visible)
        elif position == Web.EXTERNAL_COLLABORATORS:
            person = Utility.random(end=len(research.external) - 1)
            research.external[person].view()
            assert(research.external[person].is_visible)
        else:
            assert(False), \
                '"{0}" is not a recognized group'.format(group.name)

        # WHEN: they click on the group bar
        group.toggle()

        # THEN: the team member section is closed
        assert(not group.is_open)


@test_case('C210453')
@nondestructive
@web
def test_some_publications_are_listed(web_base_url, selenium):
    """Some of the research publications are summarized."""
    # GIVEN: a user viewing the research page
    home = WebHome(selenium, web_base_url).open()
    research = home.web_nav.openstax.view_research()

    # WHEN:

    # THEN: research publications our summarized with
    #       authors, a title, a description, and a link to
    #       the full document
    for publication in research.publications:
        assert(publication.authors)
        assert(publication.title)
        assert(publication.summary)
        assert(publication.document)
