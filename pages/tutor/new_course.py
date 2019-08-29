"""The Tutor course creation wizard."""

from __future__ import annotations

from time import sleep
from typing import List, Union

from pypom import Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from pages.tutor.calendar import Calendar
from utils.tutor import TutorException
from utils.utilities import Utility, go_to_


class CloneCourse(TutorBase):
    """Clone an existing course."""

    _loaded_pane_locator = (By.CSS_SELECTOR, '.new-course-wizard')
    _heading_locator = (By.CSS_SELECTOR, '.card-header')
    _cancel_button_locator = (By.CSS_SELECTOR, '.cancel')
    _back_button_locator = (By.CSS_SELECTOR, '.back')
    _continue_button_locator = (By.CSS_SELECTOR, '.next')
    _is_course_estimation_pane_locator = (By.CSS_SELECTOR, '.numbers')

    @property
    def loaded(self) -> bool:
        """Return True when the new course wizard root is found.

        :return: ``True`` when the new course wizard root element is located
        :rtype: bool

        """
        return bool(self.find_elements(*self._loaded_pane_locator))

    @property
    def heading(self) -> str:
        """Return the heading text.

        :return: the entire text heading
        :rtype: str

        """
        return (self.find_element(*self._heading_locator)
                .get_attribute('textContent'))

    def cancel(self) -> None:
        """Cancel the course creation wizard.

        :return: None

        """
        button = self.find_element(*self._cancel_button_locator)
        Utility.click_option(self.driver, element=button)

    def back(self) -> None:
        """Go to the previous step in the wizard.

        :return: None

        """
        button = self.find_element(*self._back_button_locator)
        Utility.click_option(self.driver, element=button)

    def next(self) -> Union[Calendar, None]:
        """Continue to the next step in the wizard.

        :return: the instructor's new calendar if on the course estimate step,
            otherwise None
        :rtype: :py:class:`~pages.tutor.calendar.Calendar` or NoneType

        """
        go_to_calendar = self.is_course_estimate
        button = self.find_element(*self._continue_button_locator)
        Utility.click_option(self.driver, element=button)
        if go_to_calendar:
            self.wait.until(lambda _: 'new-course' not in self.location)
            sleep(0.5)
            return go_to_(Calendar(self.driver, base_url=self.base_url))

    @property
    def is_course_estimate(self) -> bool:
        """Return True if on the course estimation step.

        :return: ``True`` if on the course estimation step, ``False`` if not
        :rtype: bool

        """
        return bool(
            self.find_elements(*self._is_course_estimation_pane_locator))

    @property
    def term(self) -> CloneCourse.Term:
        """Access the new course term pane.

        :return: the new course's term selection pane
        :rtype: :py:class:`~pages.tutor.new_course.CloneCourse.Term`

        """
        return self.Term(self)

    @property
    def name(self) -> CloneCourse.Name:
        """Access the new course name pane.

        :return: the new course's name and timezone selection pane
        :rtype: :py:class:`~pages.tutor.new_course.CloneCourse.Name`

        """
        return self.Name(self)

    @property
    def details(self) -> CloneCourse.Details:
        """Access the new course details pane.

        :return: the new course's section request and student estimate pane
        :rtype: :py:class:`~pages.tutor.new_course.CloneCourse.Details`

        """
        return self.Details(self)

    class Term(Region):
        """Select the course term."""

        _course_term_locator = (
            By.CSS_SELECTOR, '.choices-listing [role=button]')

        @property
        def loaded(self) -> bool:
            """Return True when course semesters/quarters are found.

            :return: ``True`` when course term options are found
            :rtype: bool

            :noindex:

            """
            return bool(self.terms)

        @property
        def terms(self) -> List[CloneCourse.Term.Term]:
            r"""Access the available course terms.

            :return: the list of course terms available for new courses
            :rtype: list(:py:class:`~pages.tutor.new_course \
                                    .CloneCourse.Term.Term`)

            """
            return [self.Term(self, option)
                    for option
                    in self.find_elements(*self._course_term_locator)]

        def select_by_term(self, term: str) -> None:
            """Select a term by the semester or quarter name.

            :param str term: the term to select
            :return: None

            :raises :py:class:`~utils.tutor.TutorException`: if the term is not
                found or is not available

            """
            for option in self.terms:
                if option.term.lower() == term.lower():
                    option.select()
                    return
            raise TutorException(f'"{term}" not found or not available')

        class Term(Region):
            """A course term."""

            _term_locator = (By.CSS_SELECTOR, '.term')
            _year_locator = (By.CSS_SELECTOR, '.year')
            _option_locator = (By.CSS_SELECTOR, '.content')

            @property
            def term(self) -> str:
                """Return the semester or quarter.

                :return: the semester or quarter name
                :rtype: str

                """
                return self.find_element(*self._term_locator).text

            @property
            def year(self) -> int:
                """Return the term year.

                :return: the term year
                :rtype: int

                """
                return int(self.find_element(*self._year_locator).text)

            @property
            def selected(self) -> bool:
                """Return True if the term is currently selected.

                :return: ``True`` if the term is selected, otherwise ``False``
                :rtype: bool

                """
                return 'active' in self.root.get_attribute('class')

            def select(self) -> None:
                """Click on the term option.

                :return: None

                """
                button = self.find_element(*self._option_locator)
                Utility.click_option(self.driver, element=button)

    class Name(Region):
        """Choose the course title or name."""

        _course_name_input_locator = (
            By.CSS_SELECTOR, '.course-details-name input')
        _select_course_timezone_locator = (By.CSS_SELECTOR, 'select')
        _timezone_options_locator = (By.CSS_SELECTOR, 'select option')

        @property
        def loaded(self) -> bool:
            """Return True when the course name input box is found.

            :return: ``True`` when the course name field is found
            :rtype: bool

            :noindex:

            """
            return bool(self.find_elements(*self._course_name_input_locator))

        @property
        def name(self) -> str:
            """Return the current value for the new course title.

            :return: the new course's name
            :rtype: str

            """
            return (self.find_element(*self._course_name_input_locator)
                    .get_attribute('value'))

        @name.setter
        def name(self, name: str) -> None:
            """Set the course title or name.

            .. note:

               The method uses the javascript value setter to overwrite
               whatever is in the name field.

            :param str name: the new course name
            :return: None

            """
            name_box = self.find_element(*self._course_name_input_locator)
            Utility.clear_field(self.driver, field=name_box)
            sleep(0.25)
            name_box.send_keys(name)

        @property
        def timezone(self) -> str:
            """Return the currently selected timezone.

            :return: the current timezone string
            :rtype: str

            """
            return (self.find_element(*self._select_course_timezone_locator)
                    .get_attribute('value'))

        @timezone.setter
        def timezone(self, zone: str) -> None:
            """Set the course timezone.

            :param str zone: the new timezone for the course
            :return: None

            :raises :py:class:`~utils.tutor.TutorException`: if the new
                timezone does not match any of the available options

            """
            options = [option.text
                       for option
                       in self.find_elements(*self._timezone_options_locator)]
            if zone not in options:
                raise TutorException(
                    f'"{zone}" is not an available timezone option')
            Utility.select(
                driver=self.driver,
                element_locator=self._select_course_timezone_locator,
                label=zone)

    class Details(Region):
        """Provide student information."""

        _expanation_locator = (By.CSS_SELECTOR, 'form > div:not(.form-group)')
        _course_sections_locator = (By.CSS_SELECTOR, '#number-sections')
        _student_estimate_locator = (By.CSS_SELECTOR, '#number-students')
        _alert_error_message_locator = (By.CSS_SELECTOR, '[role=alert]')

        @property
        def loaded(self) -> bool:
            """Return True when the course details fields are found.

            :return: ``True`` when the course sections and estimated students
                fields are found.
            :rtype: bool

            :noindex:

            """
            return (self.find_element(*self._course_sections_locator) and
                    self.find_element(*self._student_estimate_locator) and
                    (sleep(0.5) or True))

        @property
        def explanation(self) -> str:
            """Return the course size estimation explanation.

            :return: the course size estimation explanation
            :rtype: str

            """
            return (self.find_element(*self._expanation_locator)
                    .get_attribute('textContent'))

        @property
        def sections(self) -> int:
            """Return the initial number of course sections or periods.

            :return: the requested number of course sections to automatically
                create or 0 if the value is not set
            :rtype: int

            """
            try:
                return int(self.find_element(*self._course_sections_locator)
                           .get_attribute('value'))
            except ValueError:
                return 0

        @sections.setter
        def sections(self, sections: int = 1) -> None:
            """Set the initial number of course sections or periods to create.

            :param int sections: the requested number of sections to create for
                the new course
            :return: None

            :raises :py:class:`~utils.tutor.TutorException`: if the number of
                sections is less than 1 or greater than 10

            """
            if sections < 1:
                raise TutorException(
                    f'the minimum number of sections is 1 ({sections} < 1)')
            section_box = self.find_element(*self._course_sections_locator)
            self.driver.execute_script('arguments[0].value = "";', section_box)
            section_box.send_keys(sections)
            sleep(0.25)
            error = self.error
            if error:
                raise TutorException(error.strip())

        @property
        def students(self) -> int:
            """Return the expected number of students.

            :return: the projected number of students who will enroll in the
                course or 0 if the value is not set
            :rtype: int

            """
            try:
                return int(self.find_element(*self._student_estimate_locator)
                           .get_attribute('value'))
            except ValueError:
                return 0

        @students.setter
        def students(self, students: int = 1) -> None:
            """Set the estimated number of students who will enroll.

            :param int students: the estimated number of students who will
                enroll in the course
            :return: None

            :raises :py:class:`~utils.tutor.TutorException`: if the number of
                students is less than 1 or greater than 1,500

            """
            if students < 1:
                raise TutorException(
                    f'the minimum student estimate is 1 ({students} < 1)')
            self.find_element(*self._student_estimate_locator) \
                .send_keys(students)
            sleep(0.25)
            error = self.error
            if error:
                raise TutorException(error.strip())

        @property
        def error(self) -> str:
            """Return the input error message, if present.

            .. note:

               If both cases are true (sections > 10 and students > 1500), then
               the first input issue is displayed. If the first issue is
               remedied, the second error replaces the first.

            :return: the error message when the number of sections is greater
                than 10 or the number of students is greater than 1,500
            :rtype: str

            """
            try:
                return (self.find_element(*self._alert_error_message_locator)
                        .get_attribute('textContent'))
            except NoSuchElementException:
                return ''


class NewCourse(CloneCourse):
    """Create a new Tutor course."""

    _new_or_copy_pane_locator = (By.CSS_SELECTOR, '.new_or_copy')

    @property
    def clone_possible(self) -> bool:
        """Return True if a previous course can be cloned.

        .. note:

           This method is expected to be run after selecting the course term.

        :return: ``True`` if a previous course exists and can be cloned,
            otherwise ``False``
        :rtype: bool

        """
        sleep(0.5)
        return bool(self.find_elements(*self._new_or_copy_pane_locator))

    @property
    def course(self) -> NewCourse.Course:
        """Access the new course course pane.

        :return: the new course's section request and student estimate pane
        :rtype: :py:class:`~pages.tutor.new_course.NewCourse.Course`

        """
        return self.Course(self)

    @property
    def new_or_clone(self) -> NewCourse.NewOrClone:
        """Access the new course details pane.

        :return: the new course's section request and student estimate pane
        :rtype: :py:class:`~pages.tutor.new_course.NewCourse.NewOrClone`

        """
        return self.NewOrClone(self)

    @property
    def cloned_from(self) -> NewCourse.BaseCourse:
        """Access the new course details pane.

        :return: the new course's section request and student estimate pane
        :rtype: :py:class:`~pages.tutor.new_course.NewCourse.BaseCourse`

        """
        return self.BaseCourse(self)

    class Course(Region):
        """Select the course book."""

        _book_option_locator = (
            By.CSS_SELECTOR, '.choices-listing [role=button]')

        @property
        def loaded(self) -> bool:
            """Return True when the book options list is populated.

            :return: ``True`` when at least one book option is found
            :rtype: bool

            :noindex:

            """
            return bool(self.books)

        @property
        def books(self) -> List[NewCourse.Course.Book]:
            r"""Access the course book options.

            :return: the list of available books
            :rtype: \
                list(:py:class:`~pages.tutor.new_course.NewCourse.Course.Book`)

            """
            return [self.Book(self, option)
                    for option
                    in self.find_elements(*self._book_option_locator)]

        def select_by_title(self, title: str) -> None:
            """Select a course book by the book title.

            :param str title: the book title
            :return: None

            :raises :py:class:`~utils.tutor.TutorException`: if the title is
                not found or is not available

            """
            for option in self.books:
                if option.title.lower() == title.lower():
                    option.select()
                    return
            raise TutorException(f'"{title}" not found or not available')

        class Book(Region):
            """An available course book."""

            _book_content_locator = (By.CSS_SELECTOR, '.content')

            @property
            def appearance(self) -> str:
                """Return the book appearance code.

                :return: the book appearance code
                :rtype: str

                """
                return self.root.get_attribute('data-appearance')

            @property
            def is_selected(self) -> bool:
                """Return True if the book is currently selected.

                :return: ``True`` if the book is the current course selection,
                    otherwise ``False``
                :rtype: bool

                """
                return 'active' in self.root.get_attribute('class')

            @property
            def title(self) -> str:
                """Return the book title.

                :return: the book title
                :rtype: str

                """
                return self.find_element(*self._book_content_locator).text

            def select(self) -> None:
                """Click on the book option.

                :return: None

                """
                book = self.find_element(*self._book_content_locator)
                Utility.click_option(self.driver, element=book)

    class NewOrClone(Region):
        """Create a new course or clone an existing course."""

        _new_course_option_locator = (
            By.CSS_SELECTOR, '[data-new-or-copy=new]')
        _clone_course_option_locator = (
            By.CSS_SELECTOR, '[data-new-or-copy=copy]')

        @property
        def loaded(self) -> bool:
            """Return True when the new course option is found.

            :return: ``True`` when the 'Create a new course' option is found
            :rtype: bool

            :noindex:

            """
            return bool(self.find_element(*self._new_course_option_locator))

        def create_a_new_course(self) -> None:
            """Create a new course.

            Select the option to create a new course.

            :return: None

            """
            new_course = self.find_element(*self._new_course_option_locator)
            Utility.click_option(self.driver, element=new_course)

        def clone_a_past_course(self) -> None:
            """Clone an existing course.

            Select the option to clone an existing course.

            :return: None

            """
            clone = self.find_element(*self._clone_course_option_locator)
            Utility.click_option(self.driver, element=clone)

    class BaseCourse(Region):
        """Select the course to clone."""

        _existing_course_option_locator = (
            By.CSS_SELECTOR, '.choices-listing [role=button]')

        @property
        def loaded(self) -> bool:
            """Return True when a previous course option is found.

            :return: ``True`` when at least one course clone base is found
            :rtype: bool

            :noindex:

            """
            return bool(self.courses)

        @property
        def courses(self) -> List[NewCourse.BaseCourse.Course]:
            r"""Access the previous course options.

            :return: the list of available courses to clone
            :rtype: list(:py:class:`~pages.tutor.new_course \
                                    .NewCourse.BaseCourse.Course`)

            """
            return [self.Course(self, option)
                    for option
                    in self.find_elements(
                        *self._existing_course_option_locator)]

        def select_by_name(self, name: str) -> None:
            """Select a course to clone by name.

            :param str name: the existing course name
            :return: None

            :raises :py:class:`~utils.tutor.TutorException`: if the name is
                not found or is not available

            """
            for option in self.courses:
                if option.name.lower() == name.lower():
                    option.select()
                    return
            raise TutorException(f'"{name}" not found or not available')

        class Course(Region):
            """A previous course."""

            _course_name_locator = (By.CSS_SELECTOR, '.title')
            _course_term_locator = (By.CSS_SELECTOR, '.sub-title')

            @property
            def name(self) -> str:
                """Return the existing course name.

                :return: the course name
                :rtype: str

                """
                return self.find_element(*self._course_name_locator).text

            @property
            def term(self) -> str:
                """Return the existing course semester/quarter and year.

                :return: the course term
                :rtype: str

                """
                return self.find_element(*self._course_term_locator).text

            def select(self) -> None:
                """Click on the course option.

                :return: None

                """
                Utility.click_option(self.driver, element=self.root)
