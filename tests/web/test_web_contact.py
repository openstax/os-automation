"""Tests for the OpenStax contact us webpage."""

from tests.markers import expected_failure, test_case, web


@test_case()
@web
@expected_failure
def test_openstax_mailing_address(web_base_url, selenium):
    """Test if openstax mailing address is properly displayed."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and
    # click on contact us in the footer with dark background
    # THEN: On the right column of the contact us page, mailing address of
    # OpenStax is visible


@test_case()
@web
@expected_failure
def test_view_options_on_donating(web_base_url, selenium):
    """Test if all donate options are availble."""
    # GIVEN: On the OpenStax homepage
    # WHEN: From the give page
    # AND: Scroll down to the bottom of the page
    # and click the "contact us for help with User's gift" link
    # AND: Redirected to the contact us form
    # AND: Fill out the form
    # AND: Click the "Send" button
    # THEN: Confirmation page is loaded.


@test_case()
@web
@expected_failure
def test_submit_donation_question(web_base_url, selenium):
    """Test if user could submit question about donation."""
    # GIVEN: On the OpenStax homepage
    # WHEN: From the give page
    # AND: Scroll down to the bottom of the page and
    # click the "contact us for help with User's gift" link
    # AND: Redirected to the contact us form
    # AND: Fill out the form
    # AND: Click the "Send" button
    # THEN: Confirmation page is loaded.


@test_case()
@web
@expected_failure
def test_message_when__invalid(web_base_url, selenium):
    """Test if message is sent when email is not valid."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and
    # click on contact us in the footer with dark background
    # AND: Fill out name, and message
    # AND: For the email, put abcdedfg
    # THEN: Message should not be sent and red string
    # "Please include an '@' in the email address.
    # 'abcdedfg is missing an '@'."
    # should show up below the email input box.


@test_case()
@web
@expected_failure
def test_message_sent_when_filled(web_base_url, selenium):
    """Test if message is sent when all info is filled."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and
    # click on contact us in the footer with dark background
    # AND: Fill out name, email and message
    # AND: Click the orange send button
    # THEN: The message is sent successfully.
