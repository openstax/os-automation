"""The technology page."""

from time import sleep

from pypom import Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from pages.web.book import Book
from utils.utilities import Utility, go_to_
from utils.web import Library


class Technology(WebBase):
    """The technology options page."""

    URL_TEMPLATE = '/technology'

    _title_locator = (By.CSS_SELECTOR, '#banner h1')
    _description_locator = (By.CSS_SELECTOR, '.description p')
    _learn_more_locator = (By.CSS_SELECTOR, '.description ~ a')
    _resources_locator = (By.CSS_SELECTOR, '#steps')
    _tutor_locator = (By.CSS_SELECTOR, '#tutor')

    @property
    def loaded(self):
        """Override the base loader."""
        return self.find_element(*self._title_locator)

    def is_displayed(self):
        """Return True if the technology page is displayed."""
        return self.find_element(*self._title_locator).is_displayed()

    @property
    def title(self):
        """Return the page title."""
        return self.find_element(*self._title_locator).text.strip()

    @property
    def description(self):
        """Return the page subheading text."""
        return self.find_element(*self._description_locator).text.strip()

    def learn_more(self):
        """Click the banner page link."""
        Utility.safari_exception_click(self.driver, self._learn_more_locator)
        return self

    @property
    def resources(self):
        """Access the Steps section."""
        return self.Steps(self)

    @property
    def tutor(self):
        """Access the OpenStax Tutor beta section."""
        return self.Tutor(self)

    class Steps(Region):
        """Resource access steps."""

        INSTRUCTOR = '.step:nth-child(2) '
        TECHNOLOGY = '.step:last-child '
        BOOK = '[data-value={book}]'

        _title_locator = (By.CSS_SELECTOR, 'h2')
        _proxy_select_locator = (By.CSS_SELECTOR, '.proxy-select')
        _option_list_locator = (By.CSS_SELECTOR, '.proxy-select ul')
        _instructor_border_locator = (By.CSS_SELECTOR, INSTRUCTOR + 'div')
        _instructor_link_locator = (By.CSS_SELECTOR, INSTRUCTOR + 'a')
        _technology_link_locator = (By.CSS_SELECTOR, TECHNOLOGY + 'a')
        _partner_resource_locator = (By.CSS_SELECTOR, '#technology-options h2')

        @property
        def title(self):
            """Return the resource heading text."""
            return self.title_box.text.strip()

        @property
        def title_box(self):
            """Return the resource heading element."""
            return self.find_element(*self._title_locator)

        def select_book(self, book):
            """Select a book from the proxy menu."""
            menu = self.find_element(*self._proxy_select_locator)
            options = self.find_element(*self._option_list_locator)
            details = Library().get(book, Library.DETAILS)
            option = self.find_element(
                By.CSS_SELECTOR, '[data-value={book}]'.format(book=details))
            offset = self.driver.execute_script(
                'return arguments[0].offsetTop;',
                option)
            if 'open' not in menu.get_attribute('class'):
                Utility.safari_exception_click(self.driver, element=menu)
            self.driver.execute_script(
                'arguments[0].scrollTop = {offset};'.format(offset=offset),
                options)
            sleep(0.2)
            Utility.safari_exception_click(self.driver,
                                           element=option,
                                           force_js_click=True)
            return self.page

        def view_instructor_resources(self):
            """Click the instructor resource link."""
            return self._selection_helper(self._instructor_link_locator)

        def view_technology_options(self):
            """Click the technology options link."""
            return self._selection_helper(self._technology_link_locator)

        @property
        def book_selected(self):
            """Return the resource link border stylings."""
            link_border = self.find_element(*self._instructor_border_locator)
            return ('dimmed' not in link_border.get_attribute('class'))

        def _selection_helper(self, link):
            """Select the book reference link."""
            assert(self.book_selected), 'No book selected'
            book = self.find_element(*link)
            book_title = (
                book
                .get_attribute('href')
                .split('/')[-1]
                .split('?')[0])
            Utility.switch_to(self.driver, element=book)
            self.wait.until(
                lambda _: sleep(2) or
                self.find_element(*self._partner_resource_locator)
                .is_displayed())
            return go_to_(Book(self.driver, self.page.base_url,
                               book_name=book_title))

    class Tutor(Region):
        """Tutor information."""

        _title_locator = (By.CSS_SELECTOR, 'h1')
        _subheading_locator = (By.CSS_SELECTOR, 'h2')
        _description_locator = (
                        By.CSS_SELECTOR, '[data-html="tutor.description"] p')
        _how_it_works_locator = (By.CSS_SELECTOR, '[href*="#how-it-works"]')
        _tutor_dashboard_locator = (By.CSS_SELECTOR, '[href$=dashboard]')

        @property
        def title(self):
            """Return the section banner title."""
            return self.find_element(*self._title_locator).text.strip()

        @property
        def heading(self):
            """Return the heading text."""
            return self.find_element(*self._subheading_locator).text.strip()

        @property
        def description(self):
            """Return the description text."""
            return self.find_element(*self._description_locator).text.strip()

        def learn_more(self):
            """Click the 'Learn more' button."""
            Utility.safari_exception_click(
                self.driver, self._how_it_works_locator)
            from pages.web.tutor import TutorMarketing
            return go_to_(TutorMarketing(self.driver, self.page.base_url))

        def go_to_openstax_tutor(self, base_url=None):
            """Click the 'Go to OpenStax Tutor' button."""
            Utility.switch_to(self.driver, self._tutor_dashboard_locator)
            self.wait.until(lambda _:
                            'accounts' in self.driver.current_url or
                            'tutor' in self.driver.current_url)
            if 'accounts' in self.driver.current_url:
                from pages.accounts.home import AccountsHome
                return go_to_(AccountsHome(self.driver, base_url=base_url))
            from pages.tutor.dashboard import Dashboard
            return go_to_(Dashboard(self.driver, base_url=base_url))
