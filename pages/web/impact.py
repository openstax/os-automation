"""The OpenStax textbook impact webpage."""

from __future__ import annotations

from typing import List

from pypom import Region
from selenium.webdriver.common.by import By

from pages.rice.riceconnect import RiceConnect
from pages.web.base import WebBase
from pages.web.blog import Article
from pages.web.global_reach import GlobalReach
from pages.web.partners import Partners
from pages.web.subjects import Subjects
from pages.web.tutor import TutorMarketing
from utils.utilities import Utility, go_to_


class Impact(WebBase):
    """The Impact page."""

    _banner_give_today_button_locator = (
        By.CSS_SELECTOR, '#banner a')
    _page_description_locator = (
        By.CSS_SELECTOR, '#banner p')
    _page_heading_locator = (
        By.CSS_SELECTOR, '#banner h1')

    _doerr_statement_locator = (
        By.CSS_SELECTOR, '#revolution')

    _vision_statement_locator = (
        By.CSS_SELECTOR, '#founding')

    _student_reach_locator = (
        By.CSS_SELECTOR, '.reach > .text-block')
    _student_reach_stat_locator = (
        By.CSS_SELECTOR, '#reach .card')

    _testimonial_locator = (
        By.CSS_SELECTOR, '#testimonials .card')

    _partnerships_locator = (
        By.CSS_SELECTOR, '#sustainability .text-content')
    _partner_list_link_locator = (
        By.CSS_SELECTOR, '[href$=partners]')

    _disruption_locator = (
        By.CSS_SELECTOR, '#disruption')

    _business_books_link_locator = (
        By.CSS_SELECTOR, '#looking_ahead a')
    _looking_ahead_locator = (
        By.CSS_SELECTOR, '#lookingAhead')

    _map_exploration_locator = (
        By.CSS_SELECTOR, '#map a')
    _textbook_use_locator = (
        By.CSS_SELECTOR, '#map')

    _tutor_information_link_locator = (
        By.CSS_SELECTOR, '#tutor a')
    _tutor_locator = (
        By.CSS_SELECTOR, '#tutor')

    _philanthropic_locator = (
        By.CSS_SELECTOR, '#philanthropic-partners')

    _giving_locator = (
        By.CSS_SELECTOR, '#giving')
    _giving_give_today_button_locator = (
        By.CSS_SELECTOR, '#giving a')

    @property
    def description(self) -> str:
        """Return the page description.

        :return: the impact page description
        :rtype: str

        """
        content = self.find_element(*self._page_description_locator)
        return content.text if content.is_displayed() else ''

    @property
    def disruption(self) -> str:
        """Return the positive disruption to textbook prices statement.

        :return: the price disruption statement
        :rtype: str

        """
        return (self.find_element(*self._disruption_locator)
                .get_attribute('textContent'))

    @property
    def doerr_statement(self) -> str:
        """Return the Ann Doerr education revolution statement.

        :return: the Ann Doerr revolution in education letter
        :rtype: str

        """
        return (self.find_element(*self._doerr_statement_locator)
                .get_attribute('textContent'))

    @property
    def giving(self) -> str:
        """Return the donation request.

        :return: the donation and support request
        :rtype: str

        """
        return (self.find_element(*self._giving_locator)
                .get_attribute('textContent'))

    @property
    def heading(self) -> str:
        """Return the page heading.

        :return: the impact page heading statement
        :rtype: str

        """
        return self.find_element(*self._page_heading_locator).text

    @property
    def loaded(self) -> bool:
        """Return True when the impact page heading is found.

        :return: ``True`` when the impact page heading is found
        :rtype: bool

        """
        return super().loaded and self.heading

    @property
    def looking_ahead(self) -> str:
        """Return the OpenStax ecosystem outlook statement.

        :return: the planned direction statement for the OpenStax ecosystem
        :rtype: str

        """
        return (self.find_element(*self._looking_ahead_locator)
                .get_attribute('textContent'))

    @property
    def partnerships(self) -> str:
        """Return the textbook ecosystem partnerships statement.

        :return: the textbook ecosystem partnerships statement
        :rtype: str

        """
        return (self.find_element(*self._partnerships_locator)
                .get_attribute('textContent'))

    @property
    def philanthropic_partners(self) -> str:
        """Return the philanthropic partners statement and quote.

        :return: the philanthropic thank you and Bob Maxfield's quote
        :rtype: str

        """
        return (self.find_element(*self._philanthropic_locator)
                .get_attribute('textContent'))

    @property
    def student_reach(self) -> str:
        """Return the student impact statement.

        :return: the student reach and impact statement
        :rtype: str

        """
        return (self.find_element(*self._student_reach_locator)
                .get_attribute('textContent'))

    @property
    def student_reach_stats(self) -> List[Impact.StatBox]:
        """Access the student impact number boxes.

        :return: the list of student impact boxes
        :rtype: list(:py:class:`~pages.web.impact.Impact.StatBox`)

        """
        return [self.StatBox(self, box)
                for box
                in self.find_elements(*self._student_reach_stat_locator)]

    @property
    def testimonials(self) -> List[Impact.Testimonial]:
        """Access the user testimonial quote boxes.

        :return: the list of user testimonial quote boxes
        :rtype: list(:py:class:`~pages.web.impact.Impact.Testimonial`)

        """
        return [self.Testimonial(self, quote)
                for quote
                in self.find_elements(*self._testimonial_locator)]

    @property
    def textbook_use(self) -> str:
        """Return the global textbook use statement.

        :return: the global use of OpenStax textbooks statement
        :rtype: str

        """
        return (self.find_element(*self._textbook_use_locator)
                .get_attribute('textContent'))

    @property
    def tutor(self) -> str:
        """Return the OpenStax Tutor Beta overview statement.

        :return: the OpenStax Tutor Beta overview statement
        :rtype: str

        """
        return (self.find_element(*self._tutor_locator)
                .get_attribute('textContent'))

    @property
    def vision_statement(self) -> str:
        """Return the founding vision statement.

        :return: the founding vision statement
        :rtype: str

        """
        return (self.find_element(*self._vision_statement_locator)
                .get_attribute('textContent'))

    def business_textbooks(self) -> Subjects:
        """Click the 'business textbooks' link.

        :return: the subjects page displaying the business books
        :rtype: :py:class:`~pages.web.subjects.Subjects`

        """
        link = self.find_element(*self._business_books_link_locator)
        Utility.click_option(self.driver, element=link)
        return go_to_(Subjects(self.driver, base_url=self.base_url))

    def explore_our_interactive_map(self) -> GlobalReach:
        """Click the interactive map link.

        :return: the global reach page
        :rtype: :py:class:`~pages.web.global_reach.GlobalReach`

        """
        link = self.find_element(*self._map_exploration_locator)
        Utility.click_option(self.driver, element=link)
        return go_to_(GlobalReach(self.driver, base_url=self.base_url))

    def give_today(self, use_banner_button: bool = True) -> RiceConnect:
        """Click a 'Give today!' button.

        :param bool use_banner_button: (optional) click the banner donation
            button when ``True`` or the Give section button when ``False``
        :return: the RiceConnect OpenStax donation page
        :rtype: :py:class:`~pages.rice.riceconnect.RiceConnect`

        """
        locator = self._banner_give_today_button_locator if use_banner_button \
            else self._giving_give_today_button_locator
        button = self.find_element(*locator)
        Utility.click_option(self.driver, element=button)
        return go_to_(RiceConnect(self.driver))

    def is_displayed(self) -> bool:
        """Return True if the impact page title and description are displayed.

        :return: ``True`` when the impact page title and description are
            displayed
        :rtype: bool

        """
        title = self.find_elements(*self._page_heading_locator)
        description = self.find_elements(*self._page_description_locator)
        return (title and description and
                title[0].is_displayed() and description[0].is_displayed())

    def learn_more_about_openstax_tutor_beta(self) -> TutorMarketing:
        """Click the 'Learn more about OpenStax Tutor Beta' link.

        :return: the OpenStax Tutor Beta marketing page
        :rtype: :py:class:`~pages.web.tutor.TutorMarketing`

        """
        link = self.find_element(*self._tutor_information_link_locator)
        Utility.click_option(self.driver, element=link)
        return go_to_(TutorMarketing(self.driver, base_url=self.base_url))

    def see_a_full_list_of_our_partners(self) -> Partners:
        """Click the partnership link.

        :return: the OpenStax ecosystem partners page
        :rtype: :py:class:`~pages.web.partners.Partners`

        """
        link = self.find_element(*self._partner_list_link_locator)
        Utility.click_option(self.driver, element=link)
        return go_to_(Partners(self.driver, base_url=self.base_url))

    class StatBox(Region):
        """A student use stat box."""

        _description_locator = (
            By.CSS_SELECTOR, '.card-header ~ div')
        _number_locator = (
            By.CSS_SELECTOR, '.card-header')
        _number_extension_locator = (
            By.CSS_SELECTOR, '.smaller')

        @property
        def description(self) -> str:
            """Return the number's description.

            :return: the stat number's description/explanation
            :rtype: str

            """
            return self.find_element(*self._description_locator).text

        @property
        def number(self) -> str:
            """Return the stat number.

            :return: the textbook use stat number
            :rtype: str

            """
            number = self.find_element(*self._number_locator).text
            extension = self.find_element(*self._number_extension_locator).text
            return f'{number.strip()} {extension.strip()}'

    class Testimonial(Region):
        """A user testimonial box."""

        _content_locator = (
            By.CSS_SELECTOR, '.text-block div')
        _read_more_link_locator = (
            By.CSS_SELECTOR, '.text-block a')

        @property
        def content(self) -> str:
            """Return the testimonial quote.

            :return: the textbook use testimonial text quote
            :rtype: str

            """
            return self.find_element(*self._content_locator).text

        def read_more(self) -> Article:
            """Click the testimonial 'Read more >' link.

            :return: the testimonial's associated blog entry
            :rtype: :py:class:`~pages.web.blog.Article`

            """
            link = self.find_element(*self._read_more_link_locator)
            url = self.page.base_url
            article = link.get_attribute('href').split('/')[-1]
            Utility.click_option(self.driver, element=link)
            return go_to_(Article(self.driver, base_url=url, article=article))
