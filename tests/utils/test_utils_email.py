"""Test the e-mail hosts."""

import re

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait

from pages.utils.email import EmailVerificationError, GoogleBase  # NOQA
from pages.utils.email import GuerrillaMail, RestMail, SendMail  # NOQA
from tests.markers import nondestructive, test_case

TEST_EMAIL_SUBJECT = (
    '[OpenStax] Use PIN 999999 to confirm your email address'
)
TEST_EMAIL_BODY = (
    'Welcome!\n\nEnter your 6-digit PIN in your browser to confirm '
    'your email address:\n\nYour PIN: 999999\n\nIf you have any '
    'trouble using this PIN, you can also click the link below\nto '
    'confirm your email address:\n\nhttps://openstax.org/fake/'
    'registration/pin/url\n\nWe sent this message because someone '
    'is trying to use ... to create an\nOpenStax account. If this '
    'wasn\'t you, please disregard this message.\n\nRegards,\nThe '
    'OpenStax Team'
)
GOOGLE = ('smtp.gmail.com', 587, 10)


@test_case('C195537')
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
def test_guerrilla_mail_received_pin_email(selenium):
    """Test a Guerrilla Mail user."""
    # GIVEN: A new Guerrilla Mail session
    page = GuerrillaMail(selenium).open()

    # WHEN: A template email with a pin is sent to the current email
    # AND: The user waits for the message to show in the inbox
    page = page.compose.send_message(
        to=page.header.email,
        subject=TEST_EMAIL_SUBJECT,
        body=TEST_EMAIL_BODY)
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


@test_case('C210268')
def test_restmail_received_pin_email(gmail):
    """Test a RestMail JSON email."""
    # GIVEN: A RestMail address with a verification PIN email
    username = 'openstax'
    email = RestMail(username)
    email.empty()  # clear the message inbox

    send = SendMail(*gmail, *GOOGLE)
    sender = ('OpenStax QA', 'noreply@openstax.org')
    recipient = ('OpenStax Automation', 'openstax@restmail.net')
    send.send_mail(recipient, sender, TEST_EMAIL_SUBJECT, TEST_EMAIL_BODY)

    # WHEN: Access the rest API
    box = email.get_mail()

    # THEN: Able to retrieve a fake confirmation PIN
    assert(box), 'No emails recovered'
    assert(box[-1].has_pin), 'PIN not found'
