"""Tutor Home page objects."""

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorLoginBase
from utils.utilities import Utility, go_to_, go_to_external_


class TutorHome(TutorLoginBase):
    """The Tutor root page."""

    _slogan_locator = (By.CSS_SELECTOR, '.body-container > h1')
    _description_locator = (By.CSS_SELECTOR, '.lead')
    _learn_more_locator = (By.CSS_SELECTOR, '.learn-more')
    _log_in_locator = (By.CSS_SELECTOR, '.login')

    @property
    def title(self):
        """Return the slogan text."""
        return self.find_element(*self._slogan_locator).text

    @property
    def description(self):
        """Return the descriptive Tutor overview text."""
        return self.find_element(*self._description_locator).text

    def learn_more(self):
        """Click on the 'LEARN MORE' link to view the marketing page."""
        link = self.find_element(*self._learn_more_locator)
        url = link.get_attribute('href')
        Utility.click_option(self.driver, element=link)
        from pages.web.tutor import TutorMarketing
        return go_to_(TutorMarketing(self.driver, url))

    def go_to_log_in(self):
        """Click the 'LOG IN' button."""
        self.find_element(*self._log_in_locator).click()
        from pages.accounts.home import AccountsHome
        return go_to_(AccountsHome(self.driver))

    def service_pass_through(self):
        """Click the log in button for an active Accounts user."""
        try:
            self.find_element(*self._log_in_locator).click()
        except NoSuchElementException:
            pass
        from pages.tutor.dashboard import Dashboard
        return go_to_(Dashboard(self.driver, self.base_url))

    def log_in(self, username, password):
        """Log into Tutor with a specific user."""
        accounts = self.go_to_log_in()
        accounts.service_log_in(username, password)
        self.wait.until(lambda _: self.logged_in)
        from pages.tutor.dashboard import Dashboard
        return Dashboard(self.driver, self.base_url)

    @property
    def logged_in(self):
        """Return True if the user is logged into Tutor."""
        return 'dashboard' in self.location or 'course' in self.location

    class Footer(TutorLoginBase.Footer):
        """The Tutor root page footer."""

        _gdpr_locator = (By.CSS_SELECTOR, '[href*=gdpr]')

        def view_gdpr(self):
            """Click on the GDPR link to view the GDPR on Rice's webpage."""
            link = self.find_element(*self._gdpr_locator)
            url = link.get_attribute('href')
            Utility.switch_to(self.driver, element=link)
            from pages.rice.gdpr import GeneralDataPrivacyRegulation as GDPR
            return go_to_external_(GDPR(self.driver, url))
