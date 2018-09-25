"""The Rice University home page."""

from pypom import Page

from utils.utilities import Utility


class Rice(Page):
    """Rice homepage."""

    URL_TEMPLATE = 'http://www.rice.edu'

    @property
    def at_rice(self):
        """Return True if at Rice's homepage root."""
        return 'rice.edu' in self.selenium.current_url

    def close_tab(self):
        """Close the current tab and switch to the remaining one.

        Assumes 2 browser tabs are open.
        """
        Utility.close_tab(self.driver)
        return self
