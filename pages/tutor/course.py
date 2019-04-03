"""The student course view."""

import re

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base2 import TutorBase
from utils.tutor import Tutor, TutorException
from utils.utilities import Utility, go_to_


class StudentCourse(TutorBase):
    """The weekly course view for students."""

    _notification_bar_locator = (
                                By.CSS_SELECTOR, '.openstax-notifications-bar')
    _banner_locator = (By.CSS_SELECTOR, '.course-title-banner')
    _weekly_work_locator = (By.CSS_SELECTOR, '.row div:first-child')
    _survey_locator = (By.CSS_SELECTOR, '.research-surveys')
    _performance_guide_locator = (By.CSS_SELECTOR, '.progress-guide')
    _reference_book_locator = (By.CSS_SELECTOR, 'a.browse-the-book')

    # ---------------------------------------------------- #
    # Notifications
    # ---------------------------------------------------- #

    @property
    def notes(self):
        """Access the notifications."""
        notes = self.find_element(*self._notification_bar_locator)
        return self.Notifications(self, notes)

    # ---------------------------------------------------- #
    # Course overview
    # ---------------------------------------------------- #

    @property
    def banner(self):
        """Access the course banner."""
        banner = self.find_element(*self._banner_locator)
        return self.Banner(self, banner)

    @property
    def course_title(self):
        """Return the course title."""
        return self.banner.course_name

    @property
    def course_term(self):
        """Return the course term."""
        return self.banner.course_term

    # ---------------------------------------------------- #
    # Assignments
    # ---------------------------------------------------- #

    @property
    def this_week(self):
        """Access the student assignments for this or upcoming weeks."""
        return self._this_week

    @property
    def all_past_work(self):
        """Access the student assignments for previous weeks."""
        return self._all_past_work

    # ---------------------------------------------------- #
    # Sidebar
    # ---------------------------------------------------- #

    @property
    def survey(self):
        """Access the research surveys."""
        survey_card = self.find_element(*self._survey_locator)
        return self.Survey(self, survey_card)

    @property
    def performance_sidebar(self):
        """Access the performance forecast sidebar."""
        forecast_sidebar = self.find_element(*self._performance_guide_locator)
        return self.Performance(self, forecast_sidebar)

    @property
    def reference_book(self):
        """Return the reference book link element."""
        return self.find_element(*self._reference_book_locator)

    @property
    def book_cover(self):
        """Return the reference book cover image URL."""
        script = ('return window.getComputedStyle(arguments[0], ":before")'
                  '.backgroundImage;')
        url = self.driver.execute_script(script, self.reference_book)
        return url[5:-2]

    def browse_the_book(self):
        """Click on the 'Browse the Book' link."""
        Utility.switch_to(self.driver, element=self.reference_book)
        from pages.tutor.reference import ReferenceBook
        return go_to_(ReferenceBook(self.driver, self.base_url))

    # ---------------------------------------------------- #
    # Student Course Regions
    # ---------------------------------------------------- #

    class Notifications(Region):
        """User notifications."""

        _notification_locator = (By.CSS_SELECTOR, '.notification')

        @property
        def displayed(self):
            """Return True if a notification bar is displayed."""
            return 'viewable' in self.root.get_attribute('class')

        @property
        def notifications(self):
            """Access the individual notification bars."""
            return [self.Notification(self, note)
                    for note
                    in self.find_elements(*self._notification_locator)]

        class Notification(Region):
            """A single notification bar."""

            _content_locator = (
                By.CSS_SELECTOR,
                'div:not(.system) > .body > span , .system > span')
            _add_student_id_locator = (By.CSS_SELECTOR, 'a')
            _dismiss_locator = (By.CSS_SELECTOR, 'button')

            @property
            def type(self):
                """Return the notification type."""
                root_style = self.root.get_attribute('class')
                if Tutor.END_OF_COURSE in root_style:
                    return Tutor.END_OF_COURSE
                elif Tutor.STUDENT_ID in root_style:
                    return Tutor.STUDENT_ID
                elif Tutor.SYSTEM in root_style:
                    return Tutor.SYSTEM
                else:
                    raise ValueError(
                        '"{0}" does not contain a known notification type'
                        .format(root_style))

            @property
            def content(self):
                """Return the notification text."""
                return self.find_element(*self._content_locator).text

            @property
            def add_student_id_button(self):
                """Return the 'Add Student ID' button."""
                button = self.find_elements(*self._add_student_id_locator)
                if button:
                    return button[0]

            def add_student_id(self):
                """Click on the 'Add Student ID' button."""
                Utility.click_option(self.driver,
                                     element=self.add_student_id_button)
                from pages.tutor.student_id import TutorID
                return go_to_(TutorID(self.driver, self.page.page.base_url))

            @property
            def dismiss_button(self):
                """Return the dismiss notification 'x'."""
                button = self.find_elements(*self._dismiss_locator)
                if button:
                    return button[0]

            def dismiss_notification(self):
                """Click on the dismiss 'x'."""
                Utility.click_option(self.driver, element=self.dismiss_button)
                return self.page.page

    class Banner(Region):
        """The course banner."""

        _course_title_locator = (By.CSS_SELECTOR, '.book-title-text')
        _course_term_locator = (By.CSS_SELECTOR, '.course-term')

        @property
        def course_data(self):
            """Return the course data stored in the course banner element."""
            return {
                "title": self.root.get_attribute("data-title"),
                "book-title": self.root.get_attribute("data-book-title"),
                "appearance": self.root.get_attribute("data-appearance"),
                "is-preview": self.root.get_attribute("data-is-preview"),
                "term": self.root.get_attribute("data-term"), }

        @property
        def course_name(self):
            """Return the course name."""
            return self.find_element(*self._course_title_locator).text

        @property
        def course_term(self):
            """Return the course term."""
            return self.find_element(*self._course_term_locator).text

    class Survey(Region):
        """A course research survey access card."""

        _title_locator = (By.CSS_SELECTOR, 'p:nth-child(2)')
        _content_locator = (By.CSS_SELECTOR, 'p')
        _button_locator = (By.CSS_SELECTOR, 'button')

        @property
        def title(self):
            """Return the survey title."""
            title_text = self.find_element(*self._title_locator).text
            match = re.search(r'(["“][\w\ \.\-]+["”])', title_text)
            assert(match is not None), \
                'Survey title not located in "{0}"'.format(title_text)
            return match.group(0)[1:-1]

        @property
        def content(self):
            """Return the text content of the survey card."""
            content = [line.text
                       for line in self.find_elements(*self._content_locator)]
            return '\n'.join(list(content))

        def take_survey(self):
            """Click on the 'Take Survey' button."""
            button = self.find_element(*self._button_locator)
            Utility.click_option(self.driver, element=button)
            from pages.tutor.survey import ResearchSurvey
            return go_to_(ResearchSurvey(self.driver, self.page.base_url))

    class Performance(Region):
        """The performance forecast sidebar."""

        _title_locator = (By.CSS_SELECTOR, '.h2')
        _empty_description_locator = (By.CSS_SELECTOR, '.actions-box p')
        _section_locator = (By.CSS_SELECTOR, '.section')
        _key_guide_locator = (By.CSS_SELECTOR, '.guide-key .item')
        _practice_weakest_locator = (By.CSS_SELECTOR, '.weakest')
        _view_full_forecast_locator = (
                                By.CSS_SELECTOR, '.view-performance-forecast')

        @property
        def title(self):
            """Return the forecast sidebar title."""
            return self.find_element(*self._title_locator).text

        @property
        def is_empty(self):
            """Return True if the forecast has not been populated."""
            return 'empty' in self.root.get_attribute('class')

        @property
        def empty_description(self):
            """Return the forecast explanation if the sidebar is empty."""
            if self.is_empty:
                lines = [
                    line.text for line
                    in self.find_elements(*self._empty_description_locator)]
                return "\n".join(list(lines))
            return ""

        @property
        def sections(self):
            """Access the section forecasts."""
            if self.is_empty:
                raise TutorException("Forecast is not populated")
            return [self.Section(self, section)
                    for section in self.find_elements(*self._section_locator)]

        @property
        def key_guide(self):
            """Access the color guide for the performance bars."""
            return [self.Key(self, guide)
                    for guide in self.find_elements(*self._key_guide_locator)]

        class Section(Region):
            """A recent performance forecast section information."""

            _section_number_locator = (By.CSS_SELECTOR, '.number')
            _section_title_locator = (By.CSS_SELECTOR, '.title')
            _no_data_locator = (By.CSS_SELECTOR, '.no-data')
            _progress_bar_locator = (By.CSS_SELECTOR, '.progress-bar')
            _clue_data_locator = (By.CSS_SELECTOR, 'li')
            _problem_count_locator = (By.CSS_SELECTOR, '.count')
            _practice_section_locator = (By.CSS_SELECTOR, 'button')

            @property
            def number(self):
                """Return the book chapter and section number."""
                return self.find_element(*self._section_number_locator).text

            @property
            def title(self):
                """Return the book section title."""
                return self.find_element(*self._section_title_locator).text

            @property
            def not_enough_data(self):
                """Return True if a forecast CLUE is not available."""
                return bool(self.find_elements(*self._no_data_locator))

            @property
            def practice_more(self):
                """Return the button text if a CLUE is not available."""
                if self.not_enough_data:
                    return self.find_element(*self._no_data_locator).text
                return ""

            @property
            def progress_bar(self):
                """Return the progress bar element."""
                return self.find_element(*self._progress_bar_locator)

            @property
            def progress_data(self):
                """Return the progress bar data attributes."""
                bar = self.progress_bar
                return {
                    "minimum": int(bar.get_attribute("aria-valuemin")),
                    "value": int(bar.get_attribute("aria-valuenow")),
                    "maximum": int(bar.get_attribute("aria-valuemax")),
                    "width": float(bar.get_attribute("style")
                                   .split(": ")[-1].split("%")[0]), }

            @property
            def data(self):
                """Return the CLUE data values."""
                options = list(
                    [line.text.split(": ")[-1]
                     for line in self.find_elements(*self._clue_data_locator)])
                return {
                    "minimum": float(options[0]),
                    "most_likely": float(options[1]),
                    "maximum": float(options[2]),
                    "is_real": options[3] == "true",
                    "uuid": options(4), }

            @property
            def worked(self):
                """Return the questions worked text."""
                return self.find_element(*self._problem_count_locator).text

            @property
            def count(self):
                """Return the number of questions worked."""
                return int(self.worked.split()[0])

            def practice(self):
                """Request a practice session for this book section."""
                button = self.find_element(*self._practice_section_locator)
                Utility.click_option(self.driver, element=button)
                from pages.tutor.practice import Practice
                return go_to_(Practice(self.driver, self.page.page.base_url))

        class Key(Region):
            """The color guide for the performance forecast progress bars."""

            _color_locator = (By.CSS_SELECTOR, '.progress-bar')
            _title_locator = (By.CSS_SELECTOR, '.title')

            @property
            def progress_bar(self):
                """Return the progress bar color box."""
                return self.find_element(*self._color_locator)

            @property
            def color(self):
                """Return the bar color."""
                script = ('return window.getComputedStyle(arguments[0])'
                          '.backgroundColor;')
                return self.driver.execute_script(script, self.progress_bar)

            @property
            def description(self):
                """Return the bar color description."""
                return self.find_element(*self._title_locator).text
