"""Email providers."""
import re
from time import sleep

from pypom import Page, Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect

from pages.utils.utilities import Utility

MATCHER = re.compile(r'(PIN\:? \d{6})')


class GoogleBase(Page):
    """Use Gmail."""

    URL_TEMPLATE = (
        'https://accounts.google.com/AccountChooser?service=mail&continue='
        'https://mail.google.com/mail/')

    def wait_for_page_to_load(self):
        """Override page load."""
        self.wait.until(
            lambda _: self.find_element(By.TAG_NAME, 'body').is_displayed())
        sleep(1)

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
            self.wait.until(
                expect.visibility_of_element_located(
                    self._email_locator)) \
                .send_keys(email)
            self.find_element(*self._email_next_locator).click()
            self.wait.until(
                expect.visibility_of_element_located(
                    self._password_locator)) \
                .send_keys(password)
            self.find_element(*self._password_next_locator).click()
            return Google(self.driver)


class Google(GoogleBase):
    """Logged in e-mail interaction."""

    URL_TEMPLATE = 'https://mail.google.com/mail/u/0/#inbox'

    _root_locator = (By.CSS_SELECTOR, '.bkL .F')
    _email_row_locator = (By.CSS_SELECTOR, '.bkL .F tr')

    def wait_for_page_to_load(self):
        """Override page load."""
        self.wait.until(
            lambda _: self.find_element(*self._root_locator).is_displayed())

    @property
    def emails(self):
        """Return the first page of e-mail results."""
        self.wait_for_page_to_load()
        return [self.Email(self, el)
                for el in self.find_elements(*self._email_row_locator)]

    class Email(Region):
        """Email container."""

        _from_locator = (By.CSS_SELECTOR, '.yW .yP')
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
            return MATCHER.search(self.excerpt)

        @property
        def get_pin(self):
            """Return the numeric pin."""
            if self.has_pin:
                return (MATCHER.search(self.excerpt).group())[-6:]
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
        return Compose(self.selenium)

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
            return MATCHER.search(self.excerpt)

        @property
        def get_pin(self):
            """Return the numeric pin."""
            if self.has_pin:
                return (MATCHER.search(self.excerpt).group())[-6:]
            raise EmailVerificationError('No pin found')


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


class EmailVerificationError(Exception):
    """General e-mail registration exception."""

    pass
