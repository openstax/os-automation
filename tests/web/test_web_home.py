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
    assert(home.sticky_note.button.is_displayed)

    # WHEN: the user clicks the "Give now" button
    donation = home.sticky_note.go()

    # THEN: they are taken to the donation page
    assert('give' in donation.location)

    # WHEN: the user returns to the Web home page
    # AND:  clicks the "x" on the sticky note
    home.open()
    home.sticky_note.close()

    # THEN: the sticky note is closed (no longer visible)
    assert(not home.sticky_note.is_displayed)


@test_case('C214019')
@web
def test_the_donation_banner_is_not_displayed_after_repeat_reloads(
        web_base_url, selenium):
    """Test that the banner is not seen after five reloads."""
    # GIVEN: a user viewing the Web home page
    # AND:   the donation sticky note is present
    home = Home(selenium, web_base_url).open()
    assert(home.sticky_note.is_displayed)

    # WHEN: they reload the home page five times
    for _ in range(5):
        home.reload()

    # THEN: the donation sticky note is not displayed
    assert(not home.sticky_note.is_displayed)


@test_case('C210298')
@nondestructive
@web
def test_the_openstax_nav_is_displayed(web_base_url, selenium):
    """Test the visibility of the OpenStax nav for full and mobile users."""
    # GIVEN: a user viewing the Web home page
    home = Home(selenium, web_base_url, 20).open()

    # WHEN:

    # THEN: the OpenStax nav is visible
    assert(home.openstax_nav.is_displayed)
    assert(not home.web_nav.meta.is_displayed)

    # WHEN: the screen is reduced to 960 pixels
    home.resize_window(width=900)

    # THEN: the OpenStax nav is hidden
    # AND:  the menu toggle is displayed
    assert(not home.openstax_nav.is_displayed)
    assert(home.web_nav.meta.is_displayed)

    # WHEN: the user clicks on the menu toggle
    home.web_nav.meta.toggle_menu()

    # THEN: the OpenStax nav options are displayed
    assert(home.openstax_nav.is_displayed)
    assert(home.web_nav.meta.is_open)
