"""OpenStax Web's sticky note region."""

from time import sleep

from pypom import Region
from selenium.webdriver.common.by import By


class StickyNote(Region):
    """OpenStax Web's sticky note region."""

    _root_locator = (By.TAG_NAME, 'sticky_note')
    _display_locator = (By.CSS_SELECTOR, '[role=alert]')
    _close_button_locator = (By.TAG_NAME, 'button')
    _link_locator = (By.TAG_NAME, 'a')

    @property
    def is_displayed(self):
        """Return True if the sticky note is currently displayed."""
        return self.find_element(*self._display_locator).is_displayed

    @property
    def close(self):
        """Close the sticky note."""
        self.find_element(*self._close_button_locator).click()
        sleep(1.0)
        from pages.web.home import WebHome
        return WebHome(self.driver)

    @property
    def button(self):
        """Return the sticky note action button."""
        return self.find_element(*self._link_locator)

    def go(self):
        """Follow the sticky note link."""
        destination = self.button.get_attribute('href')
        self.button.click()
        sleep(1.0)
        if 'give' in destination:
            from pages.web.give import Donate
            return Donate(self.driver)

        # if the destination is new and unknown, return the home page
        from pages.web.home import WebHome
        return WebHome(self.driver)
