"""The instructor's course roster management page."""

from __future__ import annotations

from time import sleep

from pypom import Region
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect

from pages.tutor.base import TutorBase
from utils.tutor import TutorException
from utils.utilities import Utility

# a javascript query to get the modal and tooltip root that is a neighbor of
# the React root element
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
        :rtype: :py:class:`~pages.tutor.course.CourseRoster`

        :noindex:

        """
        button = self.find_element(*self._action_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.25)
        self.wait.until(expect.staleness_of(self.root))
        return self.page


class RemoveInstructor(Tooltip):
    """Remove a current course instructor tooltip."""

    def remove(self):
        """Remove the selected instructor from the course.

        :return: the course roster
        :rtype: :py:class:`~pages.tutor.course.CourseRoster`

        """
        return self._perform_action()


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
            return self.root.get_attribute('textContent')

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

    def drop(self):
        """Drop the student from the course.

        :return: the course roster
        :rtype: :py:class:`~pages.tutor.course.CourseRoster`

        """
        return self._perform_action()


class ReAddStudent(Tooltip):
    """Re-add a dropped student to the active roster tooltip."""

    def restore(self):
        """Readd the student to the course.

        :return: the course roster
        :rtype: :py:class:`~pages.tutor.course.CourseRoster`

        """
        return self._perform_action()


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
        sleep(0.25)
        self.wait.until(expect.staleness_of(self.root))
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

        :param str section_name: the new section name
        :return: the Add Section modal
        :rtype: :py:class:`AddSection`

        """
        self.section_name.send_keys(section_name)
        return self

    def add(self):
        """Click the 'Add' button.

        .. note::

           If the section_name matches an existing section (case-sensitive), an
           HTML 422 error will be thrown by Tutor; server errors are not
           handled by the automation code.

        :return: the course roster with the new section displayed in the
            available tabs
        :rtype: :py:class:`CourseRoster`

        """
        button = self.find_element(*self._add_section_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.25)
        self.wait.until(expect.staleness_of(self.root))
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

    def rename(self):
        """Rename the current section.

        :return: the course roster
        :rtype: :py:class:`~pages.tutor.course.CourseRoster`

        """
        return self.add()


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
        sleep(0.25)
        try:
            self.wait.until(expect.staleness_of(self.root))
        except TimeoutException:
            raise TutorException('Could not delete the course section')
        sleep(1)
        return self.page

    def cancel(self):
        """Click on the 'Cancel' button.

        :return: the course roster
        :rtype: :py:class:`CourseRoster`

        """
        button = self.find_element(*self._cancel_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.25)
        self.wait.until(expect.staleness_of(self.root))
        return self.page


# -------------------------------------------------------- #
# The Course Roster
# -------------------------------------------------------- #

class User(Region):
    """A base user row for teachers and students."""

    _first_name_locator = (By.CSS_SELECTOR, 'td:first-child')
    _last_name_locator = (By.CSS_SELECTOR, 'td:nth-child(2)')
    _remove_instructor_user_locator = (
        By.CSS_SELECTOR, '.actions a:first-child')
    _remove_student_user_locator = (
        By.CSS_SELECTOR, '.actions a:nth-child(2)')

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
        locator = self._remove_student_user_locator if student \
            else self._remove_instructor_user_locator
        button = self.find_element(*locator)
        Utility.click_option(self.driver, element=button)
        tooltip_root = self.driver.execute_script(GET_ROOT.format('tooltip'))
        if student:
            popup = DropStudent(self, tooltip_root)
            if return_tooltip:
                return popup
            popup.drop()
        else:
            popup = RemoveInstructor(self, tooltip_root)
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

    @property
    def loaded(self) -> bool:
        """Return True when the instructor list is populated.

        :return: ``True`` when at least one instructor is found
        :rtype: bool

        """
        return bool(self.instructors.instructors)

    @property
    def title(self) -> str:
        """Return the page title.

        :return: the page title
        :rtype: str

        """
        return self.find_element(*self._page_title_locator).text

    @property
    def course_name(self) -> str:
        """Return the course name.

        :return: the course name
        :rtype: str

        """
        return self.find_element(*self._course_title_locator).text

    @property
    def course_term(self) -> str:
        """Return the course term.

        :return: the course term
        :rtype: str

        """
        return self.find_element(*self._course_term_locator).text

    @property
    def instructors(self) -> CourseRoster.Teachers:
        """Access the 'Instructors' table.

        :return: the instructors table region
        :rtype: :py:class:`~pages.tutor.roster.CourseRoster.Teachers`

        """
        teachers_table = self.find_element(*self._instructor_section_locator)
        return self.Teachers(self, teachers_table)

    @property
    def roster(self) -> CourseRoster.Roster:
        """Access the student roster table.

        :return: the student rosters
        :rtype: :py:class:`~pages.tutor.roster.CourseRoster.Roster`

        """
        roster = self.find_element(*self._student_roster_section_locator)
        return self.Roster(self, roster)

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

            def remove(self, remove_instructor=True):
                """Remove this instructor from the course.

                :return: the course roster if remove_instructor is ``True``
                    else the remove instructor tooltip
                :rtype: :py:class:`CourseRoster` or
                    :py:class:`RemoveInstructor`

                """
                if remove_instructor:
                    self._remove_user(student=False)
                    return self.page.page
                return self._remove_user(student=False, return_tooltip=True)

    class Roster(Region):
        """The student roster tables."""

        _section_tab_locator = (By.CSS_SELECTOR, '[role=tab]')
        _add_section_link_locator = (By.CSS_SELECTOR, '.add-period')
        _rename_section_link_locator = (By.CSS_SELECTOR, '.rename-period')
        _delete_section_link_locator = (By.CSS_SELECTOR, '.delete-period')
        _active_section_name_locator = (By.CSS_SELECTOR, '.active h2')
        _student_row_locator = (By.CSS_SELECTOR, '.students tbody tr')
        _dropped_student_row_locator = (
            By.CSS_SELECTOR, '.dropped-students tbody tr')

        @property
        def sections(self):
            """Return the list of available course sections or periods.

            :return: the list of course section tabs
            :rtype: list(:py:class:`~CourseRoster.Roster.Section`)

            """
            return [self.Section(self, tab)
                    for tab in self.find_elements(*self._section_tab_locator)]

        def select_section(self, name=None, position=1):
            """Select a section or period tab by name or position.

            .. note::

               section/period names are case sensitive (e.g. '1st' and '1ST'
               can occur in the same course)

            :param str name: (optional) the section or period name to select
            :param int position: (optional) the position of the section or
                period tab to select from 1 to the number of tabs
            :return: the course roster displaying the selected course section
                roster
            :rtype: :py:class:`CourseRoster`

            :raises :py:class:`~utils.tutor.TutorException`: if the name does
                not match an existing tab name or if the position is not
                between 1 and number of active tabs

            """
            if name:
                section_found = False
                for section in self.sections:
                    if section.name == name:
                        section_found = True
                        section.select()
                if not section_found:
                    raise TutorException(
                        '"{name}" does not match any active section'
                        .format(name=name))
            else:
                maximum = len(self.sections)
                if position < 1 or position > maximum:
                    raise TutorException(
                        "position {pos} is not between 1 and {max}"
                        .format(position, maximum))
                self.sections[position - 1].select()
            sleep(0.5)
            return self.page

        def add_section(self, name=None):
            """Add a new section or period to the course.

            .. note::

               If the name matches an existing section (case-sensitive), an
               HTML 422 error will be thrown by Tutor; server errors are not
               handled by the automation code.

            If name is not provided, open and return the Add Section modal. If
            it is provided, add the new section or period to the course and
            return the course roster.

            :param str name: (optional) the section or period name
            :return: the Add Section modal if name is not provided or the
                course roster if name is provided
            :rtype: :py:class:`AddSection` or :py:class:`CourseRoster`

            """
            link = self.find_element(*self._add_section_link_locator)
            Utility.click_option(self.driver, element=link)
            sleep(0.5)
            dialog_root = self.driver.execute_script(GET_ROOT.format('dialog'))
            modal = AddSection(self.page, dialog_root)
            if not name:
                return modal
            modal.section_name = name
            return modal.add()

        def rename_section(self, name=None):
            """Rename a current course section or period.

            .. note::

               If the name matches an existing section (case-sensitive), an
               HTML 422 error will be thrown by Tutor; server errors are not
               handled by the automation code.

            If name is not provided, open and return the Rename Section modal.
            If it is provided, rename the current section or period and return
            the course roster.

            :param str name: (optional) the section or period name
            :return: the Rename Section modal if name is not provided or the
                course roster if name is provided
            :rtype: :py:class:`RenameSection` or :py:class:`CourseRoster`

            """
            link = self.find_element(*self._rename_section_link_locator)
            Utility.click_option(self.driver, element=link)
            sleep(0.5)
            dialog_root = self.driver.execute_script(GET_ROOT.format('dialog'))
            modal = RenameSection(self.page, dialog_root)
            if not name:
                return modal
            Utility.clear_field(self.driver, field=modal.section_name)
            modal.section_name = name
            return modal.rename()

        def delete_section(self, delete=True):
            """Delete the current section or period.

            :param bool delete: (optional) if ``True``, delete the current
                section or period; if ``False`` open and return the Delete
                Section modal
            :return: the Delete Section modal if delete is ``False`` or the
                course roster if delete is ``True``
            :rtype: :py:class:`DeleteSection` or :py:class:`CourseRoster`

            """
            link = self.find_element(*self._delete_section_link_locator)
            Utility.click_option(self.driver, element=link)
            sleep(0.5)
            dialog_root = self.driver.execute_script(GET_ROOT.format('dialog'))
            modal = DeleteSection(self.page, dialog_root)
            return modal.delete() if delete else modal

        @property
        def current_section(self) -> str:
            """Return the name of the currently selected course section.

            :return: the current course section name
            :rtype: str

            """
            return (self.find_element(*self._active_section_name_locator)
                    .get_attribute('textContent'))

        @property
        def students(self):
            """Access the student rows.

            :return: the list of students in the current section or period
            :rtype: list(:py:class:`~CourseRoster.Roster.Student`)

            """
            return [self.Student(self, row)
                    for row
                    in self.find_elements(*self._student_row_locator)]

        @property
        def dropped_students(self):
            """Access the dropped student rows.

            :return: the list of dropped students
            :rtype: list(:py:class:`~CourseRoster.Roster.Student`)

            """
            return [self.Student(self, row)
                    for row
                    in self.find_elements(*self._dropped_student_row_locator)]

        class Section(Region):
            """A section or period tab."""

            _section_name_locator = (By.CSS_SELECTOR, 'h2')
            _section_select_locator = (By.CSS_SELECTOR, 'a')

            @property
            def name(self):
                """Return the section or period name.

                :return: the section or period name
                :rtype: str

                """
                return (self.find_element(*self._section_name_locator)
                        .get_attribute('textContent'))

            @property
            def is_active(self):
                """Return True if the section is currently displayed.

                :return: ``True`` if the section is displayed else ``False``
                :rtype: bool

                """
                return self.root.get_attribute('aria-selected') == 'true'

            def select(self):
                """Click on the section or period tab.

                Click on the section or period tab to display that section's
                active students.

                :return: the course roster with the selected section active
                :rtype: :py:class:`CourseRoster`

                """
                button = self.find_element(*self._section_select_locator)
                Utility.click_option(self.driver, element=button)
                sleep(0.5)
                return self.page.page

        class Student(User):
            """A student row with actions."""

            _student_first_name_locator = (By.CSS_SELECTOR, 'td:first-child')
            _student_last_name_locator = (By.CSS_SELECTOR, 'td:nth-child(2)')
            _student_id_locator = (By.CSS_SELECTOR, '.identifier')
            _student_id_input_box_locator = (
                By.CSS_SELECTOR, '.student-id input')
            _edit_student_id_locator = (By.CSS_SELECTOR, '.student-id a')
            _change_section_link_locator = (
                By.CSS_SELECTOR, '.actions a:first-child')
            _drop_student_link_locator = (
                By.CSS_SELECTOR, '.actions a:nth-child(2)')
            _readd_student_link_locator = (
                By.CSS_SELECTOR, '.actions a:first-child')

            @property
            def name(self) -> str:
                """Return the student's full name.

                :return: the student's first and last name
                :rtype: str

                """
                first = self.find_element(*self._student_first_name_locator)
                last = self.find_element(*self._student_last_name_locator)
                return f"{first.text} {last.text}"

            @property
            def student_id(self):
                """Return the student's identification number.

                :return: the student ID number
                :rtype: str

                """
                try:
                    return self.find_element(*self._student_id_locator).text
                except NoSuchElementException:
                    return (self.find_element(
                        *self._student_id_input_box_locator)
                        .get_attribute('value'))

            @student_id.setter
            def student_id(self, _id=None):
                """Set the student's identification number.

                :param str _id: (optional) the student's new ID number; if _id
                    is '' or None, the field will be cleared
                :return: the course roster
                :rtype: :py:class:`CourseRoster`

                """
                from selenium.webdriver.common.keys import Keys
                edit_button = self.find_element(*self._edit_student_id_locator)
                Utility.click_option(self.driver, element=edit_button)
                sleep(0.25)
                id_field = self.find_element(
                    *self._student_id_input_box_locator)
                Utility.clear_field(self.driver, id_field)
                if _id:
                    edit_button = self.find_element(
                        *self._edit_student_id_locator)
                    Utility.click_option(self.driver, element=edit_button)
                    sleep(0.25)
                    id_field = self.find_element(
                        *self._student_id_input_box_locator)
                    id_field.send_keys(_id)
                id_field.send_keys(Keys.TAB)
                return self.page.page

            def change_section(self, section=None):
                """Move the student to a new section.

                :param str section: (optional) the student's new section or
                    period
                :return: the change section tooltip if section is not provided
                    else the course roster
                :rtype: :py:class:`ChangeSection` or :py:class:`CourseRoster`

                :raises :py:class:`~utils.tutor.TutorException`: if no section
                    or period matches the requested section

                """
                change_button = self.find_element(
                    *self._change_section_link_locator)
                Utility.click_option(self.driver, element=change_button)
                sleep(0.25)
                tooltip_root = self.driver.execute_script(
                    GET_ROOT.format('tooltip'))
                tooltip = ChangeSection(self.page.page, tooltip_root)
                sleep(1)
                return tooltip.switch_to(section) if section else tooltip

            def drop(self, drop_student=True):
                """Click the 'Drop' button.

                :return: the course roster if drop_student is ``True``,
                    otherwise the drop student tooltip
                :rtype: :py:class:`DropStudent` or :py:class:`CourseRoster`

                """
                if not drop_student:
                    return self._remove_user(return_tooltip=True)
                self._remove_user()
                return self.page.page

            def add_back_to_active_roster(self, return_tooltip=False):
                """Re-add the dropped student to the active roster.

                :param bool return_tooltip: (optional) return the re-add
                    tooltip instead of re-adding the student
                :return: the add back tooltip if return_tooltip is ``True``
                    else the course roster
                :rtype: :py:class:`ReAddStudent` or :py:class:`CourseRoster`

                """
                readd_button = self.find_element(
                    *self._readd_student_link_locator)
                Utility.click_option(self.driver, element=readd_button)
                sleep(0.25)
                tooltip_root = self.driver.execute_script(
                    GET_ROOT.format('tooltip'))
                tooltip = ReAddStudent(self.page.page, tooltip_root)
                return tooltip.restore() if not return_tooltip else tooltip
