"""The foundation and corporate supporters page."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Supporters(WebBase):
    """The foundation and corporate supporters page."""

    URL_TEMPLATE = '/foundation'

    _banner_locator = (By.CLASS_NAME, 'foundation-page')

    @property
    def loaded(self):
        """Return True if the hero banner is found."""
        return self.find_element(*self._banner_locator).is_displayed()

    def is_displayed(self):
        """Return True if the supporters page is displayed."""
        try:
            return self.loaded
        except Exception:
            return False
