"""The OpenStax team and advisor page."""

from __future__ import annotations

from typing import List

from pypom import Region
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.web.base import WebBase
from utils.utilities import Utility
from utils.web import Web


class Individual(Region):
    """A base class for members of the OpenStax team."""

    _bio_locator = (
        By.CSS_SELECTOR, '.bio')
    _name_locator = (
        By.CSS_SELECTOR, '.name')

    @property
    def name(self) -> str:
        """Return the advisor's name."""
        return self.find_element(*self._name_locator).text.strip()

    @property
    def bio(self) -> str:
        """Return the advisor's biography."""
        return self.find_element(*self._bio_locator).text.strip()

    def view(self) -> Region:
        """Scroll to the advisor's card."""
        Utility.scroll_to(self.driver, element=self.root, shift=-80)
        return self

    @property
    def is_visible(self) -> bool:
        """Return True if the person's card is in the viewport."""
        return Utility.in_viewport(self.driver, element=self.root,
                                   ignore_bottom=True, display_marks=True)


class Team(WebBase):
    """The OpenStax team and advisors page."""

    URL_TEMPLATE = '/team'

    _advisor_locator_full = (
        By.CSS_SELECTOR, 'tab-content .people-tab:last-child .card')
    _advisor_locator_phone = (
        By.CSS_SELECTOR, 'accordion-region .accordion-item:last-child .card')
    _bar_locator = (
        By.CSS_SELECTOR, '.accordion-item')
    _blurb_locator = (
        By.CSS_SELECTOR, '.hero h1 ~ div')
    _banner_locator = (
        By.CSS_SELECTOR, '.picture-content img')
    _people_locator_full = (
        By.CSS_SELECTOR, 'tab-content .people-tab:first-child .card')
    _people_locator_phone = (
        By.CSS_SELECTOR, 'accordion-region .accordion-item:first-child .card')
    _tab_locator = (
        By.CSS_SELECTOR, '.tab-group h3')
    _title_locator = (
        By.CSS_SELECTOR, '.hero h1')

    @property
    def loaded(self) -> bool:
        """Return True when banner is visible."""
        return (super().loaded and
                Utility.is_image_visible(self.driver, image=self.banner))

    def is_displayed(self) -> bool:
        """Return True if the team page is displayed."""
        return 'team effort' in self.title and self.banner.is_displayed()

    @property
    def title(self) -> str:
        """Return the page title."""
        return self.find_element(*self._title_locator).text

    @property
    def subheading(self) -> str:
        """Return the subheading text."""
        return self.find_element(*self._blurb_locator).text

    @property
    def banner(self) -> WebElement:
        """Return the banner image element."""
        return self.find_element(*self._banner_locator)

    @property
    def tabs(self) -> List[Team.Tab]:
        """Access the group tabs."""
        return [self.Tab(self, tab)
                for tab
                in self.find_elements(*self._tab_locator)]

    @property
    def bars(self) -> List[Team.Bar]:
        """Access the phone view group bars."""
        return [self.Bar(self, bar)
                for bar
                in self.find_elements(*self._bar_locator)]

    @property
    def people(self) -> List[Team.Person]:
        """Access the OpenStax staff bio cards."""
        return self._person_selector(self._people_locator_phone,
                                     self._people_locator_full,
                                     self.Person)

    @property
    def advisors(self) -> List[Team.Advisor]:
        """Access the strategic advisors bio cards."""
        return self._person_selector(self._advisor_locator_phone,
                                     self._advisor_locator_full,
                                     self.Advisor)

    def _person_selector(self, phone, full, group) -> List[Region]:
        """Select the appropriate list of people."""
        mobile = self.driver.get_window_size().get('width') <= Web.PHONE
        locator = phone if mobile else full
        return [group(self, card)
                for card
                in self.find_elements(*locator)]

    class Tab(Region):
        """A group tab view."""

        @property
        def name(self) -> str:
            """Return the tab group name."""
            return self.root.text.strip()

        def select(self) -> Team:
            """Select a group tab to view."""
            Utility.click_option(self.driver, element=self.root)
            return self.page

        @property
        def is_open(self) -> bool:
            """Return True if the tab is currently selected."""
            return self.root.get_attribute('aria-current') == 'page'

    class Bar(Region):
        """A group bar for a phone view accordion menu."""

        _name_locator = (
            By.CSS_SELECTOR, '.label')
        _open_status_locator = (
            By.CSS_SELECTOR, '.chevron')
        _toggle_locator = (
            By.CSS_SELECTOR, '.accordion-button , .control-bar')

        @property
        def name(self) -> str:
            """Return the bar region group name."""
            return self.find_element(*self._name_locator).text.strip()

        @property
        def toggle_bar(self) -> WebElement:
            """Return the toggle bar element."""
            return self.find_element(*self._toggle_locator)

        def toggle(self) -> Team:
            """Open or close the bar region."""
            Utility.click_option(self.driver, element=self.toggle_bar)
            return self.page

        @property
        def is_open(self) -> bool:
            """Return True if the accordion region is open."""
            chevron = self.find_element(*self._open_status_locator)
            return 'chevron-down' in chevron.get_attribute('innerHTML')

    class Person(Individual):
        """A staff member bio."""

        _image_locator = (
            By.CSS_SELECTOR, 'img')
        _role_locator = (
            By.CSS_SELECTOR, '.name ~ div')

        _bio_selector = '.card.bio.tooltip'

        @property
        def headshot(self) -> WebElement:
            """Return the headshot image."""
            return self.find_element(*self._image_locator)

        @property
        def role(self) -> str:
            """Return the person's role at OpenStax."""
            return self.find_element(*self._role_locator).text.strip()

        @property
        def bio(self) -> str:
            """Return the person's biography blurb.

            Use a script because the bio is inserted inline with the cards and
            doesn't fall within the card tree.
            """
            script = ('return document.querySelector'
                      f'("{self._bio_selector}").textContent;')
            return self.driver.execute_script(script)

        def select(self) -> Team.Person:
            """Click on the person's card to open or close the bio."""
            Utility.click_option(self.driver, element=self.root)
            return self

        @property
        def has_bio(self) -> bool:
            """Return True if the person has an associated biography."""
            return self.root.get_attribute('role') == 'button'

        @property
        def bio_visible(self) -> bool:
            """Return True if the bio is currently open."""
            try:
                return bool(self.bio)
            except WebDriverException:
                return False

    class Advisor(Individual):
        """A strategic advisor bio."""

    class FacultyAdvisor(Individual):
        """A faculty advisory board member bio."""
