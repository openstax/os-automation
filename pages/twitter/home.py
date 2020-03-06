"""The OpenStax Twitter landing page."""

from time import sleep

from pypom import Page
from selenium.webdriver.common.by import By


class Twitter(Page):
    """The OpenStax Twitter feed."""

    URL_TEMPLATE = 'https://twitter.com/openstax'

    _body_tag_locator = (
        By.CSS_SELECTOR, 'body')
    _username_locator = (
        By.CSS_SELECTOR, 'a[href*=OpenStax][role=link]')

    @property
    def loaded(self):
        """Return True if the username is found."""
        self.wait.until(
            lambda _: self.find_elements(*self._body_tag_locator))
        script = (r'document.addEventListener("load", function(event) {});')
        sleep(0.5)
        return (self.driver.execute_script(script) or
                bool(self.find_elements(*self._username_locator)))

    def is_displayed(self):
        """Return True if the main content is loaded."""
        return self.find_element(*self._username_locator).is_displayed()

    @property
    def location(self):
        """Return the current URL."""
        return self.driver.current_url
