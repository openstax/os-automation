"""Rice e-Bank donation acceptance form site."""


from pypom import Page
from selenium.webdriver.common.by import By


class EBank(Page):
    """The Rice University donation system."""

    URL_TEMPLATE = 'https://ebank.rice.edu/'

    _amount_header_locator = (By.CSS_SELECTOR, '#upayAmountHeader')

    @property
    def loaded(self):
        """Return True if ebank is in the current URL."""
        return 'ebank.rice' in self.driver.current_url

    def is_displayed(self):
        """Return True if the amount header is displayed."""
        return self.find_element(*self._amount_header_locator).is_displayed()

    @property
    def location(self):
        """Return the current URL."""
        return self.driver.current_url
