"""OpenStax Web's sticky note region."""

from time import sleep

from pypom import Region
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from utils.web import Web as Support


class StickyNote(Region):
    """OpenStax Web's sticky note region."""

    _root_locator = (By.TAG_NAME, 'sticky-note')
    _close_button_locator = (By.TAG_NAME, 'button')
    _link_destination_locator = (By.TAG_NAME, 'a')
    _mobile_link_locator = (By.CSS_SELECTOR, 'img.mobile')
    _desktop_link_locator = (By.CSS_SELECTOR, 'img.desktop')

    def is_displayed(self):
        """Return True if the sticky note is currently displayed."""
        return self.root.is_displayed()

    def close(self):
        """Close the sticky note."""
        try:
            self.find_element(*self._close_button_locator).click()
        except WebDriverException:
            sleep(1.0)
            self.find_element(*self._close_button_locator).click()
        sleep(1.0)
        from pages.web.home import WebHome
        return WebHome(self.driver)

    @property
    def button(self):
        """Return the sticky note action button."""
        if self.driver.get_window_size().get('width') <= 600:
            return self.find_element(*self._mobile_link_locator)
        return self.find_element(*self._desktop_link_locator)

    def go(self):
        """Follow the sticky note link.

        Return a 'Destination' so the function will fail if
        a new link is added.
        """
        destination = (self.find_element(*self._link_destination_locator)
                       .get_attribute('href'))
        for _ in range(10):
            try:
                self.button.click()
                break
            except WebDriverException:
                sleep(1.0)
        sleep(1.0)
        if Support.GIVE in destination:
            from pages.web.donation import Give as Destination
        return Destination(self.driver)
