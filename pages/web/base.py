"""Basic page parent for all OpenStax Web pages."""

from time import sleep

from pypom import Page
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

from regions.web.footer import Footer
from regions.web.openstax_nav import OpenStaxNav
from regions.web.sticky_note import StickyNote
from regions.web.web_nav import WebNav
from utils.utilities import Utility


class WebBase(Page):
    """Base class."""

    _root_locator = (By.CSS_SELECTOR, 'body.page-loaded')

    def __init__(self, driver, base_url=None, timeout=60, **url_kwargs):
        """Override the initialization to hold onto the Web timeout."""
        super(WebBase, self).__init__(driver, base_url, timeout, **url_kwargs)

    @property
    def loaded(self):
        """Return True when the page-loaded class is added to the body tag."""
        return self.root.is_displayed()

    @property
    def sticky_note(self):
        """Access the sticky note."""
        return StickyNote(self)

    @property
    def openstax_nav(self):
        """Access the OpenStax header navigation."""
        return OpenStaxNav(self)

    @property
    def web_nav(self):
        """Access the website header navigation."""
        return WebNav(self)

    @property
    def footer(self):
        """Return Web footer."""
        return Footer(self)

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
