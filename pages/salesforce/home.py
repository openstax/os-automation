"""Salesforce support page."""

from pypom import Page
from selenium.webdriver.common.by import By

from utils.utilities import Utility


class Salesforce(Page):
    """OpenStax Salesforce help homepage."""

    URL_TEMPLATE = 'http://openstax.force.com/help/'

    _loader_locator = (By.CSS_SELECTOR, '.articleHeader')
    _title_locator = (By.CSS_SELECTOR, '.articleTitle')

    @property
    def loaded(self):
        """Override the basic loader."""
        return self.find_element(*self._loader_locator)

    @property
    def at_salesforce(self):
        """Return True if at the OpenStax Salesforce help page."""
        return 'force.com' in self.selenium.current_url

    @property
    def title(self):
        """Return the article title."""
        self.wait.until(lambda _: self.find_element(*self._title_locator)
                        .is_displayed())
        return self.find_element(*self._title_locator).text.strip()

    def close_tab(self):
        """Close the current tab and switch to the remaining one.

        Assumes 2 browser tabs are open.
        """
        Utility.close_tab(self.driver)
        return self
