"""Basic page parent for all Accounts pages."""
from pypom import Page, Region
from selenium.webdriver.common.by import By

from pages.rice.home import Rice


class AccountsBase(Page):
    """Base class."""

    @property
    def header(self):
        """Return Accounts' header."""
        return self.Header(self)

    @property
    def footer(self):
        """Return Accounts' footer."""
        return self.Footer(self)

    @property
    def login(self):
        """Return the login pane."""
        return self.Login(self)

    def log_in(self, user, password):
        """Log into the site with a specific user."""
        return self.Login(self).login(user, password)

    def logged_in(self):
        """Return user log in status."""
        return self.Login(self).logged_in()

    class Header(Region):
        """Accounts header."""

        _root_locator = (By.ID, 'application-header')
        _logo_locator = (By.ID, 'top-nav-logo')

        @property
        def is_header_displayed(self):
            """Header display boolean."""
            return self.is_element_displayed(*self._root_locator)

        def go_to_accounts_home(self):
            """Follow the OpenStax icon link back to the site root."""
            self.find_element(*self._logo_locator).click()
            return self

    class Login(Region):
        """User login pane."""

        _user_field_locator = (By.ID, 'login_username_or_email')
        _password_field_locator = (By.ID, 'login_password')
        _login_submit_button_locator = (By.CSS_SELECTOR, '.footer > input')
        _password_reset_locator = (By.CSS_SELECTOR, '.footer a')
        _trouble_locator = (By.CSS_SELECTOR, '.trouble')
        _login_help_locator = (By.CSS_SELECTOR, '.login-help')
        _error_locator = (By.CSS_SELECTOR, '.alert')

        def logged_in(self):
            """Return True if a user is logged in."""
            return 'profile' in self.selenium.current_url

        def login(self, user, password):
            """Log into the site with a specific user."""
            self.find_element(*self._user_field_locator).send_keys(user)
            self.find_element(*self._login_submit_button_locator).click()
            self.find_element(*self._password_field_locator) \
                .send_keys(password)
            self.find_element(*self._login_submit_button_locator).click()
            self.wait.until(lambda _: self.logged_in)

        def is_help_shown(self):
            """Return True if help text is visible."""
            return self.is_element_displayed(*self._login_help_locator)

        def toggle_help(self):
            """Show or hide Account help info."""
            self.find_element(*self._trouble_locator).click()

        def get_login_error(self):
            """Return Account log in error message."""
            return self.find_element(*self._error_locator).text

    class Footer(Region):
        """Accounts footer."""

        _root_locator = (By.ID, 'application-footer')
        _rice_link_locator = (By.ID, 'footer-rice-logo')
        _copyright_locator = (By.PARTIAL_LINK_TEXT, 'Copyright')
        _terms_locator = (By.PARTIAL_LINK_TEXT, 'Terms')

        @property
        def is_footer_displayed(self):
            """Footer display boolean."""
            return self.is_element_displayed(*self._root_locator)

        def show_copyright(self):
            """Display the copyright."""
            self.find_element(*self._copyright_locator).click()
            return self

        def show_terms_of_use(self):
            """Display the terms of use."""
            self.find_element(*self._terms_locator).click()
            return self

        def go_to_rice(self):
            """Load the Rice webpage."""
            self.find_element(*self._rice_link_locator).click()
            return Rice(self.driver)
