"""OpenStax About Us Page."""

from time import sleep

from pypom import Region
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
        return (self.who_we_are.is_displayed
                and self.what_we_do.is_displayed
                and self.where_were_going.is_displayed)

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
        _foundation_link_locator = (By.CSS_SELECTOR, '[href$=foundation]')
        _resources_link_locator = (By.CSS_SELECTOR, '[href$=partners]')
        _faq_link_locator = (By.CSS_SELECTOR, '[href$=faq]')

        @property
        def is_displayed(self):
            """Return True if the panel is displayed."""
            return self.root.is_displayed

        def foundations(self):
            """Follow the philanthropic foundations link."""
            self.find_element(*self._foundation_link_locator).click()
            sleep(1.0)
            from pages.web.supporters import Supporters
            return Supporters(self.driver)

        def resources(self):
            """Follow the educational resources link."""
            self.find_element(*self._resources_link_locator).click()
            sleep(1.0)
            from pages.web.partners import Partners
            return Partners(self.driver)

        def faq(self):
            """Follow the FAQ link."""
            self.find_element(*self._faq_link_locator).click()
            sleep(1.0)
            from pages.web.faq import FAQ
            return FAQ(self.driver)

    class WhatWeDo(Region):
        """The What we do panel."""

        @property
        def is_displayed(self):
            """Return True if the panel is displayed."""
            return self.root.is_displayed

    class WhereWereGoing(Region):
        """The Where we're going panel."""

        @property
        def is_displayed(self):
            """Return True if the panel is displayed."""
            return self.root.is_displayed
