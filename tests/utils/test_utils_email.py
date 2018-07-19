"""Test the e-mail hosts."""

import re

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait

from pages.utils.email import EmailVerificationError, GoogleBase, GuerrillaMail
from tests.markers import expected_failure, nondestructive, test_case


@test_case('C195537')
@expected_failure
@nondestructive
def test_google_mail_user_has_pin_emails(gmail, selenium):
    """Test a Google Gmail user."""
    # GIVEN: A valid logged in Gmail user with previous validation emails
    page = GoogleBase(selenium).open()
    email = page.login.go(*gmail)
    emails = email.emails

    # WHEN:

    # THEN: There is a mixture of emails with and without pins
    assert(emails), 'No e-mails found'
    for mail in emails:
        if mail.has_pin:
            assert(mail.sender), 'E-mail does not show a sender'
            assert(mail.subject), 'E-mail does not show a subject'
            assert(mail.excerpt), 'Excerpt not shown'
            assert(mail.get_pin), 'Pin not recovered'
        else:
            assert(mail.sender), 'E-mail does not show a sender'
            assert(mail.subject), 'E-mail does not show a subject'
            assert(mail.excerpt), 'Excerpt not shown'
            with pytest.raises(EmailVerificationError):
                mail.get_pin


@test_case('C195538')
@nondestructive
def test_guerrilla_mail_received_pin_email(selenium):
    """Test a Guerrilla Mail user."""
    # GIVEN: A new Guerrilla Mail session
    page = GuerrillaMail(selenium).open()

    # WHEN: A template email with a pin is sent to the current email
    page = page.compose.send_message(
        to=page.header.email,
        subject='[OpenStax] Use PIN 999999 to confirm your email address',
        body=('Welcome!\n\nEnter your 6-digit PIN in your browser to confirm '
              'your email address:\n\nYour PIN: 999999\n\nIf you have any '
              'trouble using this PIN, you can also click the link below\nto '
              'confirm your email address:\n\nhttps://openstax.org/fake/'
              'registration/pin/url\n\nWe sent this message because someone '
              'is trying to use ... to create an\nOpenStax account. If this '
              'wasn\'t you, please disregard this message.\n\nRegards,\nThe '
              'OpenStax Team'))
    # AND: The user waits for the message to show in the inbox
    WebDriverWait(page.selenium, 30).until(
        expect.presence_of_element_located(
            (By.XPATH, '//*[contains(text(),"999999")]')))
    emails = page.emails

    # THEN: There is an email with a pin and an email without a pin
    assert(page.header.is_header_displayed), 'Header not available'
    assert(page.emails), 'No e-mails found'
    assert(page.header.email), 'No e-mail address returned'
    assert(re.compile(r'[^@]+@[^@]+\.[^@]+').match(page.header.email)), \
        'E-mail is not a valid format'
    assert(emails), 'No e-mails found'
    for mail in emails:
        if mail.has_pin:
            assert(mail.subject), 'E-mail does not show a subject'
            assert(mail.excerpt), 'Excerpt not shown'
            assert(mail.get_pin), 'Pin not recovered'
        else:
            assert(mail.subject), 'E-mail does not show a subject'
            assert(mail.excerpt), 'Excerpt not shown'
            with pytest.raises(EmailVerificationError):
                mail.get_pin

    # TODO: move Guerrilla Mail email manipulation tests to a separate test
    '''assert(page.header.is_scrambled), 'E-mail is in plain text'
    assert(email_layout.match(page.header.email)), \
        'E-mail is not a valid format'
    assert(not page.header.scramble().is_scrambled), 'E-mail is scrambled'
    '''
    '''new_user = Utility.random_hex(12).lower()
    page.header.email = new_user
    assert(new_user in page.header.email), \
        'E-mail user ID did not change'
    assert(page.header.host == 'sharklasers.com'), \
        'Incorrect default host name'
    page.header.host = 'guerrillamail.com'
    assert(page.header.host == 'guerrillamail.com'), 'Host name unchanged'
    # wait for the flash headers to disappear
    sleep(5.0)
    page.header.forget_address()
    assert(selenium.find_element('css selector', '#inbox-id input')
           .text == ''), 'Username not blank' '''
