"""Salesforce support page."""

from time import sleep

from pypom import Page
from selenium.webdriver.common.by import By


class Salesforce(Page):
    """OpenStax Salesforce help homepage."""

    URL_TEMPLATE = 'http://openstax.force.com/help/'

    _loader_locator = (By.CSS_SELECTOR, 'body')

    def wait_for_page_to_load(self):
        """Override page load."""
        sleep(1.0)
        self.wait.until(lambda _: self.find_element(*self._loader_locator))

    @property
    def at_salesforce(self):
        """Return True if at the OpenStax Salesforce help page."""
        return 'force.com' in self.selenium.current_url
