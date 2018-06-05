"""Basic page parent for all OpenStax Web pages."""
import os

from pypom import Page, Region
from selenium.webdriver.common.by import By


class WebBase(Page):
    """Base class."""

    URL_TEMPLATE = 'https://{0}openstax.org'.format(
        ('oscms' + os.getenv('INSTANCE', '-qa') + '.')
        if os.getenv('INSTANCE', '') != '' else '')

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
        return self.Footer(self)

    class Header(Region):
        """Web page header."""

        _root_locator = (By.CLASS_NAME, 'container')

        @property
        def is_header_displayed(self):
            """Header display boolean."""
            return self.loaded

    class Footer(Region):
        """Web page footer."""

        _root_locator = (By.TAG_NAME, 'footer')

        @property
        def is_footer_displayed(self):
            """Footer display boolean."""
            return self.loaded
