"""The textbook suppliers page."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility


class Bookstore(WebBase):
    """The campus bookstore supplier page."""

    URL_TEMPLATE = '/bookstore-suppliers'

    _initial_image_locators = (By.CSS_SELECTOR, '#main .img')
    _banner_heading_locator = (By.CSS_SELECTOR, '.hero h1')

    @property
    def loaded(self):
        """Return True when the images are loaded."""
        return Utility.is_image_visible(
            driver=self.driver,
            locator=self._initial_image_locators)

    def is_displayed(self):
        """Return True if the blog pinned article is displayed."""
        print(self.driver.page_source)
        return self.find_element(*self._banner_heading_locator).is_displayed()
