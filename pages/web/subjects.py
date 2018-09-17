"""The Subjects page."""

# from time import sleep
#
# from pypom import Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Subjects(WebBase):
    """The subjects page."""

    URL_TEMPLATE = '/subjects'

    _root_locator = (By.CSS_SELECTOR, 'main.loaded')

    @property
    def loaded(self):
        return self.find_element(*self._root_locator).is_displayed
