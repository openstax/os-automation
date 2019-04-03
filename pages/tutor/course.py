"""The student course view."""

import re

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base2 import TutorBase
from utils.tutor import Tutor
from utils.utilities import Utility, go_to_


class StudentCourse(TutorBase):
    """The weekly course view for students."""

    _notification_bar_locator = (
                                By.CSS_SELECTOR, '.openstax-notifications-bar')
    _banner_locator = (By.CSS_SELECTOR, '.course-title-banner')
    _survey_locator = (By.CSS_SELECTOR, '.research-surveys')

    @property
    def notes(self):
        """Access the notifications."""
        notes = self.find_element(*self._notification_bar_locator)
        return self.Notifications(self, notes)

    @property
    def banner(self):
        """Access the course banner."""
        banner = self.find_element(*self._banner_locator)
        return self.Banner(self, banner)

    @property
    def survey(self):
        """Access the research surveys."""
        survey_card = self.find_element(*self._survey_locator)
        return self.Survey(self, survey_card)

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
                "term": self.root.get_attribute("data-term"),
            }

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
