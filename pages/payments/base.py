"""Basic page parent for all Payment pages."""
import time

from pypom import Page
from selenium.webdriver.common.by import By


class PaymentsBase(Page):
    """Base class."""

    _root_locator = (By.TAG_NAME, 'body')

    def wait_for_page_to_load(self):
        self.wait.until(
            lambda _: (self.find_element(*self._root_locator).is_displayed())
        )

    @property
    def logged_in(self):
        """Return if user is logged in."""
        return ('login' not in self. driver.current_url) \
            and ('logout' not in self.driver.current_url)
