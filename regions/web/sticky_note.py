"""OpenStax Web's sticky note region."""

from time import sleep

from pypom import Region
from selenium.common.exceptions import NoSuchElementException, WebDriverException  # NOQA
from selenium.webdriver.common.by import By

from utils.utilities import Utility
from utils.web import Web as Support, WebException


class StickyNote(Region):
    """OpenStax Web's sticky note region."""

    _root_locator = (By.CSS_SELECTOR, '#lower-sticky-note')
    _close_button_locator = (By.CSS_SELECTOR, '.put-away')
    _link_destination_locator = (By.CSS_SELECTOR, 'a')
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
        locator = (self._mobile_link_locator
                   if self.driver.get_window_size().get('width') <= 600
                   else self._desktop_link_locator)
        try:
            return self.find_element(*locator)
        except NoSuchElementException:
            raise WebException('The sticky note button was not found.')

    def go(self):
        """Follow the sticky note link.

        Return a 'Destination' so the function will fail if
        a new link is added.
        """
        destination = (self.find_element(*self._link_destination_locator)
                       .get_attribute('href'))
        try:
            self.button.click()
        except WebDriverException:
            sleep(1.0)
            Utility.click_option(self.driver, element=self.button)
        sleep(1.0)
        if Support.GIVE in destination:
            from pages.web.donation import Give as Destination
        return Destination(self.driver)
