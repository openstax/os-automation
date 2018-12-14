"""The Web contact form."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Contact(WebBase):
    """The web contact form."""

    URL_TEMPLATE = '/contact'

    _hero_quote_locator = (By.CSS_SELECTOR, '.hero h1')
    _form_locator = (By.CSS_SELECTOR, '.form')
    _topic_locator = (By.CSS_SELECTOR, '.form .item')

    @property
    def loaded(self):
        """Return the form when it is found."""
        return (self.find_element(*self._form_locator) and
                self.find_element(*self._topic_locator))

    def is_displayed(self):
        """Return True if the heading is displayed."""
        return self.find_element(*self._hero_quote_locator).is_displayed()

    @property
    def topic(self):
        """Return the currently selected contact topic."""
        return self.find_element(*self._topic_locator).text
