"""A Bookshare book order landing page."""

from pypom import Page

from utils.utilities import Utility


class Bookshare(Page):
    """An Bookshare book page."""

    URL_TEMPLATE = 'https://www.bookshare.org/'

    _book_details_locator = ('class name', 'bookDetail')

    @property
    def loaded(self):
        """Return True if Bookshare is in the current URL."""
        return ('bookshare' in self.location and
                'openstax' in self.driver.page_source.lower())

    def is_displayed(self):
        """Return True if the main content is loaded."""
        return self.find_element(*self._book_details_locator).is_displayed()

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
