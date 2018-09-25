"""The OpenStax blog."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility


class Blog(WebBase):
    """The OpenStax web log."""

    URL_TEMPLATE = '/blog'

    _root_locator = (By.TAG_NAME, 'main')
    _initial_image_locators = (By.CSS_SELECTOR, '#main .img')
    _pinned_article_locator = (By.CLASS_NAME, 'pinned')

    @property
    def loaded(self):
        """Return True when all of the blog article images are loaded."""
        test = Utility.load_background_images(
            driver=self.driver,
            locator=self._initial_image_locators)
        print('Blog: %s' % test)
        return test

    def is_displayed(self):
        """Return True if the blog pinned article is displayed."""
        return self.find_element(*self._pinned_article_locator).is_displayed()
