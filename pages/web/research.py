"""The Web research overview page."""

import re

from pypom import Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility
from utils.web import Web


class Research(WebBase):
    """The researchers page."""

    URL_TEMPLATE = '/research'

    FULL = 'tab-content'
    PHONE = '.accordion-item'
    ALUMNI_FIRST = ':first-child .entry'
    ALUMNI_LAST = ':last-child .entry'
    MEMBER = ' .members-tab .card'

    _title_locator = (By.CSS_SELECTOR, '.hero h1')
    _mission_locator = (By.CSS_SELECTOR, '.hero h1 ~ div')
    _banner_locator = (By.CSS_SELECTOR, '.images img')
    _project_locator = (By.CSS_SELECTOR, '.current-projects .card')
    _publication_locator = (By.CSS_SELECTOR, '.publication')

    _tab_locator = (By.CSS_SELECTOR, '.tab')
    _bar_locator = (By.CSS_SELECTOR, '.accordion-item')

    _alumni_locator_full = (
        By.CSS_SELECTOR, FULL + ' .alumni-tab' + ALUMNI_FIRST)
    _members_locator_full = (By.CSS_SELECTOR, FULL + MEMBER)
    _external_locator_full = (
        By.CSS_SELECTOR, FULL + '.alumni-tab' + ALUMNI_LAST)

    _alumni_locator_phone = (By.CSS_SELECTOR, PHONE + ALUMNI_FIRST)
    _members_locator_phone = (By.CSS_SELECTOR, PHONE + MEMBER)
    _external_locator_phone = (By.CSS_SELECTOR, PHONE + ALUMNI_LAST)

    @property
    def loaded(self):
        """Override the base loader."""
        return self.find_element(*self._title_locator)

    def is_displayed(self):
        """Return True if the research page is displayed."""
        return self.find_element(*self._title_locator).is_displayed()

    @property
    def title(self):
        """Return the banner title."""
        return self.find_element(*self._title_locator).text

    @property
    def mission(self):
        """Return the mission statement body."""
        return self.find_element(*self._mission_locator).text

    @property
    def banner(self):
        """Return the banner image elements."""
        return self.find_elements(*self._banner_locator)

    @property
    def projects(self):
        """Access the research project cards."""
        return [self.Card(self, project)
                for project in self.find_elements(*self._project_locator)]

    @property
    def tabs(self):
        """Access the research team display tabs."""
        return [self.Tab(self, tab)
                for tab in self.find_elements(*self._tab_locator)]

    @property
    def bars(self):
        """Access the phone view group bars."""
        return [self.Bar(self, bar)
                for bar in self.find_elements(*self._bar_locator)]

    @property
    def alumni(self):
        """Access the research alumni cards."""
        return self._person_selector(self._alumni_locator_phone,
                                     self._alumni_locator_full,
                                     self.Entry)

    @property
    def team(self):
        """Access the current research team member cards."""
        return self._person_selector(self._members_locator_phone,
                                     self._members_locator_full,
                                     self.Person)

    @property
    def external(self):
        """Access the external collaborator cards."""
        return self._person_selector(self._external_locator_phone,
                                     self._external_locator_full,
                                     self.Entry)

    @property
    def publications(self):
        """Access the published research paper overviews."""
        return [self.Publication(self, document)
                for document in self.find_elements(*self._publication_locator)]

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
            Utility.click_option(self.driver, element=self.root)
            return self.page

        @property
        def is_open(self):
            """Return True if the tab is currently selected."""
            return self.root.get_attribute('aria-current') == 'page'

    class Bar(Region):
        """A group bar for a phone view accordion menu."""

        _name_locator = (By.CSS_SELECTOR, '.label')
        _toggle_locator = (By.CSS_SELECTOR, '.accordion-button')
        _open_status_locator = (By.CSS_SELECTOR, '.accordion-button .chevron')

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
            Utility.click_option(self.driver, element=self.toggle_bar)
            return self.page

        @property
        def is_open(self):
            """Return True if the accordion region is open."""
            chevron = self.find_element(*self._open_status_locator)
            return 'chevron-down' in chevron.get_attribute('innerHTML')

    class Card(Region):
        """A current research project."""

        _topic_locator = (By.CSS_SELECTOR, 'h2')
        _summary_locator = (By.CSS_SELECTOR, 'h2 ~ div')

        @property
        def topic(self):
            """Return the research project topic."""
            return self.find_element(*self._topic_locator).text

        @property
        def summary(self):
            """Return the research summary."""
            return self.find_element(*self._summary_locator).text

        def view(self):
            """Scroll to the individual card."""
            Utility.scroll_to(self.driver, element=self.root)
            return self

    class Entry(Region):
        """An alumni researcher or external collaborator."""

        _name_locator = (By.CSS_SELECTOR, '.name')
        _role_locator = (By.CSS_SELECTOR, '.description')

        @property
        def name(self):
            """Return the member's name."""
            return self.find_element(*self._name_locator).text.strip()

        @property
        def role(self):
            """Return the member's role or affiliation."""
            return self.find_element(*self._role_locator).text.strip()

        def view(self):
            """Scroll to the individual card."""
            Utility.scroll_to(self.driver, element=self.root, shift=-15)
            return self

        @property
        def is_visible(self):
            """Return True if the person's card is in the viewport."""
            return Utility.in_viewport(self.driver, element=self.root,
                                       ignore_bottom=True, display_marks=True)

    class Person(Entry):
        """A current member of the research team."""

        _headshot_locator = (By.CSS_SELECTOR, 'img')
        _role_locator = (By.CSS_SELECTOR, '.name ~ div')

        @property
        def headshot(self):
            """Return the image element."""
            return self.find_element(*self._headshot_locator)

    class Publication(Region):
        """A research publication."""

        _headline_locator = (By.CSS_SELECTOR, '.headline')
        _summary_locator = (By.CSS_SELECTOR, '[data-html$=excerpt]')
        _document_locator = (By.CSS_SELECTOR, 'a')

        @property
        def headline(self):
            """Return the headline text."""
            return self.find_element(*self._headline_locator).text

        @property
        def authors(self):
            """Return the authors from the headline."""
            return re.split(r' \(|\). ', self.headline)[Web.AUTHOR]

        @property
        def title(self):
            """Return the publication title from the headline."""
            return re.split(r' \(|\). ', self.headline)[Web.TITLE]

        @property
        def year(self):
            """Return the publication year from the headline."""
            return re.split(r' \(|\). ', self.headline)[Web.YEAR]

        @property
        def summary(self):
            """Return the publication summary."""
            return self.find_element(*self._summary_locator).text

        @property
        def document(self):
            """Return the publication PDF URL."""
            return (self.find_element(*self._document_locator)
                    .get_attribute('href'))

        def view(self):
            """Scroll to the individual card."""
            Utility.scroll_to(self.driver, element=self.root)
            return self
