"""OpenStax Partners."""

from time import sleep

from pypom import Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility, go_to_
from utils.web import TechProviders, Web


class Institutional(WebBase):
    """The OpenStax Institutional Partners page."""

    URL_TEMPLATE = '/institutional-partnership'

    _title_locator = (By.CSS_SELECTOR, '.banner h1')

    @property
    def loaded(self) -> bool:
        """Return True when the page is loaded.

        :return: ``True`` when the async hide class is not found, the template
            URL is in use, and the title banner is found
        :rtype: bool

        """
        return (super().loaded and
                self.URL_TEMPLATE in self.location and
                bool(self.find_elements(*self._title_locator)))

    def is_displayed(self) -> bool:
        """Return True when the page is displayed.

        :return: ``True`` when the page is loaded and the title is found
        :rtype: bool

        """
        title = self.find_elements(*self._title_locator)
        if not title:
            return False
        return self.loaded and 'Institutional' in title[0].text


class Partners(WebBase):
    """The OpenStax Partners page."""

    URL_TEMPLATE = '/partners'

    _company_locator = (
        By.CSS_SELECTOR, '.icons .logo:not(.spacer)')
    _current_filter_locator = (
        By.CSS_SELECTOR, '[aria-pressed=true]')
    _description_locator = (
        By.CSS_SELECTOR, '.hero .text-content p:nth-child(2)')
    _filter_button_locator = (
        By.CSS_SELECTOR, '.filter-button')
    _image_locator = (
        By.CSS_SELECTOR, 'img')
    _logo_description_locator = (
        By.CSS_SELECTOR, '.logo-text')
    _logo_locator = (
        By.CSS_SELECTOR, '.ally-logo')
    _return_to_your_book_link_locator = (
        By.CSS_SELECTOR, '[href*=details]')
    _summary_locator = (
        By.CSS_SELECTOR, '.text[id$=blurb]')
    _title_locator = (
        By.CSS_SELECTOR, '.hero h1')

    @property
    def loaded(self):
        """Return True if the title is set and images are visible."""
        return ('OpenStax Tech Scout' in self.title and
                Utility.is_image_visible(self.driver,
                                         locator=self._image_locator))

    @property
    def banner(self):
        """Return the page heading object."""
        return self.find_element(*self._title_locator)

    @property
    def companies(self):
        """Access the OpenStax Ally companies by their logos."""
        return [self.Company(self, logo)
                for logo in self.find_elements(*self._company_locator)]

    @property
    def current_filter(self):
        """Return the current filter."""
        return self.filter.text

    @property
    def description(self):
        """Return the subheading."""
        return self.find_element(*self._description_locator).text

    @property
    def filter(self):
        """Return the currently selected filter button."""
        return self.find_element(*self._current_filter_locator)

    @property
    def filter_buttons(self):
        """Access the subject filter buttons."""
        return self.find_elements(*self._filter_button_locator)

    @property
    def logo(self):
        """Return the OpenStax Ally logo."""
        return self.find_element(*self._logo_locator)

    @property
    def logo_description(self):
        """Return the ally logo meaning."""
        return self.find_element(*self._logo_description_locator).text

    @property
    def summaries(self):
        """Access the OpenStax Ally company summaries."""
        return [self.Summary(self, company)
                for company in self.find_elements(*self._summary_locator)]

    def return_to_your_book(self):
        """Click the 'your book' link."""
        print(self.find_element('css selector', '#main').get_attribute('outerHTML'))
        link = self.find_element(*self._return_to_your_book_link_locator)
        Utility.click_option(self.driver, element=link)
        from pages.web.book import Book
        return go_to_(Book(self.driver, base_url=self.base_url))

    def summary_by_name(self, name):
        """Return the summary for a particular company name."""
        for summary in self.summaries:
            if summary.name == name:
                return summary
        raise(ValueError('"{0}" not in the company summary list'.format(name)))

    @property
    def title(self):
        """Return the banner text."""
        return self.banner.text

    def filter_by(self, option):
        """Filter allies by a subject."""
        if option != self.current_filter:
            Utility.click_option(self.driver, element=self.filter)
            Utility.click_option(
                self.driver,
                element=self.filter_buttons[Web.PARTNER_FILTERS.get(option)])
        return self

    def is_displayed(self):
        """Return True if the hero banner is displayed."""
        return self.banner.is_displayed()

    class Company(Region):
        """A company logo and summary link."""

        _logo_locator = (
            By.CSS_SELECTOR, 'img')
        _link_locator = (
            By.CSS_SELECTOR, 'a')

        @property
        def link(self):
            """Return the anchor link to the company's summary."""
            return self.find_element(*self._link_locator)

        @property
        def logo(self):
            """Return the company logo."""
            return self.find_element(*self._logo_locator)

        @property
        def name(self):
            """Return the company name."""
            return self.logo.get_attribute('alt')

        def view(self):
            """Click the company logo."""
            Utility.click_option(self.driver, element=self.link)
            sleep(1.5)
            return self.page

    class Summary(Region):
        """An OpenStax Ally company summary."""

        _name_locator = (
            By.CSS_SELECTOR, 'h3')
        _description_locator = (
            By.CSS_SELECTOR, '[data-html$=description] p')
        _availability_locator = (
            By.CSS_SELECTOR, 'a')
        _return_locator = (
            By.CSS_SELECTOR, '.to-top')

        @property
        def availability(self):
            """Return the links to the resources available for an ally."""
            if self.name == TechProviders.OPEN_TEXTBOOK_NETWORK:
                return []
            return [link
                    for link
                    in (self.description_segments[-1]
                        .find_elements(*self._availability_locator))
                    if 'openstax' in link.get_attribute('href')]

        @property
        def description(self):
            """Return the full company description."""
            return '\n'.join(list(
                [paragraph.text for paragraph in self.description_segments]))

        @property
        def description_segments(self):
            """Return the pared list of description paragraphs."""
            return [paragraph
                    for paragraph
                    in self.find_elements(*self._description_locator)
                    if paragraph.text.strip()]

        @property
        def header(self):
            """Return the company name object."""
            return self.find_element(*self._name_locator)

        @property
        def name(self):
            """Return the company name."""
            return self.header.text

        @property
        def return_to_top_link(self):
            """Return the 'Return to top' link element."""
            return self.find_element(*self._return_locator)

        def return_to_top(self):
            """Click the 'Return to top' link."""
            Utility.click_option(self.driver, element=self.return_to_top_link)
            sleep(1.5)
            return self.page
