"""An Amazon book order landing page."""

from pypom import Page

from utils.utilities import Utility


class Amazon(Page):
    """An Amazon book order page."""

    URL_TEMPLATE = 'https://www.amazon.com/'

    @property
    def loaded(self):
        """Return True if Amazon is in the current URL."""
        return 'amazon' in self.location

    def is_displayed(self):
        """Return True if the main content is loaded."""
        return ('openstax' in self.driver.page_source.lower() and
                self.loaded)

    def close_tab(self):
        """Close the current tab and switch to the remaining one.

        Assumes 2 browser tabs are open.
        """
        Utility.close_tab(self.driver)
        return self

    @property
    def location(self):
        """Return the current URL."""
        return self.driver.current_url
