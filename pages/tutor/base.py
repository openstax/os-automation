"""Basic page parent for all Accounts pages."""
import os
from time import sleep

from pypom import Page, Region
from selenium.webdriver.common.by import By


class TutorBase(Page):
    """Base class."""

    URL_TEMPLATE = 'https://tutor{0}.openstax.org'.format(
        os.getenv('instance', '-qa'))

    _root_locator = (By.CSS_SELECTOR, '.start')

    def wait_for_page_to_load(self):
        """Override page load."""
        self.wait.until(
            lambda _: self.find_element(*self._root_locator).is_displayed())
