"""Home page objects."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from pages.accounts.home import AccountsHome
from pages.tutor.dashboard import TutorDashboard


class TutorHome(TutorBase):
    """Tutor home page for users that are not logged in"""

    _login_btn_locator = (By.CSS_SELECTOR, '.login')

    def log_in(self, user, password):
        """Log into the site with a specific user."""

        self.find_element(*self._login_btn_locator).click()
        AccountsHome(self.driver).service_log_in(user, password)
        self.wait.until(lambda _: self.logged_in)
        return TutorDashboard(self.driver)

    @property
    def logged_in(self):
        """Return user log in status."""
        return ('dashboard' or 'course') in self.driver.current_url
