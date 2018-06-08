"""Profile page for logged in users."""
from time import sleep

from pypom import Region
from selenium.webdriver.common.by import By

from pages.accounts import admin, home


class Profile(home.Home):
    """Profile page."""

    URL_TEMPLATE = home.Home.URL_TEMPLATE + '/profile'

    _log_out_locator = (By.CLASS_NAME, 'sign-out')
    _edit_clear_locator = (By.CLASS_NAME, 'editable-clear-x')
    _edit_submit_locator = (By.CLASS_NAME, 'editable-submit')
    _edit_cancel_locator = (By.CLASS_NAME, 'editable-cancel')
    _username_exists_locator = (By.CSS_SELECTOR, '#profile .row')
    _popup_console_locator = (By.CSS_SELECTOR, '#upper-corner-console a')
    _full_console_locator = (By.CSS_SELECTOR,
                             '#upper-corner-console a:nth-last-child(2)')

    @property
    def name(self):
        """Name field."""
        return self.Name(self)

    @property
    def username(self):
        """Username field."""
        return self.Username(self)

    @property
    def emails(self):
        """Email fields."""
        return self.Emails(self)

    @property
    def login_method(self):
        """Options for logging in."""
        return self.LoginOptions(self)

    def log_out(self):
        """Log the user out."""
        self.find_element(*self._log_out_locator).click()
        sleep(1)
        return home.Home(self.driver)

    def open_popup_console(self):
        """Open the small admin console."""
        if not self.is_admin:
            raise AccountException('User is not an administrator')
        self.find_element(*self._popup_console_locator).click()
        return self.PopupConsole(self)

    def open_full_console(self):
        """Open the full admin console."""
        if not self.is_admin:
            raise AccountException('User is not an administrator')
        self.find_element(*self._full_console_locator).click()
        return admin.AccountsAdmin(self)

    @property
    def is_admin(self):
        """Return True if a user is an Accounts administrator."""
        return self.is_element_displayed(*self._popup_console_locator)

    @property
    def has_username(self):
        """Return True if a user has a username field.

        Length is 4 fields if the username is not set and 5 if it is.
        """
        return len(self.find_elements(*self._username_exists_locator)) >= 5

    class Name(Region):
        """Name assignment."""

        TITLE = 0
        FIRST = 1
        LAST = 2
        SUFFIX = 3

        _root_locator = (By.CSS_SELECTOR, '.row.name')
        _full_name_locator = (By.ID, 'name')
        _input_locator = (By.CLASS_NAME, 'form-control')
        _edit_clear_locator = (By.CLASS_NAME, 'editable-clear-x')
        _edit_submit_locator = (By.CLASS_NAME, 'editable-submit')
        _edit_cancel_locator = (By.CLASS_NAME, 'editable-cancel')

        def full_name(self):
            """Return the complete name."""
            return self.find_element(*self._full_name_locator).text

        def get_name_parts(self):
            """Return a list of the name fields."""
            full_name = self.selenium.execute_script(
                "return $('.row.name input').serializeArray()")
            parts = ['', '', '', '']
            for position, row in enumerate(full_name):
                parts[position] = row['value']
            return parts

        def open(self):
            """Open the name inputs."""
            self.find_element(*self._full_name_locator).click()
            self._parts = self.get_name_parts()
            return self

        def confirm(self):
            """Accept the current values."""
            self.find_element(*self._edit_submit_locator).click()
            sleep(0.25)
            return self

        def cancel(self):
            """Cancel any changes."""
            self.find_element(*self._edit_cancel_locator).click()
            sleep(0.25)
            return self

        def _set_field(self, locator, position, new_value):
            """Setter helper."""
            el = self.find_elements(*locator)[position]
            el.click()
            el.clear()
            el.send_keys(new_value)

        @property
        def title(self):
            """User title or prefix."""
            return self.get_name_parts()[self.TITLE]

        @title.setter
        def title(self, title):
            """Set a new title."""
            self._set_field(self._input_locator, self.TITLE, title)

        @property
        def first_name(self):
            """User first name."""
            return self.get_name_parts()[self.FIRST]

        @first_name.setter
        def first_name(self, name):
            """Set a new first name."""
            self._set_field(self._input_locator, self.FIRST, name)

        @property
        def last_name(self):
            """User surname."""
            return self.get_name_parts()[self.LAST]

        @last_name.setter
        def last_name(self, name):
            """Set a new last name."""
            self._set_field(self._input_locator, self.LAST, name)

        @property
        def suffix(self):
            """User suffix."""
            return self.get_name_parts()[self.SUFFIX]

        @suffix.setter
        def suffix(self, suffix):
            """Set a new suffix."""
            self._set_field(self._input_locator, self.SUFFIX, suffix)

    class Username(Region):
        """Username assignment."""

        _root_locator = (By.XPATH, '//div[div[contains(text(),"Username")]]')
        _username_locator = (By.CSS_SELECTOR, '#username')
        _input_locator = (By.XPATH, '//*[@id="profile"]/div/div[3]/div[2]/'
                                    'span/div/form/div/div[1]/div[1]/input')

        @property
        def username(self):
            """Username."""
            return self.find_element(*self._username_locator).text

        @username.setter
        def username(self, username):
            """Set a new username."""
            self.find_element(*self._username_locator).click()
            self.find_element(*Profile._edit_clear_locator).click()
            self.find_element(*self._input_locator).send_keys(username)
            self.find_element(*Profile._edit_submit_locator).click()
            return Profile(self.driver)

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

    class LoginOptions(Region):
        """Login options."""

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
