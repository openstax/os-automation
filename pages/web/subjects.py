"""The Subjects page."""

from time import sleep

from pypom import Region
from pypom.exception import UsageError
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.web.base import WebBase
from utils.utilities import Utility, go_to_
from utils.web import Library, Web, WebException


class Subjects(WebBase):
    """The subjects page."""

    URL_TEMPLATE = '/subjects'
    AUTHORS = 0
    SEQUENCE = 1
    PEER_REVIEWED = 2

    category_xpath = '//div[h2[text()="{subject}"]]'

    _loader_locator = (By.CSS_SELECTOR, '.subjects-page.loaded')
    _banner_locator = (By.CSS_SELECTOR, '.hero')
    _slogan_locator = (By.CSS_SELECTOR, '.hero h2')
    _blurb_locator = (By.CSS_SELECTOR, '.hero p')
    _filter_toggle_locator = (By.CSS_SELECTOR, '.filter-buttons')
    _filter_button_locator = (By.CLASS_NAME, 'filter-button')
    _filter_by_locator = (By.CSS_SELECTOR,
                          '.filter-buttons [aria-pressed=true]')
    _about_our_textbooks_locator = (By.CSS_SELECTOR, '.text-content')
    _about_blurb_locator = (By.CSS_SELECTOR, '.text-content ~ div .blurb')

    _category_locator = (By.CSS_SELECTOR, '.book-category')
    _math_category_locator = (
        By.XPATH, category_xpath.format(subject=Web.VIEW_MATH))
    _science_category_locator = (
        By.XPATH, category_xpath.format(subject=Web.VIEW_SCIENCE))
    _social_sciences_category_locator = (
        By.XPATH, category_xpath.format(subject=Web.VIEW_SOCIAL_SCIENCES))
    _humanities_category_locator = (
        By.XPATH, category_xpath.format(subject=Web.VIEW_HUMANITIES))
    _business_category_locator = (
        By.XPATH, category_xpath.format(subject=Web.VIEW_BUSINESS))
    _essentials_category_locator = (
        By.XPATH, category_xpath.format(subject=Web.VIEW_ESSENTIALS))
    _ap_category_locator = (
        By.XPATH, category_xpath.format(subject=Web.VIEW_AP.replace('®', '')))
    _book_locator = (By.CSS_SELECTOR, 'div.book-category:not(.hidden) .cover')
    _image_locators = (By.CSS_SELECTOR, _book_locator[1] + ' img')

    @property
    def loaded(self):
        """Override the base loader."""
        return (
            self.find_element(*self._loader_locator) and
            self.find_element(*self._category_locator) and
            Utility.is_image_visible(self.driver,
                                     locator=self._image_locators))

    def wait_for_page_to_load(self):
        """Override the page wait."""
        WebDriverWait(self.driver, 15).until(
            lambda _: self.loaded)
        self.pm.hook.pypom_after_wait_for_page_to_load(page=self)
        return self

    def open(self):
        """Open the page."""
        if self.seed_url:
            tries = 0
            while tries < 1:
                try:
                    self.driver_adapter.open(self.seed_url)
                    self.wait_for_page_to_load()
                    break
                except WebDriverException:
                    tries = tries + 1
            return self
        raise UsageError("Set a base URL or URL_TEMPLATE to open this page.")

    def is_displayed(self):
        """Return True if the subjects page is displayed."""
        if self.URL_TEMPLATE not in self.location:
            return False
        return self.loaded

    @property
    def filters(self):
        """Return the available filters."""
        return [self.Filter(self, button)
                for button in self.find_elements(*self._filter_button_locator)]

    def filter_toggle(self):
        """Click on the filter menu to show the filter options."""
        toggle = self.find_element(*self._filter_toggle_locator)
        Utility.click_option(self.driver, element=toggle)
        return self

    @property
    def total_filters(self):
        """Return the number the filter options available."""
        return len(self.filters)

    def is_filtered_by(self, subject_filter):
        """Return True if the books are filtered by the submitted subject."""
        return (
            subject_filter in self.find_element(*self._filter_by_locator).text)

    @property
    def math(self):
        """Return the subjects filtered by math titles."""
        math_root = self.find_element(*self._math_category_locator)
        return self.Category(self, math_root)

    @property
    def science(self):
        """Return the subjects filtered by the science titles."""
        science_root = self.find_element(*self._science_category_locator)
        return self.Category(self, science_root)

    @property
    def social_sciences(self):
        """Return the subjects filtered by the social sciences titles."""
        social_root = self.find_element(
            *self._social_sciences_category_locator)
        return self.Category(self, social_root)

    @property
    def humanities(self):
        """Return the subjects filtered by the humanities titles."""
        humanities_root = self.find_element(*self._humanities_category_locator)
        return self.Category(self, humanities_root)

    @property
    def business(self):
        """Return the subjects filtered by the business titles."""
        business_root = self.find_element(*self._business_category_locator)
        return self.Category(self, business_root)

    @property
    def essentials(self):
        """Return the subjects filtered by the essentials titles."""
        essentials_root = self.find_element(*self._essentials_category_locator)
        return self.Category(self, essentials_root)

    @property
    def ap(self):
        """Return the subjects filtered by the AP titles."""
        ap_root = self.find_element(*self._ap_category_locator)
        return self.Category(self, ap_root)

    @property
    def _active_books(self):
        """Select active books for use by the class."""
        return [Book(self, book)
                for book in self.find_elements(*self._book_locator)]

    @property
    def ap_books(self):
        """Select active AP books."""
        return self._selection_helper(Library().ap)

    @property
    def available_books(self):
        """Select active books."""
        return self._selection_helper(Library().available)

    @property
    def bookshare_books(self):
        """Select active books available through Bookshare."""
        return self._selection_helper(Library().bookshare)

    @property
    def business_books(self):
        """Select active business books."""
        return self._selection_helper(Library().business)

    @property
    def comp_copy(self):
        """Select the current editions of each book."""
        return self._selection_helper(Library().comp_copy)

    @property
    def current_books(self):
        """Select the current editions of each book."""
        return self._selection_helper(Library().current)

    @property
    def essentials_books(self):
        """Select active essentials books."""
        return self._selection_helper(Library().essentials)

    @property
    def humanities_books(self):
        """Select active humanities books."""
        return self._selection_helper(Library().humanities)

    @property
    def kindle_books(self):
        """Select active books with a Kindle edition available."""
        return self._selection_helper(Library().kindle)

    @property
    def itunes_books(self):
        """Select active books with an iBook eddition available."""
        return self._selection_helper(Library().itunes)

    @property
    def locked_instructor(self):
        """Select active books with locked instructor resources."""
        return self._selection_helper(Library().locked_instructor)

    @property
    def locked_student(self):
        """Select active books with locked student resources."""
        return self._selection_helper(Library().locked_student)

    @property
    def math_books(self):
        """Select active math books."""
        return self._selection_helper(Library().math)

    @property
    def old_book_editions(self):
        """Select the books with a newer editions available."""
        return self._selection_helper(Library().superseded)

    @property
    def openstax_books(self, filter_current=False):
        """Select active books while excluding Polish versions."""
        return [book for book in self._active_books
                if book.language == Library.ENGLISH]

    @property
    def polish_books(self):
        """Select active books in Polish."""
        return [book for book in self._active_books
                if book.language == Library.POLISH]

    @property
    def print_books(self):
        """Select the books with a current print edition available."""
        return self._selection_helper(Library().print)

    @property
    def science_books(self):
        """Select active science books."""
        return self._selection_helper(Library().science)

    @property
    def social_sciences_books(self):
        """Select active social science books."""
        return self._selection_helper(Library().social_sciences)

    @property
    def unlocked_instructor(self):
        """Select active books with unlocked instructor resources."""
        return self._selection_helper(Library().unlocked_instructor)

    @property
    def unlocked_student(self):
        """Select active books with unlocked student resources."""
        return self._selection_helper(Library().unlocked_student)

    def select_book(self, book_title):
        """Return the book page for a specific title.

        :param str book_title: the full book title found in the alt field
        :return: the book page for the selected title
        :rtype: :py:class:`~pages.web.book.Book`

        """
        append = Library().get(book_title, field=Library.DETAILS)
        selector = '[href$="{book_details}"]'.format(book_details=append)
        book = self.find_element(By.CSS_SELECTOR, selector)
        Utility.click_option(self.driver, element=book)
        from pages.web.book import Book as Details
        return go_to_(Details(self.driver, book_name=append))

    def select_random_book(self, _from=Library.OPENSTAX, filter_current=False):
        """Return a random book from the active list."""
        using = {
            Library.ALL_BOOKS: self._active_books,
            Library.AP: self.ap_books,
            Library.AVAILABLE: self.available_books,
            Library.BOOKSHARE: self.bookshare_books,
            Library.BUSINESS: self.business_books,
            Library.COMP_COPY: self.comp_copy,
            Library.CURRENT: self.current_books,
            Library.HAS_I_LOCK: self.locked_instructor,
            Library.HAS_I_UNLOCK: self.unlocked_instructor,
            Library.HAS_S_LOCK: self.locked_student,
            Library.HAS_S_UNLOCK: self.unlocked_student,
            Library.HUMANITIES: self.humanities_books,
            Library.ITUNES: self.itunes_books,
            Library.KINDLE: self.kindle_books,
            Library.MATH: self.math_books,
            Library.OPENSTAX: self.openstax_books,
            Library.POLISH: self.polish_books,
            Library.PRINT_COPY: self.print_books,
            Library.SCIENCE: self.science_books,
            Library.SOCIAL: self.social_sciences_books,
            Library.SUPERSEDED: self.old_book_editions,
        }.get(_from)
        if filter_current:
            using = list(filter(
                lambda book: book.title not in Library.OLD_EDITIONS, using))
        total = len(using)
        if total <= 0:
            raise WebException('No books are available for selection')
        book = Utility.random(0, total - 1)
        selected = using[book]
        print('Selected book: {0}'.format(selected.title))
        destination = selected.url_append
        selected.select()
        sleep(1.0)
        from pages.web.book import Book as Details
        return go_to_(Details(self.driver, book_name=destination))

    def _selection_helper(self, modifier):
        """Return a list of books for a modified collection."""
        library = Library()
        collection = library.get_titles(modifier)
        return [book for book in self._active_books
                if book.title in collection]

    def view_about_our_textbooks(self):
        """Scroll to the textbook blurbs."""
        Utility.scroll_to(self.driver, self._about_our_textbooks_locator)
        return self

    @property
    def about(self):
        """Return the about blurb texts."""
        return [self.About(self, blurb)
                for blurb in self.find_elements(*self._about_blurb_locator)]

    class Filter(Region):
        """Subject filters."""

        _subject_locator = (By.CSS_SELECTOR, '[data-html]')

        @property
        def subject(self):
            """Return the filter subject."""
            return self.find_element(*self._subject_locator).text

        @property
        def value(self):
            """Return the category value."""
            return self.root.get_attribute('data-value')

        def view_books(self):
            """Select the filter category to view the topic textbooks."""
            Utility.click_option(self.driver, element=self.root)
            return self.page

        @property
        def is_selected(self):
            """Return True if the filter is active."""
            return self.root.get_attribute('aria-pressed') == 'true'

    class Category(Region):
        """Subject category information."""

        _category_name_locator = (By.CSS_SELECTOR, 'h2')
        _book_locator = (By.CSS_SELECTOR, '.cover')

        @property
        def section(self):
            """Return the category title."""
            return self.find_element(*self._category_name_locator).text

        @property
        def is_visible(self):
            """Return True if the category is displayed."""
            return 'hidden' not in self.root.get_attribute('class')

        @property
        def books(self):
            """Return category books."""
            return [Book(self, book)
                    for book in self.find_elements(*self._book_locator)]

    class About(Region):
        """An About Our Textbooks blurb."""

        _title_locator = (By.CSS_SELECTOR, '.title')
        _blurb_locator = (By.CSS_SELECTOR, '.text p')

        @property
        def title(self):
            """Return the blurb title."""
            return self.find_element(*self._title_locator).text

        @property
        def blurb(self):
            """Return the blurb text."""
            return self.find_element(*self._blurb_locator).text


class Book(Region):
    """A single book title."""

    _url_locator = (By.TAG_NAME, 'a')
    _image_locator = (By.TAG_NAME, 'img')

    @property
    def title(self):
        """Return the book title."""
        return self.image.get_attribute('alt')

    @property
    def image(self):
        """Return the image element."""
        return self.find_element(*self._image_locator)

    @property
    def image_source(self):
        """Return the image source URL."""
        return self.image.get_attribute('src')

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
            return 'Polish'
        return 'English'

    def select(self):
        """Click on the book cover."""
        book_name = self.url_append
        Utility.safari_exception_click(
            self.driver, element=self.find_element(*self._url_locator))
        from pages.web.book import Book as Details
        return go_to_(Details(self.driver,
                              self.page.base_url,
                              self.page.timeout,
                              book_name=book_name))
