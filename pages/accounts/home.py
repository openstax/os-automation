"""Home page objects."""

from time import sleep

from pypom import Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect

from pages.accounts.base import AccountsBase
from pages.salesforce.home import Salesforce


class AccountsHome(AccountsBase):
    """Home page base."""

    URL_TEMPLATE = ''

    @property
    def login(self):
        """Return the login pane."""
        return self.Login(self)

    def log_in(self, user, password):
        """Log into the site with a specific user."""
        return self.Login(self).login(user, password)

    def service_log_in(self, user, password):
        """Log into the site with a specific user from another service."""
        return self.Login(self).service_login(user, password)

    @property
    def logged_in(self):
        """Return user log in status."""
        return self.Login(self).logged_in

    class Login(Region):
        """User login pane."""

        _user_field_locator = (By.ID, 'login_username_or_email')
        _password_field_locator = (By.ID, 'login_password')
        _login_submit_button_locator = (By.CSS_SELECTOR, '.footer > input')
        _password_reset_locator = (By.CSS_SELECTOR, '.footer a')
        _trouble_locator = (By.CSS_SELECTOR, '.trouble')
        _login_help_locator = (By.CSS_SELECTOR, '.login-help')
        _salesforce_link_locator = (By.CSS_SELECTOR, '.login-help a')
        _salesforce_loader = (By.CSS_SELECTOR, 'div.body-and-support-buttons')
        _input_field_locator = (By.CLASS_NAME, 'form-group')
        _form_box_locator = (By.TAG_NAME, 'input')
        _error_locator = (By.CSS_SELECTOR, '.alert')
        _signup_locator = (By.CSS_SELECTOR, '.extra-info a')

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

        def login(self, user, password):
            """Log into the accounts with a specific user."""
            self.service_login(user, password)
            self.wait.until(lambda _: self.logged_in)
            from pages.accounts.profile import Profile
            return Profile(self.driver)

        def service_login(self, user, password):
            """Log into the site with a specific user from another service."""
            self.find_element(*self._user_field_locator).send_keys(user)
            self.find_element(*self._login_submit_button_locator).click()
            sleep(1)
            self.find_element(*self._password_field_locator) \
                .send_keys(password)
            self.find_element(*self._login_submit_button_locator).click()
            sleep(1)

        def facebook_login(self, user, facebook_user, password):
            """Log into the site with facebook."""
            self.find_element(*self._user_field_locator).send_keys(user)
            self.find_element(*self._login_submit_button_locator).click()
            sleep(1)
            self.find_element(*self._fb_locator).click()
            self.wait.until(
                expect.visibility_of_element_located(
                    self._fb_email_field_locator))
            self.find_element(*self._fb_email_field_locator) \
                .send_keys(facebook_user)
            self.find_element(*self._fb_password_field_locator) \
                .send_keys(password)
            self.find_element(*self._fb_submit_locator).click()
            if self.driver.capabilities['browserName'] == 'safari':
                self.wait.until(
                    expect.visibility_of_element_located(
                        self._fb_safari_specific_locator))
                self.find_element(*self._fb_safari_specific_locator).click()
            sleep(2)
            from pages.accounts.profile import Profile
            return Profile(self.driver)

        def google_login(self, user, google_user, password):
            """Log into the site with google."""
            self.find_element(*self._user_field_locator).send_keys(user)
            self.find_element(*self._login_submit_button_locator).click()
            sleep(1)
            self.find_element(*self._google_locator).click()
            self.wait.until(
                expect.visibility_of_element_located(
                    self._google_user_locator))
            self.find_element(*self._google_user_next_locator).click()
            self.wait.until(
                expect.visibility_of_element_located(
                    self._google_password_locator))
            self.find_element(*self._google_password_locator) \
                .send_keys(password)
            self.find_element(*self._google_pass_next_locator).click()
            sleep(2)
            from pages.accounts.profile import Profile
            return Profile(self.driver)

        def reset_password(self, user, new_password):
            """Reset a current user's password."""
            # TODO: add password reset method
            return

        @property
        def is_help_shown(self):
            """Return True if help text is visible."""
            return self.is_element_displayed(*self._login_help_locator)

        @property
        def toggle_help(self):
            """Show or hide Account help info."""
            self.find_element(*self._trouble_locator).click()
            from time import sleep
            sleep(0.25)
            return self

        @property
        def go_to_help(self):
            """Click the Salesforce help link."""
            if not self.is_help_shown:
                self.toggle_help
            current = self.driver.current_window_handle
            self.find_element(*self._salesforce_link_locator).click()
            sleep(1)
            new_handle = 1 if current == self.driver.window_handles[0] else 0
            if len(self.driver.window_handles) > 1:
                self.driver.switch_to.window(
                    self.driver.window_handles[new_handle])
            return Salesforce(self.driver)

        def get_login_error(self):
            """Return Account log in error message."""
            return self.find_element(*self._error_locator).text

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
            self.find_element(*self._signup_locator).click()
            sleep(1)
            from pages.accounts.signup import Signup
            return Signup(self.driver, self.page.seed_url)
