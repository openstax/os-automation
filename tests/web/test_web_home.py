"""Tests for the OpenStax Web home page."""

from pages.web.home import WebHome as Home
from tests.markers import expected_failure, nondestructive, skip_test  # NOQA
from tests.markers import test_case, web  # NOQA


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
    home.resize_window(width=1024)
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
    # AND:  the screen is reduced to 960 pixels
    # AND:  they click on the menu toggle
    # AND:  click the "Supporters" link
    home.open()
    home.resize_window(width=900)
    home.web_nav.meta.toggle_menu()
    supporters = home.openstax_nav.view_supporters()

    # THEN: the supporters webpage is displayed
    assert(supporters.is_displayed())
