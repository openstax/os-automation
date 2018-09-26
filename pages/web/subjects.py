"""The Subjects page."""

from time import sleep

from pypom import Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility
from utils.web import Web


class Subjects(WebBase):
    """The subjects page."""

    URL_TEMPLATE = '/subjects'
    category_xpath = '//div[h2[text()="{subject}"]]'

    _root_locator = (By.ID, 'main')
    _banner_locator = (By.CSS_SELECTOR, '.loaded .hero')
    _filter_by_locator = (By.CSS_SELECTOR,
                          '.filter-buttons [aria-pressed=true]')
    _math_category_locator = (
        By.XPATH, category_xpath.format(subject=Web.VIEW_MATH))
    _science_category_locator = (
        By.XPATH, category_xpath.format(subject=Web.VIEW_SCIENCE))
    _social_sciences_category_locator = (
        By.XPATH, category_xpath.format(subject=Web.VIEW_SOCIAL_SCIENCE))
    _humanities_category_locator = (
        By.XPATH, category_xpath.format(subject=Web.VIEW_HUMANITIES))
    _business_category_locator = (
        By.XPATH, category_xpath.format(subject=Web.VIEW_BUSINESS))
    _ap_category_locator = (
        By.XPATH, category_xpath.format(subject=Web.VIEW_AP.replace('®', '')))
    _book_locator = (By.CSS_SELECTOR, 'div.book-category:not(.hidden) .cover')
    _image_locators = (By.CSS_SELECTOR, _book_locator[1] + ' img')

    @property
    def loaded(self):
        """Override the base loader."""
        return (
            bool(self.find_element(*self._root_locator))
            and Utility.is_image_visible(self.driver,
                                         locator=self._image_locators))

    def is_displayed(self):
        """Return True if the subjects page is displayed."""
        if self.URL_TEMPLATE not in self.location:
            return False
        return self.loaded

    def filtered_by(self, filter_):
        """Return True if the books are filtered by the submitted subject."""
        return filter_ in self.find_element(*self._filter_by_locator).text

    @property
    def math(self):
        math_root = self.find_element(*self._math_category_locator)
        return self.Category(self, math_root)

    @property
    def science(self):
        science_root = self.find_element(*self._science_category_locator)
        return self.Category(self, science_root)

    @property
    def social_sciences(self):
        social_root = self.find_element(
            *self._social_sciences_category_locator)
        return self.Category(self, social_root)

    @property
    def humanities(self):
        humanities_root = self.find_element(*self._humanities_category_locator)
        return self.Category(self, humanities_root)

    @property
    def business(self):
        business_root = self.find_element(*self._business_category_locator)
        return self.Category(self, business_root)

    @property
    def ap(self):
        ap_root = self.find_element(*self._ap_category_locator)
        return self.Category(self, ap_root)

    @property
    def _active_books(self):
        """Select active books for use by the class."""
        return [Book(self, book)
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

    class Category(Region):
        """Subject category information."""

        _book_locator = (By.CSS_SELECTOR, '.cover')

        @property
        def is_visible(self):
            """Return True if the category is displayed."""
            return 'hidden' not in self.root.get_attribute('class')

        @property
        def books(self):
            """Return category books."""
            return [Book(self, book)
                    for book in self.find_elements(*self._book_locator)]


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
