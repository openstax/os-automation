"""Home page objects."""

from time import sleep

from pypom import Region
from selenium.common.exceptions import (ElementNotInteractableException,  # NOQA
                                        TimeoutException,  # NOQA
                                        WebDriverException)  # NOQA
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect

from pages.accounts.base import AccountsBase
from pages.salesforce.home import Salesforce
from utils.utilities import Utility, go_to_


class AccountsHome(AccountsBase):
    """Home page base."""

    URL_TEMPLATE = ''

    @property
    def login(self):
        """Return the login pane."""
        return self.Login(self)

    def log_in(self, user, password):
        """Log into the site with a specific user."""
        return self.login.login(user, password)

    def service_log_in(self, user, password,
                       destination=None, url=None, **kwargs):
        """Log into the site with a specific user from another service."""
        return (self.Login(self)
                .service_login(user, password, destination, url, **kwargs))

    @property
    def logged_in(self):
        """Return user log in status."""
        return self.Login(self).logged_in

    @property
    def location(self):
        """Return the current URL."""
        return self.driver.current_url

    class Login(Region):
        """User login pane."""

        _user_field_locator = (By.ID, 'login_username_or_email')
        _password_field_locator = (By.ID, 'login_password')
        _login_submit_button_locator = (By.CSS_SELECTOR, '[type=submit]')
        _trouble_locator = (By.CSS_SELECTOR, '.trouble')
        _login_help_locator = (By.CSS_SELECTOR, '.login-help')
        _salesforce_link_locator = (By.CSS_SELECTOR, '.login-help a')
        _salesforce_loader = (By.CSS_SELECTOR, 'div.body-and-support-buttons')
        _input_field_locator = (By.CLASS_NAME, 'form-group')
        _form_box_locator = (By.TAG_NAME, 'input')
        _error_locator = (By.CSS_SELECTOR, '.alert')
        _signup_locator = (By.CSS_SELECTOR, '.extra-info a')
        _terms_agreement = (By.CSS_SELECTOR, '#agreement_i_agree')

        _password_reset_locator = (By.CSS_SELECTOR, '.footer a')
        _password_reset_fields_locator = (By.CSS_SELECTOR, '[type=password]')
        _password_reset_submit = (By.CSS_SELECTOR, '.footer input')

        _fb_locator = (By.ID, 'facebook-login-button')
        _fb_email_field_locator = (By.ID, 'email')
        _fb_password_field_locator = (By.ID, 'pass')
        _fb_submit_locator = (By.ID, 'loginbutton')
        _fb_safari_specific_locator = (By.NAME, '__CONFIRM__')

        _google_locator = (By.ID, 'google-login-button')
        _google_user_locator = (By.CSS_SELECTOR, '[type=email]')
        _google_user_next_locator = (By.ID, 'identifierNext')
        _google_password_locator = (By.CSS_SELECTOR, '[type=password]')
        _google_pass_next_locator = (By.ID, 'passwordNext')

        @property
        def logged_in(self):
            """Return True if a user is logged in."""
            return 'profile' in self.driver.current_url

        @property
        def user(self):
            """Return the user field."""
            return self.wait.until(
                expect.presence_of_element_located(self._user_field_locator))

        @user.setter
        def user(self, login):
            """Send the login email or username."""
            self.user.send_keys(login)
            return self

        def next(self):
            """Click the NEXT button."""
            next_button = self.find_element(*self._login_submit_button_locator)
            Utility.click_option(self.driver, element=next_button)
            sleep(0.5)
            return self

        def reset(self):
            """Click the reset password link."""
            reset_button = self.find_element(*self._password_reset_locator)
            Utility.click_option(self.driver, element=reset_button)
            sleep(0.5)
            return self

        @property
        def password(self):
            """Return the password field."""
            return self.find_element(*self._password_field_locator)

        @password.setter
        def password(self, password):
            """Send the password."""
            self.password.send_keys(password)
            return self

        @property
        def agreement_checkbox(self):
            """Return the terms of use agreement checkbox."""
            return self.find_element(*self._terms_agreement)

        def login(self, user, password):
            """Log into Accounts with a specific user."""
            self.service_login(user, password)
            try:
                self.wait.until(lambda _: self.logged_in)
            except TimeoutException:
                pass
            from pages.accounts.profile import Profile
            return go_to_(Profile(self.driver, self.page.base_url))

        def service_login(self, user, password,
                          destination=None, url=None, **kwargs):
            """Log into the site with a specific user from another service."""
            self.user = user
            self.next()
            if self.page.is_safari:
                sleep(1)
            assert(not self.get_login_error()), 'Username failed'
            self.password = password
            self.next()
            if self.page.is_safari:
                sleep(1)
            assert(not self.get_login_error()), 'Password failed'
            while 'terms/pose' in self.page.location:
                Utility.click_option(self.driver,
                                     element=self.agreement_checkbox)
                self.next()
            if destination:
                return go_to_(destination(self.driver, url, **kwargs))

        def facebook_login(self, user, facebook_user, password):
            """Log into the site with facebook."""
            self.user = user
            self.next()
            fb_button = self.find_element(*self._fb_locator)
            Utility.click_option(self.driver, element=fb_button)
            self.wait.until(
                expect.visibility_of_element_located(
                    self._fb_email_field_locator))
            self.find_element(*self._fb_email_field_locator) \
                .send_keys(facebook_user)
            self.find_element(*self._fb_password_field_locator) \
                .send_keys(password)
            fb_submit = self.find_element(*self._fb_submit_locator)
            Utility.click_option(self.driver, element=fb_submit)
            if self.driver.capabilities['browserName'] == 'safari':
                fb_safari = self.wait.until(
                    expect.visibility_of_element_located(
                        self._fb_safari_specific_locator))
                Utility.click_option(self.driver, element=fb_safari)
            sleep(2.0)
            from pages.accounts.profile import Profile
            return go_to_(Profile(self.driver, self.page.base_url))

        def google_login(self, user, google_user, password):
            """Log into the site with google."""
            self.user = user
            self.next()
            g_login = self.find_element(*self._google_locator)
            Utility.click_option(self.driver, element=g_login)
            self.wait.until(
                expect.visibility_of_element_located(
                    self._google_user_locator))
            g_next = self.find_element(*self._google_user_next_locator)
            Utility.click_option(self.driver, element=g_next)
            self.wait.until(
                expect.visibility_of_element_located(
                    self._google_password_locator))
            self.find_element(*self._google_password_locator) \
                .send_keys(password)
            g_pass = self.find_element(*self._google_pass_next_locator)
            Utility.click_option(self.driver, element=g_pass)
            sleep(1.0)
            from pages.accounts.profile import Profile
            return go_to_(Profile(self.driver, self.page.base_url))

        def trigger_reset(self, user):
            """Start a password reset for a user."""
            self.user = user
            self.next()
            self.reset()

        def reset_password(self, url, password):
            """Reset the password for the current user."""
            self.driver.get(url)
            fields = self.find_elements(*self._password_reset_fields_locator)
            for field in fields:
                field.send_keys(password)
            reset = self.find_element(*self._password_reset_submit)
            Utility.click_option(self.driver, element=reset)
            sleep(0.25)
            try:
                submit = self.find_element(*self._password_reset_submit)
                Utility.click_option(self.driver, element=submit)
                sleep(0.5)
            except ElementNotInteractableException:
                sleep(1.0)
                submit = self.find_element(*self._password_reset_submit)
                Utility.click_option(self.driver, element=submit)
                sleep(0.5)
            sleep(1.0)
            try:
                submit = self.find_element(*self._password_reset_submit)
                Utility.click_option(self.driver, element=submit)
                sleep(0.5)
            except WebDriverException:
                pass
            from pages.accounts.profile import Profile
            return go_to_(Profile(self.driver, self.page.base_url))

        @property
        def is_help_shown(self):
            """Return True if help text is visible."""
            return self.is_element_displayed(*self._login_help_locator)

        @property
        def toggle_help(self):
            """Show or hide Account help info."""
            toggle = self.find_element(*self._trouble_locator)
            Utility.click_option(self.driver, element=toggle)
            sleep(0.25)
            return self

        @property
        def go_to_help(self):
            """Click the Salesforce help link."""
            if not self.is_help_shown:
                self.toggle_help
            current = self.driver.current_window_handle
            salesforce = self.find_element(*self._salesforce_link_locator)
            Utility.click_option(self.driver, element=salesforce)
            new_handle = 1 if current == self.driver.window_handles[0] else 0
            if len(self.driver.window_handles) > 1:
                self.driver.switch_to.window(
                    self.driver.window_handles[new_handle])
            return go_to_(Salesforce(self.driver))

        def get_login_error(self):
            """Return Account log in error message."""
            try:
                return self.find_element(*self._error_locator).text
            except WebDriverException:
                return ''

        def get_error_color(self):
            """Return the background color for missing or illegal fields."""
            fields = self.find_elements(*self._input_field_locator)
            issues = list(filter(
                lambda element: 'has-error' in element.get_attribute('class'),
                fields
            ))
            if not isinstance(issues, list):
                issues = [issues]
            if issues:
                return (
                    issues[0]
                    .find_element(*self._form_box_locator)
                    .value_of_css_property('background-color')
                )
            return None

        @property
        def go_to_signup(self):
            """Go to user signup."""
            signup = self.find_element(*self._signup_locator)
            Utility.click_option(self.driver, element=signup)
            from utils.accounts import Accounts
            if Accounts.accounts_old:
                from pages.accounts.signup import Signup
            else:
                from pages.accounts.signup_two import Signup
            return go_to_(Signup(self.driver, self.page.seed_url))
