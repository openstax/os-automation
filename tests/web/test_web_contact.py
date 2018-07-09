"""Tests for the OpenStax contact us web form."""

from tests.markers import expected_failure, test_case, web


@test_case()
@web
@expected_failure
def test_info_send_when_not_filled(web_base_url, selenium):
    """Test if info is sent when not all info is filled."""
    # GIVEN: On the Contact-us page
    # WHEN: Click orange send button
    # THEN: The message should not send
    # AND: String "Please fill out this field"
    # should be displayed where the input boxes are empty.


@test_case()
@web
@expected_failure
def test_info_send_when_filled(web_base_url, selenium):
    """Test if info is sent when all info is filled."""
    # GIVEN: On the Contact-us page
    # WHEN: Fill out name, email and message
    # AND: Click the orange send button
    # THEN: The message is sent successfully


@test_case()
@web
@expected_failure
def test_info_send_when_invalid_email(web_base_url, selenium):
    """Test if info is sent when an invalid email is provided."""
    # GIVEN: On the Contact-us page
    # WHEN: Fill out name, and message
    # AND: For the email, put abcdedfg
    # THEN: Message should not be sent and red string
    # "Please include an '@' in the email address. 'abcdedfg is
    # missing an '@'." should show up below the email input box."


@test_case()
@web
@expected_failure
def test_support_center(web_base_url, selenium):
    """Test if support center link works properly."""
    # GIVEN: On the Contact-us page
    # WHEN: On the right side, click support center hyper link
    # THEN: Openstax support page is loaded."


@test_case()
@web
@expected_failure
def test_box(web_base_url, selenium):
    """Test if box is visible on contact us page."""
    # GIVEN: On the Contact-us page
    # WHEN: On the Contact-us page
    # THEN: A box with green background with string "Contact Us" is displayed


@test_case()
@web
@expected_failure
def test_mailing_address(web_base_url, selenium):
    """Test if mailing address is visible on contact us page."""
    # GIVEN: On the Contact-us page
    # WHEN: On the Contact-us page
    # THEN: On the right column of the contact us page,
    # mailing address of OpenStax is visible
