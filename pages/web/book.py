"""A marketing page for an OpenStax book."""

from time import sleep

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Book(WebBase):
    """A book details page."""

    URL_TEMPLATE = '/details/books/{book_name}'

    _root_locator = (By.TAG_NAME, 'main')
    _banner_locator = (By.CLASS_NAME, 'title-image')
    _adoption_link_locator = (By.CSS_SELECTOR, '.let-us-know .link')
    _interest_link_locator = (By.CSS_SELECTOR, '.let-us-know .top')

    @property
    def title(self):
        """Return the book title."""
        return self.find_element(*self._banner_locator).get_attribute('alt')

    def is_using(self):
        """Click the adoption report link."""
        self.find_element(*self._adoption_link_locator).click()
        sleep(1.0)
        from pages.web.adoption import Adoption
        return Adoption(self.driver)

    def is_interested(self):
        """Click the interest report link."""
        self.find_element(*self._interest_link_locator).click()
        sleep(1.0)
        from pages.web.interest import Interest
        return Interest(self.driver)
