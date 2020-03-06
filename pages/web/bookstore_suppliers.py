"""The textbook suppliers page."""

from __future__ import annotations

from typing import List

from pypom import Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from pages.web.subjects import Subjects
from utils.utilities import Utility, go_to_
from utils.web import WebException

IS_DISPLAYED = (
    'return window.getComputedStyle(arguments[0]).display != "none";')


class Bookstore(WebBase):
    """The print bookstore supplier page."""

    URL_TEMPLATE = '/bookstore-suppliers'

    _description_locator = (
        By.CSS_SELECTOR, '.text .small-screen, .text .larger-screen')
    _other_provider_locator = (
        By.CSS_SELECTOR, '.cards .card')
    _preferred_provider_locator = (
        By.CSS_SELECTOR, '.card.featured')
    _price_list_locator = (
        By.CSS_SELECTOR, '.split-card > div')
    _subjects_page_link_locator = (
        By.CSS_SELECTOR, '.text .larger-screen a')
    _title_locator = (
        By.CSS_SELECTOR, '.hero h1')

    @property
    def description(self) -> str:
        """Return the explanation text.

        :return: the subheading text for either large or small displays
        :rtype: str

        """
        return ''.join([content.get_attribute('textContent')
                        for content
                        in self.find_elements(*self._description_locator)
                        if self.driver.execute_script(IS_DISPLAYED, content)])

    def is_displayed(self) -> bool:
        """Return True when the bookstore providers are found.

        :return: ``True`` when the preferred and other providers are found
        :rtype: bool

        """
        return bool(self.preferred_provider) and bool(self.other_providers)

    @property
    def other_providers(self) -> List[Bookstore.Provider]:
        r"""Access the non-preferred OpenStax book provider blocks.

        :return: the list of other available bookstore provider blocks
        :rtype: list(:py:class:`~pages.web.bookstore_suppliers \
                                .Bookstore.Provider`)

        """
        return [self.Provider(self, option)
                for option
                in self.find_elements(*self._other_provider_locator)]

    @property
    def preferred_provider(self) -> Bookstore.Provider:
        """Access the preferred OpenStax book provider block.

        :return: the preferred bookstore provider box
        :rtype: :py:class:`~pages.web.bookstore_suppliers.Bookstore.Provider`

        """
        preferred = self.find_element(*self._preferred_provider_locator)
        return self.Provider(self, preferred)

    @property
    def price_lists(self) -> List[Bookstore.PriceList]:
        r"""Access the book price list by available countries.

        :return: the list of book pricing by country
        :rtype: list(:py:class:`~pages.web.bookstore_suppliers \
                                .Bookstore.PriceList`)

        """
        return [self.PriceList(self, country)
                for country
                in self.find_elements(*self._price_list_locator)]

    @property
    def title(self) -> str:
        """Return the page heading.

        :return: the page heading
        :rtype: str

        """
        return self.find_element(*self._title_locator).text

    def subjects_page(self) -> Subjects:
        """Click the 'Subjects page' link in the larger screen description.

        :return: the book subjects page
        :rtype: :py:class:`~pages.web.subjects.Subjects`
        :raises :py:class:`~utils.web.WebException`: if the link is unavailable
            because the user is viewing the page on a phone resolution

        """
        if self.is_phone:
            raise WebException('link not available when viewing on a phone')
        link = self.find_element(*self._subjects_page_link_locator)
        Utility.click_option(self.driver, element=link)
        return go_to_(Subjects(self.driver, base_url=self.base_url))

    class PriceList(Region):
        """A print copy price list."""

        _view_list_button_locator = (
            By.CSS_SELECTOR, 'a')

        @property
        def country(self) -> str:
            """Return the price list country.

            :return: the country name for the pricing list
            :rtype: str

            """
            return self.root.text.split('(')[-1][:-1]

        @property
        def url(self) -> str:
            """Return the URL for the price list PDF.

            :return: the source URL for the price list PDF document
            :rtype: str

            """
            return (self.find_element(*self._view_list_button_locator)
                    .get_attribute('href'))

        def view(self):
            """Click the 'Order from' button.

            :return: None

            """
            button = self.find_element(*self._view_list_button_locator)
            Utility.click_option(self.driver, element=button)

    class Provider(Region):
        """A print copy provider."""

        _canadian_flag_locator = (
            By.CSS_SELECTOR, '.canada-flag')
        _description_locator = (
            By.CSS_SELECTOR, '.blurb')
        _name_locator = (
            By.CSS_SELECTOR, 'h2')
        _order_from_button_locator = (
            By.CSS_SELECTOR, 'a.primary')

        @property
        def description(self) -> str:
            """Return the bookstore company description.

            :return: the company description
            :rtype: str

            """
            return self.find_element(*self._description_locator).text

        @property
        def has_candian_flag(self) -> bool:
            """Return True if the Canadian flag icon is displayed.

            :return: ``True`` if the bookstore provider has a Canadian flag
                icon displayed
            :rtype: bool

            """
            return bool(self.find_elements(*self._canadian_flag_locator))

        @property
        def name(self) -> str:
            """Return the bookstore name.

            :return: the bookstore company name
            :rtype: str

            """
            return self.find_element(*self._name_locator).text

        @property
        def url(self) -> str:
            """Return the bookstore provider webpage URL.

            :return: the URL for the bookstore provider
            :rtype: str

            """
            return (self.find_element(*self._order_from_button_locator)
                    .get_attribute('href'))

        def order_from(self):
            """Click the 'Order from' button.

            :return: None

            """
            button = self.find_element(*self._order_from_button_locator)
            Utility.click_option(self.driver, element=button)
