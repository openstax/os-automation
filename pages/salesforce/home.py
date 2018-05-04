"""Salesforce placeholder."""
from pypom import Page
from selenium.webdriver.common.by import By


class Salesforce(Page):
    """OpenStax Salesforce help homepage."""

    URL_TEMPLATE = 'http://openstax.force.com/help/'

    _loader_locator = (By.ID, 'base')

    @property
    def loaded(self):
        """Override the load check."""
        print(self.find_element(*self._loader_locator))
        return self.find_element(*self._loader_locator)

    def wait_for_page_to_load(self):
        """Override page load."""
        self.wait.until(lambda _: self.loaded)

    @property
    def at_salesforce(self):
        """Return True if at the OpenStax Salesforce help page."""
        return 'force.com' in self.selenium.current_url
