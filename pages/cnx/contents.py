"""Content pages under CNX."""

from pypom import Page
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from utils.utilities import Utility


class Webview(Page):
    """A CNX book view."""

    _main_locator = (By.CSS_SELECTOR, '.main-page')
    _image_locator = (By.CSS_SELECTOR, 'img')
    _title_locator = (By.CSS_SELECTOR, '.large-header')

    @property
    def loaded(self):
        """Override the loaded property."""
        try:
            main = self.find_element(*self._main_locator)
            images = self.find_elements(*self._image_locator)
            return (
                Utility.has_children(main) and
                Utility.is_image_visible(self.driver, image=images)
            )
        except WebDriverException:
            return False

    def is_displayed(self):
        """Return True if the page is loaded and CNX is in the URL."""
        return self.loaded and 'cnx.org' in self.location

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
    def title(self):
        """Return the book title."""
        return self.find_element(*self._title_locator).text.strip()
