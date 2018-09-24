"""The Subjects page."""

from time import sleep

from pypom import Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility


class Subjects(WebBase):
    """The subjects page."""

    URL_TEMPLATE = '/subjects'

    _root_locator = (By.ID, 'main')
    _banner_locator = (By.CSS_SELECTOR, '.loaded .hero')
    _book_locator = (By.CSS_SELECTOR, 'div.book-category:not(.hidden) .cover')
    _image_locators = (By.CSS_SELECTOR, _book_locator[1] + ' img')

    @property
    def loaded(self):
        """Override the base loader."""
        print('Subjects')
        print(self._image_locators,
              Utility.is_image_visible(self.driver,
                                       locator=self._image_locators))
        return (
            bool(self.find_element(*self._root_locator))
            and Utility.is_image_visible(self.driver,
                                         locator=self._image_locators))

    def is_displayed(self):
        """Return True if the subjects page is displayed."""
        if self.URL_TEMPLATE not in self.location:
            print(self.location)
            return False
        return self.loaded

    @property
    def _active_books(self):
        """Select active books for use by the class."""
        return [self.Book(self, book)
                for book in self.find_elements(*self._book_locator)]

    @property
    def openstax_books(self):
        """Select active books while excluding Polish versions."""
        return [book for book in self._active_books
                if book.language == 'english']

    @property
    def polish_books(self):
        """Select active books in Polish."""
        return [book for book in self._active_books
                if book.language == 'polish']

    def select_random_book(self, all_books=False):
        """Return a random book from the active list."""
        using = self._active_books if all_books else self.openstax_books
        total = len(using) - 1
        book = Utility.random(0, total)
        selected = using[book]
        destination = selected.url_append
        selected.click()
        sleep(1.0)
        from pages.web.book import Book as Details
        return Details(self.driver, book_name=destination)

    class Book(Region):
        """A single book title."""

        _url_locator = (By.TAG_NAME, 'a')
        _image_locator = (By.TAG_NAME, 'img')

        @property
        def title(self):
            """Return the book title."""
            return self.find_element(*self._image_locator).get_attribute('alt')

        @property
        def url(self):
            """Return the book URL."""
            return self.find_element(*self._url_locator).get_attribute('href')

        @property
        def url_append(self):
            """Return the last part of the URL."""
            return self.url.split('/')[-1]

        @property
        def language(self):
            """Return the book language."""
            if 'Fizyka' in self.title:
                return 'polish'
            return 'english'
