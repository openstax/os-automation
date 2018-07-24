"""Facebook integration for social logins."""

from time import sleep

from pypom import Page
from selenium.webdriver.common.by import By

from pages.accounts import signup


class Facebook(Page):
    """Facebook homepage."""

    URL_TEMPLATE = 'https://www.facebook.com/login.php'

    _root_locator = (By.CSS_SELECTOR, '#content div div')
    _phone_email_locator = (By.ID, 'email')
    _password_locator = (By.ID, 'pass')
    _log_in_button_locator = (By.ID, 'loginbutton')

    def wait_for_page_to_load(self):
        """Override page load."""
        self.wait.until(
            lambda _: (self.find_element(*self._root_locator).is_displayed())
        )

    @property
    def at_facebook(self):
        """Return True if at Facebook's login page."""
        return 'facebook' in self.selenium.current_url

    def log_in(self, user, password):
        """Log into Facebook."""
        self.find_element(*self._phone_email_locator).send_keys(user)
        self.find_element(*self._password_locator).send_keys(password)
        self.find_element(*self._log_in_button_locator).click()
        sleep(1.0)
        return signup.Signup(self)
