"""OpenStax's Web home page."""

from time import sleep

from pypom import Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility, go_to_
from utils.web import Web as Support


class Link(Region):
    """Internal information regions."""

    _title_locator = (By.CLASS_NAME, 'title')
    _text_locator = (By.CLASS_NAME, 'blurb')
    _link_locator = (By.TAG_NAME, 'a')

    def is_displayed(self):
        """Return True if the link root is displayed."""
        return self.root.is_displayed()

    @property
    def title(self):
        """Return the resource title."""
        return self.find_element(*self._title_locator).text

    @property
    def text(self):
        """Return the resource blurb."""
        return self.find_element(*self._text_locator).text

    @property
    def link(self):
        """Return the link element."""
        return self.find_element(*self._link_locator)

    def click(self):
        """Go to the link destination.

        Return a 'Destination' so the function will fail if
        a new link is added.
        """
        destination = self.link.get_attribute('href')
        Utility.wait_for_overlay_then(self.link.click)
        if destination.endswith(Support.IMPACT):
            from pages.web.impact import OurImpact as Destination
        elif destination.endswith(Support.PARTNERS):
            from pages.web.technology import Technology as Destination
        elif destination.endswith(Support.SUBJECTS):
            from pages.web.subjects import Subjects as Destination
        elif destination.endswith(Support.TECHNOLOGY):
            from pages.web.technology import Technology as Destination
        return go_to_(Destination(self.driver))


class WebHome(WebBase):
    """OpenStax Web home page."""

    URL_TEMPLATE = ''

    _banner_locator = (By.CLASS_NAME, 'book-banners')
    _quote_locator = (By.CLASS_NAME, 'quote-buckets')
    _education_locator = (By.ID, 'education')
    _information_locator = (By.CLASS_NAME, 'buckets')

    @property
    def loaded(self):
        """Return True when the banner carousel is displayed."""
        return self.carousel.is_displayed()

    def is_displayed(self):
        """Return True when the Web home page is displayed."""
        return self.loaded

    @property
    def carousel(self):
        """Access the book banner carousel."""
        region_root = self.find_element(*self._banner_locator)
        return self.BookBanners(self, region_root)

    @property
    def quotes(self):
        """Access the quote buckets."""
        region_root = self.find_element(*self._quote_locator)
        return self.Quotes(self, region_root)

    @property
    def education(self):
        """Access the education section and related links."""
        region_root = self.find_element(*self._education_locator)
        return self.Education(self, region_root)

    @property
    def information(self):
        """Access the informational links."""
        region_root = self.find_element(*self._information_locator)
        return self.Information(self, region_root)

    class BookBanners(Region):
        """The banner carousel."""

        _banner_image_locator = (By.CSS_SELECTOR, '.image-row a')
        _dot_button_locator = (By.CSS_SELECTOR, '.dots button')

        def is_displayed(self):
            """Return True when the carousel is displayed."""
            return self.root.is_displayed()

        @property
        def banners(self):
            """Access the banner."""
            return [self.Banner(self, el)
                    for el in self.find_elements(*self._banner_image_locator)]

        @property
        def dots(self):
            """Access the banner dot buttons."""
            return [self.Dot(self, el)
                    for el in self.find_elements(*self._dot_button_locator)]

        class Banner(Region):
            """An individual banner."""

            def is_displayed(self):
                """Return True if the banner is visible."""
                return self.root.is_displayed()

            @property
            def destination(self):
                """Return the destination URL."""
                return self.root.get_attribute('href')

            @property
            def image(self):
                """Return the image file name.

                Retrieve the style for the background image.
                Extract the CSS URL using a regular expression.
                Strip off the CSS URL delimiter.
                Split the URL and return the filename.
                """
                style = self.root.get_attribute('style')
                attribute = Support.FILENAME_MATCHER.search(style)
                file_url = attribute[4:-2]
                filename = file_url.split('/')[-1]
                return filename

            def click(self):
                """Go to the banner link destination.

                Return a 'Destination' so the function will fail if
                a new banner link is added.
                """
                if self.destination.endswith(Support.SUBJECTS):
                    from pages.web.subjects import Subjects as Destination
                elif self.destination.endswith(Support.ABOUT):
                    from pages.web.about import AboutUs as Destination
                Utility.wait_for_overlay_then(self.root.click)
                return go_to_(Destination(self.driver))

        class Dot(Region):
            """An individual sellection button."""

            @property
            def is_active(self):
                """Return True if the banner's dot is selected."""
                return 'active' in self.root.get_attribute('class')

            def click(self):
                """Select a dot to display the corresponding banner."""
                Utility.wait_for_overlay_then(self.root.click)
                return go_to_(WebHome(self.driver))

    class Quotes(Region):
        """Quotes and page links."""

        _bucket_locator = (By.CLASS_NAME, 'quote-bucket')

        @property
        def quotes(self):
            """Access the individual quotes."""
            return [self.Quote(self, el)
                    for el in self.find_elements(*self._bucket_locator)]

        def get(self, index):
            """Return a particular quote box."""
            return self.quote[index]

        class Quote(Region):
            """A single quote box."""

            _image_locator = (By.CLASS_NAME, 'image')
            _block_quote_locator = (By.TAG_NAME, 'quote-html')
            _button_locator = (By.CLASS_NAME, 'btn')

            def is_displayed(self):
                """Return True if the quote box is displayed."""
                return self.root.is_displayed()

            def show(self):
                """Scroll the quote box into view."""
                Utility.scroll_to(self.driver, element=self.root, shift=-80)
                return self

            @property
            def has_image(self):
                """Return True if the quote box has a background image."""
                try:
                    self.find_element(*self._image_locator)
                except NoSuchElementException:
                    return False
                return True

            @property
            def has_button(self):
                """Return True if the quote box has a link or button."""
                try:
                    self.find_element(*self._button_locator)
                except NoSuchElementException:
                    return False
                return True

            @property
            def text(self):
                """Return the quote text."""
                return self.find_element(*self._block_quote_locator).text

            @property
            def image(self):
                """Return the image element."""
                if self.has_image:
                    return self.find_element(*self._image_locator)

            @property
            def button(self):
                """Return the button or link element."""
                if self.has_button:
                    return self.find_element(*self._button_locator)

            def click(self):
                """Go to the link destination.

                Return a 'Destination' so the function will fail if
                a new quote is added.
                """
                destination = self.button.get_attribute('href')
                if Support.NEWSLETTER in destination:
                    Utility.switch_to(self.driver, action=self.button.click)
                    from pages.web.newsletter \
                        import NewsletterSignup as Destination
                elif Support.BOOKSTORE in destination:
                    self.button.click()
                    from pages.web.bookstore_suppliers \
                        import Bookstore as Destination
                else:
                    raise ValueError('Unknown destination: %s' % destination)
                sleep(1.0)
                return go_to_(Destination(self.driver))

    class Education(Region):
        """Education and page links."""

        _square_one_locator = (By.CLASS_NAME, 'square-1')
        _square_two_locator = (By.CLASS_NAME, 'square-2')
        _quote_locator = (By.CLASS_NAME, 'quote')
        _student_locator = (By.CLASS_NAME, 'student')
        _link_locator = (By.CSS_SELECTOR, '.links li')

        @property
        def box_one(self):
            """Return element one."""
            return self.find_element(*self._square_one_locator)

        @property
        def box_two(self):
            """Return element two."""
            return self.find_element(*self._square_two_locator)

        @property
        def quote(self):
            """Return the quote text."""
            return self.find_element(*self._quote_locator).text

        @property
        def student(self):
            """Return the student image element."""
            return self.find_element(*self._student_locator)

        @property
        def links(self):
            """Access the educational links."""
            return [Link(self, el)
                    for el in self.find_elements(*self._link_locator)]

        def show(self):
            """Scroll the section into view."""
            Utility.scroll_to(self.driver, element=self.root, shift=-80)
            return self.page

    class Information(Region):
        """Information buckets."""

        _bucket_locator = (By.CLASS_NAME, 'bucket')

        @property
        def box(self):
            """Access the individual buckets."""
            return [self.Bucket(self, el)
                    for el in self.find_elements(*self._bucket_locator)]

        def show(self):
            """Scroll the section into view."""
            Utility.scroll_to(self.driver, element=self.root, shift=-80)
            return self.page

        class Bucket(Link):
            """Individual information boxes."""

            _image_locator = (By.CLASS_NAME, 'image')

            @property
            def has_image(self):
                """Return True if the box has an image."""
                try:
                    self.find_element(*self._image_locator)
                    return True
                except NoSuchElementException:
                    return False
