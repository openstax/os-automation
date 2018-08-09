"""Basic page parent for the tutor admin page."""

from time import sleep

from pypom import Page, Region
from selenium.webdriver.common.by import By


class TutorAdminBase(Page):
    """Base class."""

    _root_locator = (By.CLASS_NAME, 'admin')

    def wait_for_page_to_load(self):
        """Override page load."""
        self.wait.until(
            lambda _: self.find_element(*self._root_locator).is_displayed())

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.adminnav import TutorAdminNav
        return TutorNav(self)
