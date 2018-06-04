"""Test the e-mail hosts."""
import os
import re

import pytest
from pytest_testrail.plugin import pytestrail
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait

from pages.utils.email import EmailVerificationError, GoogleBase, GuerrillaMail
from pages.utils.utilities import Utility


@pytestrail.case('C195537')
@pytest.mark.nondestructive
def test_google_mail(base_url, selenium):
    """Test a Google Gmail user."""
    page = GoogleBase(selenium, base_url).open()
    assert('/signin' in selenium.current_url), 'Not at Google sign in'
    username = os.getenv('TEST_EMAIL_ACCOUNT')
    password = os.getenv('TEST_EMAIL_PASSWORD')
    email = page.login.go(username, password)
    emails = email.emails
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


@pytestrail.case('C195538')
@pytest.mark.nondestructive
def test_guerrilla_mail(base_url, selenium):
    """Test a Guerrilla Mail user."""
    page = GuerrillaMail(selenium, base_url).open()
    assert('guerrilla' in selenium.current_url)
    assert(page.header.is_header_displayed), 'Header not available'
    assert(page.emails), 'No e-mails found'
    assert(page.header.email), 'No e-mail address returned'
    assert(page.header.is_scrambled), 'E-mail is in plain text'
    email_layout = re.compile(r'[^@]+@[^@]+\.[^@]+')
    assert(email_layout.match(page.header.email)), \
        'E-mail is not a valid format'
    assert(not page.header.scramble().is_scrambled), 'E-mail is scrambled'
    assert(email_layout.match(page.header.email)), \
        'E-mail is not a valid format'
    # send a test message to verify pin code
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
    # wait for the message to show in the inbox
    WebDriverWait(page.selenium, 30).until(
        expect.presence_of_element_located(
            (By.XPATH, '//*[contains(text(),"999999")]')))
    emails = page.emails
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
    new_user = Utility.random_hex(12).lower()
    page.header.email = new_user
    assert(new_user in page.header.email), \
        'E-mail user ID did not change'
    assert(page.header.host == 'sharklasers.com'), \
        'Incorrect default host name'
    page.header.host = 'guerrillamail.com'
    assert(page.header.host == 'guerrillamail.com'), 'Host name unchanged'
    page.header.forget_address()
    assert(selenium.find_element('css selector', '#inbox-id input')
           .text == ''), 'Username not blank'
