"""Tutor Home page objects."""

from time import sleep

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
        """Return the slogan text.

        :return: the OpenStax Tutor Beta marketing slogan
        :rtype: str

        """
        return self.find_element(*self._slogan_locator).text

    @property
    def description(self):
        """Return the descriptive Tutor overview text.

        :return: the overview description
        :rtype: str

        """
        return self.find_element(*self._description_locator).text

    def learn_more(self):
        """Click on the 'LEARN MORE' link to view the marketing page.

        :return: the OpenStax Tutor marketing page on openstax.org
        :rtype: :py:class:`~pages.web.tutor.TutorMarketing`

        """
        link = self.find_element(*self._learn_more_locator)
        url = link.get_attribute('href')
        Utility.click_option(self.driver, element=link)
        from pages.web.tutor import TutorMarketing
        return go_to_(TutorMarketing(self.driver, url))

    def go_to_log_in(self):
        """Click the 'LOG IN' button.

        :return: the Accounts log in page
        :rtype: :py:class:`~pages.accounts.home.AccountsHome`

        """
        button = self.find_element(*self._log_in_locator)
        Utility.click_option(self.driver, element=button)
        from pages.accounts.home import AccountsHome
        return go_to_(AccountsHome(self.driver))

    def service_pass_through(self):
        """Click the log in button for an active Accounts user.

        :return: the user's dashboard
        :rtype: :py:class:`~pages.tutor.dashboard.Dashboard`

        :raises :py:class:`~selenium.common.exceptions.NoSuchElementException`:
            if the login bar is not found

        """
        try:
            button = self.find_element(*self._log_in_locator)
            Utility.click_option(self.driver, element=button)
        except NoSuchElementException:
            pass
        from pages.tutor.dashboard import Dashboard
        return go_to_(Dashboard(self.driver, self.base_url))

    def log_in(self, username, password):
        """Log into Tutor with a specific user.

        :param str username: the user to log in as
        :param str password: the user's password
        :return: the user's dashboard
        :rtype: :py:class:`~pages.tutor.dashboard.Dashboard`

        """
        accounts = self.go_to_log_in()
        accounts.service_log_in(username, password)
        self.wait.until(lambda _: self.logged_in)
        if Utility.is_browser(self.driver, 'safari'):
            sleep(2.0)
        from pages.tutor.dashboard import Dashboard
        return go_to_(Dashboard(self.driver, self.base_url))

    @property
    def logged_in(self):
        """Return True if the user is logged into Tutor.

        :return: ``True`` if the user is logged into Tutor, else ``False``
        :rtype: bool

        """
        return 'dashboard' in self.location or 'course' in self.location

    class Footer(TutorLoginBase.Footer):
        """The Tutor root page footer."""

        _gdpr_locator = (By.CSS_SELECTOR, '[href*=gdpr]')

        def view_gdpr(self):
            """Click on the GDPR link to view the GDPR on Rice's webpage.

            :return: the General Data Privacy Regulation page on Rice
                University's webpage in a new tab
            :rtype: :py:class:`~pages.rice.gdpr.GeneralDataPrivacyRegulation`

            """
            link = self.find_element(*self._gdpr_locator)
            url = link.get_attribute('href')
            Utility.switch_to(self.driver, element=link)
            from pages.rice.gdpr import GeneralDataPrivacyRegulation as GDPR
            return go_to_external_(GDPR(self.driver, url))
