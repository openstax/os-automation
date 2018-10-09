"""Tests for the OpenStax Web home page."""

import pytest
from selenium.common.exceptions import NoSuchElementException

from pages.accounts.admin.users import Search
from pages.accounts.home import AccountsHome
from pages.accounts.signup import Signup
from pages.web.home import WebHome as Home
from pages.web.impact import OurImpact
from tests.markers import accounts, nondestructive, test_case, web
from utils.accounts import Accounts
from utils.email import RestMail
from utils.utilities import Utility
from utils.web import Web


@test_case('C210296')
@nondestructive
@web
def test_the_website_loads(web_base_url, selenium):
    """Test if the OpenStax.org webpage loads."""
    # GIVEN: a web browser
    home = Home(selenium, web_base_url)

    # WHEN: a user opens the Web home page
    home.open()

    # THEN: the site loads
    assert(home.loaded), \
        '{page} did not load successfully'.format(page=web_base_url)


@test_case('C210297')
@web
def test_the_donation_banner_is_displayed(web_base_url, selenium):
    """Test if the donation banner is shown to new visitors."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN:

    # THEN: a sticky note is displayed at the top of the page
    # AND:  a button is displayed linking to the donation page
    assert(home.sticky_note.loaded)
    assert(home.sticky_note.button.is_displayed())

    # WHEN: the user clicks the "Give now" button
    donation = home.sticky_note.go()

    # THEN: they are taken to the donation page
    assert('give' in donation.location)

    # WHEN: the user returns to the Web home page
    # AND:  clicks the "x" on the sticky note
    home.open()
    home.sticky_note.close()

    # THEN: the sticky note is closed (no longer visible)
    assert(not home.sticky_note.is_displayed())


@test_case('C214019')
@web
def test_the_donation_banner_is_not_displayed_after_repeat_reloads(
        web_base_url, selenium):
    """Test that the banner is not seen after five reloads."""
    # GIVEN: a user viewing the Web home page
    # AND:   the donation sticky note is present
    home = Home(selenium, web_base_url).open()
    assert(home.sticky_note.is_displayed())

    # WHEN: they reload the home page five times
    for _ in range(5):
        home = home.reload()

    # THEN: the donation sticky note is not displayed
    assert(not home.sticky_note.is_displayed())


@test_case('C210298')
@nondestructive
@web
def test_the_openstax_nav_is_displayed(web_base_url, selenium):
    """Test the visibility of the OpenStax nav for full and mobile users."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url)
    home.open()

    # WHEN:

    # THEN: the OpenStax nav is visible
    assert(home.openstax_nav.is_displayed())

    # WHEN: the screen is reduced to 960 pixels or less
    home.resize_window(width=900)

    # THEN: the OpenStax nav is hidden
    # AND:  the menu toggle is displayed
    assert(not home.openstax_nav.is_displayed())
    assert(home.web_nav.meta.is_displayed())

    # WHEN: the user clicks on the menu toggle
    home.web_nav.meta.toggle_menu()

    # THEN: the OpenStax nav options are displayed
    assert(home.openstax_nav.is_displayed())
    assert(home.web_nav.meta.is_open)


@test_case('C210299')
@nondestructive
@web
def test_mobile_menu_navigation(web_base_url, selenium):
    """Test the ability to navigate using the mobile menu."""
    # GIVEN: a user viewing the Web home page
    # AND:   the screen width is 960 pixels or less
    home = Home(selenium, web_base_url)
    home.resize_window(width=900)
    home.open()

    # WHEN: they click on the menu toggle
    # AND:  click on the "Subjects" link
    home.web_nav.meta.toggle_menu()
    home.web_nav.subjects.open()

    # THEN: the "Subjects" links are displayed
    assert(home.web_nav.subjects.all.is_displayed())
    assert(home.web_nav.subjects.math.is_displayed())
    assert(home.web_nav.subjects.science.is_displayed())
    assert(home.web_nav.subjects.social_sciences.is_displayed())
    assert(home.web_nav.subjects.humanities.is_displayed())
    assert(home.web_nav.subjects.business.is_displayed())
    assert(home.web_nav.subjects.ap.is_displayed())

    # WHEN: they click on the "Back" link
    home.web_nav.back()

    # THEN: the nav categories are displayed
    assert(home.web_nav.subjects.is_displayed())
    assert(home.web_nav.technology.is_displayed())
    assert(home.web_nav.openstax.is_displayed())
    assert(home.web_nav.login.is_displayed())

    # WHEN: they click on the "Technology" link
    home.web_nav.technology.open()

    # THEN: the "Technology" links are displayed
    assert(home.web_nav.technology.technology.is_displayed())
    assert(home.web_nav.technology.tutor.is_displayed())
    assert(home.web_nav.technology.partners.is_displayed())

    # WHEN: they click on the "Back" link
    home.web_nav.back()

    # THEN: the nav categories are displayed
    assert(home.web_nav.subjects.is_displayed())
    assert(home.web_nav.technology.is_displayed())
    assert(home.web_nav.openstax.is_displayed())
    assert(home.web_nav.login.is_displayed())

    # WHEN: they click on the "What we do" link
    home.web_nav.openstax.open()

    # THEN: the "What we do" links are displayed
    assert(home.web_nav.openstax.about_us.is_displayed())
    assert(home.web_nav.openstax.team.is_displayed())
    assert(home.web_nav.openstax.research.is_displayed())

    # WHEN: they click on the "Back" link
    home.web_nav.back()

    # THEN: the nav categories are displayed
    assert(home.web_nav.subjects.is_displayed())
    assert(home.web_nav.technology.is_displayed())
    assert(home.web_nav.openstax.is_displayed())
    assert(home.web_nav.login.is_displayed())

    # WHEN: they click on the "X" icon
    home.web_nav.meta.toggle_menu()

    # THEN: the mobile menu is closed
    assert(not home.web_nav.meta.is_open)


@test_case('C210300')
@nondestructive
@web
def test_nav_our_impact_loads_the_impact_page(web_base_url, selenium):
    """Test the OpenStax nav link to Our Impact."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they click the "Our Impact" link in the OpenStax nav
    impact = home.openstax_nav.view_our_impact()

    # THEN: the impact webpage is displayed
    assert(impact.is_displayed())

    # WHEN: the user returns to the home page
    # AND:  the screen is reduced to 960 pixels or less
    # AND:  they click on the menu toggle
    # AND:  click the "Our Impact" link
    home.open()
    home.resize_window(width=900)
    home.web_nav.meta.toggle_menu()
    impact = home.openstax_nav.view_our_impact()

    # THEN: the impact webpage is displayed
    assert(impact.is_displayed())


@test_case('C210301')
@nondestructive
@web
def test_nav_supporters_loads_the_foundation_supporters_page(
        web_base_url, selenium):
    """Test the OpenStax nav link to Supporters."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they click the "Supporters" link in the OpenStax nav
    supporters = home.openstax_nav.view_supporters()

    # THEN: the supporters webpage is displayed
    assert(supporters.is_displayed())

    # WHEN: the user returns to the home page
    # AND:  the screen is reduced to 960 pixels or less
    # AND:  they click on the menu toggle
    # AND:  click the "Supporters" link
    home.open()
    home.resize_window(width=900)
    home.web_nav.meta.toggle_menu()
    supporters = home.openstax_nav.view_supporters()

    # THEN: the supporters webpage is displayed
    assert(supporters.is_displayed())


@test_case('C210302')
@nondestructive
@web
def test_nav_blog_loads_the_openstax_blog(web_base_url, selenium):
    """Test the OpenStax nav link to the OpenStax blog."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they click the "Blog" link in the OpenStax nav
    openstax_blog = home.openstax_nav.view_the_blog()

    # THEN: the blog webpage is displayed
    assert(openstax_blog.is_displayed())

    # WHEN: the user returns to the home page
    # AND:  the screen is reduced to 960 pixels or less
    # AND:  they click on the menu toggle
    # AND:  click the "Blog" link
    home.open()
    home.resize_window(width=900)
    home.web_nav.meta.toggle_menu()
    openstax_blog = home.openstax_nav.view_the_blog()

    # THEN: the blog webpage is displayed
    assert(openstax_blog.is_displayed())


@test_case('C210303')
@nondestructive
@web
def test_nav_give_loads_the_donation_page(web_base_url, selenium):
    """Test the OpenStax nav link to the donation page."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they click the "Give" link in the OpenStax nav
    give = home.openstax_nav.view_donation_options()

    # THEN: the donation webpage is displayed
    assert(give.is_displayed())

    # WHEN: the user returns to the home page
    # AND:  the screen is reduced to 960 pixels or less
    # AND:  they click on the menu toggle
    # AND:  click the "Give" link
    home.open()
    home.resize_window(width=900)
    home.web_nav.meta.toggle_menu()
    give = home.openstax_nav.view_donation_options()

    # THEN: the donation webpage is displayed
    assert(give.is_displayed())


@test_case('C210304')
@nondestructive
@web
def test_nav_help_loads_the_salesforce_support_site(web_base_url, selenium):
    """Test the OpenStax nav link to the support pages."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they click the "Help" link in the OpenStax nav
    support = home.openstax_nav.view_help_articles()

    # THEN: a new browser tab is opened
    # AND:  the Salesforce support site is displayed in the new tab
    assert(len(selenium.window_handles) > 1), \
        'Did not open a new tab or window'
    assert(support.at_salesforce)

    # WHEN: the user closes the new tab
    # AND:  switches back to the original tab
    # AND:  the screen is reduced to 960 pixels or less
    # AND:  they click on the menu toggle
    # AND:  click the "Help" link
    support.close_tab()
    home.resize_window(width=900)
    home.web_nav.meta.toggle_menu()
    support = home.openstax_nav.view_help_articles()

    # THEN: a new browser tab is opened
    # AND:  the Salesforce support is displayed in the new tab
    assert(len(selenium.window_handles) > 1), \
        'Did not open a new tab or window'
    assert(support.at_salesforce)


@test_case('C210305')
@nondestructive
@web
def test_nav_rice_logo_loads_the_rice_university_home_page(
        web_base_url, selenium):
    """Test clicking the Rice logo loads the Rice home page."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they click the "Rice" logo in the OpenStax nav
    rice = home.openstax_nav.go_to_rice()

    # THEN: a new browser tab is opened
    # AND:  the Rice University home page is displayed in the new tab
    assert(len(selenium.window_handles) > 1), \
        'Did not open a new tab or window'
    assert(rice.at_rice)

    # WHEN: the user closes the new tab
    # AND:  switches back to the original tab
    # AND:  the screen is reduced to 960 pixels or less
    # AND:  they click on the menu toggle
    # AND:  wait for the "Rice" logo to appear
    # AND:  click the "Rice" logo
    rice.close_tab()
    home.resize_window(width=900)
    home.web_nav.meta.toggle_menu()
    rice = home.openstax_nav.go_to_rice()

    # THEN: a new browser tab is opened
    # AND:  the Rice University home page is displayed in the new tab
    assert(len(selenium.window_handles) > 1), \
        'Did not open a new tab or window'
    assert(rice.at_rice)


@test_case('C210306')
@nondestructive
@web
def test_web_nav_is_displayed(web_base_url, selenium):
    """Test for the presence of the website navigation menu."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN:

    # THEN: the site nav is visible
    assert(home.web_nav.is_displayed())

    # WHEN: the screen is reduced to 960 pixels or less
    home.resize_window(width=900)

    # THEN: the site nav is hidden
    # AND:  the menu toggle is displayed
    assert(home.web_nav.is_hidden())
    assert(home.web_nav.meta.is_displayed())

    # WHEN: the user clicks on the menu toggle
    home.web_nav.meta.toggle_menu()

    # THEN: the site nav options are displayed
    assert(home.web_nav.subjects.is_displayed())
    assert(home.web_nav.technology.is_displayed())
    assert(home.web_nav.openstax.is_displayed())
    assert(home.web_nav.login.is_displayed())


@test_case('C210307')
@nondestructive
@web
def test_openstax_logo_loads_the_home_page(web_base_url, selenium):
    """Test clicking the OpenStax logo opens the home page."""
    # GIVEN: a user viewing the impact webpage
    impact = OurImpact(selenium, web_base_url).open()

    # WHEN: they click the OpenStax logo in the website nav
    home = impact.web_nav.go_home()

    # THEN: the Web home page is displayed
    assert(home.is_displayed())

    # WHEN: they go to the impact webpage
    # AND:  the screen is reduced to 960 pixels or less
    # AND:  they click on the menu toggle
    # AND:  click the OpenStax logo
    impact.open()
    impact.resize_window(width=900)
    impact.web_nav.meta.toggle_menu()
    home = impact.web_nav.go_home()

    # THEN: the Web home page is displayed
    assert(home.is_displayed())


@test_case('C210308')
@nondestructive
@web
def test_the_openstax_slogan_is_displayed_by_the_logo(web_base_url, selenium):
    """Test for the presence of the slogan text next to the company logo."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN:

    # THEN: the OpenStax slogan is stated
    assert(home.web_nav.slogan_visible())
    assert(home.web_nav.slogan == 'Access. The future of education.')

    # WHEN: the screen is reduced to 960 pixels or less
    home.resize_window(width=900)

    # THEN: the OpenStax slogan is hidden
    assert(not home.web_nav.slogan_visible())


@test_case('C210309')
@nondestructive
@web
def test_able_to_view_subjects_using_the_nav_menu(web_base_url, selenium):
    """Test selecting a subject option opens the subject page."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: the mouse cursor is hovered over the "Subjects" menu in the
    #       website nav
    option_display = home.web_nav.subjects.hover()

    # THEN: the subjects menu options are displayed
    assert(option_display), 'The subjects menu is not open'

    # WHEN: the subjects menu is clicked
    home.web_nav.subjects.open()

    # THEN: the subjects menu options are displayed
    for option in Web.MENU_SUBJECTS:
        assert(home.web_nav.subjects.is_available(option)), (
            '{option} should be visible'
            .format(option=option))

    # WHEN: the "All" menu option is clicked
    all_subjects = home.web_nav.subjects.view_all()

    # THEN: the subjects webpage is displayed
    # AND:  the "View All" filter button is grayed (active)
    # AND:  all subject areas are displayed ("Math", "Science", "Social
    #       Sciences", "Humanities", "Business", and "AP®")
    visibility = [all_subjects.math,
                  all_subjects.science,
                  all_subjects.social_sciences,
                  all_subjects.humanities,
                  all_subjects.business,
                  all_subjects.ap]
    assert(all_subjects.is_displayed())
    assert(all_subjects.filtered_by(Web.NO_FILTER))
    filters = all_subjects.available_filters()
    assert(filters == len(visibility) + 1), (
        'Available filters ({available}) should equal the '
        'subjects plus View All ({total})'
        .format(available=filters, total=len(visibility) + 1))
    for index, topic in enumerate(Web.FILTERS):
        assert(visibility[index].is_visible), (
            '{sub} is not visible when it should be shown'
            .format(sub=topic))

    # WHEN: the user returns to the home page
    # AND:  the screen width is reduced to 960 pixels or less
    # AND:  they click on the menu toggle
    # AND:  the "Subjects" option is clicked
    # AND:  the "All" option is clicked
    home.open()
    home.resize_window(width=900)
    home.web_nav.meta.toggle_menu()
    home.web_nav.subjects.open()
    all_subjects = home.web_nav.subjects.view_all()

    # THEN: the subjects webpage is displayed
    # AND:  the "View All" filter button is grayed (active)
    # AND:  all subject areas are displayed ("Math", "Science", "Social
    #       Sciences", "Humanities", "Business", and "AP®")
    visibility = [all_subjects.math,
                  all_subjects.science,
                  all_subjects.social_sciences,
                  all_subjects.humanities,
                  all_subjects.business,
                  all_subjects.ap]
    assert(all_subjects.is_displayed())
    assert(all_subjects.filtered_by(Web.NO_FILTER))
    filters = all_subjects.available_filters()
    assert(filters == len(visibility) + 1), (
        'Available filters ({available}) should equal the '
        'subjects plus View All ({total})'
        .format(available=filters, total=len(visibility) + 1))
    for index, topic in enumerate(Web.FILTERS):
        assert(visibility[index].is_visible), (
            '{sub} is not visible when it should be shown'
            .format(sub=topic))


@test_case('C210310', 'C210311')
@nondestructive
@web
def test_subject_menu_options_load_filtered_views(web_base_url, selenium):
    """Each subject menu option loads the filtered subject page."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url)
    for device in ['desktop', 'mobile']:
        if device == 'mobile':
            home.resize_window(width=900)
        # for each specific subject area (ignore View All)
        for index, _ in enumerate(Web.FILTERS):
            home.open()

            # WHEN: they open the "Subjects" menu in the website nav
            # AND:  click on the subject category menu option
            categories = [
                home.web_nav.subjects.view_math,
                home.web_nav.subjects.view_science,
                home.web_nav.subjects.view_social_sciences,
                home.web_nav.subjects.view_humanities,
                home.web_nav.subjects.view_business,
                home.web_nav.subjects.view_ap
            ]
            if device == 'mobile' and not home.web_nav.meta.is_open:
                home.web_nav.meta.toggle_menu()
            subject = categories[index]()

            # THEN: the subject's webpage is displayed
            # AND:  the subject filter button is grayed (active)
            # AND:  the subject category is visible
            # AND:  the other categories are not visible
            visibility = [
                subject.math,
                subject.science,
                subject.social_sciences,
                subject.humanities,
                subject.business,
                subject.ap
            ]
            assert(subject.location.endswith(Web.URL_APPENDS[index])), (
                'URL is "{current}" but should end with "{end}"'
                .format(current=subject.location, end=Web.URL_APPENDS[index]))
            assert(subject.is_displayed()), (
                '{sub} is not displayed'
                .format(sub=Web.FILTERS[index]))
            assert(subject.filtered_by(Web.FILTERS[index])), (
                'Results are not being filtered by "{filter}"'
                .format(filter=Web.FILTERS[index]))
            for topic, category in enumerate(visibility):
                if topic == index:
                    assert(category.is_visible), (
                        '{sub} is not visible when it should be shown'
                        .format(sub=Web.FILTERS[topic]))
                else:
                    assert(not category.is_visible), (
                        '{sub} is visible when it should be hidden'
                        .format(sub=Web.FILTERS[topic]))


@test_case('C210312', 'C210313')
@nondestructive
@web
def test_technology_menu_options_load_the_corresponding_pages(
        web_base_url, selenium):
    """Test each tech menu option loads the respective web page."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url)
    for device in ['desktop', 'mobile']:
        if device == 'mobile':
            home.resize_window(width=900)
        home.open()

        if device == 'desktop':
            # WHEN: the mouse cursor is hovered over the "Technology" menu
            #       in the website nav
            option_display = home.web_nav.technology.hover()

            # THEN: the technology menu options are displayed
            assert(option_display), 'The technology menu is not open'

        # WHEN: the technology menu is clicked
        if device == 'mobile' and not home.web_nav.meta.is_open:
            home.web_nav.meta.toggle_menu()
        home.web_nav.technology.open()

        # THEN: the technology menu options are displayed
        for option in Web.MENU_TECHNOLOGY:
            assert(home.web_nav.technology.is_available(option)), (
                '{option} should be visible'
                .format(option=option))

        # WHEN: the "Technology Options" menu option is clicked
        if device == 'mobile' and not home.web_nav.meta.is_open:
            home.web_nav.meta.toggle_menu()
        tech = home.web_nav.technology.view_technology()

        # THEN: the technology webpage is displayed
        assert(tech.is_displayed())

        # WHEN: the "About OpenStax Tutor" menu option is clicked
        if device == 'mobile' and not tech.web_nav.meta.is_open:
            tech.web_nav.meta.toggle_menu()
        tutor = tech.web_nav.technology.view_tutor()

        # THEN: the OpenStax Tutor marketing webpage is displayed
        assert(tutor.is_displayed())

        # WHEN: the "OpenStax Partners" menu option is clicked
        if device == 'mobile' and not tutor.web_nav.meta.is_open:
            tutor.web_nav.meta.toggle_menu()
        partners = tutor.web_nav.technology.view_partners()

        # THEN: the OpenStax parners webpage is displayed
        assert(partners.is_displayed())


@test_case('C210314', 'C210315')
@nondestructive
@web
def test_what_we_do_menu_options_load_corresponding_pages(
        web_base_url, selenium):
    """Test each team menu option loads the respective web page."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url)
    for device in ['desktop', 'mobile']:
        if device == 'mobile':
            home.resize_window(width=900)
        home.open()

        if device == 'desktop':
            # WHEN: the mouse cursor is hovered over the "What we do"
            #       menu in the website nav
            option_display = home.web_nav.openstax.hover()

            # THEN: the OpenStax menu options are displayed
            assert(option_display), 'The about us menu is not open'

        # WHEN: the "What we do" menu is clicked
        if device == 'mobile' and not home.web_nav.meta.is_open:
            home.web_nav.meta.toggle_menu()
        home.web_nav.openstax.open()

        # THEN: the OpenStax menu options are displayed
        for option in Web.MENU_WHAT_WE_DO:
            assert(home.web_nav.openstax.is_available(option)), (
                '{option} should be visible'
                .format(option=option))

        # WHEN: the "About Us" menu option is clicked
        if device == 'mobile' and not home.web_nav.meta.is_open:
            home.web_nav.meta.toggle_menu()
        about = home.web_nav.openstax.view_about_us()

        # THEN: the about webpage is displayed
        assert(about.is_displayed())

        # WHEN: they click on the "What we do" menu
        # AND:  click on the "Team" menu option
        if device == 'mobile' and not about.web_nav.meta.is_open:
            about.web_nav.meta.toggle_menu()
        team = about.web_nav.openstax.view_team()

        # THEN: the team webpage is displayed
        assert(team.is_displayed())

        # WHEN: they click on the "What we do" menu
        # AND:  click on the "Research" menu option
        if device == 'mobile' and not team.web_nav.meta.is_open:
            team.web_nav.meta.toggle_menu()
        research = team.web_nav.openstax.view_research()

        # THEN: the research mission webpage is displayed
        assert(research.is_displayed())


@test_case('C210316', 'C210322')
@web
def test_able_to_log_into_the_web_site(web_base_url, selenium, student):
    """Test a student logging into the web site."""
    # GIVEN: a student with a valid user account viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they click on the "Login" menu
    accounts = home.web_nav.login.go_to_log_in()

    # THEN: they are taken to Accounts
    assert('accounts' in accounts.current_url)

    # WHEN: they log into Accounts
    # AND:  close the OpenStax Tutor beta modal
    accounts.login.service_login(*student)
    # wait for the page load because we're accessing
    # Accounts directly instead of using the Web page
    # object log in routine (Safari issue)
    home.wait_for_page_to_load()
    if home.web_nav.login.modal_displayed:
        home.web_nav.login.training_wheel.close_modal()

    # THEN: the Web home page is displayed
    # AND:  the "Login" menu is replaced by the "Hi <first_name>" user menu
    assert(home.web_nav.login.name != 'Login')

    # WHEN: they open the user menu
    # AND:  click on the "Logout" menu option
    home.web_nav.login.log_out()

    # THEN: the user is logged out of the Web page
    # AND:  the "Hi <first_name>" user menu is replaced by
    #       the "Login" menu option
    assert('Login' in home.web_nav.login.name)


@test_case('C210317', 'C210323')
@web
def test_able_to_log_into_the_web_site_using_the_mobile_display(
        web_base_url, selenium, student):
    """Test a student logging into the web site on a reduced screen size."""
    # GIVEN: a student with a valid user account viewing the Web home page
    # AND:   the screen width is 960 pixels or less
    home = Home(selenium, web_base_url)
    home.resize_window(width=900)
    home.open()

    # WHEN: they click on the menu toggle
    # AND:  click on the "Login" link
    home.web_nav.meta.toggle_menu()
    accounts = home.web_nav.login.go_to_log_in()

    # THEN: they are taken to Accounts
    assert('accounts' in accounts.current_url)

    # WHEN: they log into Accounts
    accounts.login.service_login(*student)
    # wait for the page load because we're accessing
    # Accounts directly instead of using the Web page
    # object log in routine (Safari issue)
    home.wait_for_page_to_load()

    # THEN: the Web home page is displayed
    assert(home.is_displayed())

    # WHEN: they click on the menu toggle
    home.web_nav.meta.toggle_menu()

    # THEN: the "Login" menu is replaced by the "Hi <first_name>" user menu
    assert(home.web_nav.login.name != 'Login')

    # WHEN: they click on the user menu
    # AND:  click on the "Logout" menu option
    # AND:  click on the menu toggle
    home.web_nav.login.log_out()
    home.web_nav.meta.toggle_menu()

    # THEN: the user is logged out of the Web page
    # AND:  the "Hi <first_name>" user menu is replaced by
    #       the "Login" menu option
    assert('Login' in home.web_nav.login.name)


@test_case('C210318')
@nondestructive
@web
def test_user_menu_profile_link_loads_accounts_profile_for_the_student(
        web_base_url, selenium, student):
    """Test a student viewing their Accounts profile from the Web user menu."""
    # GIVEN: a user logged into the Web home page
    home = Home(selenium, web_base_url).open()
    home = home.web_nav.login.log_in(*student)
    if home.web_nav.login.modal_displayed:
        home.web_nav.login.training_wheel.close_modal()

    # WHEN: they open the user menu
    # AND:  click on the "Account Profile" menu option
    profile = home.web_nav.login.view_profile()

    # THEN: the Accounts profile page for the user is displayed in a new tab
    assert(profile.is_displayed() and 'accounts' in profile.current_url), \
        'Not viewing the user profile: {url}'.format(url=profile.current_url())

    # WHEN: they close the new tab
    # AND:  reduce the screen width to 960 pixels or fewer
    # AND:  click on the menu toggle
    # AND:  click on the "Hi <first_name>" link
    # AND:  click on the "Account Profile" link
    profile.close_tab()
    home.resize_window(width=900)
    home.web_nav.meta.toggle_menu()
    profile = home.web_nav.login.view_profile()

    # THEN: the Accounts profile page for the user is displayed
    assert(profile.is_displayed() and 'accounts' in profile.current_url), \
        'Not viewing the user profile: {url}'.format(url=profile.current_url())


@test_case('C210319')
@nondestructive
@web
def test_go_to_the_users_openstax_tutor_dashboard(
        web_base_url, selenium, student):
    """Test a student going to their Tutor dashboard from the Web user menu."""
    # GIVEN: a user logged into the Web home page
    home = Home(selenium, web_base_url).open()
    home = home.web_nav.login.log_in(*student)
    if home.web_nav.login.modal_displayed:
        home.web_nav.login.training_wheel.close_modal()

    # WHEN: they open the user menu
    # AND:  click on the "OpenStax Tutor" menu option
    # AND:  click on the Tutor "LOG IN" button
    dashboard = home.web_nav.login.view_tutor()

    # THEN: the OpenStax Tutor dashboard for the user is displayed
    assert(dashboard.is_displayed())

    # WHEN: they close the new tab
    # AND:  reduce the screen width to 960 pixels or fewer
    # AND:  click on the menu toggle
    # AND:  click on the "Hi <first_name>" link
    # AND:  click on the "OpenStax Tutor" link
    dashboard.close_tab()
    home.resize_window(width=900)
    home.web_nav.meta.toggle_menu()
    dashboard = home.web_nav.login.view_tutor()

    # THEN: the OpenStax Tutor dashboard for the user is displayed
    assert(dashboard.is_displayed())


@test_case('C210320')
@accounts
@web
def test_instructor_access_application(
        accounts_base_url, web_base_url, selenium, admin, teacher):
    """Test a teacher applying for instructor resource access."""
    # GIVEN: a user with rejected instructor access
    # AND:   logged into the Web home page
    name = Utility.random_name()
    email = RestMail('{first}.{last}.{tag}'.format(
        first=name[1], last=name[2], tag=Utility.random_hex(3)).lower())
    email.empty()
    address = email.address
    password = teacher[1]
    accounts = AccountsHome(selenium, accounts_base_url).open()
    profile = accounts.login.go_to_signup.account_signup(
        name=name, email=address, password=password, _type=Signup.INSTRUCTOR,
        provider=Signup.RESTMAIL, school='Automation', news=False,
        phone=Utility.random_phone(), webpage=web_base_url,
        subjects=Signup(selenium).subject_list(2), students=10,
        use=Signup.RECOMMENDED)
    profile.log_out()
    profile = accounts.log_in(*admin)
    search = Search(selenium, accounts_base_url).open()
    details = Utility.switch_to(
        driver=selenium,
        action=search.find(terms={'email': address}).users[0].edit)
    details.faculty_status = Accounts.REJECTED
    details.save()
    details.close_tab()
    search.nav.user_menu.sign_out()
    accounts.log_in(address, password)
    home = Home(selenium, web_base_url).open()

    # WHEN: they open the user menu
    # AND:  click on the "Request instructor access" menu
    #       option
    form = home.web_nav.login.request_access()

    # THEN: the instructor application form is displayed
    assert(form.is_displayed())

    # WHEN: they their role from the drop down menu
    # AND:  enter their school-assigned email address
    # AND:  a contact telephone number
    # AND:  the school name
    # AND:  the school website address
    # AND:  select at least one book or "Not Listed"
    # AND:  click on the "APPLY" button
    # AND:  check the box to receive confirmation
    #       concerning instructor resources
    # AND:  click on the "OK" button
    # AND:  open the Web homepage
    # AND:  open the user menu
    form.instructor_access(
        role=Signup.INSTRUCTOR,
        school_email=address,
        phone_number=Utility.random_phone(),
        school='Automation',
        students=10,
        webpage=web_base_url,
        using=Signup.RECOMMENDED,
        interests=Signup(selenium).subject_list(Utility.random(2, 4)),
        get_newsletter=False
    )
    home.open()
    home.web_nav.login.open()

    # THEN: "Request instructor access" is no longer
    #       visible in the user menu
    with pytest.raises(NoSuchElementException):
        home.web_nav.login.instructor_access.is_displayed()


@test_case('C210321')
@accounts
@web
def test_instructor_access_application_on_mobile(
        accounts_base_url, web_base_url, selenium, admin, teacher):
    """Test a teacher applying for instructor resource access."""
    # GIVEN: a user with rejected instructor access
    # AND:   logged into the Web home page
    # AND:   the screen width is 960 pixels or less
    name = Utility.random_name()
    email = RestMail('{first}.{last}.{tag}'.format(
        first=name[1], last=name[2], tag=Utility.random_hex(3)).lower())
    email.empty()
    address = email.address
    password = teacher[1]
    accounts = AccountsHome(selenium, accounts_base_url).open()
    profile = accounts.login.go_to_signup.account_signup(
        name=name, email=address, password=password, _type=Signup.INSTRUCTOR,
        provider=Signup.RESTMAIL, school='Automation', news=False,
        phone=Utility.random_phone(), webpage=web_base_url,
        subjects=Signup(selenium).subject_list(2), students=10,
        use=Signup.RECOMMENDED)
    profile.log_out()
    profile = accounts.log_in(*admin)
    search = Search(selenium, accounts_base_url).open()
    details = Utility.switch_to(
        driver=selenium,
        action=search.find(terms={'email': address}).users[0].edit)
    details.faculty_status = Accounts.REJECTED
    details.save()
    details.close_tab()
    search.nav.user_menu.sign_out()
    accounts.log_in(address, password)
    home = Home(selenium, web_base_url)
    home.resize_window(width=900)
    home.open()

    # WHEN: they open the user menu
    # AND:  click on the "Request instructor access" menu
    #       option
    home.web_nav.meta.toggle_menu()
    form = home.web_nav.login.request_access()

    # THEN: the instructor application form is displayed
    assert(form.is_displayed())

    # WHEN: they their role from the drop down menu
    # AND:  enter their school-assigned email address
    # AND:  a contact telephone number
    # AND:  the school name
    # AND:  the school website address
    # AND:  select at least one book or "Not Listed"
    # AND:  click on the "APPLY" button
    # AND:  check the box to receive confirmation
    #       concerning instructor resources
    # AND:  click on the "OK" button
    # AND:  open the Web homepage
    # AND:  open the user menu
    form.instructor_access(
        role=Signup.INSTRUCTOR,
        school_email=address,
        phone_number=Utility.random_phone(),
        school='Automation',
        students=10,
        webpage=web_base_url,
        using=Signup.RECOMMENDED,
        interests=Signup(selenium).subject_list(Utility.random(2, 4)),
        get_newsletter=False
    )
    home.open()
    home.web_nav.meta.toggle_menu()
    home.web_nav.login.open()

    # THEN: "Request instructor access" is no longer
    #       visible in the user menu
    with pytest.raises(NoSuchElementException):
        home.web_nav.login.instructor_access.is_displayed()


@test_case('C210324')
@nondestructive
@web
def test_tutor_training_wheel_is_displayed_when_a_tutor_user_logs_in(
        web_base_url, selenium, student):
    """The Tutor modal is displayed when a Tutor user logs into Web."""
    # GIVEN: an OpenStax Tutor user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they log into the Web home
    # AND:  wait for up to one minute
    home = home.web_nav.login.log_in(*student)

    # THEN: an OpenStax Tutor modal is presented
    assert(home.wait.until(lambda _: home.web_nav.login.modal_displayed)), \
        'Modal was not displayed within the wait period'

    # WHEN: they click "GOT IT"
    home.web_nav.login.training_wheel.close_modal()

    # THEN: the modal closes
    assert(not home.web_nav.login.modal_displayed)


@test_case('C210325')
@nondestructive
@web
def test_switch_panels_in_banner_carousel(web_base_url, selenium):
    """Test a user switching between the various banners in the carousel."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they click each of the carousel dots
    for index, banner in enumerate(home.carousel.banners):
        home.carousel.dots[index].click()

    # THEN: the banner changes
        assert(banner.is_displayed())


@test_case('C210326')
@nondestructive
@web
def test_carousel_banners_link_to_other_pages(web_base_url, selenium):
    """Test clicking on each banner in the carousel."""
    # GIVEN: a user viewing the Web home page
    carousel = ['subjects', 'about', 'subjects', 'subjects']
    home = Home(selenium, web_base_url).open()

    # WHEN: they click on the banner
    free_books = home.carousel.banners[Web.FREE_BOOKS_NO_CATCH].click()

    # THEN: the subjects page is displayed
    assert(free_books.is_displayed())
    assert(free_books.url == carousel[Web.FREE_BOOKS_NO_CATCH])

    # WHEN: they return to the home page
    # AND:  select the second banner
    # AND:  click on the banner
    home.open()
    home.carousel.dots[Web.EDUCATION_OVER_PROFIT].click()
    nonprofit = home.carousel.banners[Web.EDUCATION_OVER_PROFIT].click()

    # THEN: the about OpenStax page is displayed
    assert(nonprofit.is_displayed())
    assert(nonprofit.url == carousel[Web.EDUCATION_OVER_PROFIT])

    # WHEN: they return to the home page
    # AND:  select the third banner
    # AND:  click on the banner
    home.open()
    home.carousel.dots[Web.ACADEMIC_FREEDOM].click()
    freedom = home.carousel.banners[Web.ACADEMIC_FREEDOM].click()

    # THEN: the subjects page is displayed
    assert(freedom.is_displayed())
    assert(freedom.url == carousel[Web.ACADEMIC_FREEDOM])

    # WHEN: they return to the home page
    # AND:  select the fourth banner
    # AND:  click on the banner
    home.open()
    home.carousel.dots[Web._29_BOOKS].click()
    books = home.carousel.banners[Web._29_BOOKS].click()

    # THEN: the subjects page is displayed
    assert(books.is_displayed())
    assert(books.url == carousel[Web._29_BOOKS])


@test_case('C210327')
@nondestructive
@web
def test_home_page_quote_boxes(web_base_url, selenium):
    """Test the three home page quote boxes."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they scroll to the quotes
    home.quotes.quotes[Web.SUBSCRIBE].show()

    # THEN: they are presented 3 quote boxes
    # AND:  the first box discusses information updates with a mail list
    for quote in home.quotes.quotes:
        assert(quote.is_displayed())
    assert(home.quotes.quotes[Web.SUBSCRIBE].has_image)
    assert('OpenStax updates' in home.quotes.quotes[Web.SUBSCRIBE].text)
    assert(home.quotes.quotes[Web.SUBSCRIBE].has_button)

    # WHEN: the user clicks the "Subscribe" link
    subscribe = Utility.switch_to(
        selenium, action=home.quotes.quotes[Web.SUBSCRIBE].click)

    # THEN: they are taken to the subscription form in a new tab
    assert(subscribe.is_displayed())
    assert('www2.openstax.org' in subscribe.location)

    # WHEN: they close the new tab
    subscribe.close_tab()

    # THEN: the second box displays a quote
    # AND:  the third box discusses information for book stores
    assert('OpenStax is amazing. Access to these high-quality textbooks '
           'is game-changing for our students.'
           in home.quotes.quotes[Web.BOOK_QUALITY_RIGGS].text)
    assert('a campus bookstore or school and looking for print copies'
           in home.quotes.quotes[Web.BOOKSTORE_SUPPLIERS].text)
    assert(home.quotes.quotes[Web.BOOKSTORE_SUPPLIERS].has_button)

    # WHEN: the user clicks the "Learn more" link
    bookstore = home.quotes.quotes[Web.BOOKSTORE_SUPPLIERS].click()

    # THEN: they are taken to the bookstore suppliers page
    assert(bookstore.is_displayed())


@test_case('C210328')
@nondestructive
@web
def test_the_home_page_education_section(web_base_url, selenium):
    """Test the education section and links of the home page."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they scroll to the education section
    # AND:  click the "Books" pane
    home.education.show()
    subjects = home.education.links[Web.BOOKS].click()

    # THEN: the book subjects page is displayed
    assert(subjects.is_displayed())
    assert('subjects' in subjects.location)

    # WHEN: the user opens the Web home page
    # AND:  click the "Technology" pane
    home.open()
    home.education.show()
    technology = home.education.links[Web.TECH].click()

    # THEN: the technology page is displayed
    assert(technology.is_displayed())
    assert('technology' in technology.location)


@test_case('C210329')
@nondestructive
@web
def test_the_home_page_information_bars(web_base_url, selenium):
    """Test the information bars."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they scroll to the information bars
    home.information.show()

    # THEN: they are presented 2 boxes
    # AND:  the first discusses the OpenStax impact
    assert(home.information.box[Web.OUR_IMPACT].is_displayed())
    assert(home.information.box[Web.OPENSTAX_PARTNERS].is_displayed())
    assert('Wolchonok has saved students' in
           home.information.box[Web.OUR_IMPACT].text)
    assert(home.information.box[Web.OUR_IMPACT].has_image)

    # WHEN: the user clicks the "See our impact" button
    impact = home.information.box[Web.OUR_IMPACT].click()

    # THEN: the impact page is displayed
    assert(impact.is_displayed())
    assert('impact' in impact.location)

    # WHEN: the user opens the Web home page
    # AND:  scroll to the information bars
    home.open()
    home.information.show()

    # THEN: the second box discusses OpenStax partners
    assert('OpenStax partners have united with us' in
           home.information.box[Web.OPENSTAX_PARTNERS].text)

    # WHEN: the user clicks the "View Partners" button
    partners = home.information.box[Web.OPENSTAX_PARTNERS].click()

    # THEN: the partners page is displayed
    assert(partners.is_displayed())
    assert('partners' in partners.location)
