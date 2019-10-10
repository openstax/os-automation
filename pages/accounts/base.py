"""Basic page parent for all Accounts pages."""

from time import sleep

from pypom import Page, Region
from selenium.webdriver.common.by import By

from pages.rice.home import Rice
from utils.utilities import Utility


class AccountsBase(Page):
    """Base class."""

    _root_locator = (By.CSS_SELECTOR, 'body')
    _root_locator_logged_in = (By.ID, 'application-header')

    @property
    def loaded(self):
        """Override the default loaded function."""
        return (self.find_element(*self._root_locator) and
                Utility.load_background_images(self.driver,
                                               self._root_locator) and
                'accounts' in self.driver.current_url)

    def is_displayed(self):
        """Return True when Accounts is loaded."""
        return self.loaded

    @property
    def header(self):
        """Return Accounts' header."""
        return self.Header(self)

    @property
    def footer(self):
        """Return Accounts' footer."""
        return self.Footer(self)

    @property
    def current_url(self):
        """Return the current page URL."""
        return self.driver.current_url

    def reload(self):
        """Reload the current page."""
        self.driver.refresh()
        self.wait_for_page_to_load()

    def back(self):
        """Go back to the previous page."""
        self.driver.execute_script('window.history.go(-1)')
        return self

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

    @property
    def url(self):
        """Return the last segment of the current URL."""
        return self.location.split('/')[-1]

    def resize_window(self, width=1024, height=768):
        """Set the browser window size.

        Args:
            width (int): browser window width, default 4:3
            height (int): browser window height, default 4:3

        """
        self.driver.set_window_size(width, height)
        sleep(1.5)

    @property
    def is_safari(self):
        """Return True if the browser in use is Safari."""
        return self.driver.capabilities.get('browserName').lower() == 'safari'

    class Header(Region):
        """Accounts header."""

        _root_locator = (By.ID, 'application-header')
        _logo_locator = (By.ID, 'top-nav-logo')

        @property
        def is_header_displayed(self):
            """Header display boolean."""
            return self.loaded

        def go_to_accounts_home(self):
            """Follow the OpenStax icon link back to the site root."""
            go_home = self.find_element(*self._logo_locator)
            Utility.click_option(self.driver, element=go_home)
            return self

    class Footer(Region):
        """Accounts footer."""

        _root_locator = (By.ID, 'application-footer')
        _rice_link_locator = (By.CSS_SELECTOR, '#footer-rice-logo img')
        _copyright_locator = (By.PARTIAL_LINK_TEXT, 'Copyright')
        _terms_locator = (By.PARTIAL_LINK_TEXT, 'Terms')

        @property
        def is_footer_displayed(self):
            """Footer display boolean."""
            return self.loaded

        @property
        def show_copyright(self):
            """Display the copyright."""
            copyright = self.find_element(*self._copyright_locator)
            Utility.click_option(self.driver, element=copyright)
            return self

        @property
        def show_terms_of_use(self):
            """Display the terms of use."""
            terms = self.find_element(*self._terms_locator)
            Utility.click_option(self.driver, element=terms)
            sleep(1.0)
            return self

        def go_to_rice(self):
            """Load the Rice webpage."""
            rice = self.find_element(*self._rice_link_locator)
            Utility.click_option(self.driver, element=rice)
            return Rice(self.driver)
