"""Tests for the OpenStax Web home page."""

from pages.web.home import WebHome as Home
from pages.web.impact import OurImpact
from tests.markers import expected_failure, nondestructive, skip_test  # NOQA
from tests.markers import test_case, web  # NOQA
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
    assert(option_display), 'The subjects menu isn not open'

    # WHEN: the subjects menu is clicked
    home.web_nav.subjects.open()

    # THEN: the subjects menu options are displayed
    assert(home.web_nav.subjects.is_available('All'))

    # WHEN: the "All" menu option is clicked
    all_subjects = home.web_nav.subjects.view_all()

    # THEN: the subjects webpage is displayed
    # AND:  the "View All" filter button is grayed (active)
    # AND:  all subject areas are displayed ("Math", "Science", "Social
    #       Sciences", "Humanities", "Business", and "AP®")
    assert(all_subjects.is_displayed())
    assert(all_subjects.filtered_by(Web.VIEW_ALL))
    assert(all_subjects.math.is_visible)
    assert(all_subjects.science.is_visible)
    assert(all_subjects.social_sciences.is_visible)
    assert(all_subjects.humanities.is_visible)
    assert(all_subjects.business.is_visible)
    assert(all_subjects.ap.is_visible)

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
    #       Sciences", "Humanities", "Business", and "APÂ¨")
    assert(all_subjects.is_displayed())
    assert(all_subjects.filtered_by(Web.VIEW_ALL))
    assert(all_subjects.math.is_visible)
    assert(all_subjects.science.is_visible)
    assert(all_subjects.social_sciences.is_visible)
    assert(all_subjects.humanities.is_visible)
    assert(all_subjects.business.is_visible)
    assert(all_subjects.ap.is_visible)
