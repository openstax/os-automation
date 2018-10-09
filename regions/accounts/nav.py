"""The Accounts admin console nav."""

from time import sleep

from pypom import Region
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from utils.utilities import go_to_


class AccountsNavMenu(Region):
    """Toggle controls shared by the console menus."""

    _mobile_menu_toggle_locator = (By.CSS_SELECTOR, '.dropdown-toggle')
    _first_menu_option_locator = (By.CSS_SELECTOR, 'li:first-child a')
    _second_menu_option_locator = (By.CSS_SELECTOR, 'li:nth-child(2) a')
    _third_menu_option_locator = (By.CSS_SELECTOR, 'li:nth-child(3) a')
    _last_menu_option_locator = (By.CSS_SELECTOR, 'li:last-child a')

    def open(self):
        """Click the toggle to open the menu."""
        self.find_element(*self._mobile_menu_toggle_locator).click()

    @property
    def is_open(self):
        """Return True if the menu is open."""
        return 'open' in self.root.get_attribute('class')

    def _selection_helper(self, locator, destination):
        """Menu option helper for duplicated actions."""
        if not self.is_open:
            self.open()
        self.find_element(*locator).click()
        sleep(1.0)
        return go_to_(destination(self.driver))


class AccountsAdminNav(Region):
    """Navigate the admin console controls."""

    _mobile_menu_toggle_locator = (By.CSS_SELECTOR, '.navbar-toggle')
    _brand_locator = (By.CSS_SELECTOR, '.navbar-brand')
    _users_menu_locator = (By.CSS_SELECTOR, '.nav .dropdown:first-child')
    _security_log_link_locator = (
        By.CSS_SELECTOR, '.nav:not(.navbar-right) > li:nth-child(2) a')
    _salesforce_menu_locator = (By.CSS_SELECTOR, '.nav .dropdown:nth-child(3)')
    _settings_link_locator = (
        By.CSS_SELECTOR, '.nav:not(.navbar-right) > li:nth-child(4) a')
    _banners_menu_locator = (By.CSS_SELECTOR, '.nav .dropdown:nth-child(3)')
    _terms_link_locator = (
        By.CSS_SELECTOR, '.nav:not(.navbar-right) > li:last-child a')
    _console_exit_link_locator = (
        By.CSS_SELECTOR, '.navbar-right > li:first-child a')
    _user_menu_locator = (By.CSS_SELECTOR, '.navbar-right .dropdown')

    @property
    def loaded(self):
        """Return True when the console nav is present."""
        return self.root.is_displayed()

    def is_displayed(self):
        """Return True when the console nav is displayed."""
        try:
            return self.loaded
        except WebDriverException:
            return False

    @property
    def menu_toggle(self):
        """Return the menu toggle element."""
        return self.find_element(*self._mobile_menu_toggle_locator)

    @property
    def menu_is_open(self):
        """Return True if the mobile menu is open."""
        return 'collapsed' not in self.menu_toggle.get_attribute('class')

    @property
    def is_mobile(self):
        """Return True if the menu toggle is displayed."""
        return self.menu_toggle.is_displayed()

    def view_console_home(self):
        """Click on the console brand link."""
        self.find_element(*self._brand_locator).click()
        sleep(1.0)
        from pages.accounts.admin.console import Console
        return go_to_(Console(self.driver))

    @property
    def users(self):
        """Access the Users menu."""
        users_menu_root = self.find_element(*self._users_menu_locator)
        return self.Users(self, users_menu_root)

    def security(self):
        """View the security log."""
        self.find_element(*self._security_log_link_locator).click()
        sleep(1.0)
        from pages.accounts.admin.security import Security
        return go_to_(Security(self.driver))

    @property
    def salesforce(self):
        """Access the Salesforce menu."""
        salesforce_menu_root = self.find_element(
            *self._salesforce_menu_locator)
        return self.Salesforce(self, salesforce_menu_root)

    def settings(self):
        """View the settings for Accounts."""
        self.find_element(*self._settings_link_locator).click()
        sleep(1.0)
        from pages.accounts.admin.settings import Settings
        return go_to_(Settings(self.driver))

    @property
    def banners(self):
        """Access the Banners menu."""
        banners_menu_root = self.find_element(*self._banners_menu_locator)
        return self.Banners(self, banners_menu_root)

    def terms(self):
        """View the contracts for Accounts."""
        self.find_element(*self._terms_link_locator).click()
        sleep(1.0)
        from pages.accounts.admin.contracts import Contracts
        return go_to_(Contracts(self.driver))

    def close_console(self):
        """Close the admin console and return to Accounts."""
        self.find_element(*self._console_exit_link_locator).click()
        sleep(1.0)
        from pages.accounts.profile import Profile
        return go_to_(Profile(self.driver))

    @property
    def user_menu(self):
        """Access the user menu."""
        user_menu_root = self.find_element(*self._user_menu_locator)
        return self.UserMenu(self, user_menu_root)

    class Users(AccountsNavMenu):
        """The user menu actions."""

        def view_search(self):
            """View the user search."""
            from pages.accounts.admin.users import Search
            return self._selection_helper(
                self._first_menu_option_locator,
                Search)

        def view_actions(self):
            """View user record action."""
            from pages.accounts.admin.users import Actions
            return self._selection_helper(
                self._second_menu_option_locator,
                Actions)

        def view_accounts_in_preauth(self):
            """View the accounts in a pre-authorization state."""
            from pages.accounts.admin.users import PreAuth
            return self._selection_helper(
                self._third_menu_option_locator,
                PreAuth)

        def view_reports(self):
            """View user account totals."""
            from pages.accounts.admin.users import Reports
            return self._selection_helper(
                self._last_menu_option_locator,
                Reports)

    class Salesforce(AccountsNavMenu):
        """The Salesforce options menu."""

        def view_setup(self):
            """View the Salesforce user info."""
            from pages.accounts.admin.salesforce import Setup
            return self._selection_helper(
                self._first_menu_option_locator,
                Setup)

        def view_actions(self):
            """View the Salesforce account actions."""
            from pages.accounts.admin.salesforce import Actions
            return self._selection_helper(
                self._last_menu_option_locator,
                Actions)

    class Banners(AccountsNavMenu):
        """The Accounts banner control menu."""

        def see_active(self):
            """View active banner notifications."""
            from pages.accounts.admin.banners import Active
            return self._selection_helper(
                self._first_menu_option_locator,
                Active)

        def create_new_banner(self):
            """View the new banner setup form."""
            from pages.accounts.admin.banners import Create
            return self._selection_helper(
                self._last_menu_option_locator,
                Create)

    class UserMenu(AccountsNavMenu):
        """The console admin user menu."""

        _sign_out_locator = (By.CSS_SELECTOR, '.dropdown-menu a')

        def sign_out(self):
            """Log out of Accounts."""
            from pages.accounts.home import AccountsHome
            return self._selection_helper(
                self._sign_out_locator,
                AccountsHome)
