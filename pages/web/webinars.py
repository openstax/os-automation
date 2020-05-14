"""The upcoming and recorded webinars page."""

# from pypom import Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Webinars(WebBase):
    """The upcoming and past webinars page."""

    URL_TEMPLATE = '/webinars'

    _webinar_card_locator = (By.CSS_SELECTOR, '.webinar-list .card')

    @property
    def loaded(self) -> bool:
        """Return True when the webinars page is loaded.

        :return: ``True`` when upcoming or past webinars are found
        :rtype: bool

        """
        return (super().loaded and
                self.find_elements(*self._webinar_card_locator))

    def is_displayed(self) -> bool:
        """Return True when the page is loaded.

        :return: ``True`` when the page is loaded
        :rtype: bool

        """
        return self.loaded
