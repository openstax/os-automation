"""The OpenStax SE app download page."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.web.base import WebBase
from utils.utilities import Utility, go_to_


class StudyEdge(WebBase):
    """The app download option link page."""

    _title_locator = (By.CSS_SELECTOR, '.block-heading')
    _apple_app_store_button_locator = (By.CSS_SELECTOR, '[href*=apple]')
    _google_app_store_button_locator = (By.CSS_SELECTOR, '[href*=google]')

    @property
    def loaded(self) -> bool:
        """Return True when the app store buttons are displayed.

        :return: ``True`` when the Apple and Google app store buttons are
            displayed
        :rtype: bool

        """
        return self.apple.is_displayed() and self.google.is_displayed()

    def is_displayed(self) -> bool:
        """Return True when the SE App download page is loaded.

        :return: ``True`` when the page is loaded
        :rtype: bool

        """
        return self.loaded

    @property
    def apple(self) -> WebElement:
        """Return the Apple app store button/link.

        :return: the Apple app store button
        :rtype: :py:class:`~`

        """
        return self.find_element(*self._apple_app_store_button_locator)

    @property
    def google(self) -> WebElement:
        """Return the Google app store button/link.

        :return: the Google app store button
        :rtype: :py:class:`~`

        """
        return self.find_element(*self._google_app_store_button_locator)

    def download_on_the_app_store(self):
        """Download the app from Apple.

        :return: the OpenStax SE app download page in the Apple app store
        :rtype: :py:class:`~pages.apple.store.AppStore`

        """
        button = self.apple
        url = button.get_attribute('href')
        from pages.apple.store import AppStore
        Utility.switch_to(self.driver, element=button)
        return go_to_(AppStore(self.driver), base_url=url)

    def get_it_on_google_play(self):
        """Download the app from Google.

        :return: the OpenStax SE app download page in the Google app store
        :rtype: :py:class:`~pages.google.store.Play`

        """
        button = self.google
        url = button.get_attribute('href')
        from pages.google.store import GooglePlay
        Utility.switch_to(self.driver, element=button)
        return go_to_(GooglePlay(self.driver), base_url=url)
