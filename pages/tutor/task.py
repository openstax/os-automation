"""Student assignment tasks.

Externals, Events, Homeworks, and Readings

"""

from __future__ import annotations

from time import sleep
from typing import Dict, List, Union

from pypom import Region
# from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from pages.tutor.course import StudentCourse
# from pages.web.errata import ErrataForm
from utils.tutor import Tutor, TutorException
from utils.utilities import Utility, go_to_


class Assignment(TutorBase):
    """The shared assignment features."""

    _assignment_nav_bar_locator = (
        By.CSS_SELECTOR, '[class*=SecondaryToolbar]')
    _assignment_body_locator = (
        By.CSS_SELECTOR, '[class*="Content-sc-"]')
    _assignment_footer_locator = (
        By.CSS_SELECTOR, '.tutor-navbar')
    _assignment_type_locator = (
        By.CSS_SELECTOR, '.task-screen')
    _debug_information_locator = (
        By.CSS_SELECTOR, '.visible-when-debugging li')

    @property
    def assignment_type(self) -> str:
        """Return the assignment type.

        :return: the assignment type
        :rtype: str

        """
        task_type = (self.find_element(*self._assignment_type_locator)
                     .get_attribute('class'))
        if Tutor.EVENT in task_type:
            return Tutor.EVENT
        elif Tutor.EXTERNAL in task_type:
            return Tutor.EXTERNAL
        elif Tutor.HOMEWORK in task_type:
            return Tutor.HOMEWORK
        return Tutor.READING

    @property
    def nav(self) -> Union[Assignment.Nav, None]:
        """Access the assignment navigaton bar.

        :return: the assignment navigation bar for readings and homeworks
        :rtype: :py:class:`~pages.tutor.task.Assignment.Nav` or None

        """
        assignment_type = self.assignment_type
        if assignment_type == Tutor.EVENT or assignment_type == Tutor.EXTERNAL:
            return
        nav_root = self.find_element(*self._assignment_nav_bar_locator)
        return self.Nav(self, nav_root)

    @property
    def body(self) -> Assignment.Content:
        """Access the assignment content and assessments.

        :return: the region housing the assignment content and assessments
        :rtype: :py:class:`~pages.tutor.task.Assignment.Content`

        """
        body_root = self.find_element(*self._assignment_body_locator)
        if self.assignment_type == Tutor.HOMEWORK:
            return self.Content(self, body_root).pane
        return self.Content(self, body_root)

    @property
    def footer(self) -> Assignment.Footer:
        """Access the assignment footer content.

        :return: the assignment footer
        :rtype: :py:class:`~pages.tutor.task.Assignment.Footer`

        """
        footer_root = self.find_element(*self._assignment_footer_locator)
        return self.Footer(self, footer_root)

    @property
    def debug_information(self) -> Dict[str, str]:
        """Return the debugging information for the current page.

        :return: the group of debugging keys and values for the current page,
            task, or assessment
        :rtype: dict(str, str)

        """
        data = {}
        lines = self.find_elements(*self._debug_information_locator)
        for line in lines:
            key, value = line.split(':', 1)
            data[line.strip()] = value.string()
        return data

    class Content(Region):
        """A placeholder for the assignment body."""

        def __init__(self):
            """Override the initialization to toss an implementation error."""
            raise NotImplementedError("Must use an individual assignment type,"
                                      " not Assignment")

    class Footer(Region):
        """The assignment footer."""

        _assignment_title_locator = (By.CSS_SELECTOR, '[class*=Title]')
        _assignment_due_date_locator = (By.CSS_SELECTOR, '[class*=DueDate]')
        _back_to_dashboard_button_locator = (By.CSS_SELECTOR, '.btn-default')

        @property
        def title(self) -> str:
            """Return the assignment name.

            :return: the assignment name
            :rtype: str

            """
            return self.find_element(*self._assignment_title_locator).text

        @property
        def due_date(self) -> str:
            r"""Return the assignment due date.

            https://docs.python.org/3.7/library/datetime.html \
            #strftime-and-strptime-behavior

            :return: the assignment due date as a string with the format
                "due %a, %b %d, %Y %I:%M %p"
            :rtype: str

            """
            return self.find_element(*self._assignment_due_date_locator).text

        def back_to_dashboard(self) -> StudentCourse:
            """Click the 'Back to Dashboard' button.

            :return: the student course page
            :rtype: :py:class:`~pages.tutor.course.StudentCourse`

            """
            button = self.find_element(*self._back_to_dashboard_button_locator)
            Utility.click_option(self.driver, element=button)
            return go_to_(
                StudentCourse(self.driver, base_url=self.page.base_url))

    class Nav(Region):
        """A placeholder for the assignment navigation bar."""

        def __init__(self):
            """Override the initialization to toss an implementation error."""
            raise NotImplementedError("Must use an individual assignment type,"
                                      " not Assignment")


class Event(Assignment):
    """A calendar event."""

    class Content(Region):
        """The interactive assignment body."""

        _assignment_name_locator = (By.CSS_SELECTOR, '.event-task h1')
        _assignment_description_locator = (By.CSS_SELECTOR, '.event-task h3')
        _back_to_dashboard_button_locator = (By.CSS_SELECTOR, '.event-task a')

        @property
        def name(self) -> str:
            """Return the assignment name.

            .. note:

               This should match the footer's assignment title.

            :return: the assignment name.
            :rtype: str

            """
            return self.find_element(*self._assignment_name_locator).text

        @property
        def description(self) -> str:
            """Return the assignment description, if present.

            :return: the assignment description, if found, otherwise an empty
                string
            :rtype: str

            """
            description = self.find_elements(
                *self._assignment_description_locator)
            return description[0].text if description else ''

        def back_to_dashboard(self) -> StudentCourse:
            """Click on the 'Back to Dashboard' button in the assignment body.

            :return: the student course page
            :rtype: :py:class:`~pages.tutor.course.StudentCourse`

            """
            button = self.find_element(*self._back_to_dashboard_button_locator)
            Utility.click_option(self.driver, element=button)
            return go_to_(StudentCourse(self.driver, base_url=self.base_url))


class External(Assignment):
    """An assignment found outside of OpenStax Tutor Beta."""

    class Content(Region):
        """The interactive assignment body."""

        _assignment_name_locator = (By.CSS_SELECTOR, '.external-url-task h1')
        _assignment_description_locator = (
                                    By.CSS_SELECTOR, '.external-url-task h3')
        _external_url_locator = (By.CSS_SELECTOR, '[class*=Link]')

        @property
        def name(self) -> str:
            """Return the assignment name.

            .. note:

               This should match the footer's assignment title.

            :return: the assignment name.
            :rtype: str

            """
            return self.find_element(*self._assignment_name_locator).text

        @property
        def description(self) -> str:
            """Return the assignment description, if present.

            :return: the assignment description, if found, otherwise an empty
                string
            :rtype: str

            """
            description = self.find_elements(
                *self._assignment_description_locator)
            return description[0].text if description else ''

        @property
        def assignment_url(self) -> str:
            """Return the external URL for the assignment.

            :return: the assignment URL
            :rtype: str

            """
            return (self.find_element(*self._external_url_locator)
                    .get_attribute('href'))

        def go_to_assignment(self) -> str:
            """Click on the assignment URL.

            :return: the assignment URL
            :rtype: str

            """
            link = self.find_element(*self._external_url_locator)
            url = link.get_attribute('href')
            Utility.switch_to(self.driver, element=link)
            sleep(1)
            return url


class Homework(Assignment):
    """A collection of assessments selected by the course instructor."""

    class Content(Region):
        """The assessment pane."""

        _is_free_response_locator = (
            By.CSS_SELECTOR, '[class*=FreeResponse]')
        _is_multipart_locator = (
            By.CSS_SELECTOR, '[class*=MultipartGroup]')
        _is_multiple_choice_locator = (
            By.CSS_SELECTOR, '[class*=ExerciseQuestion]')

        @property
        def pane(self):
            """Access the question pane."""
            multipart = self.find_elements(*self._is_multipart_locator)
            if multipart:
                from regions.tutor.assessment import MultipartQuestion
                return MultipartQuestion(self, multipart[0])
            free_response = self.find_elements(*self._is_free_response_locator)
            if free_response:
                from regions.tutor.assessment import FreeResponse
                return FreeResponse(self, free_response[0])
            multiple_choice = self.find_element(
                *self._is_multiple_choice_locator)
            from regions.tutor.assessment import MultipleChoice
            return MultipleChoice(self, multiple_choice)

    class Nav(Region):
        """The homework step navigation."""

        _homework_step_locator = (By.CSS_SELECTOR, '.breadcrumbs-wrapper span')

        @property
        def steps(self) -> List[Homework.Nav.Step]:
            """Access the individual homework steps.

            :return: the list of available steps
            :rtype: list(:py:class:`~pages.tutor.task.Homework.Nav.Step`)

            """
            return [self.Step(self, crumb)
                    for crumb
                    in self.find_elements(*self._homework_step_locator)]

        class Step(Region):
            """A homework step, review, or completion."""

            @property
            def title(self) -> str:
                """Return the homework step title.

                :return: the homework step title
                :rtype: str

                """
                return self.root.get_attribute('title')

            @property
            def step_id(self) -> str:
                """Return the step identification number.

                :return: the homework step ID number
                :rtype: str

                """
                return self.root.get_attribute('data-step-id')

            @property
            def index(self) -> int:
                """Return the exercise step index.

                :return: the exercise step index number or ``-1`` for non-
                    exercise steps
                :rtype: int

                """
                index = self.root.get_attribute('data-step-index')
                return int(index) if index else -1

            @property
            def step_type(self) -> str:
                """Return the step type.

                :return: the step type
                    :py:data:`~utils.tutor.Tutor.EXERCISE` or
                    :py:data:`~utils.tutor.Tutor.REVIEW_CARD` or
                    :py:data:`~utils.tutor.Tutor.END_CARD`
                :rtype: str

                """
                classes = self.root.get_attribute('class')
                if 'breadcrumb-exercise' in classes:
                    return Tutor.EXERCISE
                elif 'individual-review' in classes:
                    return Tutor.REVIEW_CARD
                elif 'breadcrumb-end' in classes:
                    return Tutor.END_CARD
                return TutorException(f'Step type not found in "{classes}"')

            @property
            def answered(self) -> bool:
                """Return True if the step is answered.

                :return: ``True`` if the step is answered, otherwise ``False``
                :rtype: bool

                """
                return 'completed' in self.root.get_attribute('class')

            @property
            def correctness(self) -> str:
                """Return the correctness for the step.

                :return: the correctness (answered correctly or incorrectly) of
                    the step if past the due date and answered
                    :py:data:`~utils.tutor.Tutor.CORRECT` or
                    :py:data:`~utils.tutor.Tutor.INCORRECT` or
                    :py:data:`~utils.tutor.Tutor.NOT_ANSWERED` or
                    :py:data:`~utils.tutor.Tutor.NOT_GRADED`
                :rtype: str

                """
                if not self.answered:
                    return Tutor.NOT_ANSWERED
                classes = self.root.get_attribute('class')
                if 'status-correct' in classes:
                    return Tutor.CORRECT
                elif 'status-incorrect' in classes:
                    return Tutor.INCORRECT
                return Tutor.NOT_GRADED

            @property
            def selection(self) -> str:
                """Return the selection type for the assessment.

                :return: the selection type for the assessment question or
                    :py:data:`~utils.tutor.Tutor.NOT_A_QUESTION` for an
                    interstitial card; standard responses will be
                    :py:data:`~utils.tutor.Tutor.CORE` or
                    :py:data:`~utils.tutor.Tutor.PERSONALIZED` or
                    :py:data:`~utils.tutor.Tutor.SPACED_PRACTICE`
                :rtype: str

                """
                classes = self.root.get_attribute('class')
                if 'core' in classes:
                    return Tutor.CORE
                elif 'personalized' in classes:
                    return Tutor.PERSONALIZED
                elif 'spaced' in classes:
                    return Tutor.SPACED_PRACTICE
                return Tutor.NOT_A_QUESTION

            @property
            def is_active(self) -> bool:
                """Return True if the step is currently selected and active.

                :return: ``True`` if the step is active and displayed in the
                    body, otherwise ``False``
                :rtype: bool

                """
                return 'active' in self.root.get_attribute('class')

            def select(self) -> Homework:
                """Select the step to display it in the main body.

                :return: the homework assignment with the selected step active
                :rtype: :py:class:`~pages.tutor.task.Homework`

                """
                Utility.click_option(self.driver, element=self.root)
                sleep(1)
                return self.page.page


class Reading(Assignment):
    """A collection of book sections selected by the course instructor."""

    class Nav(Region):
        """The reading progress bar."""

        _progress_bar_locator = (By.CSS_SELECTOR, '.progressbar')

        @property
        def progress(self) -> int:
            """Return the current assignment progress.

            :return: the current assignment progress percentage out of 100
            :rtype: int

            """
            return int(self.find_element(*self._progress_bar_locator)
                       .get_attribute('aria-valuenow'))
