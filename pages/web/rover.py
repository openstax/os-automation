"""Rover by OpenStax."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Rover(WebBase):
    """The Rover by OpenStax marketing page."""

    URL_TEMPLATE = '/rover-by-openstax'

    _title_banner_locator = (
        By.CSS_SELECTOR, '#banner img')

    @property
    def loaded(self) -> bool:
        """Return True when the page is loaded.

        :return: ``True`` when the async hide class is not found and a banner
            image is found
        :rtype: bool

        """
        return (super().loaded and
                self.URL_TEMPLATE in self.location and
                self.find_elements(*self._title_banner_locator))

    def is_displayed(self) -> bool:
        """Return True when the page is displayed.

        :return: ``True`` when the page is loaded
        :rtype: bool

        """
        return self.loaded
