"""The Subjects page."""

# from time import sleep
#
# from pypom import Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Subjects(WebBase):
    """The subjects page."""

    URL_TEMPLATE = '/subjects'

    _root_locator = (By.TAG_NAME, 'main')

    @property
    def loaded(self):
        """Override the base loader."""
        return self.find_element(*self._root_locator).is_displayed
