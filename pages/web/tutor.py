"""The OpenStax Tutor Beta marketing page."""

from time import sleep

from pypom import Region
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from pages.web.blog import Article
from pages.web.home import WebHome
from utils.utilities import Utility, go_to_
from utils.web import Web


class Section(Region):
    """A marketing page section."""

    _heading_locator = (By.CSS_SELECTOR, 'h1')
    _description_locator = (By.CSS_SELECTOR, 'div[data-html] p')

    @property
    def section(self):
        """Return the section header element."""
        return self.find_element(*self._heading_locator)

    @property
    def heading(self):
        """Return the heading text."""
        return self.section.text

    @property
    def description(self):
        """Return the section description."""
        return self.find_element(*self._description_locator).text


class TutorMarketing(WebHome):
    """The Tutor marketing page."""

    URL_TEMPLATE = '/openstax-tutor'

    _image_locators = (By.CSS_SELECTOR, '#main img')

    _floating_tools_locator = (By.CSS_SELECTOR, '.floating-tools')
    _sticky_footer_locator = (By.CSS_SELECTOR, '.sticky-footer')
    _new_frontier_locator = (By.CSS_SELECTOR, '#new-frontier')
    _how_it_works_locator = (By.CSS_SELECTOR, '#how-it-works')
    _what_students_get_locator = (By.CSS_SELECTOR, '#what-students-get')
    _feature_matrix_locator = (By.CSS_SELECTOR, '#feature-matrix')
    _where_money_goes_locator = (By.CSS_SELECTOR, '#where-money-goes')
    _science_locator = (By.CSS_SELECTOR, '#science')
    _faq_locator = (By.CSS_SELECTOR, '#faq')
    _learn_more_locator = (By.CSS_SELECTOR, '#learn-more')

    @property
    def loaded(self):
        """Override the base loader."""
        sleep(1.0)
        visible = Utility.is_image_visible(
            self.driver,
            locator=self._image_locators)
        return visible and self.find_element(*self._new_frontier_locator)

    def is_displayed(self):
        """Return True if the marketing page is displayed."""
        if self.URL_TEMPLATE not in self.location:
            return False
        return self.loaded

    @property
    def sidebar(self):
        """Access the sidebar navigation."""
        sidebar_root = self.find_element(*self._floating_tools_locator)
        return self.Sidebar(self, sidebar_root)

    def view(self, section):
        """Scroll to a particular section."""
        self.sidebar._go_to(section)
        return self

    @property
    def marketing_footer(self):
        """Access the marketing page sticky footer."""
        footer_root = self.find_element(*self._sticky_footer_locator)
        return self.StickyFooter(self, footer_root)

    @property
    def introduction(self):
        """Access the 'New Frontier' section."""
        frontier_root = self.find_element(*self._new_frontier_locator)
        return self.NewFrontier(self, frontier_root)

    @property
    def how_it_works(self):
        """Access the 'How It Works' section."""
        how_it_works_root = self.find_element(*self._how_it_works_locator)
        return self.HowItWorks(self, how_it_works_root)

    @property
    def what_students_get(self):
        """Access the 'What Students Get' section."""
        what_students_get_root = self.find_element(
                                            *self._what_students_get_locator)
        return self.WhatStudentsGet(self, what_students_get_root)

    @property
    def features(self):
        """Access the 'Feature Matrix' section."""
        features_root = self.find_element(*self._feature_matrix_locator)
        return self.FeatureMatrix(self, features_root)

    @property
    def where_money_goes(self):
        """Access the 'Where Money Goes' section."""
        money_root = self.find_element(*self._where_money_goes_locator)
        return self.WhereMoneyGoes(self, money_root)

    @property
    def science(self):
        """Access the 'Science' section."""
        science_root = self.find_element(*self._science_locator)
        return self.Science(self, science_root)

    @property
    def faq(self):
        """Access the frequently asked questions section."""
        faq_root = self.find_element(*self._faq_locator)
        return self.FAQ(self, faq_root)

    @property
    def learn_more(self):
        """Access the 'Learn More' section."""
        more_root = self.find_element(*self._learn_more_locator)
        return self.LearnMore(self, more_root)

    @property
    def sections(self):
        """Return a list of available sections."""
        return [
            self.introduction,
            self.how_it_works,
            self.what_students_get,
            self.features,
            self.where_money_goes,
            self.science,
            self.faq,
            self.learn_more
        ]

    class Sidebar(Region):
        """The marketing page sidebar navigation."""

        _nav_dot_locator = (By.CSS_SELECTOR, '[data-id]')
        _pulse_dot_locator = (By.CSS_SELECTOR, '.pulsing-dot')
        _alert_text_locator = (By.CSS_SELECTOR, '.pulsing-dot p')

        def is_displayed(self):
            """Return True if the sidebar has height."""
            return self.driver.execute_script(
                'return arguments[0].clientHeight != 0', self.root)

        @property
        def nav(self):
            """Return the navigation dots."""
            return self.find_elements(*self._nav_dot_locator)

        def select(self, nav):
            """Select a nav dot."""
            return self._go_to(element=nav)

        def view_new_frontier(self):
            """Jump to the New Frontier section."""
            return self._go_to(Web.NEW_FRONTIER)

        def view_how_it_works(self):
            """Jump to the How It Works section."""
            return self._go_to(Web.HOW_IT_WORKS)

        def view_what_students_get(self):
            """Jump to the What Students Get section."""
            return self._go_to(Web.WHAT_STUDENTS_GET)

        def view_feature_matrix(self):
            """Jump to the Feature Matrix section."""
            return self._go_to(Web.FEATURE_MATRIX)

        def view_where_money_goes(self):
            """Jump to the Where Money Goes section."""
            return self._go_to(Web.WHERE_MONEY_GOES)

        def view_science(self):
            """Jump to the Science section."""
            return self._go_to(Web.THE_SCIENCE)

        def view_faq(self):
            """Jump to the FAQ section."""
            return self._go_to(Web.TUTOR_FAQ)

        def view_learn_more(self):
            """Jump to the Learn More section."""
            return self._go_to(Web.LEARN_MORE)

        def alert_dot(self):
            """Return the pulse dot element."""
            return self.find_element(*self._pulse_dot_locator)

        def alert_text(self):
            """Return the alert message text."""
            return self.find_element(*self._alert_text_locator).text

        def _go_to(self, destination=None, element=None):
            """Select a nav dot."""
            try:
                target = self.nav[destination] if destination else element
            except IndexError:
                sleep(1.0)
                target = self.nav[destination] if destination else element
            Utility.safari_exception_click(self.driver, element=target)
            sleep(0.75)
            return self.page

    class StickyFooter(Region):
        """The marketing page sticky footer."""

        _button_locator = (By.CSS_SELECTOR, '.button-group')

        @property
        def is_visible(self):
            """Return True if the footer is visible."""
            return 'collapsed' not in self.root.get_attribute('class')

        @property
        def buttons(self):
            """Access the footer buttons."""
            return [self.Button(self, button)
                    for button in self.find_elements(*self._button_locator)]

        def get_started(self, base_url=None):
            """Go to Tutor."""
            assert(self.is_visible), \
                'The sticky footer is not available at this area of the page.'
            logged_in = self.page.web_nav.login.logged_in
            button = self.buttons[Web.GO_TO_TUTOR].button
            return go_to_tutor(self.driver, logged_in, button, base_url)

        def join_a_webinar(self):
            """Go to the webinar blog post."""
            assert(self.is_visible), \
                'The sticky footer is not available at this area of the page.'
            webinar = (self.buttons[Web.JOIN_A_WEBINAR]
                       .button.get_attribute('href')
                       .split('/')[-1])
            Utility.safari_exception_click(
                self.driver, element=self.buttons[Web.JOIN_A_WEBINAR])
            return go_to_(
                Article(self.driver, self.page.base_url, article=webinar))

        class Button(Region):
            """A sticky footer button."""

            _button_locator = (By.CSS_SELECTOR, 'a')
            _description_locator = (By.CSS_SELECTOR, '.description')

            @property
            def button(self):
                """Return the button link."""
                return self.find_element(*self._button_locator)

            @property
            def description(self):
                """Return the button description."""
                return self.find_element(*self._description_locator).text

    class NewFrontier(Section):
        """The 'New Frontier' section."""

        _course_access_locator = (By.CSS_SELECTOR, '.above-head a')
        _tutor_logo_locator = (By.CSS_SELECTOR, '#tutor-logo')
        _blurb_locator = (
                        By.CSS_SELECTOR, '.headline-text .blurb:nth-child(2)')
        _how_it_works_locator = (By.CSS_SELECTOR, '[href="#how-it-works"]')

        def access_your_course(self, base_url=None):
            """Click the 'Access Your Course' link."""
            logged_in = self.page.web_nav.login.logged_in
            button = self.find_element(*self._course_access_locator)
            return go_to_tutor(self.driver, logged_in, button, base_url)

        @property
        def logo(self):
            """Return the OpenStax Tutor beta logo."""
            return self.find_element(*self._tutor_logo_locator)

        @property
        def subheading(self):
            """Return the subheading text."""
            return self.find_element(*self._blurb_locator).text.strip()

        def learn_more(self):
            """Click the 'Learn More' button."""
            Utility.safari_exception_click(
                self.driver,
                element=self.find_element(*self._how_it_works_locator))
            sleep(0.75)
            return self.page

    class HowItWorks(Section):
        """The 'How It Works' section."""

        _subheading_locator = (By.CSS_SELECTOR, 'h2')
        _box_locator = (By.CSS_SELECTOR, '.blurb-table .blurb')

        @property
        def subheading(self):
            """Return the subheading element."""
            return self.find_element(*self._subheading_locator)

        @property
        def how_it_works(self):
            """Return the subheading text."""
            return self.subheading.text.strip()

        @property
        def boxes(self):
            """Access the blurb boxes."""
            return [self.Box(self, box)
                    for box in self.find_elements(*self._box_locator)]

        class Box(Region):
            """A How It Works blurb box."""

            _icon_locator = (By.CSS_SELECTOR, 'img')
            _title_locator = (By.CSS_SELECTOR, 'h3')
            _description_locator = (By.CSS_SELECTOR, '.smaller')

            @property
            def icon(self):
                """Return the icon element."""
                return self.find_element(*self._icon_locator)

            @property
            def title(self):
                """Return the box title."""
                return self.find_element(*self._title_locator).text.strip()

            @property
            def description(self):
                """Return the box description."""
                return (self.find_element(*self._description_locator)
                        .text.strip())

    class WhatStudentsGet(Section):
        """The 'What Students Get' section."""

        _carousel_locator = (By.CSS_SELECTOR, '.carousel')

        @property
        def tutor(self):
            """Access the student view intro carousel."""
            carousel_root = self.find_element(*self._carousel_locator)
            return self.Carousel(self, carousel_root)

        class Carousel(Region):
            """The student view introductory videos and images."""

            RECT = 'return arguments[0].getBoundingClientRect();'
            SET_BAR = 'arguments[0].scrollLeft = {left}'

            _viewport_locator = (By.CSS_SELECTOR, '.viewport')
            _media_locator = (
                By.CSS_SELECTOR,
                '{0} > video, {0} > img'.format(_viewport_locator[1]))
            _description_locator = (
                                By.CSS_SELECTOR, '[data-html$=description]')
            _option_container_locator = (By.CSS_SELECTOR, '.thumbnails')
            _option_locator = (By.CSS_SELECTOR, 'span')

            @property
            def viewport(self):
                """Return the image viewer."""
                return self.find_element(*self._viewport_locator)

            @property
            def description(self):
                """Return the current image description."""
                return (self.find_element(*self._description_locator)
                        .text.strip())

            @property
            def option_container(self):
                """Return the option parent element."""
                return self.find_element(*self._option_container_locator)

            @property
            def options(self):
                """Return the list of available info buttons."""
                return self.find_elements(*self._option_locator)

            def scroll_to(self, x=0, option=None, element=None):
                """Scroll the option list."""
                if element:
                    _x = self.driver.execute_script(self.RECT, option).get('x')
                elif option:
                    _x = (self.driver
                          .execute_script(self.RECT, self.options[option])
                          ).get('x') - 16
                else:
                    _x = x
                self.driver.execute_script(self.SET_BAR.format(left=_x),
                                           self.option_container)
                return self.page.page

            def view(self, option):
                """Select and option to view."""
                self.scroll_to(option=option)
                sleep(0.25)
                Utility.safari_exception_click(self.driver,
                                               element=self.options[option])
                Utility.scroll_to(self.driver,
                                  element=self.viewport,
                                  shift=-80)
                sleep(1)
                return self.page.page

            @property
            def media_ready(self):
                """Return True if the current media is ready."""
                from selenium.webdriver.support import expected_conditions
                media = self.wait.until(
                    expected_conditions.presence_of_element_located(
                        self._media_locator))
                media_type = media.tag_name.lower()
                if media_type == 'img':
                    return Utility.is_image_visible(self.driver, media)
                elif media_type == 'video':
                    return self.driver.execute_script(
                        'return arguments[0].duration;', media) > 0
                raise WebDriverException('Unknown media type: {0}'
                                         .format(media_type))

    class FeatureMatrix(Section):
        """The available features list."""

        _feature_locator = (By.CSS_SELECTOR, '.flexrow:not(.caption)')
        _new_feature_locator = (By.CSS_SELECTOR, '.future-text p')

        @property
        def features(self):
            """Return the current features."""
            return list([feature.find_element_by_tag_name('div').text.strip()
                        for feature
                        in self.find_elements(*self._feature_locator)
                        if 'false' not in feature.get_attribute('innerHTML')])

        @property
        def new_features(self):
            """Return the list of new features."""
            element = self.find_element(*self._new_feature_locator)
            inner_html = element.get_attribute('innerHTML')
            text = inner_html.replace('<br>', '|')[1:-1].split('||')
            return text

        @property
        def planned_features(self):
            """Return the list of planned features."""
            return list([feature.find_element_by_tag_name('div').text.strip()
                         for feature
                         in self.find_elements(*self._feature_locator)
                         if 'false' in feature.get_attribute('innerHTML')])

    class WhereMoneyGoes(Section):
        """The 'Where the Money Goes' section."""

        _breakdown_locator = (By.CSS_SELECTOR, '#breakdown-description')
        _large_image_locator = (By.CSS_SELECTOR, 'img.boxed')
        _small_image_locator = (By.CSS_SELECTOR, '.boxed img')

        @property
        def breakdown(self):
            """Return the cost breakdown text."""
            return self.find_element(*self._breakdown_locator).text.strip()

        @property
        def breakdown_image(self):
            """Return the breakdown image element for any screen size."""
            if self.driver.get_window_size().get('width') < Web.PHONE:
                return self.find_element(*self._small_image_locator)
            return self.find_element(*self._large_image_locator)

    class Science(Section):
        """The 'Science behind OpenStax Tutor Beta' section."""

        _particle_locator = (By.CSS_SELECTOR, '#particles canvas')

        @property
        def particles(self):
            """Return the flying particles canvas."""
            return self.find_element(*self._particle_locator)

    class FAQ(Section):
        """The 'Frequently Asked Questions' section."""

        _question_locator = (By.CSS_SELECTOR, '.qna:not(.see-more)')
        _support_locator = (By.CSS_SELECTOR, '[href$=help]')

        @property
        def description(self):
            """Override the description field."""
            return ''

        @property
        def questions(self):
            """Access the individual questions."""
            return [self.Quetion(self, question)
                    for question
                    in self.find_elements(*self._question_locator)]

        def view_support(self):
            """Click the 'Support page' link."""
            support_link = self.find_element(*self._support_locator)
            Utility.switch_to(self.driver, element=support_link)
            from pages.salesforce.home import Salesforce
            return go_to_(Salesforce(self.driver))

        class Quetion(Region):
            """A frequently asked question."""

            _toggle_locator = (By.CSS_SELECTOR, '.toggled-item')
            _is_open_locator = (By.CSS_SELECTOR, '.toggler')
            _question_locator = (By.CSS_SELECTOR, '.question p')
            _answer_locator = (By.CSS_SELECTOR, '.answer p')

            def toggle(self):
                """Open or close the question."""
                toggle = self.find_element(*self._toggle_locator)
                Utility.safari_exception_click(self.driver, element=toggle)
                return self.page.page

            @property
            def is_open(self):
                """Return True if the answer is visible."""
                toggled = self.find_element(*self._is_open_locator)
                return 'open' in toggled.get_attribute('class')

            @property
            def question(self):
                """Return the question text."""
                return self.find_element(*self._question_locator).text.strip()

            @property
            def answer(self):
                """Return the answer if the answer is visible."""
                assert(self.is_open), 'The question is closed.'
                return self.find_element(*self._answer_locator).text.strip()

    class LearnMore(Section):
        """The 'Learn More' section."""

        _button_locator = (By.CSS_SELECTOR, '.button-box')

        @property
        def buttons(self):
            """Return the button boxes."""
            return [self.Button(self, box)
                    for box in self.find_elements(*self._button_locator)]

        def get_started(self, base_url=None):
            """Click the 'Get Started' button."""
            logged_in = self.page.web_nav.login.logged_in
            button = self.buttons[Web.GET_STARTED].button
            return go_to_tutor(self.driver, logged_in, button, base_url)

        def join_a_webinar(self):
            """Click the 'Join a webinar' button."""
            button = self.buttons[Web.JOIN_A_WEBINAR]
            append = button.button.get_attribute('href').split('/')[-1]
            button.click()
            return go_to_(Article(self.driver,
                          base_url=self.page.base_url,
                          article=append))

        class Button(Region):
            """A Learn More button box."""

            _button_locator = (By.CSS_SELECTOR, 'a')
            _description_locator = (By.CSS_SELECTOR, 'div')

            @property
            def button(self):
                """Return the button link."""
                return self.find_element(*self._button_locator)

            def click(self):
                """Click on the link."""
                Utility.safari_exception_click(self.driver,
                                               element=self.button)
                return self.page

            @property
            def description(self):
                """Return the button description."""
                return (self.find_element(*self._description_locator)
                        .text.strip())


def go_to_tutor(driver, logged_in, target, base_url=None):
    """Go to the Tutor dashboard."""
    Utility.switch_to(driver, element=target)
    if not logged_in:
        from pages.accounts.home import AccountsHome as Destination
    else:
        from pages.tutor.dashboard import Dashboard as Destination
    return go_to_(Destination(driver, base_url=base_url))
