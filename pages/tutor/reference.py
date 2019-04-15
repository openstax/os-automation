"""The Tutor reference view of the textbook."""

from pypom import Page, Region
from selenium.webdriver.common.by import By


class ReferenceBook(Page):
    """The complete textbook reading experience."""

    _nav_bar_locator = (By.CSS_SELECTOR, '.tutor-navbar')
    _table_of_contents_locator = (By.CSS_SELECTOR, )

    @property
    def nav(self):
        """Access the reference book navigation bar."""
        nav_root = self.find_element(*self._nav_bar_locator)
        return self.Nav(self, nav_root)

    class Nav(Region):
        """The reference book navigation controls."""
