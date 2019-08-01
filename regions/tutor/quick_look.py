"""An assignment quick look analytics modal pane."""

from time import sleep

from pypom import Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from utils.tutor import Tutor, TutorException
from utils.utilities import Utility, go_to_


class QuickLookBase(Region):
    """A shared base for the analytics quick look modal."""

    _root_locator = (By.CSS_SELECTOR, '.modal')
    _assignment_type_locator = (By.CSS_SELECTOR, '[data-assignment-type]')
    _title_locator = (By.CSS_SELECTOR, '.modal-title')
    _close_button_locator = (By.CSS_SELECTOR, '.close')

    # ---------------------------------------------------- #
    # Banner
    # ---------------------------------------------------- #

    @property
    def assignment_type(self):
        """Return the assignment type."""
        return (self.find_element(*self._assignment_type_locator)
                .get_attribute('data-assignment-type').text)

    @property
    def title(self):
        """Return the assignment name."""
        return self.find_element(*self._title_locator).text

    @property
    def close_button(self):
        """Return the close button 'x'."""
        return self.find_element(*self._close_button_locator)

    def close_quick_look(self):
        """Click on the close button and return to the calendar."""
        Utility.click_option(self.driver, element=self.close_button)
        sleep(0.25)
        return self.page


class QuickLook(QuickLookBase):
    """The quick look analytics modal."""

    _assignment_sections_locator = (
        By.CSS_SELECTOR, '.nav-tabs li')
    _event_sections_locator = (
        By.CSS_SELECTOR, '.event-stats strong')
    _no_students_locator = (
        By.CSS_SELECTOR, '.no-students')
    _no_students_info_locator = (
        By.CSS_SELECTOR, '.no-students p')
    _course_settings_locator = (
        By.CSS_SELECTOR, '.no-students a')
    _body_data_locator = (
        By.CSS_SELECTOR, '.task-stats-data')
    _review_metrics_locator = (
        By.CSS_SELECTOR, '.modal-footer [href*=metrics]')
    _view_scores_locator = (
        By.CSS_SELECTOR, '.modal-footer [href*=scores]')
    _view_assignment_locator = (
        By.CSS_SELECTOR, f'.modal-footer [href*=assign]')
    _assignment_link_locator = (
        By.CSS_SELECTOR, '.modal-footer button')

    # ---------------------------------------------------- #
    # Section navigation
    # ---------------------------------------------------- #

    @property
    def sections(self):
        """Return the sections navigation or event section names."""
        if self.assignment_type == Tutor.EVENT:
            return (self.find_element(*self._event_sections_locator).text
                    .split(', '))
        return [self.Section(self, section)
                for section
                in self.find_elements(*self._assignment_sections_locator)]

    # ---------------------------------------------------- #
    # Body data
    # ---------------------------------------------------- #

    @property
    def no_students(self):
        """Return True if the 'No students enrolled.' message is displayed."""
        return bool(self.find_elements(*self._no_students_locator))

    @property
    def no_student_information(self):
        """Return the 'No students enrolled.' text."""
        if self.no_students:
            return self.find_element(*self._no_students_info_locator).text
        return ""

    def view_course_settings(self):
        """Click on the 'Course settings' link if there are no students."""
        if self.no_students:
            link = self.find_element(*self._course_settings_locator)
            Utility.click_option(self.driver, element=link)
            from pages.tutor.settings import CourseSettings
            return go_to_(CourseSettings(self.driver, self.page.base_url))

    @property
    def body(self):
        """Access the body data for non-event assignments."""
        if not self.no_students and self.assignment_type != Tutor.EVENT:
            body_root = self.find_element(*self._body_data_locator)
            return self.Body(self, body_root)
        return None

    # ---------------------------------------------------- #
    # Modal footer buttons
    # ---------------------------------------------------- #

    def review_metrics(self):
        """Click on the 'Review Metrics' button."""
        button = self.find_element(*self._review_metrics_locator)
        Utility.click_option(self.driver, element=button)
        from pages.tutor.review_metrics import Metrics
        return go_to_(Metrics(self.driver, self.page.base_url))

    def view_scores(self):
        """Click on the 'View Scores' button.

        External assignments only

        """
        button = self.find_element(*self._view_scores_locator)
        Utility.click_option(self.driver, element=button)
        from pages.tutor.scores import Scores
        return go_to_(Scores(self.driver, self.page.base_url))

    def view_assignment(self):
        """Click on the 'View Assignment' or 'View Event' button."""
        button = self.find_element(*self._view_assignment_locator)
        button_url = button.get_attribute('href')
        if Tutor.EVENT in button_url:
            from pages.tutor.assignment import Event as Edit
        elif Tutor.EXTERNAL in button_url:
            from pages.tutor.assignment import External as Edit
        elif Tutor.HOMEWORK in button_url:
            from pages.tutor.assignment import Homework as Edit
        elif Tutor.READING in button_url:
            from pages.tutor.assignment import Reading as Edit
        else:
            raise ValueError('{url} contains an unknown assignment type'
                             .format(url=button_url))
        Utility.click_option(self.driver, element=button)
        return go_to_(Edit(self.driver, self.page.base_url))

    def assignment_link(self):
        """Click on the 'Get assignment link' button."""
        link = self.find_element(*self._assignment_link_locator)
        Utility.click_option(self.driver, element=link)
        sleep(0.5)
        return AssignmentLink(self.page)

    # ---------------------------------------------------- #
    # Quick look modal sub-regions
    # ---------------------------------------------------- #

    class Section(Region):
        """The course section or period tab navigation."""

        _name_locator = (By.CSS_SELECTOR, '.tab-item-period-name')
        _link_locator = (By.CSS_SELECTOR, 'a')

        @property
        def name(self):
            """Return the section or period name."""
            return self.find_element(*self._name_locator).text

        @property
        def is_active(self):
            """Return True if the section or period is currently selected."""
            return 'active' in self.root.get_attribute('class')

        def select(self):
            """Click on the section or period link."""
            link = self.find_element(*self._link_locator)
            Utility.click_option(self.driver, element=link)
            return self.page

    class Body(Region):
        """The quick look data bars."""

        _complete_locator = (By.CSS_SELECTOR, '.complete div')
        _in_progress_locator = (By.CSS_SELECTOR, '.in-progress div')
        _not_started_locator = (By.CSS_SELECTOR, '.not-started div')
        _performance_locator = (By.CSS_SELECTOR, 'section:not(:first-child)')

        @property
        def complete(self):
            """Return the number of students who finished."""
            return int(self.find_element(*self._complete_locator).text)

        @property
        def in_progress(self):
            """Return the number of students working the assignment."""
            if self.page.page.assignment_type == Tutor.EXTERNAL:
                raise TutorException(
                    'External assignments do not have '
                    'an "In Progress" category.')
            return int(self.find_element(*self._in_progress_locator).text)

        @property
        def not_started(self):
            """Return the number of students who have not started."""
            return int(self.find_element(*self._not_started_locator).text)

        @property
        def performance(self):
            """Access the performance bars for homeworks and readings."""
            if self.page.assignment_type == Tutor.EXTERNAL:
                return TutorException(
                    'External assignments do not have performance bars.')
            return [self.Performance(self, bar)
                    for bar in self.find_elements(*self._performance_locator)]

        class Performance(Region):
            """A section performance group."""

            _title_locator = (By.CSS_SELECTOR, 'label')
            _topic_locator = (By.CSS_SELECTOR, '.reading-progress')

            @property
            def title(self):
                """Return the section title."""
                return self.find_element(*self._title_locator).text

            @property
            def topics(self):
                """Access the individual topic bars."""
                return [self.Topic(self, bar)
                        for bar in self.find_elements(*self._topic_locator)]

            def get_section(self):
                """Return the section data."""
                return {
                    "title": self.title,
                    "topics": [topic.data for topic in self.topics], }

            class Topic(Region):
                """An individual topic performance bar."""

                _section_number_locator = (
                            By.CSS_SELECTOR, '[class*="-heading"] span')
                _section_title_locator = (
                            By.CSS_SELECTOR, '[class*="-heading"] strong')
                _section_progress_locator = (
                            By.CSS_SELECTOR, '.reading-progress-student-count')
                _correct_percentage_locator = (
                            By.CSS_SELECTOR, '[type=correct] span')
                _incorrect_percentage_locator = (
                            By.CSS_SELECTOR, '[type=incorrect] span')

                @property
                def section_number(self):
                    """Return the book section number."""
                    return (self.find_element(*self._section_number_locator)
                            .text)

                @property
                def section_title(self):
                    """Return the book section title."""
                    return (self.find_element(*self._section_title_locator)
                            .text)

                @property
                def progress(self):
                    """Return the number of students who worked the section."""
                    return int(
                        self.find_element(*self._section_progress_locator)
                        .text
                        .split()[0][1:])

                @property
                def correct(self):
                    """Return the average percent of correct answers."""
                    try:
                        return int(
                            self.find_element(
                                *self._correct_percentage_locator).text[:-1])
                    except NoSuchElementException:
                        return 0

                @property
                def incorrect(self):
                    """Return the average percent of incorrect answers."""
                    try:
                        return int(
                            self.find_element(
                                *self._incorrect_percentage_locator).text[:-1])
                    except NoSuchElementException:
                        return 0

                @property
                def data(self):
                    """Return a dictionary of the section data."""
                    return {
                        "section-number": self.section_number,
                        "section-title": self.section_title,
                        "worked-by": self.progress,
                        "correct": self.correct,
                        "incorrect": self.incorrect, }


class AssignmentLink(QuickLookBase):
    """The assignment link modal."""

    _back_button_locator = (By.CSS_SELECTOR, '[class*=BackLinkButton]')
    _description_locator = (By.CSS_SELECTOR, 'p')
    _assignment_url_locator = (By.CSS_SELECTOR, 'label:nth-child(3) input')
    _due_date_time_locator = (By.CSS_SELECTOR, 'label:last-child input')

    def back(self):
        """Return to the quick look analytics modal."""
        button = self.find_element(*self._back_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.5)
        return QuickLook(self.page)

    @property
    def description(self):
        """Return the URL description text."""
        return self.find_element(*self._description_locator).text

    @property
    def url(self):
        """Return the assignment URL."""
        return (self.find_element(*self._assignment_url_locator)
                .get_attribute('value'))

    @property
    def due_date(self):
        """Return the due date."""
        return (self.find_element(*self._due_date_time_locator)
                .get_attribute('value'))

    @property
    def get_datetime(self):
        """Return a datetime object for the due date."""
        from datetime import datetime
        return datetime.strptime(self.due_date + " CST",
                                 "%m/%d/%Y at %I:%M%p %z")
