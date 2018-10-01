"""The Web research overview page."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Research(WebBase):
    """The researchers page."""

    URL_TEMPLATE = '/research'

    _title_locator = (By.TAG_NAME, 'h1')

    @property
    def loaded(self):
        """Override the base loader."""
        print('Research')
        return self.find_element(*self._title_locator)

    def is_displayed(self):
        """Return True if the research page is displayed."""
        return self.find_element(*self._title_locator).is_displayed()
