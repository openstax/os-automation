"""The Rice University home page."""

from pypom import Page

from utils.utilities import Utility


class Rice(Page):
    """Rice homepage."""

    URL_TEMPLATE = 'http://www.rice.edu'

    _rice_banner_logo_locator = ('css selector', '.header__logo')

    @property
    def at_rice(self):
        """Return True if at Rice's homepage root."""
        return 'rice.edu' in self.driver.current_url

    @property
    def loaded(self) -> bool:
        """Return True when the Rice banner logo is found.

        :return: ``True`` when the header logo is found
        :rtype: bool

        """
        return bool(self.find_elements(*self._rice_banner_logo_locator))

    def close_tab(self):
        """Close the current tab and switch to the remaining one.

        Assumes 2 browser tabs are open.
        """
        Utility.close_tab(self.driver)
        return self
