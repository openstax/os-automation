"""Profile page for logged in users."""
from pypom import Region
from selenium.webdriver.common.by import By

from pages.accounts.home import Home


class Profile(Home):
    """Profile page."""

    URL_TEMPLATE = '/profile'

    _log_out_locator = (By.CLASS_NAME, 'sign-out')
    _edit_clear_locator = (By.CLASS_NAME, 'editable-clear-x')
    _edit_submit_locator = (By.CLASS_NAME, 'editable-submit')
    _edit_cancel_locator = (By.CLASS_NAME, 'editable-cancel')
    _username_exists_locator = (By.CSS_SELECTOR, '#profile .row')
    _console_locator = (By.CSS_SELECTOR, '#upper-corner-console a')

    @property
    def name(self):
        """Name field."""
        return self.Name(self)

    @property
    def username(self):
        """Username field."""
        return self.User(self)

    @property
    def emails(self):
        """Email fields."""
        return self.Email(self)

    @property
    def login_method(self):
        """Options for logging in."""
        return self.LoginOption(self)

    def log_out(self):
        """Log the user out."""
        self.find_element(*self._log_out_locator).click()
        return Home(self.driver)

    def open_popup_console(self):
        """Open the small admin console."""
        if not self.is_admin:
            raise AccountException('User is not an administrator')
        self.find_element(*self._console_locator).click()
        return self.PopupConcole(self)

    @property
    def is_admin(self):
        """Return True if a user is an Accounts administrator."""
        return self.is_element_displayed(*self._console_locator)

    @property
    def has_username(self):
        """Return True if a user has a username field.

        Length is 4 fields if the username is not set and 5 if it is.
        """
        return len(self.find_elements(*self._username_exists_locator)) >= 5

    class Name(Region):
        """Name assignment."""

        _root_locator = (By.ID, 'name')
        _title_locator = (By.CSS_SELECTOR, '[placeholder=Title]')
        _first_name_locator = (By.CSS_SELECTOR, '[placeholder="First name"]')
        _last_name_locator = (By.CSS_SELECTOR, '[placeholder="Last name"]')
        _suffix_locator = (By.CSS_SELECTOR, '[placeholder=Suffix]')

        def _replace_value(self, field, new_value):
            """Single value replacement."""
            self.find_element(*field).clear().send_keys(new_value)
            self.find_element(*Profile._edit_submit_locator).click()
            return Profile(self)

        @property
        def title(self):
            """User title or prefix."""
            return self.find_element(*self._title_locator).text

        @title.setter
        def title(self, title):
            """Set a new title."""
            return self._replace_value(self._title_locator, title)

        @property
        def first_name(self):
            """User first name."""
            return self.find_element(*self._first_name_locator).text

        @first_name.setter
        def first_name(self, name):
            """Set a new first name."""
            return self._replace_value(self._first_name_locator, name)

        @property
        def last_name(self):
            """User surname."""
            return self.find_element(*self._last_name_locator).text

        @last_name.setter
        def last_name(self, name):
            """Set a new last name."""
            return self._replace_value(self._last_name_locator, name)

        @property
        def suffix(self):
            """User suffix."""
            return self.find_element(*self._suffix_locator).text

        @suffix.setter
        def suffix(self, suffix):
            """Set a new suffix."""
            return self._replace_value(self._suffix_locator, suffix)

    class Username(Region):
        """Username assignment."""

        _root_locator = (By.XPATH, '//div[div[contains(text(),"Username")]]')
        _username_locator = (By.CSS_SELECTOR, '#username + span input')

        @property
        def username(self):
            """Username."""
            return self.find_element(*self._username_locator).text

        @username.setter
        def username(self, username):
            """Set a new username."""
            self.find_element(*Profile._edit_clear_locator).click()
            self.find_element(*self._username_locator).send_keys(username)
            self.find_element(*Profile._edit_submit_locator)
            return Profile(self)

    class Emails(Region):
        """Email sections."""

        _root_locator = (By.XPATH, '//div[div[contains(text(),"Emails")]]')
        _email_locator = (By.CSS_SELECTOR, '.info > .email-entry')

        @property
        def emails(self):
            """Return a list of e-mail objects."""
            return [self.Email(self, element)
                    for element in self.find_elements(*self._email_locator)]

        class Email(Region):
            """Individual email section."""

            _email_locator = (By.CLASS_NAME, 'value')
            _unverified_locator = (By.CLASS_NAME, 'unconfirmed-warning')

    class ActiveOption(Region):
        """Login options."""

        _root_locator = (By.CSS_SELECTOR, '.enabled-providers')

    class InactiveOption(Region):
        """Additional login options requiring setup."""

        _root_locator = (By.CSS_SELECTOR, '.other-sign-in')

    class PopupConsole(Region):
        """Popup console interaction."""

        _root_locator = (By.CSS_SELECTOR, '.modal-content')


class AccountException(Exception):
    """Account exception."""

    pass
