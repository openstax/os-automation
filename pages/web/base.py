"""Basic page parent for all OpenStax Web pages."""

from pypom import Page
from selenium.webdriver.common.by import By

from regions.web.footer import Footer
from regions.web.openstax_nav import OpenStaxNav
from regions.web.sticky_note import StickyNote
from regions.web.web_nav import WebNav


class WebBase(Page):
    """Base class."""

    _root_locator = (By.CSS_SELECTOR, 'body.page-loaded')

    @property
    def loaded(self):
        """Return True when the page-loaded class is added to the body tag."""
        return self.find_element(*self._root_locator).is_displayed()

    @property
    def sticky_note(self):
        """Access the sticky note."""
        return StickyNote(self)

    @property
    def openstax_nav(self):
        """Access the OpenStax header navigation."""
        return OpenStaxNav(self)

    @property
    def web_nav(self):
        """Access the website header navigation."""
        return WebNav(self)

    @property
    def footer(self):
        """Return Web footer."""
        return Footer(self)

    def reload(self):
        """Reload the current page."""
        self.driver.navigate().refresh()
        return self

    def back(self):
        """Go back to the previous page."""
        self.driver.execute_script('window.history.go(-1)')
        return self
