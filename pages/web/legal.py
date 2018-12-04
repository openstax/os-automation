"""The legal / intellectual property frequently asked questions page."""

from time import sleep

from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility


class LegalBase(WebBase):
    """The base page for the legal document pages."""

    _heading_locator = (By.CSS_SELECTOR, '#main h1')
    _content_locator = (By.CSS_SELECTOR, '#main [data-html*=content]')
    _text_locator = (By.CSS_SELECTOR, 'p')

    @property
    def loaded(self):
        """Return True when the content is available."""
        return sleep(1) or Utility.has_children(self.content)

    @property
    def heading(self):
        """Return the heading."""
        return self.find_element(*self._heading_locator)

    @property
    def content(self):
        """Return the content wrapper."""
        return self.find_element(*self._content_locator)

    @property
    def title(self):
        """Return the heading text."""
        return self.heading.text.strip()

    @property
    def text(self):
        """Return the body text."""
        return [paragraph.text.strip()
                for paragraph
                in self.content.find_elements(*self._text_locator)]

    def is_displayed(self):
        """Return True if the heading is displayed."""
        return self.heading.is_displayed()


class License(LegalBase):
    """The OpenStax.org licensing overview page."""

    URL_TEMPLATE = '/license'

    _heading_locator = (By.CSS_SELECTOR, '#maincontent h2')


class Terms(LegalBase):
    """The OpenStax.org terms of use."""

    URL_TEMPLATE = '/tos'


class PrivacyPolicy(LegalBase):
    """The OpenStax.org terms of use."""

    URL_TEMPLATE = '/privacy-policy'
