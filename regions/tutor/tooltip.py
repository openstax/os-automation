"""An OpenStax Tutor Beta tooltip region."""

from time import sleep

from pypom import Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from utils.utilities import Utility


class Tooltip(Region):
    """An individual tooltip pane."""

    _joyride_root_selector = '.joyride'
    _heading_locator = (By.CSS_SELECTOR, '.heading , [class*="__header"]')
    _subheading_locator = (By.CSS_SELECTOR, '.sub-heading')
    _content_locator = (By.CSS_SELECTOR, '[class*=main] p')
    _column_locator = (By.CSS_SELECTOR, '.column')
    _close_tooltip_locator = (By.CSS_SELECTOR, '[class*=close]')
    _previous_button_locator = (By.CSS_SELECTOR, '[class*="--secondary"]')
    _continue_button_locator = (By.CSS_SELECTOR, '[class*="--primary"]')
    _view_later_button_locator = (By.CSS_SELECTOR, '[class*="--skip"]')

    @property
    def title(self):
        """Return the heading text."""
        return self.find_element(*self._heading_locator).text

    @property
    def subtitle(self):
        """Return the subheading text."""
        try:
            return self.find_element(*self._subheading_locator).text
        except NoSuchElementException:
            return ""

    @property
    def content(self):
        """Return the standard tooltip content."""
        try:
            return self.find_element(*self._content_locator).text
        except NoSuchElementException:
            return ""

    @property
    def columns(self):
        """Access the tooltip columns."""
        return [self.Column(self, column)
                for column in self.find_elements(*self._column_locator)]

    @property
    def window_close(self):
        """Return the 'x' close button."""
        return self.find_element(*self._close_tooltip_locator)

    def close(self):
        """Click on the window close button."""
        Utility.click_option(self.driver, element=self.window_close)
        return self.page(self.driver, self.page.base_url)

    @property
    def previous_tooltip(self):
        """Return the 'Back' button."""
        return self.find_element(*self._continue_button_locator)

    def previous(self):
        """Click on the 'Back' button."""
        Utility.click_option(self.driver, element=self.previous_tooltip)
        sleep(0.5)
        tooltip = self.driver.execute_script(
            "return document.querySelector({0});"
            .format(self._joyride_root_selector))
        return Tooltip(self.page, tooltip)

    @property
    def next_tooltip(self):
        """Return the 'Continue', 'Next #/#', or 'Got It' button."""
        return self.find_element(*self._continue_button_locator)

    def next(self):
        """Click on the 'Continue', 'Next', or 'Got It' button."""
        Utility.click_option(self.driver, element=self.next_tooltip)
        sleep(0.5)
        tooltip = self.driver.execute_script(
            "return document.querySelector({0});"
            .format(self._joyride_root_selector))
        if tooltip:
            return Tooltip(self.page, tooltip)
        return self.page(self.driver, self.page.base_url)

    @property
    def skip(self):
        """Return the 'View later' button."""
        return self.find_element(*self._view_later_button_locator)

    def view_later(self):
        """Click on the 'View later' button."""
        Utility.click_option(self.driver, element=self.skip)
        return self.page(self.driver, self.page.base_url)

    class Column(Region):
        """A display column."""

        _title_locator = (By.CSS_SELECTOR, 'h3')
        _text_locator = (By.CSS_SELECTOR, 'p')

        @property
        def title(self):
            """Return the column title."""
            return self.find_element(*self._title_locator).text

        @property
        def text(self):
            """Return the explanation text."""
            return self.find_element(*self._text_locator).text
