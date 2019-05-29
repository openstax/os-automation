"""Student assignment tasks.

Externals, Events, Homeworks, and Readings

"""

from __future__ import annotations

from time import sleep
from typing import Dict, Union

from pypom import Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.tutor.base import TutorBase
from pages.tutor.course import StudentCourse
from pages.web.errata import ErrataForm
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
