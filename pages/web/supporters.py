"""The foundation and corporate supporters page."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Supporters(WebBase):
    """The foundation and corporate supporters page."""

    URL_TEMPLATE = '/foundation'

    _title_locator = (By.CSS_SELECTOR, '.hero h1')
    _blurb_locator = (By.CSS_SELECTOR, '.hero p')
    _supporter_locator = (By.CSS_SELECTOR, '.funder h2')

    @property
    def loaded(self):
        """Return whether the hero banner is found."""
        return (
            self.find_element(*self._title_locator) and
            self.find_element(*self._supporter_locator))

    def is_displayed(self):
        """Return True if the supporters page is displayed."""
        return self.find_element(*self._title_locator).is_displayed()

    @property
    def title(self):
        """Return the banner title."""
        return self.find_element(*self._title_locator).text.strip()

    @property
    def blurb(self):
        """Return the subheading text."""
        return self.find_element(*self._blurb_locator).text.strip()

    @property
    def supporters(self):
        """Return the list of funders."""
        return [funder.text.strip()
                for funder in self.find_elements(*self._supporter_locator)]
