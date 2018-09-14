"""OpenStax About Us Page."""

from pypom import Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class AboutUs(WebBase):
    """About Us page."""

    URL_TEMPLATE = '/about'

    _who_section_locator = (By.CLASS_NAME, 'who')
    _what_section_locator = (By.CLASS_NAME, 'what')
    _where_section_locator = (By.CLASS_NAME, 'where')
    _map_locator = (By.CLASS_NAME, 'map')

    @property
    def loaded(self):
        return (self.who_we_are.loaded
                and self.what_we_do.loaded
                and self.where_were_going.loaded)

    @property
    def who_we_are(self):
        """Access the Who we are panel."""
        who = self.find_element(*self._who_section_locator)
        return self.WhoWeAre(self, who)

    @property
    def what_we_do(self):
        """Access the What we do panel."""
        what = self.find_element(*self._what_section_locator)
        return self.WhatWeDo(self, what)

    @property
    def where_were_going(self):
        where = self.find_element(*self._where_section_locator)
        return self.WhereWereGoing(self, where)

    @property
    def content_map(self):
        return self.find_element(*self._map_locator)

    class WhoWeAre(Region):
        """The Who we are panel."""

        _child_locator = (By.TAG_NAME, 'div')

        @property
        def loaded(self):
            try:
                self.find_element(*self._child_locator)
            except NoSuchElementException:
                return False
            return True

        @property
        def is_displayed(self):
            return self.root.is_displayed

    class WhatWeDo(Region):
        """The What we do panel."""

        @property
        def is_displayed(self):
            return self.root.is_displayed

    class WhereWereGoing(Region):
        """The Where we're going panel."""

        @property
        def is_displayed(self):
            return self.root.is_displayed
