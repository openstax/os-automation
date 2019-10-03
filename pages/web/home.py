"""OpenStax's Web home page."""

from __future__ import annotations

from time import sleep

from pypom import Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from pages.web.legal import PrivacyPolicy
from utils.utilities import Utility, go_to_
from utils.web import Web, WebException


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
        if destination.endswith(Web.IMPACT):
            from pages.web.impact import OurImpact as Destination
        elif destination.endswith(Web.ANNUAL_REPORT):
            from pages.web.annual import AnnualReport as Destination
        elif destination.endswith(Web.PARTNERS):
            from pages.web.partners import Partners as Destination
        elif destination.endswith(Web.SUBJECTS):
            from pages.web.subjects import Subjects as Destination
        elif destination.endswith(Web.TECHNOLOGY):
            from pages.web.technology import Technology as Destination
        return go_to_(Destination(self.driver))


class WebHome(WebBase):
    """OpenStax Web home page."""

    URL_TEMPLATE = ''

    _banner_locator = (By.CSS_SELECTOR, '.banner-carousel')
    _quote_locator = (By.CSS_SELECTOR, '.quotes')
    _education_locator = (By.CSS_SELECTOR, '.education-banner')
    _information_locator = (By.CSS_SELECTOR, '.buckets-section')

    _cookie_notice_selector = '#dialog'

    @property
    def loaded(self):
        """Return True when the banner carousel and navs are displayed."""
        if self.driver.get_window_size().get('width') <= 960:
            return (self.carousel.is_displayed() and
                    self.footer.is_displayed() and
                    (sleep(1.0) or True))
        return (self.carousel.is_displayed() and
                self.web_nav.is_displayed() and
                self.openstax_nav.is_displayed() and
                self.footer.is_displayed() and
                (sleep(1.0) or True))

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

    @property
    def privacy(self):
        """Access the privacy and cookies notice.

        :return: the privacy and cookies dialog notice
        :rtype: :py:class:`~pages.web.home.WebHome.Dialog`

        """
        dialog = self.execute_script(
            f'return document.querySelector("{self._cookie_notice_selector}");'
        )
        return self.Dialog(self, dialog)

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
                attribute = Web.FILENAME_MATCHER.search(style)
                file_url = attribute[4:-2]
                filename = file_url.split('/')[-1]
                return filename

            def click(self):
                """Go to the banner link destination.

                Return a 'Destination' so the function will fail if
                a new banner link is added.
                """
                if self.destination.endswith(Web.SUBJECTS):
                    from pages.web.subjects import Subjects as Destination
                elif self.destination.endswith(Web.ABOUT):
                    from pages.web.about import AboutUs as Destination
                elif self.destination.endswith(Web.SE_APP):
                    from pages.web.se_app import StudyEdge as Destination
                else:
                    raise WebException(
                        'Unknown destination: {0}'
                        .format(self.destination.split('/')[-1]))
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

    class Dialog(Region):
        """The Privacy and Cookies dialog box pop up."""

        _dialog_title_locator = (By.CSS_SELECTOR, '#dialog-title')
        _got_it_button_locator = (By.CSS_SELECTOR, '.cookie-notice button')
        _message_content_locator = (By.CSS_SELECTOR, '.message')
        _privacy_policy_link_locator = (By.CSS_SELECTOR, '.message a')

        @property
        def content(self) -> str:
            """Return the dialog box text content.

            :return: the Privacy and Cookies dialog box text content
            :rtype: str

            """
            return (self.find_element(*self._message_content_locator)
                    .get_attribute('textContent'))

        def displayed(self) -> bool:
            """Return True if the dialog box is displayed.

            :return: ``True`` if the dialog box is displayed
            :rtype: bool

            """
            return self.driver.execute_script(
                'return arguments[0].hidden == false;',
                self.root)

        def got_it(self) -> WebHome:
            """Click the 'Got it!' button.

            :return: the home page
            :rtype: :py:class:`~pages.web.home.WebHome`

            """
            button = self.find_element(*self._got_it_button_locator)
            Utility.click_option(self.driver, element=button)
            self.wait.until(lambda _: not self.displayed())
            return self.page

        def privacy_policy(self) -> PrivacyPolicy:
            """Click on the privacy policy link.

            :return: the privacy policy page
            :rtype: :py:class:`~pages.web.legal.PrivacyPolicy`

            """
            link = self.find_element(*self._privacy_policy_link_locator)
            Utility.click_option(self.driver, element=link)
            return go_to_(
                PrivacyPolicy(self.driver, base_url=self.page.base_url))

        @property
        def title(self) -> str:
            """Return the dialog box title.

            :return: the Privacy and Cookies dialog box title
            :rtype: str

            """
            return self.find_element(*self._dialog_title_locator).text

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
            return self.quotes[index]

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
                if Web.NEWSLETTER in destination:
                    Utility.switch_to(self.driver, action=self.button.click)
                    from pages.web.newsletter \
                        import NewsletterSignup as Destination
                elif Web.BOOKSTORE in destination:
                    Utility.switch_to(self.driver, action=self.button.click)
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
