"""Facebook integration for social logins."""

from time import sleep

from pypom import Page
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class Facebook(Page):
    """Facebook homepage."""

    URL_TEMPLATE = 'https://www.facebook.com/login.php'

    _root_locator = (By.CSS_SELECTOR, '#content div div')
    _phone_email_locator = (By.ID, 'email')
    _password_locator = (By.ID, 'pass')
    _log_in_button_locator = (By.ID, 'loginbutton')
    _continue_button_locator = (By.CLASS_NAME, '_51_n')

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
        sleep(1.0)
        self.find_element(*self._phone_email_locator).send_keys(user)
        self.find_element(*self._password_locator).send_keys(password)
        self.find_element(*self._log_in_button_locator).click()
        sleep(1.0)
        # get by the 'logged in previously' to another Accounts instance
        for _ in range(3):
            try:
                self.find_element(*self._continue_button_locator).click()
                break
            except NoSuchElementException:
                pass
            finally:
                sleep(1.0)
        # poll the webpage until it changes due to Safari slowness
        if self.at_facebook:
            from time import perf_counter
            start = perf_counter()
            timer = 0
            while self.at_facebook and timer < 15.0:
                timer = perf_counter() - start
                sleep(0.25)
        from pages.accounts.signup import Signup
        return Signup(self.selenium)
