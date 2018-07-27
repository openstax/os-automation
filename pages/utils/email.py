"""Email providers."""

import re
import smtplib
from contextlib import contextmanager
from email.mime.text import MIMEText
from email.utils import formataddr as format_address
from time import sleep

import requests
from pypom import Page, Region
from selenium.webdriver.common.by import By

from pages.utils.utilities import Utility

PIN_MATCHER = re.compile(r'(PIN\:? \d{6})')
URL_MATCHER = re.compile(
    r'(https:\/\/accounts([-\w]*)?\.openstax\.org\/confirm\?code=\w{1,64})'
)


class GoogleBase(Page):
    """Use Gmail."""

    URL_TEMPLATE = (
        'https://accounts.google.com/AccountChooser?service=mail&continue='
        'https://mail.google.com/mail/')

    def wait_for_page_to_load(self):
        """Override page load."""
        sleep(1)
        self.wait.until(
            lambda _: self.find_element(By.TAG_NAME, 'body').is_displayed())

    def log_in(self, username, password):
        """Log into google account."""
        sleep(1)
        if 'google' in self.driver.current_url:
            return self.login.go(username, password)
        else:
            return Google(self.driver)

    @property
    def login(self):
        """Return the Login control."""
        return self.Login(self)

    class Login(Region):
        """Gmail login."""

        _root_locator = (By.ID, 'view_container')
        _email_locator = (By.CSS_SELECTOR, '[type=email]')
        _email_next_locator = (By.ID, 'identifierNext')
        _password_locator = (By.CSS_SELECTOR, '[type=password]')
        _password_next_locator = (By.ID, 'passwordNext')

        def go(self, email, password):
            """Log into Google."""
            self.find_element(*self._email_locator).click()
            sleep(0.3)
            self.find_element(*self._email_locator).send_keys(email)
            sleep(0.3)
            self.find_element(*self._email_next_locator).click()
            sleep(2)
            self.find_element(*self._password_locator).click()
            sleep(0.3)
            self.find_element(*self._password_locator).send_keys(password)
            sleep(0.5)
            self.find_element(*self._password_next_locator).click()
            # self.wait.until(
            #    expect.visibility_of_element_located(
            #        self._email_locator)) \
            #    .send_keys(email)
            # self.find_element(*self._email_next_locator).click()
            # self.wait.until(
            #    expect.visibility_of_element_located(
            #        self._password_locator)) \
            #    .send_keys(password)
            # self.find_element(*self._password_next_locator).click()
            return Google(self.driver)


class Google(GoogleBase):
    """Logged in e-mail interaction."""

    URL_TEMPLATE = 'https://mail.google.com/mail/u/0/#inbox'

    _root_locator = (By.CSS_SELECTOR, '.bkL .F')
    _email_row_locator = (By.CSS_SELECTOR, '.bkL .F tr')

    def wait_for_page_to_load(self):
        """Override page load."""
        sleep(3)
        # self.wait.until(
        #    lambda _: self.find_element(*self._root_locator).is_displayed())

    @property
    def emails(self):
        """Return the first page of e-mail results."""
        self.wait_for_page_to_load()
        return [self.Email(self, el)
                for el in self.find_elements(*self._email_row_locator)]

    class Email(Region):
        """Email container."""

        _from_locator = (By.CSS_SELECTOR, '.yW span[email]')
        _subject_locator = (By.CLASS_NAME, 'bog')
        _excerpt_locator = (By.CSS_SELECTOR, '.y6 .y2')

        @property
        def sender(self):
            """Return the e-mail sender."""
            return self.find_element(*self._from_locator) \
                .get_attribute('email')

        @property
        def subject(self):
            """Return the e-mail subject."""
            return self.find_element(*self._subject_locator).text

        @property
        def excerpt(self):
            """Return the e-mail body excerpt."""
            return self.find_element(*self._excerpt_locator).text

        @property
        def has_pin(self):
            """Return True if a pin string is in the body excerpt."""
            return PIN_MATCHER.search(self.excerpt)

        @property
        def get_pin(self):
            """Return the numeric pin."""
            if self.has_pin:
                return (PIN_MATCHER.search(self.excerpt).group())[-6:]
            raise EmailVerificationError('No pin found')


class GuerrillaMail(Page):
    """Use Guerrilla short term mail."""

    URL_TEMPLATE = 'https://www.guerrillamail.com/'

    _root_locator = (By.ID, 'guerrilla_mail')
    _mail_locator = (By.CLASS_NAME, 'mail_row')
    _compose_locator = (By.CSS_SELECTOR, '[title=Compose]')

    def wait_for_page_to_load(self):
        """Override page load."""
        self.wait.until(
            lambda _: self.find_element(*self._root_locator).is_displayed())

    def wait_for_email(self):
        """Wait for more than one email in inbox."""
        n = len(self.emails)
        self.wait.until(lambda _: len(self.emails) > n)

    @property
    def header(self):
        """Return the e-mail control panel."""
        return self.Header(self)

    @property
    def emails(self):
        """Return the e-mail inbox."""
        return [self.Emails(self, el)
                for el in self.find_elements(*self._mail_locator)]

    @property
    def compose(self):
        """Return a composition page."""
        self.find_element(*self._compose_locator).click()
        return Compose(self.driver)

    @property
    def openedmail(self):
        """Return a opened email region."""
        return self.OpenedMail(self)

    class Header(Region):
        """E-mail address controls."""

        _root_locator = (By.CLASS_NAME, 'show_address')
        _address_id_locator = (By.ID, 'inbox-id')
        _address_id_edit_locator = (By.CSS_SELECTOR, '#inbox-id [type]')
        _save_button_locator = (By.CSS_SELECTOR, '.save.button')
        _cancel_button_locator = (By.ID, 'edit-cancel')
        _address_stem_locator = (By.ID, 'gm-host-select')
        _forget_address_locator = (By.ID, 'forget_button')
        _email_locator = (By.ID, 'email-widget')
        _scramble_address_locator = (By.ID, 'use-alias')

        @property
        def is_header_displayed(self):
            """Header is displayed."""
            return self.loaded

        @property
        def is_scrambled(self):
            """Return True if the e-mail ID is scrambled."""
            return self.find_element(*self._scramble_address_locator) \
                .is_selected()

        def scramble(self):
            """Toggle between scrambled and unscrambled IDs."""
            self.find_element(*self._scramble_address_locator).click()
            return self

        @property
        def email(self):
            """Return the current e-mail."""
            return self.find_element(*self._email_locator).text

        @email.setter
        def email(self, new_id):
            """Change the email ID."""
            self.find_element(*self._address_id_locator).click()
            self.find_element(*self._address_id_edit_locator).clear()
            self.find_element(*self._address_id_edit_locator).send_keys(new_id)
            self.find_element(*self._save_button_locator).click()
            sleep(0.5)
            return self

        @property
        def host(self):
            """Host name suffix."""
            return Utility.selected_option(
                self.selenium,
                self._address_stem_locator)

        @host.setter
        def host(self, host_name):
            """Set a new host name."""
            Utility.select(self.selenium,
                           self._address_stem_locator,
                           host_name)
            return self

        def forget_address(self):
            """Purge the current e-mail."""
            self.find_element(*self._forget_address_locator).click()
            sleep(1.0)
            return self

    class Emails(Region):
        """E-mail inbox."""

        _subject_locator = (By.CLASS_NAME, 'td3')
        _excerpt_locator = (By.CLASS_NAME, 'email-excerpt')
        _emails_locator = (By.CSS_SELECTOR, 'tbody > tr')

        @property
        def subject(self):
            """Message subject."""
            return self.find_element(*self._subject_locator).text

        @property
        def excerpt(self):
            """Body excerpt."""
            return self.find_element(*self._excerpt_locator).text

        @property
        def has_pin(self):
            """Return True if a pin string is in the body excerpt."""
            return PIN_MATCHER.search(self.excerpt)

        @property
        def get_pin(self):
            """Return the numeric pin."""
            if self.has_pin:
                return (PIN_MATCHER.search(self.excerpt).group())[-6:]
            raise EmailVerificationError('No pin found')

        def open_email(self):
            """Open this email."""
            Utility.scroll_to(self.driver, self._subject_locator)
            sleep(4)
            self.find_element(*self._subject_locator).click()
            sleep(0.5)
            self.driver.refresh()

    class OpenedMail(Region):
        """The email page after it's opened."""

        _confirmation_link_locator = (By.CSS_SELECTOR, '.email_body a')

        def confirm_email(self):
            """Clicks the openstax email confirmation link."""
            Utility.switch_to(self.driver, self._confirmation_link_locator)


class Compose(GuerrillaMail):
    """Compose an e-mail."""

    URL_TEMPLATE = '/compose'

    _root_locator = (By.ID, 'send-form')
    _to_field_locator = (By.CSS_SELECTOR, '[name=to]')
    _subject_field_locator = (By.CSS_SELECTOR, '[name=subject]')
    _body_field_locator = (By.CSS_SELECTOR, '[name=body]')
    _send_button_locator = (By.ID, 'send-button')

    def wait_for_page_to_load(self):
        """Override page loading."""
        self.wait.until(
            lambda _: self.find_element(*self._root_locator).is_displayed())

    def send_message(self, to, subject, body):
        """Send an e-mail message from Guerrilla."""
        self.wait_for_page_to_load()
        sleep(0.5)
        to_box = self.find_element(*self._to_field_locator)
        to_box.click()
        to_box.clear()
        to_box.send_keys(to)
        subject_box = self.find_element(*self._subject_field_locator)
        subject_box.click()
        subject_box.clear()
        subject_box.send_keys(subject)
        body_box = self.find_element(*self._body_field_locator)
        body_box.click()
        body_box.clear()
        body_box.send_keys(body)
        self.find_element(*self._send_button_locator).click()
        sleep(1.0)
        return GuerrillaMail(self.selenium)


class RestMail(object):
    """RestMail API for non-interactive e-mail testing."""

    MAIL_URL = 'http://restmail.net/mail/{username}'

    def __init__(self, username):
        """Initialize a mailbox."""
        self._inbox = []
        self.username = username

    @property
    def inbox(self):
        """Return the e-mail messages."""
        return self._inbox

    def get_mail(self):
        """Get email for a dynamic user."""
        messages = requests.get(self.MAIL_URL.format(username=self.username))
        self._inbox = [self.Email(message) for message in messages.json()]
        return self._inbox

    def wait_for_mail(self):
        """Sleep for 5 seconds."""
        sleep(2.0)
        return self.get_mail()

    @property
    def size(self):
        """Return the number of messages in the inbox."""
        return self._inbox.__len__

    def empty(self):
        """Delete all message in the inbox."""
        requests.delete(self.MAIL_URL.format(username=self.username))

    class Email(object):
        """E-mail message structure."""

        def __init__(self, package):
            """Read possible RestMail fields."""
            self._html = self._pull_data('html', package, '')
            self._text = self._pull_data('text', package, '')
            self._headers = self._pull_data('headers', package, {})
            self._subject = self._pull_data('subject', package, '')
            self._references = self._pull_data('references', package, [])
            self._id = self._pull_data('messageId', package, '')
            self._reply = self._pull_data('inReplyTo', package, [])
            self._priority = self._pull_data('priority', package, '')
            self._from = self._pull_data('from', package, [])
            self._to = self._pull_data('to', package, [])
            self._date = self._pull_data('date', package, '')
            self._received = self._pull_data('receivedDate', package, '')
            self._received_at = self._pull_data('receivedAt', package, '')
            self._excerpt = (
                self._text if self._text else (
                    self._subject
                )
            )

        def _pull_data(self, field, package, default):
            """Pull data from the JSON package."""
            return package[field] if field in package else default

        @property
        def html(self):
            """Return the HTML formatted message body."""
            return self._html

        @property
        def text(self):
            """Return the unformatted message body."""
            return self._text

        @property
        def excerpt(self):
            """Return an excerpt from the HTML, text, or subject fields."""
            return self._excerpt

        @property
        def headers(self):
            """Return a dict of email headers."""
            return self._headers

        @property
        def subject(self):
            """Return the message subject."""
            return self._subject

        @property
        def id(self):
            """Return the message ID."""
            return self._id

        @property
        def priority(self):
            """Return the message priority."""
            return self._priority

        @property
        def sender(self):
            """Return the sender."""
            return self._from

        @property
        def recipients(self):
            """Return the list of recipients."""
            return self._to

        @property
        def date(self):
            """Return the UTC message date and time."""
            return self._date

        @property
        def received_on(self):
            """Return the message receive date."""
            return self._received

        @property
        def received_at(self):
            """Return the message receive time."""
            return self._received_at

        @property
        def has_pin(self):
            """Return True if a pin string is in the body excerpt."""
            return bool(PIN_MATCHER.search(self._excerpt))

        @property
        def pin(self):
            """Return the numeric pin."""
            if self.has_pin:
                return (PIN_MATCHER.search(self._excerpt).group())[-6:]
            raise EmailVerificationError('No pin found')

        @property
        def has_link(self):
            """Return True if a confirmation URL is in the excerpt."""
            return bool(URL_MATCHER.search(self._excerpt))

        @property
        def confirmation_link(self):
            """Access the confirmation URL link."""
            if self.has_link:
                return URL_MATCHER.search(self._excerpt).group()
            raise EmailVerificationError('No confirmation link found')

        def confirm_email(self, driver):
            """Access the confirmation link."""
            send = requests.get(self.confirmation_link)
            if not send.status_code == requests.codes.ok:
                raise EmailVerificationError('Email not confirmed. ({code})'
                                             .format(code=send.status_code))
            driver.refresh()


class SendMail(object):
    """Send an email through Gmail."""

    def __init__(self, username, password, host, port, timeout=10):
        """Initialize an email sender."""
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.timeout = timeout

    @contextmanager
    def _sender(self):
        """Start a relay for Gmail."""
        smtp_server = smtplib.SMTP(self.host, self.port, self.timeout)
        smtp_server.set_debuglevel(True)
        try:
            smtp_server.ehlo_or_helo_if_needed()
            smtp_server.starttls()
            smtp_server.ehlo(name='automated-qa.openstax.org')
            smtp_server.login(self.username, self.password)
            yield smtp_server
        finally:
            smtp_server.quit()
        sleep(3.0)

    def send_mail(self, recipients, sender, subject, message):
        """Send an email through Gmail."""
        with self._sender() as smtp:
            msg = MIMEText(message)
            msg['From'] = format_address(sender)
            msg['To'] = format_address(recipients)
            msg['Subject'] = subject
            smtp.send_message(msg=msg)


class EmailVerificationError(Exception):
    """General e-mail registration exception."""

    pass
