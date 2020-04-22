"""Tests for the OpenStax Web home page."""

from pages.accounts.admin.users import Search
from pages.accounts.home import AccountsHome
from pages.accounts.signup import SignupOld
from pages.web.home import WebHome as Home
from tests.markers import accounts, expected_failure, nondestructive, skip_test, smoke_test, test_case, web  # NOQA
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
    assert(home.loaded), (
        f'{web_base_url} did not load successfully; '
        f'ended at {selenium.current_url}')


@test_case('C210297')
@skip_test(reason='Sticky note may or may not be active')
@web
def test_the_donation_banner_is_displayed(web_base_url, selenium):
    """Test if the donation banner is shown to new visitors."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN:

    # THEN: a sticky note is displayed at the top of the page
    # AND:  a button is displayed linking to the donation page
    assert(home.sticky_note.loaded), 'Sticky note not loaded'

    assert(home.sticky_note.button.is_displayed()), \
        'Sticky note found but not displayed'

    # WHEN: the user clicks the "Give now" button
    donation = home.sticky_note.go()

    # THEN: they are taken to the donation page
    assert('give' in donation.location), \
        f'Donation page not loaded {donation.location}'

    # WHEN: the user returns to the Web home page
    # AND:  clicks the "x" on the sticky note
    home.open()

    home.sticky_note.close()

    # THEN: the sticky note is closed (no longer visible)
    assert(not home.sticky_note.is_displayed()), \
        'Sticky note is still visible and did not close'


@test_case('C214019')
@expected_failure(reason='Sticky note may or may not be active')
@web
def test_the_donation_banner_is_not_displayed_after_repeat_reloads(
        web_base_url, selenium):
    """Test that the banner is not seen after five reloads."""
    # SETUP:
    reloads = 5

    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN:

    # THEN:  the donation sticky note is present
    assert(home.sticky_note.is_displayed()), 'Sticky note not displayed'

    # WHEN: they reload the home page five times
    for _ in range(reloads):
        home = home.reload()

    # THEN: the donation sticky note is not displayed
    assert(not home.sticky_note.is_displayed()), \
        f'Sticky note still displayed after {reloads} page reloads'


@test_case('C210298')
@nondestructive
@web
def test_the_openstax_nav_is_displayed(web_base_url, selenium):
    """Test the visibility of the OpenStax nav for full and mobile users."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN:

    # THEN: the OpenStax nav is visible
    assert(home.openstax_nav.is_displayed()), 'OpenStax nav not displayed'

    # WHEN: the screen is reduced to 960 pixels or less
    home.resize_window(width=Web.TABLET)

    # THEN: the OpenStax nav is hidden
    # AND:  the menu toggle is displayed
    assert(not home.openstax_nav.is_displayed()), \
        f'OpenStax nav not hidden at {Web.TABLET}px wide'

    assert(home.web_nav.meta.is_displayed()), \
        'Mobile menu toggle is not displayed'

    # WHEN: the user clicks on the menu toggle
    home.web_nav.meta.toggle_menu()

    # THEN: the OpenStax nav options are displayed
    assert(home.openstax_nav.is_displayed()), 'OpenStax nav not displayed'
    assert(home.web_nav.meta.is_open), 'Meta nav not open'


@test_case('C210299')
@smoke_test
@nondestructive
@web
def test_mobile_menu_navigation(web_base_url, selenium):
    """Test the ability to navigate using the mobile menu."""
    # GIVEN: a user viewing the Web home page
    # AND:   the screen width is 960 pixels or less
    home = Home(selenium, web_base_url)

    home.resize_window(width=Web.TABLET)
    home.open()

    # WHEN: they click on the menu toggle
    # AND:  click on the "Subjects" link
    home.web_nav.meta.toggle_menu()

    home.web_nav.subjects.open()

    # THEN: the "Subjects" links are displayed
    assert(home.web_nav.subjects.all.is_displayed()), \
        'Subjests::All not displayed'
    assert(home.web_nav.subjects.math.is_displayed()), \
        'Subjests::Math not displayed'
    assert(home.web_nav.subjects.science.is_displayed()), \
        'Subjests::Science not displayed'
    assert(home.web_nav.subjects.social_sciences.is_displayed()), \
        'Subjests::Social Sciences not displayed'
    assert(home.web_nav.subjects.humanities.is_displayed()), \
        'Subjests::Humanities not displayed'
    assert(home.web_nav.subjects.business.is_displayed()), \
        'Subjests::Business not displayed'
    assert(home.web_nav.subjects.essentials.is_displayed()), \
        'Subjests::Essentials not displayed'

    # WHEN: they click on the "Back" link
    home.web_nav.back()

    # THEN: the nav categories are displayed
    assert(home.web_nav.subjects.is_displayed()), \
        'Subjects nav item not displayed'
    assert(home.web_nav.technology.is_displayed()), \
        'Technology nav item not displayed'
    assert(home.web_nav.openstax.is_displayed()), \
        'What we do nav item not displayed'
    assert(home.web_nav.login.is_displayed()), \
        'Log in nav item not displayed'

    # WHEN: they click on the "Technology" link
    home.web_nav.technology.open()

    # THEN: the "Technology" links are displayed
    assert(home.web_nav.technology.tutor.is_displayed()), \
        'Technology::OpenStax Tutor nav item not displayed'
    assert(home.web_nav.technology.rover.is_displayed()), \
        'Technology::Rover by OpenStax nav item not displayed'
    assert(home.web_nav.technology.partners.is_displayed()), \
        'Technology::OpenStax Partners nav item not displayed'

    # WHEN: they click on the "Back" link
    home.web_nav.back()

    # THEN: the nav categories are displayed
    assert(home.web_nav.subjects.is_displayed()), \
        'Subjects nav item not displayed'
    assert(home.web_nav.technology.is_displayed()), \
        'Technology nav item not displayed'
    assert(home.web_nav.openstax.is_displayed()), \
        'What we do nav item not displayed'
    assert(home.web_nav.login.is_displayed()), \
        'Log in nav item not displayed'

    # WHEN: they click on the "What we do" link
    home.web_nav.openstax.open()

    # THEN: the "What we do" links are displayed
    assert(home.web_nav.openstax.about_us.is_displayed()), \
        'What we do::About Us nav item not displayed'
    assert(home.web_nav.openstax.team.is_displayed()), \
        'What we do::Team nav item not displayed'
    assert(home.web_nav.openstax.research.is_displayed()), \
        'What we do::Research nav item not displayed'
    assert(home.web_nav.openstax.partnerships.is_displayed()), \
        'What we do::Institutional Partnerships nav item not displayed'
    assert(home.web_nav.openstax.creator_fest.is_displayed()), \
        'What we do::Creator Fest nav item not displayed'

    # WHEN: they click on the "Back" link
    home.web_nav.back()

    # THEN: the nav categories are displayed
    assert(home.web_nav.subjects.is_displayed()), \
        'Subjects nav item not displayed'
    assert(home.web_nav.technology.is_displayed()), \
        'Technology nav item not displayed'
    assert(home.web_nav.openstax.is_displayed()), \
        'What we do nav item not displayed'
    assert(home.web_nav.login.is_displayed()), \
        'Log in nav item not displayed'

    # WHEN: they click on the "X" icon
    home.web_nav.meta.toggle_menu()

    # THEN: the mobile menu is closed
    assert(not home.web_nav.meta.is_open), 'Mobile nav still open'


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
    assert(impact.is_displayed()), \
        f'Our Impact page not displayed ({impact.location})'

    # WHEN: the user returns to the home page
    # AND:  the screen is reduced to 960 pixels or less
    # AND:  they click on the menu toggle
    # AND:  click the "Our Impact" link
    home.open()

    home.resize_window(width=Web.TABLET)

    home.web_nav.meta.toggle_menu()

    impact = home.openstax_nav.view_our_impact()

    # THEN: the impact webpage is displayed
    assert(impact.is_displayed()), \
        f'Our Impact page not displayed ({impact.location})'


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
    assert(supporters.is_displayed()), \
        f'Foundation page not displayed ({supporters.location})'

    # WHEN: the user returns to the home page
    # AND:  the screen is reduced to 960 pixels or less
    # AND:  they click on the menu toggle
    # AND:  click the "Supporters" link
    home.open()

    home.resize_window(width=Web.TABLET)

    home.web_nav.meta.toggle_menu()

    supporters = home.openstax_nav.view_supporters()

    # THEN: the supporters webpage is displayed
    assert(supporters.is_displayed()), \
        f'Foundation page not displayed ({supporters.location})'


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
    assert(openstax_blog.is_displayed()), \
        f'Blog page not displayed ({openstax_blog.location})'

    # WHEN: the user returns to the home page
    # AND:  the screen is reduced to 960 pixels or less
    # AND:  they click on the menu toggle
    # AND:  click the "Blog" link
    home.open()

    home.resize_window(width=Web.TABLET)

    home.web_nav.meta.toggle_menu()

    openstax_blog = home.openstax_nav.view_the_blog()

    # THEN: the blog webpage is displayed
    assert(openstax_blog.is_displayed()), \
        f'Blog page not displayed ({openstax_blog.location})'


@test_case('C210303')
@smoke_test
@nondestructive
@web
def test_nav_give_loads_the_donation_page(web_base_url, selenium):
    """Test the OpenStax nav link to the donation page."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they click the "Give" link in the OpenStax nav
    give = home.openstax_nav.view_donation_options()

    # THEN: the donation webpage is displayed
    assert(give.is_displayed()), \
        f'Donation page not displayed ({give.location})'

    # WHEN: the user returns to the home page
    # AND:  the screen is reduced to 960 pixels or less
    # AND:  they click on the menu toggle
    # AND:  click the "Give" link
    home = home.close_tab()
    home.open()

    home.resize_window(width=Web.TABLET)

    home.web_nav.meta.toggle_menu()

    give = home.openstax_nav.view_donation_options()

    # THEN: the donation webpage is displayed
    assert(give.is_displayed()), \
        f'Donation page not displayed ({give.location})'


@test_case('C210304')
@smoke_test
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

    assert(support.at_salesforce), \
        f'Not at the Salesforce support site ({support.location})'

    # WHEN: the user closes the new tab
    # AND:  switches back to the original tab
    # AND:  the screen is reduced to 960 pixels or less
    # AND:  they click on the menu toggle
    # AND:  click the "Help" link
    support.close_tab()

    home.resize_window(width=Web.TABLET)

    home.web_nav.meta.toggle_menu()

    support = home.openstax_nav.view_help_articles()

    # THEN: a new browser tab is opened
    # AND:  the Salesforce support is displayed in the new tab
    assert(len(selenium.window_handles) > 1), \
        'Did not open a new tab or window'

    assert(support.at_salesforce), \
        f'Not at the Salesforce support site ({support.location})'


@test_case('C210305')
@smoke_test
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

    assert(rice.at_rice), f'Not at the Rice University site ({rice.location})'

    # WHEN: the user closes the new tab
    # AND:  switches back to the original tab
    # AND:  the screen is reduced to 960 pixels or less
    # AND:  they click on the menu toggle
    # AND:  wait for the "Rice" logo to appear
    # AND:  click the "Rice" logo
    rice.close_tab()

    home.resize_window(width=Web.TABLET)

    home.web_nav.meta.toggle_menu()

    rice = home.openstax_nav.go_to_rice()

    # THEN: a new browser tab is opened
    # AND:  the Rice University home page is displayed in the new tab
    assert(len(selenium.window_handles) > 1), \
        'Did not open a new tab or window'

    assert(rice.at_rice), f'Not at the Rice University site ({rice.location})'


@test_case('C210306')
@nondestructive
@web
def test_web_nav_is_displayed(web_base_url, selenium):
    """Test for the presence of the website navigation menu."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN:

    # THEN: the site nav is visible
    assert(home.web_nav.is_displayed()), 'Main nav not displayed'

    # WHEN: the screen is reduced to 960 pixels or less
    home.resize_window(width=Web.TABLET)

    # THEN: the site nav is hidden
    # AND:  the menu toggle is displayed
    assert(home.web_nav.is_hidden()), \
        f'Main nav not hidden when screen {Web.TABLET}px wide'

    assert(home.web_nav.meta.is_displayed()), 'Mobile nav not displayed'

    # WHEN: the user clicks on the menu toggle
    home.web_nav.meta.toggle_menu()

    # THEN: the site nav options are displayed
    assert(home.web_nav.subjects.is_displayed()), \
        'Subjects nav item not displayed'
    assert(home.web_nav.technology.is_displayed()), \
        'Technology nav item not displayed'
    assert(home.web_nav.openstax.is_displayed()), \
        'What we do nav item not displayed'
    assert(home.web_nav.login.is_displayed()), \
        'Log in nav item not displayed'


@test_case('C210307')
@nondestructive
@web
def test_openstax_logo_loads_the_home_page(web_base_url, selenium):
    """Test clicking the OpenStax logo opens the home page."""
    # GIVEN: a user viewing the supporters webpage
    home = Home(selenium, web_base_url).open()
    supporters = home.openstax_nav.view_supporters()

    # WHEN: they click the OpenStax logo in the website nav
    home = supporters.web_nav.go_home()

    # THEN: the Web home page is displayed
    assert(home.is_displayed()), \
        f'Home page not displayed; ended at: {home.location}'

    # WHEN: they go to the supporters webpage
    # AND:  the screen is reduced to 960 pixels or less
    # AND:  they click on the menu toggle
    # AND:  click the OpenStax logo
    home.open()
    supporters = home.openstax_nav.view_supporters()

    supporters.resize_window(width=Web.TABLET)

    supporters.web_nav.meta.toggle_menu()

    home = supporters.web_nav.go_home()

    # THEN: the Web home page is displayed
    assert(home.is_displayed()), \
        f'Home page not displayed; ended at: {home.location}'


@test_case('C210308')
@nondestructive
@web
def test_the_openstax_slogan_is_displayed_by_the_logo(web_base_url, selenium):
    """Test for the presence of the slogan text next to the company logo."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN:

    # THEN: the OpenStax slogan is stated
    slogan = 'Access. The future of education.'
    assert(home.web_nav.slogan_visible()), 'Main nav slogan text not visible'
    assert(home.web_nav.slogan == slogan), (
        'Main nav slogan text incorrect: '
        f'"{home.web_nav.slogan}" != "{slogan}"')

    # WHEN: the screen is reduced to 960 pixels or less
    home.resize_window(width=Web.TABLET)

    # THEN: the OpenStax slogan is hidden
    assert(not home.web_nav.slogan_visible()), \
        'Main nav slogan text still visible in mobile display'


@test_case('C210309')
@smoke_test
@nondestructive
@web
def test_able_to_view_subjects_using_the_nav_menu(web_base_url, selenium):
    """Test selecting a subject option opens the subject page."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: the subjects menu is opened
    home.web_nav.subjects.open()

    # THEN: the subjects menu options are displayed
    for option in Web.MENU_SUBJECTS:
        assert(home.web_nav.subjects.is_available(option)), \
            f'Subjects::{option} is not visible'

    # WHEN: the "All" menu option is clicked
    all_subjects = home.web_nav.subjects.view_all()
    visibility = [all_subjects.math,
                  all_subjects.science,
                  all_subjects.social_sciences,
                  all_subjects.humanities,
                  all_subjects.business,
                  all_subjects.essentials,
                  all_subjects.college_success,
                  all_subjects.high_school]

    # THEN: the subjects webpage is displayed
    # AND:  the "View All" filter button is grayed (active)
    # AND:  all subject areas are displayed ("Math", "Science", "Social
    #       Sciences", "Humanities", "Business", "Essentials", "College
    #       Success", and "High School")
    assert(all_subjects.is_displayed()), \
        f'Subjects page not displayed; ended at: {all_subjects.location}'

    assert(all_subjects.is_filtered_by(Web.NO_FILTER)), \
        'View All filter option not set'

    filters = all_subjects.total_filters
    assert(filters == len(visibility) + 1), (
        f'Available filters ({filters}) should equal the '
        f'subjects plus "View All" ({len(visibility)})')
    for index, topic in enumerate(Web.FILTERS):
        assert(visibility[index].is_visible), \
            f'{topic} is not visible when it should be shown'

    # WHEN: the user returns to the home page
    # AND:  the screen width is reduced to 960 pixels or less
    # AND:  they click on the menu toggle
    # AND:  the "Subjects" option is clicked
    # AND:  the "All" option is clicked
    home.open()

    home.resize_window(width=Web.TABLET)

    home.web_nav.meta.toggle_menu()

    home.web_nav.subjects.open()

    all_subjects = home.web_nav.subjects.view_all()
    visibility = [all_subjects.math,
                  all_subjects.science,
                  all_subjects.social_sciences,
                  all_subjects.humanities,
                  all_subjects.business,
                  all_subjects.essentials,
                  all_subjects.college_success,
                  all_subjects.high_school]

    # THEN: the subjects webpage is displayed
    # AND:  the "View All" filter button is grayed (active)
    # AND:  all subject areas are displayed ("Math", "Science", "Social
    #       Sciences", "Humanities", "Business", and "Essentials", "College
    #       Success", and "High School")
    assert(all_subjects.is_displayed()), \
        f'Subjects page not displayed; ended at: {all_subjects.location}'

    assert(all_subjects.is_filtered_by(Web.NO_FILTER)), \
        'View All filter option not set'

    filters = all_subjects.total_filters
    assert(filters == len(visibility) + 1), (
        f'Available filters ({filters}) should equal the '
        f'subjects plus "View All" ({len(visibility)})')
    for index, topic in enumerate(Web.FILTERS):
        assert(visibility[index].is_visible), \
            f'{topic} is not visible when it should be shown'


@test_case('C210310', 'C210311')
@nondestructive
@web
def test_subject_menu_options_load_filtered_views(web_base_url, selenium):
    """Each subject menu option loads the filtered subject page."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()
    for device in ['desktop', 'mobile']:
        if device == 'mobile':
            home.resize_window(width=Web.TABLET)
        # for each specific subject area (ignore View All)
        for index, _ in enumerate(Web.FILTERS):

            # WHEN: they open the "Subjects" menu in the website nav
            # AND:  click on the subject category menu option
            categories = [
                home.web_nav.subjects.view_math,
                home.web_nav.subjects.view_science,
                home.web_nav.subjects.view_social_sciences,
                home.web_nav.subjects.view_humanities,
                home.web_nav.subjects.view_business,
                home.web_nav.subjects.view_essentials,
                home.web_nav.subjects.view_college_success,
                home.web_nav.subjects.view_high_school
            ]
            if device == 'mobile' and not home.web_nav.meta.is_open:
                home.web_nav.meta.toggle_menu()

            subject = categories[index]()
            visibility = [
                subject.math,
                subject.science,
                subject.social_sciences,
                subject.humanities,
                subject.business,
                subject.essentials,
                subject.college_success,
                subject.high_school
            ]

            # THEN: the subject's webpage is displayed
            # AND:  the subject filter button is grayed (active)
            # AND:  the subject category is visible
            # AND:  the other categories are not visible
            assert(subject.location.endswith(Web.URL_APPENDS[index])), (
                f'URL is "{subject.location}" '
                f'but should end with "{Web.URL_APPENDS[index]}"')

            assert(subject.is_displayed()), \
                f'{Web.FILTERS[index]} is not displayed'

            assert(subject.is_filtered_by(Web.FILTERS[index])), \
                f'Results are not being filtered by "{Web.FILTERS[index]}"'

            for topic, category in enumerate(visibility):
                if topic == index:
                    assert(category.is_visible), (
                        f'{Web.FILTERS[topic]} is not visible '
                        'when it should be shown')
                else:
                    assert(not category.is_visible), (
                        f'{Web.FILTERS[topic]} is visible '
                        'when it should be hidden')


@test_case('C210312', 'C210313')
@smoke_test
@nondestructive
@web
def test_technology_menu_options_load_the_corresponding_pages(
        web_base_url, selenium):
    """Test each tech menu option loads the respective web page."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url)
    for device in ['desktop', 'mobile']:
        if device == 'mobile':
            home.resize_window(width=Web.TABLET)
        home.open()

        # WHEN: the technology menu is clicked
        if device == 'mobile' and not home.web_nav.meta.is_open:
            home.web_nav.meta.toggle_menu()
        home.web_nav.technology.open()

        # THEN: the technology menu options are displayed
        for option in Web.MENU_TECHNOLOGY:
            assert(home.web_nav.technology.is_available(option)), \
                f'Technology::{option} nav item not displayed'

        # WHEN: the "About OpenStax Tutor" menu option is clicked
        if device == 'mobile' and not home.web_nav.meta.is_open:
            home.web_nav.meta.toggle_menu()
        tutor = home.web_nav.technology.view_tutor()

        # THEN: the OpenStax Tutor marketing webpage is displayed
        assert(tutor.is_displayed()), \
            f'Tutor marketing page not displayed; ended at: {tutor.location}'

        # WHEN: the "Rover by OpenStax" menu option is clicked
        if device == 'mobile' and not tutor.web_nav.meta.is_open:
            tutor.web_nav.meta.toggle_menu()
        rover = tutor.web_nav.technology.view_rover()

        # THEN: the Rover by OpenStax marketing webpage is displayed
        assert(rover.is_displayed()), \
            f'Rover page not displayed; ended at: {rover.location}'

        # WHEN: the "OpenStax Partners" menu option is clicked
        if device == 'mobile' and not rover.web_nav.meta.is_open:
            rover.web_nav.meta.toggle_menu()
        partners = rover.web_nav.technology.view_partners()

        # THEN: the OpenStax parners webpage is displayed
        assert(partners.is_displayed()), \
            f'Partners page not displayed; ended at: {partners.location}'


@test_case('C210314', 'C210315')
@smoke_test
@nondestructive
@web
def test_what_we_do_menu_options_load_corresponding_pages(
        web_base_url, selenium):
    """Test each team menu option loads the respective web page."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url)
    for device in ['desktop', 'mobile']:
        if device == 'mobile':
            home.resize_window(width=Web.TABLET)
        home.open()

        # WHEN: the "What we do" menu is clicked
        if device == 'mobile' and not home.web_nav.meta.is_open:
            home.web_nav.meta.toggle_menu()
        home.web_nav.openstax.open()

        # THEN: the OpenStax menu options are displayed
        for option in Web.MENU_WHAT_WE_DO:
            assert(home.web_nav.openstax.is_available(option)), \
                f'What we do::{option} nav item not displayed'

        # WHEN: the "About Us" menu option is clicked
        if device == 'mobile' and not home.web_nav.meta.is_open:
            home.web_nav.meta.toggle_menu()
        about = home.web_nav.openstax.view_about_us()

        # THEN: the about webpage is displayed
        assert(about.is_displayed()), \
            f'About page not displayed; ended at: {about.location}'

        # WHEN: they click on the "What we do" menu
        # AND:  click on the "Team" menu option
        if device == 'mobile' and not about.web_nav.meta.is_open:
            about.web_nav.meta.toggle_menu()
        team = about.web_nav.openstax.view_team()

        # THEN: the team webpage is displayed
        assert(team.is_displayed()), \
            f'Team page not displayed; ended at: {team.location}'

        # WHEN: they click on the "What we do" menu
        # AND:  click on the "Research" menu option
        if device == 'mobile' and not team.web_nav.meta.is_open:
            team.web_nav.meta.toggle_menu()
        research = team.web_nav.openstax.view_research()

        # THEN: the research mission webpage is displayed
        assert(research.is_displayed()), \
            f'Research page not displayed; ended at: {research.location}'

        # WHEN: they click on the "What we do" menu
        # AND:  click on the "Institutional Partnerships" menu option
        if device == 'mobile' and not research.web_nav.meta.is_open:
            research.web_nav.meta.toggle_menu()
        partnerships = research.web_nav.openstax.view_partnerships()

        # THEN: the institutional partnerships webpage is displayed
        assert(partnerships.is_displayed()), (
            'Institutional Partnerships page not displayed; '
            f'ended at: {partnerships.location}')

        # WHEN: they click on the "What we do" menu
        # AND:  click on the "Creator Fest" menu option
        if device == 'mobile' and not partnerships.web_nav.meta.is_open:
            partnerships.web_nav.meta.toggle_menu()
        creator_fest = partnerships.web_nav.openstax.view_creator_fest()

        # THEN: the Creator Fest webpage is displayed
        assert(creator_fest.is_displayed()), (
            'Creator Fest page not displayed; '
            f'ended at: {creator_fest.location}')


@test_case('C210316', 'C210322')
@smoke_test
@web
def test_able_to_log_into_the_web_site(web_base_url, selenium, student):
    """Test a student logging into the web site."""
    # GIVEN: a student with a valid user account viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they click on the "Log in" menu
    accounts = home.web_nav.login.go_to_log_in()

    # THEN: they are taken to Accounts
    assert('accounts' in accounts.location), \
        f'Not viewing Accounts ({accounts.location})'

    # WHEN: they log into Accounts
    accounts.log_in(*student, Home, web_base_url)
    # wait for the page load because we're accessing
    # Accounts directly instead of using the Web page
    # object log in routine (Safari issue)
    home.wait_for_page_to_load()

    # THEN: the Web home page is displayed
    # AND:  the "Log in" menu is replaced by the "Hi <first_name>" user menu
    assert(home.web_nav.login.name != 'Log in'), \
        'User not logged into the site'

    # WHEN: they open the user menu
    # AND:  click on the "Logout" menu option
    home.web_nav.login.log_out()

    # THEN: the user is logged out of the Web page
    # AND:  the "Hi <first_name>" user menu is replaced by
    #       the "Log in" menu option
    assert('Log in' in home.web_nav.login.name), \
        'User still shown as logged in'


@test_case('C210317', 'C210323')
@web
def test_able_to_log_into_the_web_site_using_the_mobile_display(
        web_base_url, selenium, student):
    """Test a student logging into the web site on a reduced screen size."""
    # GIVEN: a student with a valid user account viewing the Web home page
    # AND:   the screen width is 960 pixels or less
    home = Home(selenium, web_base_url)

    home.resize_window(width=Web.TABLET)
    home.open()

    # WHEN: they click on the menu toggle
    # AND:  click on the "Log in" link
    home.web_nav.meta.toggle_menu()

    accounts = home.web_nav.login.go_to_log_in()

    # THEN: they are taken to Accounts
    assert('accounts' in accounts.location), \
        f'Not viewing Accounts ({accounts.location})'

    # WHEN: they log into Accounts
    home = accounts.log_in(*student, Home, web_base_url)
    # wait for the page load because we're accessing
    # Accounts directly instead of using the Web page
    # object log in routine (Safari issue)
    home.wait_for_page_to_load()

    # THEN: the Web home page is displayed
    assert(home.is_displayed()), \
        f'Home page not displayed; ended at: {home.location}'

    # WHEN: they click on the menu toggle
    home.web_nav.meta.toggle_menu()

    # THEN: the "Log in" menu is replaced by the "Hi <first_name>" user menu
    assert(home.web_nav.login.name != 'Log in'), \
        'User not logged into the site'

    # WHEN: they click on the user menu
    # AND:  click on the "Logout" menu option
    # AND:  click on the menu toggle
    home.web_nav.login.log_out()

    home.web_nav.meta.toggle_menu()

    # THEN: the user is logged out of the Web page
    # AND:  the "Hi <first_name>" user menu is replaced by
    #       the "Log in" menu option
    assert('Log in' in home.web_nav.login.name), \
        'User still shown as logged in'


@test_case('C210318')
@nondestructive
@web
def test_user_menu_profile_link_loads_accounts_profile_for_the_student(
        web_base_url, selenium, student):
    """Test a student viewing their Accounts profile from the Web user menu."""
    # GIVEN: a user logged into the Web home page
    home = Home(selenium, web_base_url).open()
    home = home.web_nav.login.log_in(*student, Home, web_base_url)

    # WHEN: they open the user menu
    # AND:  click on the "Account Profile" menu option
    profile = home.web_nav.login.view_profile()

    # THEN: the Accounts profile page for the user is displayed in a new tab
    assert(profile.is_displayed() and
           'accounts' in profile.location), \
        f'Not viewing the user profile: {profile.location}'

    # WHEN: they close the new tab
    # AND:  reduce the screen width to 960 pixels or fewer
    # AND:  click on the menu toggle
    # AND:  click on the "Hi <first_name>" link
    # AND:  click on the "Account Profile" link
    profile.close_tab()

    home.resize_window(width=Web.TABLET)

    home.web_nav.meta.toggle_menu()

    profile = home.web_nav.login.view_profile()

    # THEN: the Accounts profile page for the user is displayed
    assert(profile.is_displayed() and
           'accounts' in profile.location), \
        f'Not viewing the user profile: {profile.location}'


@test_case('C210319')
@smoke_test
@nondestructive
@web
def test_go_to_the_users_openstax_tutor_dashboard(
        web_base_url, selenium, student):
    """Test a student going to their Tutor dashboard from the Web user menu."""
    # GIVEN: a user logged into the Web home page
    home = Home(selenium, web_base_url).open()
    home = home.web_nav.login.log_in(*student, Home, web_base_url)

    # WHEN: they open the user menu
    # AND:  click on the "OpenStax Tutor" menu option
    # AND:  click on the Tutor "LOG IN" button
    dashboard = home.web_nav.login.view_tutor()

    # THEN: the OpenStax Tutor dashboard for the user is displayed
    assert(dashboard.is_displayed()), \
        f'Tutor dashboard not displayed: {dashboard.location}'

    # WHEN: they close the new tab
    # AND:  reduce the screen width to 960 pixels or fewer
    # AND:  click on the menu toggle
    # AND:  click on the "Hi <first_name>" link
    # AND:  click on the "OpenStax Tutor" link
    dashboard.close_tab()

    home.resize_window(width=Web.TABLET)

    home.web_nav.meta.toggle_menu()

    dashboard = home.web_nav.login.view_tutor()

    # THEN: the OpenStax Tutor dashboard for the user is displayed
    assert(dashboard.is_displayed()), \
        f'Tutor dashboard not displayed: {dashboard.location}'


@test_case('C210320')
@smoke_test
@accounts
@web
def test_instructor_access_application(
        accounts_base_url, web_base_url, selenium, admin):
    """Test a teacher applying for instructor resource access."""
    # SETUP:
    name = Utility.random_name()
    email = RestMail(f'{name[1]}.{name[2]}.{Utility.random_hex(4)}'.lower())
    email.empty()
    address = email.address
    password = Utility.random_hex(15)

    # GIVEN: a user with rejected instructor access
    # AND:   logged into the Web home page
    accounts = AccountsHome(selenium, accounts_base_url).open()
    sign_up = accounts.content.view_sign_up()
    educator = sign_up.content.sign_up_as_an_educator()
    profile = educator.account_signup(
        name=name, email=address, password=password, _type=Accounts.INSTRUCTOR,
        provider=Accounts.RESTMAIL, school='Automation', news=False,
        phone=Utility.random_phone(), webpage=web_base_url,
        subjects=SignupOld(selenium).subject_list(2), students=10,
        use=Accounts.RECOMMENDED)
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
    assert(form.is_displayed()), 'Instructor application form not displayed'

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
    form = SignupOld(selenium, accounts_base_url)
    form.instructor_access(
        role=SignupOld.INSTRUCTOR,
        school_email=address,
        phone_number=Utility.random_phone(),
        school='Automation',
        students=10,
        webpage=web_base_url,
        using=SignupOld.RECOMMENDED,
        interests=SignupOld(selenium).subject_list(Utility.random(2, 4)),
        get_newsletter=False
    )

    # THEN: the application process is complete
    # No final verification


@test_case('C210321')
@accounts
@web
def test_instructor_access_application_on_mobile(
        accounts_base_url, web_base_url, selenium, admin):
    """Test a teacher applying for instructor resource access."""
    # SETUP:
    name = Utility.random_name()
    email = RestMail(f'{name[1]}.{name[2]}.{Utility.random_hex(7)}'.lower())
    email.empty()
    address = email.address
    password = Utility.random_hex(17)

    # GIVEN: a user with rejected instructor access
    # AND:   logged into the Web home page
    # AND:   the screen width is 960 pixels or less
    accounts = AccountsHome(selenium, accounts_base_url).open()
    sign_up = accounts.content.view_sign_up()
    educator = sign_up.content.sign_up_as_an_educator()
    profile = educator.account_signup(
        name=name, email=address, password=password, _type=Accounts.INSTRUCTOR,
        provider=Accounts.RESTMAIL, school='Automation', news=False,
        phone=Utility.random_phone(), webpage=web_base_url,
        subjects=SignupOld(selenium).subject_list(2), students=10,
        use=Accounts.RECOMMENDED)
    accounts = profile.log_out()
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
    home.resize_window(width=Web.TABLET)
    home.open()

    # WHEN: they open the user menu
    # AND:  click on the "Request instructor access" menu
    #       option
    home.web_nav.meta.toggle_menu()
    form = home.web_nav.login.request_access()

    # THEN: the instructor application form is displayed
    assert(form.is_displayed()), 'Instructor application form not displayed'

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
    form = SignupOld(selenium, accounts_base_url)
    form.instructor_access(
        role=Accounts.INSTRUCTOR,
        school_email=address,
        phone_number=Utility.random_phone(),
        school='Automation',
        students=10,
        webpage=web_base_url,
        using=Accounts.RECOMMENDED,
        interests=SignupOld(selenium).subject_list(Utility.random(2, 4)),
        get_newsletter=False
    )
    home.open()
    home.web_nav.meta.toggle_menu()
    home.web_nav.login.open()

    # THEN: the application process is complete
    # No final verification


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
        assert(banner.is_displayed()), \
            f'Carousel banner {banner.destination} not displayed'


@test_case('C210326')
@nondestructive
@web
def test_carousel_banners_link_to_other_pages(web_base_url, selenium):
    """Test clicking on each banner in the carousel."""
    # SETUP:
    carousel = ['global-reach', 'download-openstax-se-app']

    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they click on the initial banner
    global_reach = home.carousel.banners[Web.F_INTERACTIVE_MAP].click()

    # THEN: the interactive map page is displayed
    assert(global_reach.is_displayed()), 'Global reach page not displayed'
    assert(global_reach.url == carousel[Web.F_INTERACTIVE_MAP]), (
        f'Expected {carousel[Web.F_INTERACTIVE_MAP]}, '
        f'ended at: {global_reach.url}')

    # WHEN: they return to the home page
    # AND:  select the second banner
    # AND:  click on the banner
    home.open()

    home.carousel.dots[Web.F_NEW_APP].click()

    new_app = home.carousel.banners[Web.F_NEW_APP].click()

    # THEN: the OpenStax + SE app page is displayed
    assert(new_app.is_displayed()), 'SE App page not displayed'
    assert(new_app.url == carousel[Web.F_NEW_APP]), (
        f'Expected: {carousel[Web.F_NEW_APP]}, '
        f'ended at: {new_app.url}')

    # WHEN: they return to the home page
    # AND:  select the third banner
    # AND:  click on the banner
    '''
    # Third banner removed
    home.open()

    home.carousel.dots[Web.FREE_BOOKS_NO_CATCH].click()

    nonprofit = home.carousel.banners[Web.FREE_BOOKS_NO_CATCH].click()

    # THEN: the subjects page is displayed
    assert(nonprofit.is_displayed()), 'Subjects page not displayed'
    assert(nonprofit.url == carousel[Web.FREE_BOOKS_NO_CATCH]), (
        f'Expected: {carousel[Web.FREE_BOOKS_NO_CATCH]}, '
        f'ended at: {nonprofit.url}')'''


@test_case('C210327')
@nondestructive
@web
def test_home_page_quote_boxes(web_base_url, selenium):
    """Test the three home page quote boxes."""
    # SETUP:
    quote_boxes = 3

    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they scroll to the quotes
    home.quotes.quotes[Web.SUBSCRIBE].show()

    # THEN: they are presented 3 quote boxes
    # AND:  the first box discusses information updates with a mail list
    assert(len(home.quotes.quotes) == quote_boxes), \
        f'Expected {quote_boxes} boxes; found {len(home.quotes.quotes)}'
    for index, quote in enumerate(home.quotes.quotes):
        assert(quote.is_displayed()), \
            f'Quote box {index + 1} not displayed'

    assert(home.quotes.quotes[Web.SUBSCRIBE].has_image), \
        'Subscribe box image not found'
    assert('OpenStax updates' in home.quotes.quotes[Web.SUBSCRIBE].text), \
        'Subscribe box text does not match'
    assert(home.quotes.quotes[Web.SUBSCRIBE].has_button), \
        'Subscribe box button not found'

    # WHEN: the user clicks the "Subscribe" link
    subscribe = Utility.switch_to(
        selenium, action=home.quotes.quotes[Web.SUBSCRIBE].click)

    # THEN: they are taken to the subscription form in a new tab
    assert(subscribe.is_displayed()), \
        f'Subscription site not displayed ({subscribe.location})'
    assert('www2.openstax.org' in subscribe.location), \
        f'Not at the subscription site: {subscribe.location})'

    # WHEN: they close the new tab
    subscribe.close_tab()

    # THEN: the second box displays a quote
    # AND:  the third box discusses information for book stores
    assert('OpenStax is amazing. Access to these high-quality textbooks '
           'is game-changing for our students.'
           in home.quotes.quotes[Web.BOOK_QUALITY_RIGGS].text), \
        'Riggs quote box text does not match'

    assert('a campus bookstore or school and looking for print copies'
           in home.quotes.quotes[Web.BOOKSTORE_SUPPLIERS].text), \
        'Bookstore suppliers box text does not match'
    assert(home.quotes.quotes[Web.BOOKSTORE_SUPPLIERS].has_button), \
        'Bookstore suppliers box button not found'

    # WHEN: the user clicks the "Learn more" link
    bookstore = home.quotes.quotes[Web.BOOKSTORE_SUPPLIERS].click()

    # THEN: they are taken to the bookstore suppliers page
    assert(bookstore.is_displayed()), (
        'Bookstore suppliers site not displayed; '
        f'ended at: {bookstore.location}')


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
    assert(subjects.is_displayed()), 'Subjects page not displayed'
    assert('subjects' in subjects.location), \
        f'Not viewing the subjects page: {subjects.location}'

    # WHEN: the user opens the Web home page
    # AND:  click the "Technology" pane
    home.open()

    home.education.show()
    technology = home.education.links[Web.TECH].click()

    # THEN: the partners page is displayed
    assert(technology.is_displayed()), 'Tech partners page not displayed'
    assert('partners' in technology.location), \
        f'Not viewing the tech partners page: {technology.location}'


@test_case('C210329')
@nondestructive
@web
def test_the_home_page_information_bars(web_base_url, selenium):
    """Test the information bars."""
    # SETUP:
    information_bars = 2

    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they scroll to the information bars
    home.information.show()

    # THEN: they are presented 2 boxes
    # AND:  the first discusses the OpenStax impact
    assert(len(home.information.box) == information_bars), (
        f'{len(home.information.box)} bar(s) shown; '
        f'expected {information_bars}')

    assert(home.information.box[Web.OUR_IMPACT].is_displayed()), \
        'Our Impact info box not displayed'
    assert('Wolchonok has saved students' in
           home.information.box[Web.OUR_IMPACT].text), \
        'Our Impact info box text changed'
    assert(home.information.box[Web.OUR_IMPACT].has_image), \
        'Our Impact info box image missing'

    # WHEN: the user clicks the "See our impact" button
    impact = home.information.box[Web.OUR_IMPACT].click()

    # THEN: the impact page is displayed
    assert(impact.is_displayed()), 'Our Impact page not displayed'
    assert('impact' in impact.location), \
        f'Not viewing the Our Impact page; ended at: {impact.location}'

    # WHEN: the user opens the Web home page
    # AND:  scroll to the information bars
    home.open()

    home.information.show()

    # THEN: the second box discusses OpenStax partners
    assert(home.information.box[Web.OPENSTAX_PARTNERS].is_displayed()), \
        'Partners info box not displayed'
    assert('OpenStax partners have united with us' in
           home.information.box[Web.OPENSTAX_PARTNERS].text), \
        'Partners info box text changed'

    # WHEN: the user clicks the "View Partners" button
    partners = home.information.box[Web.OPENSTAX_PARTNERS].click()

    # THEN: the partners page is displayed
    assert(partners.is_displayed()), 'Partners page not displayed'
    assert('partners' in partners.location), \
        f'Not viewing the Partners page; ended at: {partners.location}'


@test_case('C210330')
@nondestructive
@web
def test_page_footer_is_displayed(web_base_url, selenium):
    """Test the page footer is beng displayed."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they scroll to the bottom of the page
    home.footer.show()

    # THEN: the footer is visible
    assert(home.footer.is_displayed()), 'Web footer not displayed'


@test_case('C210339')
@nondestructive
@web
def test_footer_static_text(web_base_url, selenium):
    """Test for the footer nonprofit status, mission and copyright info."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url).open()

    # WHEN: they view the page footer
    home.footer.show()
    non_profit = home.footer.directory.non_profit
    mission = home.footer.directory.our_mission
    copyright = home.footer.supplemental.copyright
    ap_statement = home.footer.supplemental.ap_statement

    # THEN: the company nonprofit status is stated
    # AND:  the company mission statement is stated
    # AND:  the copyright and trademark information is
    #       stated
    assert(non_profit), 'Footer non-profit status missing'
    assert('501(c)(3) nonprofit' in non_profit), \
        'Footer non-profit organization type not listed'

    assert(mission), 'Footer OpenStax mission statement missing'
    assert("It's our mission to give every student the tools they need to be" +
           " successful in the classroom." in mission), \
        'Footer mission statement text is incorrect'

    assert(copyright), 'Footer copyright missing'
    assert('licensed under a Creative Commons' in copyright), \
        'Footer licensing text is incorrect'

    assert(ap_statement), 'Footer AP® statement missing'
    assert('trademarks registered and/or owned by the College Board'
           in ap_statement), \
        'Footer AP text is incorrect'


@test_case('C210337')
@smoke_test
@nondestructive
@web
def test_the_contact_us_link_in_the_footer_opens_the_contact_form(
        web_base_url, selenium):
    """Test the footer's contact link."""
    # GIVEN: a user viewing the Web page footer
    home = Home(selenium, web_base_url).open()
    home.footer.show()

    # WHEN: they click the "Contact Us" link
    contact = home.footer.directory.contact_us()

    # THEN: the contact form is displayed
    assert(contact.is_displayed()), 'Contact page not displayed'
    assert('contact' in contact.location), \
        f'Not viewing the contact page; ended at: {contact.location}'


@test_case('C476813')
@nondestructive
@web
def test_the_support_center_link_in_the_footer(web_base_url, selenium):
    """Test the footer's 'Support Center' link."""
    # GIVEN: a user viewing the Web page footer
    home = Home(selenium, web_base_url).open()
    home.footer.show()

    # WHEN: they click the "Support Center" link
    salesforce = home.footer.directory.support_center()

    # THEN: the Salesforce support page is loaded in a new
    #       tab
    assert(salesforce.is_displayed()), 'Salesforce support page not displayed'
    assert('openstax.secure.force.com' in salesforce.location), \
        f'Not viewing the Salesforce site; ended at: {salesforce.location}'


@test_case('C476814')
@nondestructive
@web
def test_the_faq_link_in_the_footer(web_base_url, selenium):
    """Test the footer's 'FAQ' link."""
    # GIVEN: a user viewing the Web page footer
    home = Home(selenium, web_base_url).open()
    home.footer.show()

    # WHEN: they click the "FAQ" link
    faq = home.footer.directory.faq()

    # THEN: the frequently asked questions page is displayed
    assert(faq.is_displayed()), 'FAQ page not displayed'
    assert('faq' in faq.location), \
        f'Not viewing the FAQ page; ended at: {faq.location}'


@test_case('C210338')
@nondestructive
@web
def test_the_press_link_in_the_footer(web_base_url, selenium):
    """Test the footer's press and news page link."""
    # GIVEN: a user viewing the Web page footer
    home = Home(selenium, web_base_url).open()
    home.footer.show()

    # WHEN: they click the "Press" link
    press = home.footer.directory.press()

    # THEN: the press page is displayed
    assert(press.is_displayed()), 'Press page not displayed'
    assert('press' in press.location), \
        f'Not viewing the press page; ended at: {press.location}'


@test_case('C476815')
@nondestructive
@web
def test_the_newsletter_sign_up_link_in_the_footer(web_base_url, selenium):
    """Test the footer's newsletter sign link."""
    # GIVEN: a user viewing the blog page
    home = Home(selenium, web_base_url).open()
    home.footer.show()

    # WHEN: they click on the "Sign Up" button
    sign_up = home.footer.directory.newsletter()

    # THEN: the newsletter sign up form is displayed in the new tab
    assert(sign_up.is_displayed()), 'Newsletter signup site not displayed'
    assert('www2' in sign_up.location), \
        f'Not viewing the newsletter signup site; ended at: {sign_up.location}'


@test_case('C210335')
@nondestructive
@web
def test_the_careers_link_in_the_footer(web_base_url, selenium):
    """Test the footer's careers link."""
    # GIVEN: a user viewing the Web page footer
    home = Home(selenium, web_base_url).open()
    home.footer.show()

    # WHEN: they click the "Careers" link
    careers = home.footer.directory.careers()

    # THEN: the jobs page is displayed
    assert(careers.is_displayed()), 'Careers page not displayed'
    assert('careers' in careers.location), \
        f'Not viewing the careers page; ended at: {careers.location}'


@test_case('C210334')
@nondestructive
@web
def test_the_accessibility_statement_link_in_the_footer(
        web_base_url, selenium):
    """Test the footer's accessibility statement link."""
    # GIVEN: a user viewing the Web page footer
    home = Home(selenium, web_base_url).open()
    home.footer.show()

    # WHEN: they click the "Accessibility Statement" link
    accessibility = home.footer.directory.accessibility_statement()

    # THEN: the accessibility statement page is displayed
    assert(accessibility.is_displayed()), 'Accessibility page not displayed'
    assert('accessibility-statement' in accessibility.location), (
        'Not viewing the accessibility page; '
        f'ended at: {accessibility.location}')


@test_case('C210332')
@nondestructive
@web
def test_the_terms_of_use_link_in_the_footer(web_base_url, selenium):
    """Test the footer's terms of use link."""
    # GIVEN: a user viewing the Web page footer
    home = Home(selenium, web_base_url).open()
    home.footer.show()

    # WHEN: they click the "Terms of Use" link
    terms = home.footer.directory.terms_of_use()

    # THEN: the terms page is displayed
    assert(terms.is_displayed()), 'Terms of use page not displayed'
    assert('tos' in terms.location), \
        f'Not viewing the terms of use page; ended at: {terms.location}'


@test_case('C210331')
@nondestructive
@web
def test_the_licensing_link_in_the_footer(web_base_url, selenium):
    """Test the footer's licensing link."""
    # GIVEN: a user viewing the Web page footer
    home = Home(selenium, web_base_url).open()
    home.footer.show()

    # WHEN: they click the "Licensing" link
    license = home.footer.directory.licensing()

    # THEN: the licensing page is displayed
    assert(license.is_displayed()), 'Licensing page not displayed'
    assert('license' in license.location), \
        f'Not viewing the licensing page; ended at: {license.location}'


@test_case('C210333')
@nondestructive
@web
def test_the_privacy_policy_link_in_the_footer(web_base_url, selenium):
    """Test the footer's privacy policy link."""
    # GIVEN: a user viewing the Web page footer
    home = Home(selenium, web_base_url).open()
    home.footer.show()

    # WHEN: they click the "Privacy Policy" link
    privacy = home.footer.directory.privacy_policy()

    # THEN: the privacy policy page is displayed
    assert(privacy.is_displayed()), 'Privacy policy page not displayed'
    assert('privacy-policy' in privacy.location), \
        f'Not viewing the privacy policy page; ended at: {privacy.location}'


@test_case('C210340')
@nondestructive
@web
def test_the_footer_openstax_facebook_link(web_base_url, selenium):
    """Test the footer Facebook icon loads the OpenStax Facebook page."""
    # GIVEN: a user viewing the Web page footer
    home = Home(selenium, web_base_url).open()
    home.footer.show()

    # WHEN: they click the Facebook icon
    facebook = home.footer.supplemental.facebook()

    # THEN: the OpenStax Facebook page is displayed in a new tab
    assert(facebook.is_displayed()), 'Facebook site not displayed in a new tab'
    assert('facebook' in facebook.location), (
        'Not viewing the OpenStax Facebook page; '
        f'ended at: {facebook.location}')


@test_case('C210341')
@nondestructive
@web
def test_the_footer_openstax_twitter_link(web_base_url, selenium):
    """Test the footer Twitter icon loads the OpenStax Twitter feed."""
    # GIVEN: a user viewing the Web page footer
    home = Home(selenium, web_base_url).open()
    home.footer.show()

    # WHEN: they click the Twitter icon
    twitter = home.footer.supplemental.twitter()

    # THEN: the OpenStax Twitter feed is displayed in a new tab
    assert(twitter.is_displayed()), 'Twitter site not displayed in a new tab'
    assert('twitter' in twitter.location), (
        'Not viewing the OpenStax Twitter page; '
        f'ended at: {twitter.location}')


@test_case('C210342')
@nondestructive
@web
def test_the_footer_openstax_linkedin_link(web_base_url, selenium):
    """Test the footer LinkedIn icon loads the OpenStax LinkedIn page."""
    # GIVEN: a user viewing the Web page footer
    home = Home(selenium, web_base_url).open()
    home.footer.show()

    # WHEN: they click the LinkedIn icon
    linkedin = home.footer.supplemental.linkedin()

    # THEN: the OpenStax LinkedIn company page is displayed in a new tab
    assert(linkedin.is_displayed()), 'LinkedIn site not displayed in a new tab'
    assert('linkedin' in linkedin.location), (
        'Not viewing the OpenStax LinkedIn page; '
        f'ended at: {linkedin.location}')


@test_case('C214021')
@nondestructive
@web
def test_the_footer_openstax_instagram_link(web_base_url, selenium):
    """Test the footer Instagram icon loads the OpenStax Instagram page."""
    # GIVEN: a user viewing the Web page footer
    home = Home(selenium, web_base_url).open()
    home.footer.show()

    # WHEN: they click the Instagram icon
    instagram = home.footer.supplemental.instagram()

    # THEN: the OpenStax Instagram page is displayed in a new tab
    assert(instagram.is_displayed()), \
        'Instagram site not displayed in a new tab'
    assert('instagram' in instagram.location), (
        'Not viewing the OpenStax Instagram page; '
        f'ended at: {instagram.location}')
