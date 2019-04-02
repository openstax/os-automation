"""The Tutor base objects."""

from time import sleep

from pypom import Page, Region
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

from regions.tutor.nav import TutorNav
from utils.utilities import Utility, go_to_, go_to_external_


class TutorShared(Page):
    """Shared base page functions."""

    _root_locator = (By.CSS_SELECTOR, 'body')
    _nav_locator = (By.CSS_SELECTOR, '.navbar')

    def __init__(self, driver, base_url=None, timeout=60, **url_kwargs):
        """Override the initialization to hold onto the Tutor timeout."""
        super(TutorBase, self) \
            .__init__(driver, base_url, timeout, **url_kwargs)

    @property
    def loaded(self):
        """Override the default loaded function."""
        return self.find_element(*self._root_locator)

    def is_displayed(self):
        """Return True when the Tutor page is loaded."""
        return self.loaded.is_displayed()

    @property
    def nav(self):
        """Access the page nav."""
        nav = self.find_element(*self._nav_locator)
        return self.Nav(self, nav)

    def reload(self):
        """Reload the current page.

        Ignore stale element issues because we're reloading the page;
        everything is going to be stale if accessed too quickly
        (multi-process Firefox issue).
        """
        try:
            self.driver.execute_script('location.reload();')
            self.wait_for_page_to_load()
        except StaleElementReferenceException:
            pass
        sleep(1.0)
        return self

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


class TutorLoginBase(TutorShared):
    """The base page for the Tutor URI root.

    Used for `/` and `/terms`
    """

    _footer_locator = (By.CSS_SELECTOR, 'footer')

    @property
    def footer(self):
        """Access the page footer."""
        footer = self.find_element(*self._footer_locator)
        return self.Footer(self, footer)

    class Nav(Region):
        """The log in base navigation."""

        _home_locator = (By.CSS_SELECTOR, '.navbar-brand')
        _help_link_locator = (By.CSS_SELECTOR, '[href*="force.com"]')
        _rice_link_locator = (By.CSS_SELECTOR, '.navbar-brand-rice')

        @property
        def logo(self):
            """Return the Tutor Beta logo."""
            return self.find_element(*self._home_locator)

        def go_home(self):
            """Click on the logo."""
            Utility.safari_exception_click(self.driver, element=self.logo)
            return go_to_(self.page)

        def view_help_articles(self):
            """Click on the Help link to view Salesforce articles."""
            link = self.find_element(*self._help_link_locator)
            url = link.get_attribute('href')
            Utility.switch_to(self.driver, element=link)
            from pages.salesforce.home import Salesforce
            return go_to_external_(Salesforce(self.driver), url)

        @property
        def rice_logo(self):
            """Return the Rice University logo."""
            return self.find_element(*self._rice_link_locator)

        def go_to_rice(self):
            """Click on the Rice logo to view the Rice University home page."""
            logo = self.rice_logo
            url = logo.get_attribute('href')
            Utility.switch_to(self.driver, element=logo)
            from pages.rice.home import Rice
            return go_to_external_(Rice(self.driver), url)

    class Footer(Region):
        """The log in base footer."""

        _rice_link_locator = (By.CSS_SELECTOR, 'a:first-child')
        _terms_link_locator = (By.CSS_SELECTOR, '[href$=terms]')

        def go_to_rice(self):
            """Click the Rice University link."""
            link = self.find_element(*self._rice_link_locator)
            url = link.get_attribute('href')
            Utility.switch_to(self.driver, element=link)
            from pages.rice.home import Rice
            return go_to_external_(Rice(self.driver), url)

        def view_terms(self):
            """View the general Tutor terms of service and privacy policy."""
            link = self.find_element(*self._terms_link_locator)
            Utility.safari_exception_click(self.driver, element=link)
            from pages.tutor.legal import Terms
            return go_to_(Terms(self.driver, base_url=self.page.base_url))


class TutorBase(TutorShared):
    """The base page for the Tutor app."""

    class Nav(TutorNav):
        """Use the shared region Tutor navigation."""

        pass
