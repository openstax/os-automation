"""The legal / intellectual property frequently asked questions page."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class LegalBase(WebBase):
    """The base page for the legal document pages."""

    _heading_locator = (By.CSS_SELECTOR, 'h1')

    @property
    def loaded(self):
        """Return True when the heading is found."""
        return self.find_element(*self._heading_locator)

    def is_displayed(self):
        """Return True if the heading is displayed."""
        return self.loaded.is_displayed()


class License(LegalBase):
    """The OpenStax.org licensing overview page."""

    URL_TEMPLATE = '/license'


class Terms(LegalBase):
    """The OpenStax.org terms of use."""

    URL_TEMPLATE = '/tos'


class PrivacyPolicy(LegalBase):
    """The OpenStax.org terms of use."""

    URL_TEMPLATE = '/privacy-policy'
