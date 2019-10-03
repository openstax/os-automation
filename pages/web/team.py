"""The OpenStax team and advisor page."""

from pypom import Region
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility
from utils.web import Web


class Individual(Region):
    """A base class for members of the OpenStax team."""

    _name_locator = (By.CSS_SELECTOR, '.name')
    _bio_locator = (By.CSS_SELECTOR, '.bio')

    @property
    def name(self):
        """Return the advisor's name."""
        return self.find_element(*self._name_locator).text.strip()

    @property
    def bio(self):
        """Return the advisor's biography."""
        return self.find_element(*self._bio_locator).text.strip()

    def view(self):
        """Scroll to the advisor's card."""
        Utility.scroll_to(self.driver, element=self.root, shift=-80)
        return self

    @property
    def is_visible(self):
        """Return True if the person's card is in the viewport."""
        return Utility.in_viewport(self.driver, element=self.root,
                                   ignore_bottom=True, display_marks=True)


class Team(WebBase):
    """The OpenStax team and advisors page."""

    URL_TEMPLATE = '/team'

    PHONE = 'accordion-region'
    FULL = 'tab-content'
    PERSON = ' .people-tab:not(.inline-bios) .card:not(.bio)'
    ADVISOR = ' .people-tab.inline-bios .card:not(.bio)'
    FAB = ' '

    _title_locator = (By.CSS_SELECTOR, '.hero h1')
    _blurb_locator = (By.CSS_SELECTOR, _title_locator[1] + ' ~ div')
    _banner_locator = (By.CSS_SELECTOR, '.picture-content img')

    _tab_locator = (By.CSS_SELECTOR, '.tab-group h3')
    _bar_locator = (By.CSS_SELECTOR, '.accordion-item')

    _advisor_locator_phone = (By.CSS_SELECTOR, PHONE + ADVISOR)
    _people_locator_phone = (By.CSS_SELECTOR, PHONE + PERSON)
    _fab_locator_phone = (By.CSS_SELECTOR, PHONE + FAB)

    _people_locator_full = (By.CSS_SELECTOR, FULL + PERSON)
    _advisor_locator_full = (By.CSS_SELECTOR, FULL + ADVISOR)
    _fab_locator_full = (By.CSS_SELECTOR, FULL + FAB)

    @property
    def loaded(self):
        """Return True when banner is visible."""
        return (super().loaded and
                Utility.is_image_visible(self.driver, image=self.banner))

    def is_displayed(self):
        """Return True if the team page is displayed."""
        return ('team effort' in self.title and
                self.banner.is_displayed())

    @property
    def title(self):
        """Return the page title."""
        return self.find_element(*self._title_locator).text

    @property
    def subheading(self):
        """Return the subheading text."""
        return self.find_element(*self._blurb_locator).text

    @property
    def banner(self):
        """Return the banner image element."""
        return self.find_element(*self._banner_locator)

    @property
    def tabs(self):
        """Access the group tabs."""
        return [self.Tab(self, tab)
                for tab in self.find_elements(*self._tab_locator)]

    @property
    def bars(self):
        """Access the phone view group bars."""
        return [self.Bar(self, bar)
                for bar in self.find_elements(*self._bar_locator)]

    @property
    def people(self):
        """Access the OpenStax staff bio cards."""
        return self._person_selector(self._people_locator_phone,
                                     self._people_locator_full,
                                     self.Person)

    @property
    def advisors(self):
        """Access the strategic advisors bio cards."""
        return self._person_selector(self._advisor_locator_phone,
                                     self._advisor_locator_full,
                                     self.Advisor)

    @property
    def fab(self):
        """Access the faculty adisory board bio cards."""
        return self._person_selector(self._fab_locator_phone,
                                     self._fab_locator_full,
                                     self.FacultyAdvisor)

    def _person_selector(self, phone, full, group):
        """Select the appropriate list of people."""
        mobile = self.driver.get_window_size().get('width') <= Web.PHONE
        locator = phone if mobile else full
        return [group(self, card)
                for card in self.find_elements(*locator)]

    class Tab(Region):
        """A group tab view."""

        @property
        def name(self):
            """Return the tab group name."""
            return self.root.text.strip()

        def select(self):
            """Select a group tab to view."""
            Utility.safari_exception_click(self.driver, element=self.root)
            return self.page

        @property
        def is_open(self):
            """Return True if the tab is currently selected."""
            return self.root.get_attribute('aria-current') == 'page'

    class Bar(Region):
        """A group bar for a phone view accordion menu."""

        _name_locator = (By.CSS_SELECTOR, '.label')
        _toggle_locator = (By.CSS_SELECTOR, '.control-bar')
        _open_status_locator = (By.CSS_SELECTOR, '.control-bar .chevron')

        @property
        def name(self):
            """Return the bar region group name."""
            return self.find_element(*self._name_locator).text.strip()

        @property
        def toggle_bar(self):
            """Return the toggle bar element."""
            return self.find_element(*self._toggle_locator)

        def toggle(self):
            """Open or close the bar region."""
            Utility.safari_exception_click(self.driver,
                                           element=self.toggle_bar)
            return self.page

        @property
        def is_open(self):
            """Return True if the accordion region is open."""
            chevron = self.find_element(*self._open_status_locator)
            return 'chevron-down' in chevron.get_attribute('innerHTML')

    class Person(Individual):
        """A staff member bio."""

        _image_locator = (By.CSS_SELECTOR, 'img')
        _role_locator = (By.CSS_SELECTOR, '.name ~ div')
        _bio_selector = '.card.bio.tooltip'

        @property
        def headshot(self):
            """Return the headshot image."""
            return self.find_element(*self._image_locator)

        @property
        def role(self):
            """Return the person's role at OpenStax."""
            return self.find_element(*self._role_locator).text.strip()

        @property
        def bio(self):
            """Return the person's biography blurb.

            Use a script because the bio is inserted inline with the cards and
            doesn't fall within the card tree.
            """
            script = ('return document.querySelector("{locator}").textContent;'
                      .format(locator=self._bio_selector))
            return self.driver.execute_script(script)

        def select(self):
            """Click on the person's card to open or close the bio."""
            Utility.safari_exception_click(self.driver, element=self.root)
            return self

        @property
        def has_bio(self):
            """Return True if the person has an associated biography."""
            return self.root.get_attribute('role') == 'button'

        @property
        def bio_visible(self):
            """Return True if the bio is currently open."""
            try:
                return self.bio
            except WebDriverException:
                return False

    class Advisor(Individual):
        """A strategic advisor bio."""

    class FacultyAdvisor(Individual):
        """A faculty advisory board member bio."""
