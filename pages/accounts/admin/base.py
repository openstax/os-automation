"""Base class for the Accounts administrator console."""

from pypom import Page
from selenium.webdriver.common.by import By

from regions.accounts.nav import AccountsAdminNav
from utils.utilities import Utility


class AccountsAdmin(Page):
    """Accounts admin console base."""

    URL_TEMPLATE = '/admin'

    _root_locator = (By.CSS_SELECTOR, '.admin')
    _nav_locator = (By.CSS_SELECTOR, 'nav.navbar.navbar-default')

    @property
    def loaded(self):
        """Return True when the console is loaded and the nav is displayed."""
        return (bool(self.find_elements(*self._root_locator)) and
                self.nav.is_displayed())

    def is_displayed(self):
        """Return True when the console is loaded."""
        return self.loaded

    @property
    def nav(self):
        """Access the admin console navigation menu."""
        nav_root = self.find_element(*self._nav_locator)
        return AccountsAdminNav(self, nav_root)

    def close_tab(self):
        """Close the current tab and switch to the remaining one.

        Assumes 2 browser tabs are open.
        """
        Utility.close_tab(self.driver)
        return self
