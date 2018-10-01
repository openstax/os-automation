"""Tutor Home page objects."""

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.accounts.home import AccountsHome
from pages.tutor.base import TutorBase
from pages.tutor.dashboard import Dashboard


class TutorHome(TutorBase):
    """Tutor home page for users that are not logged in."""

    _login_button_locator = (By.CSS_SELECTOR, '.login')

    def go_to_log_in(self):
        """Click the LOG IN button."""
        self.find_element(*self._login_button_locator).click()
        return AccountsHome(self.driver)

    def service_pass_through(self):
        """Click the LOG IN button if session information is new or missing."""
        try:
            self.find_element(*self._login_button_locator).click()
        except NoSuchElementException:
            pass
        dash = Dashboard(self.driver)
        dash.wait_for_page_to_load()
        return dash

    def log_in(self, user, password):
        """Log into the site with a specific user."""
        self.find_element(*self._login_button_locator).click()
        AccountsHome(self.driver).service_log_in(user, password)
        self.wait.until(lambda _: self.logged_in)
        return Dashboard(self)

    @property
    def logged_in(self):
        """Return user log in status."""
        return ('dashboard' or 'course') in self.driver.current_url
