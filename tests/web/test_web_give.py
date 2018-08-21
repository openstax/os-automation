"""Tests for the OpenStax give webpage."""

from tests.markers import skip_test, test_case, web


@test_case()
@skip_test(reason='Script not written')
@web
def test_other_ways_to_give(web_base_url, selenium):
    """Test to ensure that other ways to give section is present."""
    # GIVEN: On the Give page
    # WHEN: Scroll to the "Other ways to give" section"
    # THEN: Once on the Give page user can
    # view the different options on viewing the page


@test_case()
@skip_test(reason='Script not written')
@web
def test_donation_question(web_base_url, selenium):
    """Tests the ability to submit a donation question."""
    # GIVEN: On the Give page
    # WHEN:  "contact us for help with User's gift" link
    # AND: Redirected to the contact us form
    # AND: Fill out the form
    # AND: Click the "Send" button
    # THEN: Confirmation page is loaded


@test_case()
@skip_test(reason='Script not written')
@web
def test_alpha(web_base_url, selenium):
    """Test entering an alpha character takes user to the first item."""
    # GIVEN: On the web give form
    # WHEN: Type an alpha key when in the country or state drop down
    # THEN: First state or country that
    # starts with the letter they typed is displayed


@test_case()
@skip_test(reason='Script not written')
@web
def test_donation_fields(web_base_url, selenium):
    """Test all required fields."""
    # GIVEN: On the web give form
    # WHEN: Click on the give link
    # AND: Select price user'd like to donate and click the donate button
    # AND: Fill out required fields
    # THEN: Form should be submitted


@test_case()
@skip_test(reason='Script not written')
@web
def test_view_social_media(web_base_url, selenium):
    """Test if social media option is avaible upon donating."""
    # GIVEN: On the web give form
    # WHEN: Fill out required fields (everything but "title" field)
    # AND: Click "Continue"
    # AND: Fill out credit card information
    # AND: Once completed click confirm
    # THEN: Give page is loaded back. The donate buttons is gone and
    # social media icons (facebook, twitter, linkedin) should be visible
