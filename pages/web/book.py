"""A marketing page for an OpenStax book."""

import re
from time import sleep

from pypom import Region
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from pages.accounts.home import AccountsHome
from pages.web.base import WebBase
from utils.utilities import Utility, go_to_
from utils.web import Web

DISPLAY_TAB = (
    'return document.querySelectorAll(".tab")[{tab}]'
    '.attributes["aria-current"].value == "page";')


class ResourceTab(Region):
    """A base region for instructor and student resources."""

    _slogan_locator = (By.CSS_SELECTOR, '.free-stuff-blurb h2')
    _resource_locator = (By.CSS_SELECTOR, '.resource-box:not(.double)')

    def _displayed(self, tab):
            """Return True if the instructor resources content is visible."""
            return self.driver.execute_script(
                DISPLAY_TAB.format(tab=tab))

    @property
    def slogan(self):
        """Return the instructor resource slogan."""
        return self.find_element(*self._slogan_locator).text

    @property
    def resources(self):
        """Return a list of available resources."""
        return [Resource(self, box)
                for box in self.find_elements(*self._resource_locator)]


class Accordion(Region):
    """A base region for phone-view expandable menus."""

    _toggle_locator = (By.CSS_SELECTOR, '.control-bar')
    _is_open_locator = (By.CSS_SELECTOR, '.content-pane')

    def toggle(self):
        """Click on a toggle bar to open or close the menu."""
        self.find_element(*self._toggle_locator).click()
        sleep(0.5)
        return self

    @property
    def is_open(self):
        """Return True if the menu is open."""
        return not self.driver.execute_script(
            'return arguments[0].hidden;',
            self.find_element(*self._is_open_locator))

    def is_displayed(self):
        """Return True if the menu is open."""
        return self.is_open


class AccordionSubRegion(Accordion):
    """A base region for accordion subsections."""

    _is_open_locator = (By.CSS_SELECTOR, '.content-region')


class Book(WebBase):
    """A book details page."""

    URL_TEMPLATE = '/details/books/{book_name}'

    _banner_locator = (By.CLASS_NAME, 'title-image')
    _tab_locator = (By.CSS_SELECTOR, '.tab')

    _content_locator = (By.CSS_SELECTOR, '.details-tab')
    _book_content_locator = (By.CSS_SELECTOR, '.main')
    _instructor_locator = (By.CSS_SELECTOR, '.instructor-resources')
    _student_locator = (By.CSS_SELECTOR, '.student-resources')

    _sidebar_locator = (By.CSS_SELECTOR, '.sidebar')
    _phone_view_locator = (By.CSS_SELECTOR, '.phone-view')

    @property
    def loaded(self):
        """Return True when the book details page is loaded."""
        try:
            details = self.find_element(*self._content_locator)
            if 'fizyka' not in self.location:
                instructor = self.find_element(*self._instructor_locator)
                student = self.find_element(*self._student_locator)
        except WebDriverException:
            return False
        return (
            Utility.is_image_visible(
                self.driver, image=self.find_element(*self._banner_locator))
            and Utility.has_children(details)
            and (Utility.has_children(instructor)
                 if 'fizyka' not in self.location else True)
            and (Utility.has_children(student)
                 if 'fizyka' not in self.location else True)
        )

    def is_displayed(self):
        """Return True if the book details banner image is displayed."""
        return self.find_element(*self._banner_locator).is_displayed()

    @property
    def title(self):
        """Return the book title."""
        return self.find_element(*self._banner_locator).get_attribute('alt')

    @property
    def phone(self):
        """Access the book details for mobile devices."""
        phone_root = self.find_element(*self._phone_view_locator)
        return self.PhoneDisplay(self, phone_root)

    def is_using(self):
        """Click the adoption report link."""
        if self.driver.get_window_size().get('width') > Web.PHONE:
            return self.sidebar.submit_adoption_form()
        return self.phone.submit_adoption_form()

    def is_interested(self):
        """Click the interest report link."""
        if self.driver.get_window_size().get('width') > Web.PHONE:
            return self.sidebar.submit_interest_form()
        return self.phone.submit_interest_form()

    @property
    def tabs(self):
        """Return the resource tabs."""
        assert(self.driver.get_window_size().get('width') > Web.PHONE), \
            'Tab viewing is not available in the phone display'
        return [tab for tab in self.find_elements(*self._tab_locator)]

    def select_tab(self, tab):
        """Select a specific resource tab."""
        self.tabs[tab].click()
        sleep(0.5)
        return self

    @property
    def details(self):
        """Access the book details."""
        if self.driver.get_window_size().get('width') > Web.PHONE:
            main_root = self.find_element(*self._book_content_locator)
            return self.Details(self, main_root)
        return self.phone.details

    @property
    def sidebar(self):
        """Access the sidebar links."""
        assert(self.driver.get_window_size().get('width') > Web.PHONE), \
            'Sidebar not available in the phone display'
        sidebar_root = self.find_element(*self._sidebar_locator)
        return self.Sidebar(self, sidebar_root)

    @property
    def instructor(self):
        """Access the instructor resources."""
        if self.driver.get_window_size().get('width') > Web.PHONE:
            instructor_root = self.find_element(*self._book_content_locator)
            return self.InstructorResources(self, instructor_root)
        return self.phone.instructor

    @property
    def partners(self):
        """Access the partner resources."""
        if self.driver.get_window_size().get('width') > Web.PHONE:
            partner_root = self.find_element(*self._book_content_locator)
            return self.PartnerResources(self, partner_root)
        return None

    @property
    def student(self):
        """Access the student resources."""
        if self.driver.get_window_size().get('width') > Web.PHONE:
            student_root = self.find_element(*self._book_content_locator)
            return self.StudentResources(self, student_root)
        return self.phone.student

    @property
    def table_of_contents(self):
        """Shortcut the table of contents."""
        if self.driver.get_window_size().get('width') > Web.PHONE:
            return self.sidebar.table_of_contents
        return self.phone.table_of_contents

    class Sidebar(Region):
        """The large view sidebar."""

        _toc_locator = (By.CSS_SELECTOR, '.show-toc')
        _online_view_locator = (By.CSS_SELECTOR, '[href*="cnx.org"]')
        _pdf_download_locator = (By.CSS_SELECTOR, '.option [href*=cloudfront]')
        _print_copy_locator = (By.CSS_SELECTOR, '.show-print-submenu')
        _bookshare_locator = (By.CSS_SELECTOR, '[href*=bookshare]')
        _ibook_download_locator = (By.CSS_SELECTOR, '[href*=itunes]')
        _kindle_download_locator = (
            By.CSS_SELECTOR, '[href*=amazon] , [href*="/a.co/"]')
        _interest_locator = (By.CSS_SELECTOR, '[href*=interest]')
        _adoption_locator = (By.CSS_SELECTOR, '[href*=adoption]')

        @property
        def table_of_contents(self):
            """Access the book table of contents."""
            return TableOfContents(self)

        def view_table_of_contents(self):
            """Open the Table of Contents modal."""
            Utility.safari_exception_click(self.driver,
                                           locator=self._toc_locator)
            return self.table_of_contents

        def view_online(self):
            """View the book on CNX.org."""
            link = self.find_element(*self._online_view_locator)
            Utility.switch_to(self.driver, element=link)
            from pages.cnx.contents import Webview
            return go_to_(Webview(self.driver))

        @property
        def pdf_url(self):
            """Return the book PDF download URL."""
            return (self.find_element(*self._pdf_download_locator)
                    .get_attribute('href'))

        def download_pdf(self):
            """Click the download link."""
            link = self.find_element(*self._pdf_download_locator)
            return Utility.switch_to(self.driver, element=link)

        @property
        def order_book(self):
            """Access the book order options."""
            return BookOrder(self)

        def view_book_order_options(self):
            """Open the Book Order modal."""
            Utility.safari_exception_click(self.driver,
                                           locator=self._print_copy_locator)
            return self.order_book

        def view_bookshare(self):
            """Open the Bookshare page for the textbook."""
            link = self.find_element(*self._bookshare_locator)
            Utility.switch_to(self.driver, element=link)
            from pages.bookshare.home import Bookshare
            return go_to_(Bookshare(self.driver))

        @property
        def ibooks(self):
            """Return the available iBook links."""
            return self.find_elements(*self._ibook_download_locator)

        def view_ibook(self, book=1):
            """Open the iTunes store page for the iBook."""
            assert(book <= len(self.ibooks)), \
                'iBook {number} not available.'.format(number=book)
            link = self.ibooks[book - 1]
            Utility.switch_to(self.driver, element=link)
            from pages.apple.itunes import ITunes
            return go_to_(ITunes(self.driver))

        def view_kindle(self):
            """Open the Amazon store page for the Kindle ebook."""
            link = self.find_element(*self._kindle_download_locator)
            Utility.switch_to(self.driver, element=link)
            from pages.amazon.home import Amazon
            return go_to_(Amazon(self.driver))

        def submit_interest_form(self):
            """Go to the interest form."""
            Utility.safari_exception_click(
                self.driver, locator=self._interest_locator)
            from pages.web.interest import Interest
            return go_to_(Interest(self.driver))

        def submit_adoption_form(self):
            """Go to the adoption form."""
            Utility.safari_exception_click(
                self.driver, locator=self._adoption_locator)
            from pages.web.adoption import Adoption
            return go_to_(Adoption(self.driver))

    class Details(Region):
        """The book details main region."""

        _summary_locator = (By.CSS_SELECTOR, '.loc-summary-text div')
        _senior_auth_locator = (By.CSS_SELECTOR, '.loc-senior-author')
        _other_auth_locator = (By.CSS_SELECTOR, '.loc-nonsenior-author')
        _errata_blurb_locator = (By.CSS_SELECTOR, '[data-html=errataBlurb]')
        _correction_locator = (By.CSS_SELECTOR, '[href*="errata/form"]')
        _pl_correction_locator = (By.CSS_SELECTOR, '[href$="/pl/errata"]')
        _errata_list_locator = (By.CSS_SELECTOR, '[href*="errata/?book"]')
        _publish_date_locator = (By.CSS_SELECTOR, '.loc-pub-date')
        _print_locator = (By.CSS_SELECTOR, '.loc-print-isbn')
        _digital_locator = (By.CSS_SELECTOR, '.loc-digital-isbn')
        _ibook_locator = (By.CSS_SELECTOR, '.loc-ibook-isbn')
        _license_locator = (By.CSS_SELECTOR, '.loc-license')

        def is_displayed(self):
            """Return True if the book details content is visible."""
            return self.driver.execute_script(
                DISPLAY_TAB.format(tab=Web.BOOK_DETAILS))

        @property
        def summary(self):
            """Return the book summary."""
            return self.find_element(*self._summary_locator).text

        @property
        def senior_authors(self):
            """Return the list of senior authors."""
            authors = self.find_elements(*self._senior_auth_locator)
            authors = [
                (author.text.split(', ', 1)[0], author.text.split(', ', 1)[-1])
                for author in authors]
            for index, author in enumerate(authors):
                if author[0] == author[1]:
                    authors[index] = (author[0], '')
            return authors

        @property
        def has_nonsenior_authors(self):
            """Return True if the contributing authors section exists."""
            return '<h3>Contributing Authors</h3>' in self.driver.page_source

        @property
        def nonsenior_authors(self):
            """Return the list of non-senior authors."""
            authors = self.find_elements(*self._other_auth_locator)
            authors = [
                (author.text.split(', ', 1)[0], author.text.split(', ', 1)[-1])
                for author in authors]
            for index, author in enumerate(authors):
                if author[0] == author[1]:
                    authors[index] = (author[0], '')
            return authors

        @property
        def errata_text(self):
            """Return the errata explanation text."""
            return self.find_element(*self._errata_blurb_locator).text

        @property
        def errata_append(self):
            """Return the errata URL append."""
            return (self.find_element(*self._correction_locator)
                    .get_attribute('href')
                    .split('=')[1])

        def submit_errata(self):
            """Click on the 'Suggest a correction' button."""
            book = None
            try:
                button = self.find_element(*self._correction_locator)
                from pages.web.errata import ErrataForm
                book = self.errata_append
            except WebDriverException:
                button = self.find_element(*self._pl_correction_locator)
                from pages.katalyst.errata import ErrataForm
            Utility.safari_exception_click(self.driver, element=button)
            if not self.page.web_nav.login.logged_in:
                return go_to_(AccountsHome(self.driver))
            if book:
                return go_to_(ErrataForm(self.driver, book=book))
            return go_to_(ErrataForm(self.driver))

        def view_errata(self):
            """Click on the 'Errata list' button."""
            try:
                button = self.find_element(*self._errata_list_locator)
                from pages.web.errata import Errata
                book = button.get_attribute('href').split('=')[1]
            except WebDriverException:
                return
            Utility.safari_exception_click(self.driver, element=button)
            return go_to_(Errata(self.driver, book=book))

        @property
        def published_on(self, as_date_obj=False):
            """Return the publishing date."""
            date = (self.find_element(*self._publish_date_locator)
                    .get_attribute('innerHTML')
                    .split('>')[-1])
            if as_date_obj:
                from datetime import datetime
                return datetime.strptime(date + ' +0000', '%b %d, %Y %z')
            return date

        @property
        def print_isbns(self):
            """Return the print book ISBNs."""
            return _split_isbn(self.driver, self._print_locator)

        @property
        def digital_isbns(self):
            """Return the digital book ISBNs."""
            return _split_isbn(self.driver, self._digital_locator)

        @property
        def ibook_isbns(self):
            """Return the iBook ISBNs."""
            return _split_isbn(self.driver, self._ibook_locator)

        @property
        def license(self):
            """Return the license information."""
            return self.find_element(*self._license_locator).text

    class InstructorResources(ResourceTab):
        """The instructor resources tab."""

        _account_signup_locator = (By.CSS_SELECTOR, '.free-stuff-blurb a')
        _oer_commons_locator = (By.CSS_SELECTOR, '.resource-box.double')
        _webinar_link_locator = (By.CSS_SELECTOR, '.webinars')

        def is_displayed(self):
            """Return True if the instructor resources content is visible."""
            return self._displayed(tab=Web.INSTRUCTOR_RESOURCES)

        def sign_up(self):
            """Click the account sign up link."""
            Utility.switch_to(
                self.driver, link_locator=self._account_signup_locator)
            from pages.accounts.signup import Signup
            return go_to_(Signup(self.driver))

        @property
        def oer_commons(self):
            """Return the OER Commons resource."""
            oer_commons_root = self.find_element(*self._oer_commons_locator)
            return Resource(self, oer_commons_root)

        def view_webinars(self):
            """Click on the 'Find a webinar' link."""
            webinar = self.find_element(*self._webinar_link_locator)
            article_url = webinar.get_attribute('href').split('/')[-1]
            Utility.safari_exception_click(self.driver, element=webinar)
            from pages.web.blog import Article
            return go_to_(Article(self.driver, article=article_url))

    class PartnerResources(ResourceTab):
        """The partner resources tab."""

        _slogan_locator = (By.CSS_SELECTOR, '.ally-blurb h2')
        _partner_info_locator = (By.CSS_SELECTOR, '.ally-blurb a')
        _resource_locator = (By.CSS_SELECTOR, '.ally-box')

        def is_displayed(self):
            """Return True if the partner resources content is visible."""
            return self._displayed(tab=Web.PARTNER_RESOURCES)

        @property
        def partners(self):
            """Return a list of available resources."""
            return [Partner(self, box)
                    for box in self.find_elements(*self._resource_locator)]

        @property
        def resources(self):
            """Override the resource box property."""
            return self.partners

    class StudentResources(ResourceTab):
        """The student resources tab."""

        def is_displayed(self):
            """Return True if the student resources content is visible."""
            return self._displayed(tab=Web.STUDENT_RESOURCES)

    class PhoneDisplay(Region):
        """The book details page for small devices."""

        _online_view_locator = (By.CSS_SELECTOR, '.option [href*="cnx.org"]')
        _pdf_download_locator = (By.CSS_SELECTOR, '.option [href*=cloudfront]')
        _print_copy_locator = (By.CSS_SELECTOR, '.show-print-submenu')
        _bookshare_locator = (By.CSS_SELECTOR, '.option [href*=bookshare]')
        _ibook_download_locator = (By.CSS_SELECTOR, '[href*=itunes]')
        _kindle_download_locator = (By.CSS_SELECTOR, '[href*=amazon]')
        _interest_locator = (By.CSS_SELECTOR, '[href*=interest]')
        _adoption_locator = (By.CSS_SELECTOR, '[href*=adoption]')

        _book_details_locator = (
            By.CSS_SELECTOR, '.accordion-item:first-child')
        _toc_locator = (
            By.XPATH, ('//div[text()="Table of contents"]'
                       '/ancestor::node()[2]'))
        _instructor_locator = (
            By.XPATH, ('//div[text()="Instructor resources"]'
                       '/ancestor::node()[2]'))
        _student_locator = (
            By.XPATH, ('//div[text()="Student resources"]'
                       '/ancestor::node()[2]'))
        _errata_locator = (
            By.CSS_SELECTOR, '.accordion-item:last-child')

        def view_online(self):
            """View the book on CNX.org."""
            link = self.find_element(*self._online_view_locator)
            Utility.switch_to(self.driver, element=link)
            from pages.cnx.contents import Webview
            return go_to_(Webview(self.driver))

        def download_pdf(self):
            """Click the download link."""
            link = self.find_element(*self._pdf_download_locator)
            Utility.safari_exception_click(self.driver, element=link)
            return self.page

        @property
        def order_book(self):
            """Access the book order options."""
            return BookOrder(self)

        def view_book_order_options(self):
            """Open the Book Order modal."""
            Utility.safari_exception_click(self.driver,
                                           locator=self._print_copy_locator)
            return self.order_book

        def view_bookshare(self):
            """Open the Bookshare page for the textbook."""
            link = self.find_element(*self._bookshare_locator)
            Utility.switch_to(self.driver, element=link)
            from pages.bookshare.home import Bookshare
            return go_to_(Bookshare(self.driver))

        @property
        def ibooks(self):
            """Return the available iBook links."""
            return self.find_elements(*self._ibook_download_locator)

        def view_ibook(self, book=1):
            """Open the iTunes store page for the iBook."""
            assert(book <= len(self.ibooks)), \
                'iBook {number} not available.'.format(number=book)
            link = self.ibooks[book - 1]
            Utility.switch_to(self.driver, element=link)
            from pages.itunes.home import ITunes
            return go_to_(ITunes(self.driver))

        def view_kindle(self):
            """Open the Amazon store page for the Kindle ebook."""
            link = self.find_element(*self._kindle_download_locator)
            Utility.switch_to(self.driver, element=link)
            from pages.amazon.home import Amazon
            return go_to_(Amazon(self.driver))

        def submit_interest_form(self):
            """Go to the interest form."""
            Utility.safari_exception_click(
                self.driver, locator=self._interest_locator)
            from pages.web.interest import Interest
            return go_to_(Interest(self.driver))

        def submit_adoption_form(self):
            """Go to the adoption form."""
            Utility.safari_exception_click(
                self.driver, locator=self._adoption_locator)
            from pages.web.adoption import Adoption
            return go_to_(Adoption(self.driver))

        @property
        def details(self):
            """Access the book details pane."""
            phone_details_root = self.find_element(*self._book_details_locator)
            return self.CompactBookDetails(self, phone_details_root)

        @property
        def table_of_contents(self):
            """Access the table of contents pane."""
            toc_root = self.find_element(*self._toc_locator)
            return self.CompactTableOfContents(self, toc_root)

        @property
        def instructor(self):
            """Access the instructor resources pane."""
            instructor_root = self.find_element(*self._instructor_locator)
            return self.CompactInstructorResources(self, instructor_root)

        @property
        def student(self):
            """Access the student resources pane."""
            student_root = self.find_element(*self._student_locator)
            return self.CompactStudentResources(self, student_root)

        @property
        def errata(self):
            """Access the errata pane."""
            errata_root = self.find_element(*self._errata_locator)
            return self.CompactErrata(self, errata_root)

        class CompactBookDetails(Accordion):
            """The compact bood details pane."""

            _summary_locator = (By.CSS_SELECTOR, '[data-html=description]')
            _authors_locator = (By.CSS_SELECTOR, '.authors-region')
            _pub_details_locator = (By.CSS_SELECTOR, '.product-details-region')

            @property
            def summary(self):
                """Return the book summary text."""
                return self.find_element(*self._summary_locator).text.strip()

            @property
            def authors(self):
                """Access the authors section."""
                authors_root = self.find_element(*self._authors_locator)
                return self.Authors(self, authors_root)

            @property
            def product_details(self):
                """Access the product details section."""
                details_root = self.find_element(*self._pub_details_locator)
                return self.ProductDetails(self, details_root)

            class Authors(AccordionSubRegion):
                """The authors information section."""

                _senior_auth_locator = (
                    By.CSS_SELECTOR, '.loc-senior-author')
                _other_auth_locator = (
                    By.CSS_SELECTOR, '.loc-nonsenior-author')

                @property
                def senior_authors(self):
                    """Return a list of senior authors."""
                    authors = self.find_elements(*self._senior_auth_locator)
                    authors = [
                        (author.text.split(', ', 1)[0],
                         author.text.split(', ', 1)[-1])
                        for author in authors]
                    for index, author in enumerate(authors):
                        if author[0] == author[1]:
                            authors[index] = (author[0], '')
                    return authors

                @property
                def has_nonsenior_authors(self):
                    """Return True if the contributing authors section exists.

                    """
                    return '<h4>Contributing Authors</h4>' \
                        in self.driver.page_source

                @property
                def nonsenior_authors(self):
                    """Return a list of non-senior authors."""
                    authors = self.find_elements(*self._other_auth_locator)
                    authors = [
                        (author.text.split(', ', 1)[0],
                         author.text.split(', ', 1)[-1])
                        for author in authors]
                    for index, author in enumerate(authors):
                        if author[0] == author[1]:
                            authors[index] = (author[0], '')
                    return authors

            class ProductDetails(AccordionSubRegion):
                """The product details information section."""

                _print_locator = (By.CSS_SELECTOR, '.loc-print-isbn')
                _digital_locator = (By.CSS_SELECTOR, '.loc-digital-isbn')
                _ibook_locator = (By.CSS_SELECTOR, '.loc-ibook-isbn')
                _license_locator = (By.CSS_SELECTOR, '.license')

                @property
                def print_isbns(self):
                    """Return the print book ISBNs."""
                    return _split_isbn(self.driver, self._print_locator)

                @property
                def digital_isbns(self):
                    """Return the digital book ISBNs."""
                    return _split_isbn(self.driver, self._digital_locator)

                @property
                def ibook_isbns(self):
                    """Return the iBook ISBNs."""
                    return _split_isbn(self.driver, self._ibook_locator)

                @property
                def license(self):
                    """Return the license information."""
                    return self.find_element(*self._license_locator).text

        class CompactTableOfContents(Accordion):
            """The compact table of contents pane."""

            _chapter_list_locator = (
                By.CSS_SELECTOR, '.table-of-contents > li')
            _online_view_locator = (By.CSS_SELECTOR, 'a')

            @property
            def chapters(self):
                """Access the chapter list."""
                return [Chapter(self, chapter)
                        for chapter
                        in self.find_elements(*self._chapter_list_locator)]

            def get(self, number=None, chapter=None):
                """Return a particular chapter and scroll it into view."""
                target = None
                for ch in self.chapters:
                    if number and ch.chapter == str(number):
                        target = ch
                        break
                    elif chapter and ch.title == chapter:
                        target = ch
                        break
                if target:
                    Utility.scroll_to(self.driver, element=target, shift=-80)
                return target

            def view_online(self):
                """View the book on CNX.org."""
                button = self.find_element(*self._online_view_locator)
                Utility.switch_to(self.driver, element=button)
                from pages.cnx.contents import Webview
                return go_to_(Webview(self.driver))

        class CompactInstructorResources(Accordion):
            """The compact instructor resource pane."""

            _instructor_resource_locator = (
                By.CSS_SELECTOR, '.free-resources-region .resource-box')
            _partner_resource_locator = (
                By.CSS_SELECTOR, '.paid-resources-region a')

            @property
            def resources(self):
                """Return the list of available instructor resources."""
                return [Resource(self, option)
                        for option in self.find_elements(
                            *self._instructor_resource_locator)]

            @property
            def partners(self):
                """Return the list of available partner resources."""
                return [Partner(self, option)
                        for option in self.find_elements(
                            *self._partner_resource_locator)]

        class CompactStudentResources(Accordion):
            """The compact student resource pane."""

            _student_resource_locator = (By.CSS_SELECTOR, 'a')

            @property
            def resources(self):
                """Return the list of available student resources."""
                return [Resource(self, option)
                        for option
                        in self.find_elements(*self._student_resource_locator)]

        class CompactErrata(Accordion):
            """The compact errata information pane."""

            _errata_blurb_locator = (
                By.CSS_SELECTOR, '[data-html=errataBlurb]')
            _correction_locator = (By.CSS_SELECTOR, '.secondary')
            _errata_list_locator = (By.CSS_SELECTOR, '[href*="errata/?"]')

            @property
            def errata_text(self):
                """Return the errata explanation text."""
                return self.find_element(*self._errata_blurb_locator).text

            @property
            def errata_append(self):
                """Return the errata URL append."""
                return (self.find_element(*self._correction_locator)
                        .get_attribute('href')
                        .split('=')[1])

            def submit_errata(self):
                """Click on the 'Suggest a correction' button."""
                book = None
                try:
                    button = self.find_element(*self._correction_locator)
                    from pages.web.errata import ErrataForm
                    book = self.errata_append
                except WebDriverException:
                    button = self.find_element(*self._pl_correction_locator)
                    from pages.katalyst.errata import ErrataForm
                Utility.safari_exception_click(self.driver, element=button)
                if not self.page.page.web_nav.login.logged_in:
                    return go_to_(AccountsHome(self.driver))
                if book:
                    return go_to_(ErrataForm(self.driver, book=book))
                return go_to_(ErrataForm(self.driver))

            def view_errata(self):
                """Click on the 'Errata list' button."""
                try:
                    button = self.find_element(*self._errata_list_locator)
                    from pages.web.errata import Errata
                    book = button.get_attribute('href').split('=')[1]
                except WebDriverException:
                    return
                Utility.safari_exception_click(self.driver, element=button)
                return go_to_(Errata(self.driver, book=book))


class Resource(Region):
    """A resource box."""

    _title_locator = (By.CSS_SELECTOR, 'h3')
    _description_locator = (By.CSS_SELECTOR, '[data-html=description]')
    _is_locked_locator = (By.CSS_SELECTOR, '.fa-lock')
    _can_download_locator = (By.CSS_SELECTOR, '.fa-download')
    _is_external_locator = (By.CSS_SELECTOR, '.fa-external-link-alt')

    def is_displayed(self):
        """Return True if the box is displayed."""
        return self.root.is_displayed()

    @property
    def title(self):
        """Return the resource title or company name."""
        return self.find_element(*self._title_locator).text.strip()

    @property
    def description(self):
        """Return the resource description."""
        return self.find_element(*self._description_locator).text.strip()

    def select(self):
        """Click on the resource box."""
        self.root.click()
        return self

    @property
    def is_locked(self):
        """Return True if the resource is locked requiring a login."""
        return self._status_helper(self._is_locked_locator)

    @property
    def can_be_downloaded(self):
        """Return True if the resource is available for download."""
        return self._status_helper(self._can_download_locator)

    @property
    def is_external(self):
        """Return True if the resource is an external site."""
        return self._status_helper(self._is_external_locator)

    def _status_helper(self, locator):
        """Return True if the element is found."""
        try:
            self.find_element(*locator)
            return True
        except WebDriverException:
            return False


class Partner(Region):
    """A partner resource."""

    _name_locator = (By.CSS_SELECTOR, 'img')
    _description_locator = (By.CSS_SELECTOR, '.hover-blurb')

    @property
    def name(self):
        """Return the partner's name."""
        return (self.find_element(*self._name_locator)
                .get_attribute('alt').strip())

    @property
    def description(self):
        """Return the partner's short bio."""
        return self.find_element(*self._description_locator).text

    @property
    def url(self):
        """Return the partner's website URL."""
        return self.root.get_attribute('href')

    def view_partner(self):
        """Click on the partner resource box and return the new URL."""
        Utility.safari_exception_click(self.driver, element=self.root)
        return self.driver.current_url


class Chapter(Region):
    """An individual book chapter listing."""

    _section_locator = (By.CSS_SELECTOR, 'li')

    @property
    def title(self):
        """Return the chapter title."""
        title = self._line(self.root.get_attribute('innerHTML'))
        return title[0] if len(title) == 1 else '. '.join(title[1:])

    @property
    def chapter(self):
        """Return the chapter number."""
        number = self._line(self.root.get_attribute('innerHTML'))
        if len(number) == 1:
            return ''
        return number[0]

    @property
    def sections(self):
        """Return the section names."""
        return [section.strip()
                for section in self.find_elements(*self._section_locator)]

    @property
    def _line(self, text):
        """Break up the innerHTML strings."""
        return text.split('<')[0].split('. ')


class Modal(Region):
    """A base setup for the page modals."""

    _root_locator = (By.CSS_SELECTOR, '#dialog')
    _close_locator = (By.CSS_SELECTOR, '.put-away')

    @property
    def root(self):
        """Override the root variable."""
        return self.driver.execute_script(
            'return document.querySelector("#dialog");')

    def is_displayed(self):
        """Return True if the order modal is currently active."""
        return (Utility.has_children(self.root) and
                not self.root.get_attribute('hidden'))

    def close(self):
        """Close the order form."""
        assert(self.is_displayed), 'Order options are not visible'
        Utility.safari_exception_click(self.driver,
                                       locator=self._close_locator)
        return self.page


class TableOfContents(Modal):
    """The book table of contents modal display."""

    _chapter_list_locator = (By.CSS_SELECTOR, '.table-of-contents > li')
    _online_view_locator = (By.CSS_SELECTOR, 'a')

    @property
    def chapters(self):
        """Access the chapter list."""
        return [Chapter(self, chapter)
                for chapter
                in self.find_elements(*self._chapter_list_locator)]

    def get(self, number=None, chapter=None):
        """Return a particular chapter and scroll it into view."""
        target = None
        for ch in self.chapters:
            if number and ch.chapter == str(number):
                target = ch
                break
            elif chapter and ch.title == chapter:
                target = ch
                break
        if target:
            Utility.scroll_to(self.driver, element=target, shift=-80)
        return target

    def view_online(self):
        """View the book on CNX.org."""
        button = self.find_element(*self._online_view_locator)
        Utility.switch_to(self.driver, element=button)
        from pages.cnx.contents import Webview
        return go_to_(Webview(self.driver))


class BookOrder(Modal):
    """The book order modal dialog box."""

    _phone_version_locator = (By.CSS_SELECTOR, '.phone-version')
    _large_version_locator = (By.CSS_SELECTOR, '.larger-version')
    _box_locator = (By.CSS_SELECTOR, '.box')
    _section_locator = (By.CSS_SELECTOR, 'h1')
    _context_locator = (By.CSS_SELECTOR, '[data-html] p')
    _info_locator = (By.CSS_SELECTOR, '.info')
    _select_locator = (By.CSS_SELECTOR, 'a')

    @property
    def boxes(self):
        """Access the order boxes."""
        sleep(0.5)
        if self.driver.get_window_size().get('width') <= Web.PHONE:
            base = self.find_element(*self._phone_version_locator)
        else:
            base = self.find_element(*self._large_version_locator)
        return [self.Box(self, el)
                for el in base.find_elements(*self._box_locator)]

    class Box(Region):
        """An order box."""

        _title_locator = (By.CSS_SELECTOR, 'h1')
        _content_locator = (By.CSS_SELECTOR, '[data-html]')
        _info_locator = (By.CSS_SELECTOR, '.info')
        _non_root_link_locator = (By.CSS_SELECTOR, 'a')

        @property
        def title(self):
            """Return the intended user type."""
            return self.find_element(*self._title_locator).text.strip()

        @property
        def description(self):
            """Return the box description."""
            return self.find_element(*self._content_locator).text.strip()

        @property
        def additional_information(self):
            """Return any post-button information."""
            try:
                return self.find_element(*self._info_locator).text.strip()
            except WebDriverException:
                return ''

        def select(self):
            """Click on the order option."""
            if self.root.tag_name == 'a':
                target = self.root
            else:
                target = self.find_element(*self._non_root_link_locator)
            if self.title == 'Individual':
                Utility.switch_to(self.driver, element=target)
                from pages.amazon.home import Amazon
                return go_to_(Amazon(self.driver))
            elif self.title == 'Bookstore':
                Utility.safari_exception_click(self.driver, element=target)
                from pages.web.bookstore_suppliers import Bookstore
                return go_to_(Bookstore(self.driver))


def _split_isbn(driver, locator):
    """Break up an innerHTML string to retrieve the ISBN numbers."""
    try:
        isbns = driver.find_elements(*locator)
        group = ''
        for book in isbns:
            group = group + book.get_attribute('innerHTML')
        return sorted(list(set(filter(
            lambda string: string.startswith('ISBN'),
            re.split('<|>', group)
        ))))
    except WebDriverException:
        return []
