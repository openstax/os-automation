"""The legal / intellectual property frequently asked questions page."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility


class LegalBase(WebBase):
    """The base page for the legal document pages."""

    _heading_locator = (By.CSS_SELECTOR, 'h1')
    _content_locator = (By.CSS_SELECTOR, '[data-html*=content]')

    @property
    def loaded(self):
        """Return True when the content is available."""
        return Utility.has_children(self.content)

    @property
    def content(self):
        """Return the content wrapper."""
        return self.find_element(*self._content_locator)

    def is_displayed(self):
        """Return True if the heading is displayed."""
        return self.find_element(*self._heading_locator).is_displayed()


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
