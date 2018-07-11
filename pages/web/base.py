"""Basic page parent for all OpenStax Web pages."""

from pypom import Page, Region
from selenium.webdriver.common.by import By

from regions.web.footer import Footer
from regions.web.openstax_nav import OpenStaxNav
from regions.web.web_nav import WebNav


class WebBase(Page):
    """Base class."""

    _root_locator = (By.ID, 'home')

    def wait_for_page_to_load(self):
        """Override page load."""
        self.wait.until(
            lambda _: self.find_element(*self._root_locator).is_displayed())

    @property
    def header(self):
        """Return Web header."""
        return self.Header(self)

    @property
    def footer(self):
        """Return Web footer."""
        return Footer(self)

    class Header(Region):
        """Web page header."""

        _root_locator = (By.CLASS_NAME, 'page-header')

        @property
        def is_header_displayed(self):
            """Header display boolean."""
            return self.loaded

        @property
        def web_nav(self):
            """Web nav region."""
            return WebNav(self)

        @property
        def openstax_nav(self):
            """Openstax nav region."""
            return OpenStaxNav(self)
