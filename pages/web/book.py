"""A marketing page for an OpenStax book."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility, go_to_


class Book(WebBase):
    """A book details page."""

    URL_TEMPLATE = '/details/books/{book_name}'

    _root_locator = (By.TAG_NAME, 'main')
    _banner_locator = (By.CLASS_NAME, 'title-image')
    _adoption_link_locator = (By.CSS_SELECTOR, '.let-us-know .link')
    _interest_link_locator = (By.CSS_SELECTOR, '.let-us-know .top')

    _content_locator = (By.CSS_SELECTOR, '.details-tab')
    _instructor_locator = (By.CSS_SELECTOR, '.instructor-resources')
    _student_locator = (By.CSS_SELECTOR, '.student-resources')

    @property
    def root(self):
        """Return the base node for the content."""
        return self.find_element(*self._root_locator)

    @property
    def loaded(self):
        """Return True when the book details page is loaded."""
        details = self.find_element(*self._content_locator)
        instructor = self.find_element(*self._instructor_locator)
        student = self.find_element(*self._student_locator)
        return (
            Utility.is_image_visible(
                self.driver, image=self.find_element(*self._banner_locator))
            and Utility.has_children(details)
            and Utility.has_children(instructor)
            and Utility.has_children(student)
        )

    def is_displayed(self):
        """Return True if the book details banner image is displayed."""
        return self.find_element(*self._banner_locator).is_displayed()

    @property
    def title(self):
        """Return the book title."""
        return self.find_element(*self._banner_locator).get_attribute('alt')

    def is_using(self):
        """Click the adoption report link."""
        Utility.safari_exception_click(
            self.driver, locator=self._adoption_link_locator)
        from pages.web.adoption import Adoption
        return go_to_(Adoption(self.driver))

    def is_interested(self):
        """Click the interest report link."""
        Utility.safari_exception_click(
            self.driver, locator=self._interest_link_locator)
        from pages.web.interest import Interest
        return go_to_(Interest(self.driver))
