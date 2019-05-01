"""The instructor's course roster management page."""

from time import sleep

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from utils.tutor import TutorException
from utils.utilities import Utility

GET_ROOT = 'return document.querySelector("[role={0}]");'


# -------------------------------------------------------- #
# Tooltips found on the course roster
# -------------------------------------------------------- #

class Tooltip(Region):
    """A limited page tooltip action box."""

    _user_action_request_locator = (By.CSS_SELECTOR, '.popover-header')
    _action_button_locator = (By.CSS_SELECTOR, 'button')

    @property
    def request(self):
        """Return the action description text found in the header.

        :return: the action description
        :rtype: str

        """
        return (self.find_element(*self._user_action_request_locator)
                .get_attribute('textContent'))

    def _perform_action(self):
        """Use the tooltip button.

        Click on the tooltip button to perform the action request after which
        the tooltip closes and the course roster is returned. The method name
        will be attached in subclasses.

        :return: the course roster
        :rtype: :py:class:`CourseRoster`

        :noindex:

        """
        button = self.find_element(*self._action_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(1)
        return self.page


class RemoveInstructor(Tooltip):
    """Remove a current course instructor tooltip."""

    remove = super()._perform_action


class ChangeSection(Tooltip):
    """Move a student to another section tooltip."""

    _section_locator = (By.CSS_SELECTOR, '.nav a')

    @property
    def sections(self):
        """Return the list of available other sections.

        :return: the course roster
        :rtype: :py:class:`CourseRoster`

        """
        return [self.Section(self, section)
                for section in self.find_elements(*self._section_locator)]

    def switch_to(self, section_name):
        """Select a new section for the current student.

        .. note::

           section/period names are case sensitive (e.g. '1st' and '1ST' can
           occur in the same course)

        :param str section_name: the new section for the student
        :return: the course roster
        :rtype: :py:class:`CourseRoster`
        :raises TutorException: if the section_name does not match an active
            course section or period name

        """
        for section in self.sections:
            if section.name == section_name:
                section.select()
                sleep(1)
                return self.page
        raise TutorException(
            '"{0}" is not a valid section name (case-sensitive match)'
            .format(section_name))

        class Section(Region):
            """An available section for a student."""

            @property
            def name(self):
                """Return the section name.

                :return: the section name
                :rtype: str

                """
                return self.root.text

            def select(self):
                """Click on the section name to transfer the student.

                :return: the course roster
                :rtype: :py:class:`CourseRoster`

                """
                Utility.click_option(self.driver, element=self.root)
                sleep(1)
                return self.page.page


class DropStudent(Tooltip):
    """Drop a current student from the course tooltip."""

    drop = super()._perform_action


class ReAddStudent(Tooltip):
    """Re-add a dropped student to the active roster tooltip."""

    restore = super()._perform_action


# -------------------------------------------------------- #
# Page modals found on the course roster
# -------------------------------------------------------- #

class Modal(Region):
    """A pop up modal with overlay."""

    _title_locator = (By.CSS_SELECTOR, '.modal-title')
    _close_button_locator = (By.CSS_SELECTOR, '.close')
    _description_locator = (By.CSS_SELECTOR, '.modal-body p:first-child')
    _warning_locator = (By.CSS_SELECTOR, '.warning , .modal-body p:last-child')

    @property
    def title(self):
        """Return the modal title.

        :return: the modal title
        :rtype: str

        """
        return (self.find_element(*self._title_locator)
                .get_attribute('textContent'))

    def close(self):
        """Click the close link or 'x' button to close the modal.

        :return: the course roster
        :rtype: :py:class:`CourseRoster`

        """
        button = self.find_element(*self._close_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(1)
        return self.page

    @property
    def description(self):
        """Return the modal description.

        :return: the description within the modal body, if found, else an empty
            string
        :rtype: str

        """
        text = self.find_elements(*self._description_locator)
        return text[0].get_attribute('textContent') if text else ''

    @property
    def warning(self):
        """Return the modal warning text.

        :return: the warning text within the modal body, if found, else an
            empty string
        :rtype: str

        """
        text = self.find_elements(*self._warning_locator)
        return text[0].text if text else ''


class AddInstructor(Modal):
    """The add instructor modal."""

    _registration_url_locator = (By.CSS_SELECTOR, 'input')

    @property
    def url_input(self):
        """Return the input containing the registration link input element.

        :return: the registration URL input box
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._registration_url_locator)

    @property
    def url(self):
        """Return the registration URL for other instructors.

        :return: the registration URL needed for other instructors and TAs to
            join the course as teachers
        :rtype: str

        """
        return self.url_input.get_attribute('value')


class AddSection(Modal):
    """Add a new section or period to the course."""

    _section_name_locator = (By.CSS_SELECTOR, 'input')
    _add_section_button_locator = (By.CSS_SELECTOR, '.-edit-period-confirm')

    @property
    def section_name(self):
        """Return the section name input box.

        :return: the section name input box element
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._section_name_locator)

    @section_name.setter
    def section_name(self, section_name):
        """Type the section name in the box.

        .. note::

           If the section_name matches an existing section (case-sensitive), an
           HTML 422 error will be thrown by Tutor; server errors are not
           handled by the automation code.

        :param str section_name: the new section name
        :return: the Add Section modal
        :rtype: :py:class:`AddSection`

        """
        self.section_name.send_keys(section_name)
        return self

    def add(self):
        """Click the 'Add' button.

        :return: the course roster with the new section displayed in the
            available tabs
        :rtype: :py:class:`CourseRoster`

        """
        button = self.find_element(*self._add_section_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(1)
        return self.page


class RenameSection(AddSection):
    """Edit an existing section's name."""

    @property
    def current_name(self):
        """Return the existing section's name.

        :return: the text currently held in the input box's value field
        :rtype: str

        """
        return self.section_name.get_attribute('value')

    rename = super().add


class DeleteSection(Modal):
    """Delete an existing section.

    .. note::

       Sections are not deleted; they are archived and may be reactivated by a
       Tutor administrator in the admin console.

    """

    _delete_button_locator = (By.CSS_SELECTOR, '.delete')
    _cancel_button_locator = (
        By.CSS_SELECTOR, '.modal-footer button:last-child')

    def delete(self):
        """Click on the 'Delete' button confirming the section removal.

        :return: the course roster
        :rtype: :py:class:`CourseRoster`

        """
        button = self.find_element(*self._delete_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(1)
        return self.page

    def cancel(self):
        """Click on the 'Cancel' button.

        :return: the course roster
        :rtype: :py:class:`CourseRoster`

        """
        button = self.find_element(*self._cancel_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(1)
        return self.page


# -------------------------------------------------------- #
# The Course Roster
# -------------------------------------------------------- #

class User(Region):
    """A base user row for teachers and students."""

    _first_name_locator = (By.CSS_SELECTOR, 'td:first-child')
    _last_name_locator = (By.CSS_SELECTOR, 'td:nth-child(2)')
    _remove_user_locator = (By.XPATH, '//a[*[@data-icon="ban"]]')

    @property
    def first_name(self):
        """Return the user's first name.

        :return: the user's first name
        :rtype: str

        """
        return self.find_element(*self._first_name_locator).text

    @property
    def last_name(self):
        """Return the user's last name/surname.

        :return: the user's last name
        :rtype: str

        """
        return self.find_element(*self._last_name_locator).text

    def _remove_user(self, student=True, return_tooltip=False):
        """Remove the user from the course.

        :param bool student: (optional) use the Drop Student tooltip if
            ``True`` and the Remove Instructor tooltip if ``False``
        :param bool return_tooltip: (optional) don't drop the user; click the
            'Remove' or 'Drop' button to open the tooltip and return the pop up
        :return: None or the open tooltip
        :rtype: NoneType or :py:class:`Tooltip`

        """
        button = self.find_element(*self._remove_user_locator)
        Utility.click_option(self.driver, element=button)
        tooltip_root = self.driver.execute_script(GET_ROOT.format('tooltip'))
        if student:
            popup = self.DropStudent(self, tooltip_root)
            if return_tooltip:
                return popup
            popup.drop()
        else:
            popup = self.RemoveInstructor(self, tooltip_root)
            if return_tooltip:
                return popup
            popup.remove()


class CourseRoster(TutorBase):
    """The Tutor course roster."""

    _page_title_locator = (By.CSS_SELECTOR, '.title')
    _course_title_locator = (By.CSS_SELECTOR, '.course-settings-title')
    _course_term_locator = (By.CSS_SELECTOR, '.course-settings-term')
    _instructor_section_locator = (By.CSS_SELECTOR, '.teachers')
    _student_roster_section_locator = (By.CSS_SELECTOR, '.periods')

    class Teachers(Region):
        """The 'Instructors' table."""

        _add_teacher_locator = (By.CSS_SELECTOR, '.add-teacher')
        _teacher_row_locator = (By.CSS_SELECTOR, 'tbody tr')

        def add_instructor(self):
            """Click the 'Add Instructor' link.

            :return: the open AddInstructor modal
            :rtype: :py:class:`AddInstructor`

            """
            link = self.find_element(*self._add_teacher_locator)
            Utility.click_option(self.driver, element=link)
            sleep(1)
            modal_root = self.driver.execute_script(GET_ROOT.format('dialog'))
            return AddInstructor(self.page, modal_root)

        @property
        def instructors(self):
            """Return the current list of instructors.

            :return: the list of teachers in the instructor table
            :rtype: list(:py:class:`~CourseRoster.Teachers.Teacher`)

            """
            return [self.Teacher(self, instructor)
                    for instructor
                    in self.find_elements(*self._teacher_row_locator)]

        def get_instructor(
                self, first_name=None, last_name=None, position=None):
            """Return the instructor row based on their name or position.

            :param str first_name: (optional) match the instructor row by the
                first match on the teacher's first name
            :param str last_name: (optional) match the instructor row by the
                first match on the teacher's last name
            :param int position: (optional) select the instructor row by the
                row position (e.g. ``position = 1`` is the first instructor)
            :return: the instructor row
            :rtype: :py:class:`~CourseRoster.Teachers.Teacher`
            :raises TutorException: if a match isn't found

            """
            if position:
                return self.instructors[position - 1]
            elif first_name:
                for instructor in self.instructors:
                    if instructor.first_name == first_name:
                        return instructor
                raise TutorException('No instructor matches first name "{0}"'
                                     .format(first_name))
            elif last_name:
                for instructor in self.instructors:
                    if instructor.last_name == last_name:
                        return instructor
                raise TutorException('No instructor matches last name "{0}"'
                                     .format(last_name))
            raise TutorException('No match option provided')

        class Teacher(User):
            """An instructor row with actions."""

            def remove(self):
                """Click the 'Remove' button.

                :return: the remove instructor tooltip
                :rtype: :py:class:`RemoveInstructor`

                """
                return self._remove_user(student=False, return_tooltip=True)

            def remove_instructor(self):
                """Remove this instructor from the course.

                :return: the course roster
                :rtype: :py:class:`CourseRoster`

                """
                self._remove_user(student=False)
                return self.page.page

    class Roster(Region):
        """The student roster tables."""

        _section_tab_locator = (By.CSS_SELECTOR, '[role=tab]')
        _add_section_link_locator = (By.CSS_SELECTOR, '.add-period')
        _rename_section_link_locator = (By.CSS_SELECTOR, '.rename-period')
        _delete_section_link_locator = (By.CSS_SELECTOR, '.delete-period')
        _student_row_locator = (By.CSS_SELECTOR, '.students tbody tr')
        _dropped_student_row_locator = (
            By.CSS_SELECTOR, '.dropped-students tbody tr')

        class Section(Region):
            """A section or period tab."""

            _section_name_locator = (By.CSS_SELECTOR, 'h2')

        class Student(User):
            """A student row with actions."""

            _student_id_locator = (By.CSS_SELECTOR, '.identifier')
            _edit_student_id_locator = (By.CSS_SELECTOR, '.student-id a')
            _change_section_link_locator = (
                By.XPATH, '//a[*[@data-icon="clock"]]')
            _readd_student_link_locator = (
                By.XPATH, '//a[*[@data-icon="user-plus"]]')
