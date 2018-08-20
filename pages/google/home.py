"""Google integration for social logins and e-mail."""

from time import sleep

from pypom import Page
from selenium.webdriver.common.by import By


class Google(Page):
    """Google homepage."""

    URL_TEMPLATE = 'https://accounts.google.com/signin/'

    _root_locator = (By.ID, 'initialView')
    _identifier_locator = (By.ID, 'identifierId')
    _identifier_next_button_locator = (By.ID, 'identifierNext')
    _password_locator = (By.ID, '[name=password]')
    _password_next_button_locator = (By.ID, 'passwordNext')

    def wait_for_page_to_load(self):
        """Override page load."""
        self.wait.until(
            lambda _: (self.find_element(*self._root_locator).is_displayed())
        )

    @property
    def at_google(self):
        """Return True if at one of Google's pages."""
        return 'google' in self.selenium.current_url

    def log_in(self, user, password):
        """Log into Google."""
        from pages.accounts.signup import Signup
        if not self.at_google:
            return Signup(self.driver)
        self.find_element(*self._identifier_locator).send_keys(user)
        self.find_element(*self._identifier_next_button_locator).click()
        sleep(0.5)
        self.find_element(*self._password_locator).send_keys(password)
        self.find_element(*self._password_next_button_locator).click()
        sleep(0.5)
        return Signup(self.driver)
