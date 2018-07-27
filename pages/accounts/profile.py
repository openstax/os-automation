"""Profile page for logged in users."""

from time import sleep

from pypom import Region
from selenium.webdriver.common.by import By

from pages.accounts.home import AccountsHome
from pages.utils.utilities import Utility


class Profile(AccountsHome):
    """Profile page."""

    URL_TEMPLATE = '/profile'

    _title_locator = (By.CLASS_NAME, 'title')
    _log_out_locator = (By.CLASS_NAME, 'sign-out')
    _edit_clear_locator = (By.CLASS_NAME, 'editable-clear-x')
    _edit_submit_locator = (By.CLASS_NAME, 'editable-submit')
    _edit_cancel_locator = (By.CLASS_NAME, 'editable-cancel')
    _username_exists_locator = (By.CSS_SELECTOR, '#profile .row')
    _popup_console_locator = (By.CSS_SELECTOR, '#upper-corner-console a')
    _popup_console_body_locator = (By.ID, 'admin_console_dialog')
    _full_console_locator = (By.CSS_SELECTOR,
                             '#upper-corner-console a:nth-last-child(2)')

    @property
    def title(self):
        """Page title."""
        return self.find_element(*self._title_locator).text

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
        return AccountsHome(self.driver)

    def open_popup_console(self):
        """Open the small admin console."""
        if not self.is_admin:
            raise AccountException('User is not an administrator')
        self.find_element(*self._popup_console_locator).click()
        sleep(0.25)
        return self.PopupConsole(self)

    def open_full_console(self):
        """Open the full admin console."""
        if not self.is_admin:
            raise AccountException('User is not an administrator')
        self.find_element(*self._full_console_locator).click()
        sleep(1)
        from pages.accounts.admin import AccountsAdmin
        return AccountsAdmin(self.driver)

    @property
    def is_popup_console_displayed(self):
        """Return True if the admin pop up console is open."""
        return self.is_element_displayed(*self._popup_console_body_locator)

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

        _full_name_locator = (By.ID, 'name')
        _input_locator = (By.CLASS_NAME, 'form-control')
        _edit_clear_locator = (By.CLASS_NAME, 'editable-clear-x')
        _edit_submit_locator = (By.CLASS_NAME, 'editable-submit')
        _edit_cancel_locator = (By.CLASS_NAME, 'editable-cancel')

        def __init__(self, x):
            """Add a username field."""
            self._name = []
            super().__init__(x)

        @property
        def full_name(self):
            """Return the complete name."""
            return self.find_element(*self._full_name_locator).text

        def get_name_parts(self):
            """Return a list of the name fields."""
            if self._name:
                return self._name
            self.open()
            full_name = self.selenium.execute_script(
                "return $('.row.name input').serializeArray()")
            self._name = ['', '', '', '']
            for position, row in enumerate(full_name):
                self._name[position] = row['value']
            self.cancel()
            return self._name

        def open(self):
            """Open the name inputs."""
            full_name = self.find_element(*self._full_name_locator)
            if 'editable-open' not in full_name.get_attribute('class'):
                full_name.click()
                sleep(0.25)
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
            if self._name:
                return self._name[self.TITLE]
            return self.get_name_parts()[self.TITLE]

        @title.setter
        def title(self, title):
            """Set a new title."""
            self._set_field(self._input_locator, self.TITLE, title)

        @property
        def first_name(self):
            """User first name."""
            if self._name:
                return self._name[self.FIRST]
            return self.get_name_parts()[self.FIRST]

        @first_name.setter
        def first_name(self, name):
            """Set a new first name."""
            self._set_field(self._input_locator, self.FIRST, name)

        @property
        def last_name(self):
            """User surname."""
            if self._name:
                return self._name[self.LAST]
            return self.get_name_parts()[self.LAST]

        @last_name.setter
        def last_name(self, name):
            """Set a new last name."""
            self._set_field(self._input_locator, self.LAST, name)

        @property
        def suffix(self):
            """User suffix."""
            if self._name:
                return self._name[self.SUFFIX]
            return self.get_name_parts()[self.SUFFIX]

        @suffix.setter
        def suffix(self, suffix):
            """Set a new suffix."""
            self._set_field(self._input_locator, self.SUFFIX, suffix)

    class Username(Region):
        """Username assignment."""

        _root_locator = (By.XPATH, '//div[div[contains(text(),"Username")]]')
        _username_locator = (By.CSS_SELECTOR, '#username')
        _input_locator = (By.CSS_SELECTOR, "#username + span input")

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
            sleep(0.25)
            return Profile(self.driver)

    class Emails(Region):
        """Email sections."""

        _root_locator = (By.XPATH, '//div[div[contains(text(),"Emails")]]')
        _email_locator = (By.CSS_SELECTOR, '.info > .email-entry')
        _add_locator = (By.ID, 'add-an-email')
        _text_locator = (By.CLASS_NAME, 'input-sm')
        _unverified_locator = (By.CLASS_NAME, 'unconfirmed-warning')
        _add_email_locator = (By.ID, 'add-an-email')
        _email_form_locator = (By.CSS_SELECTOR, '.editable-input input')
        _email_submit_locator = (
            By.CSS_SELECTOR, '.editable-input + div > button')

        @property
        def emails(self):
            """Return a list of e-mail objects."""
            return [self.Email(self, element)
                    for element in self.find_elements(*self._email_locator)]

        def add_email(self, email):
            """Add a email to the account's email list."""
            sleep(0.1)
            self.find_element(*self._add_email_locator).click()
            sleep(0.1)
            self.find_element(*self._email_form_locator).send_keys(email)
            self.find_element(*self._email_submit_locator).click()
            sleep(0.1)
            self.driver.refresh()
            return Profile(self.driver)

        class Email(Region):
            """Individual email section."""

            _email_locator = (By.CLASS_NAME, 'value')
            _unverified_locator = (By.CLASS_NAME, 'unconfirmed-warning')
            _delete_locator = (By.CSS_SELECTOR, '.glyphicon-trash + a')
            _ok_locator = (By.CSS_SELECTOR, '.btn-danger')
            _specific_locator = (By.CSS_SELECTOR, '.editable-click  .value')
            _unverified_btn_locator = (
                By.CSS_SELECTOR, '.unconfirmed-warning > *')
            _confirmation_btn_locator = (
                By.CSS_SELECTOR, '.button_to>[type="submit"]')

            def delete(self):
                """Delete an individual email section."""
                self.find_element(*self._specific_locator).click()
                sleep(0.25)
                self.find_element(*self._delete_locator).click()
                sleep(0.5)
                self.find_element(*self._ok_locator).click()
                sleep(0.25)
                return Profile(self.driver)

            def resend_confirmation(self):
                """Resend confirmation email for a certain email."""
                self.find_element(*self._unverified_btn_locator).click()
                sleep(0.1)
                self.find_element(*self._confirmation_btn_locator).click()
                return Profile(self.driver)

            @property
            def is_confirmed(self):
                """Check if the email is already verified."""
                return 'verified' in self._root.get_attribute('class')

    class LoginOptions(Region):
        """Login options."""

        _active_option_locator = (
            By.CSS_SELECTOR, '.enabled-providers .authentication')
        _inactive_option_locator = (
            By.CSS_SELECTOR, '.other-sign-in .authentication')
        _inactive_option_expander_locator = (By.ID, 'enable-other-sign-in')

        def get_active_options(self):
            """Return current, active log in options."""
            return [self.Option(self, el) for el in
                    self.find_elements(*self._active_option_locator)]

        def get_other_options(self):
            """Return inactive log in options."""
            return [self.Option(self, el) for el in
                    self.find_elements(*self._inactive_option_locator)]

        def view_other_options(self):
            """Open the inactive option menu."""
            link = self.find_element(*self._inactive_option_expander_locator)
            link.click()
            sleep(0.25)
            #if link.is_displayed():
            #    link.click()
            #    sleep(0.25)
            return self

        def add_password(self, password):
            for options in self.view_other_options().get_other_options():
                if options.name == 'Password':
                    options.add
                    self.SetPassword(self).set_password(password)

        class SetPassword(Region):
            """The page for adding password."""

            _password_locator = (By.ID, 'set_password_password')
            _confirm_locator = (By.ID, 'set_password_password_confirmation')
            _submit_locator = (By.CSS_SELECTOR, '[type=submit]')
            _cancel_locator = (By.PARTIAL_LINK_TEXT, 'Cancel')
            _continue_locator = (By.CSS_SELECTOR, '[type=submit]')

            def set_password(self, password):
                self.find_element(*self._password_locator).send_keys(password)
                self.find_element(*self._confirm_locator).send_keys(password)
                self.find_element(*self._submit_locator).click()
                sleep(0.5)
                self.find_element(*self._continue_locator).click()
                sleep(0.5)
                return Profile(self.driver)

        class Option(Region):
            """Login options."""

            _name_locator = (By.CLASS_NAME, 'name')
            _edit_button_locator = (By.CLASS_NAME, 'edit')
            _delete_button_locator = (By.CLASS_NAME, 'delete')
            _add_button_locator = (By.CLASS_NAME, 'add')
            _ok_locator = (By.CSS_SELECTOR, '.btn-danger')

            @property
            def name(self):
                """Return the option name."""
                return self.find_element(*self._name_locator).text

            @property
            def edit(self):
                """Edit the login option."""
                self.find_element(*self._edit_button_locator).click()
                sleep(0.5)
                return self

            @property
            def delete(self):
                """Delete an active login option."""
                self.find_element(*self._delete_button_locator).click()
                sleep(0.5)
                self.find_element(*self._ok_locator).click()
                return self

            @property
            def add(self):
                """Add an inactive login option."""
                self.find_element(*self._add_button_locator).click()
                sleep(0.5)
                return self

    class PopupConsole(Region):
        """Popup console interaction."""

        _users_locator = (By.LINK_TEXT, 'Users')
        _misc_locator = (By.LINK_TEXT, 'Misc')
        _links_locator = (By.LINK_TEXT, 'Links')
        _full_console_locator = (By.LINK_TEXT, 'Full Console >>')

        @property
        def misc(self):
            """Goes to misc tab of the pop up console."""
            self.find_element(*self._misc_locator).click()
            return self.Misc(self)

        @property
        def users(self):
            """Goes to user tab of the pop up console."""
            self.find_element(*self._users_locator).click()
            return self.Users(self)

        @property
        def links(self):
            """Goes to links tab of the pop up console."""
            self.find_element(*self._links_locator).click()
            return self.Links(self)

        def full_console(self):
            """Goes to full_console tab of the pop up console."""
            self.find_element(*self._full_console_locator).click()
            return self

        class Misc(Region):
            """Misc section."""

            _users_locator = (By.LINK_TEXT, 'Users')
            _links_locator = (By.LINK_TEXT, 'Links')
            _full_console_locator = (By.LINK_TEXT, 'Full Console >>')

            def go_to_user_section(self):
                """Go to user section on the tab."""
                self.find_element(*self._users_locator).click()
                return self

            def go_to_links_section(self):
                """Go to links section on the tab."""
                self.find_element(*self._links_locator).click()
                return self

            def go_to_full_section(self):
                """Go to full section on the tab."""
                self.find_element(*self._full_console_locator).click()
                return self

        class Users(Region):
            """User section."""

            _search_bar_locator = (By.ID, 'search_terms')
            _search_button_locator = (By.NAME, 'commit')
            _row_locator = (By.CSS_SELECTOR, "tr.action-list-data-row")

            def search_for(self, topic):
                """Search given string."""
                self.find_element(*self._search_bar_locator).send_keys(
                    topic)
                self.find_element(*self._search_button_locator).click()
                sleep(1)
                return [self.Result(self, el)
                        for el in self.find_elements(*self._row_locator)]

            class Result(Region):
                """class for the search list column."""

                _data_locator = (By.CSS_SELECTOR, ".action-list-col-6")
                _id_locator = \
                    (By.CSS_SELECTOR, '.action-list-col-6:nth-child(1)')
                _username_locator = (By.CSS_SELECTOR, '.action-list-col-6 a')
                _first_name_locator = \
                    (By.CSS_SELECTOR, '.action-list-col-6:nth-child(3)')
                _last_name_locator = \
                    (By.CSS_SELECTOR, '.action-list-col-6:nth-child(4)')
                _is_admin = \
                    (By.CSS_SELECTOR, '.action-list-col-6:nth-child(5)')
                _is_test = (By.CSS_SELECTOR, '.action-list-col-6:nth-child(6)')
                _sign_in_locator = (By.LINK_TEXT, 'Sign in as')
                _edit_locator = (By.LINK_TEXT, 'Edit')

                def find_data(self):
                    """Return all the data by columns."""
                    return self.find_elements(*self._data_locator)

                @property
                def id(self):
                    """Return the user id."""
                    return self.find_element(*self._id_locator).text

                @property
                def username(self):
                    """Return the username."""
                    return self.find_element(*self._username_locator).text

                @property
                def username_link(self):
                    """Return the username specific link."""
                    self.find_element(*self._username_locator).click()
                    return self

                @property
                def first_name(self):
                    """Return the frist name."""
                    return self.find_element(*self._first_name_locator).text

                @property
                def last_name(self):
                    """Return the last name."""
                    return self.find_element(*self._last_name_locator).text

                @property
                def is_admin(self):
                    """Return the admin."""
                    return self.find_element(
                        *self._is_admin).text.lower() == 'yes'

                @property
                def is_test(self):
                    """Return the test."""
                    return self.find_element(
                        *self._is_test).text.lower() == "yes"

                def sign_in_as(self):
                    """Return the sign in page."""
                    self.find_element(*self._sign_in_locator).click()

                    if "terms" in self.driver.current_url:
                        checkbox_id = 'agreement_i_agree'
                        target = self.find(By.ID, checkbox_id)
                        target.click()
                        target = self.find(By.ID, 'agreement_submit')
                        target.click()
                    return self

                def edit(self):
                    """Return the edit page."""
                    Utility.switch_to(self.driver, self._edit_locator)
                    return self

        class Links(Region):
            """Link section."""

            _security_log_locator = (By.PARTIAL_LINK_TEXT, 'Security')
            _application_locator = (By.PARTIAL_LINK_TEXT, 'OAuth')
            _print_locator = (By.PARTIAL_LINK_TEXT, 'FinePrint')
            _api_locator = (By.PARTIAL_LINK_TEXT, 'API')

            def go_to_security_log(self):
                """Goes to the security log."""
                self.find_element(*self._security_log_locator).click()
                return self

            def go_to_oauth_application(self):
                """Goes to the OAuth application."""
                self.find_element(*self._application_locator).click()
                return self

            def go_to_fineprint(self):
                """Goes to the FinePrint."""
                self.find_element(*self._print_locator).click()
                return self

            def go_to_api(self):
                """Goes to the API v1 documentation."""
                self.find_element(*self._api_locator).click()
                return self


class AccountException(Exception):
    """Account exception."""

    pass
