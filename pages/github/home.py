"""The OpenStax GitHub repositories page."""

from pypom import Page
from selenium.webdriver.common.by import By


class GitHub(Page):
    """The GitHub landing page for the OpenStax user repositories."""

    URL_TEMPLATE = 'https://github.com/openstax'

    _organization_name_locator = (By.CSS_SELECTOR, '.org-name')

    @property
    def loaded(self):
        """Return the org name element when it is found."""
        return self.find_element(*self._organization_name_locator)

    def is_displayed(self):
        """Return True when the org name is displayed."""
        return self.loaded.is_displayed()

    @property
    def name(self):
        """Return the user or organization name."""
        return self.loaded.text.strip()

    @property
    def location(self):
        """Return the current URL."""
        return self.driver.current_url
