"""The instructor's assignment control pages.

Add/Edit/Delete Event
Add/Edit/Delete External
Add/Edit/Delete Homework
Add/Edit/Delete Reading

"""

from __future__ import annotations

from time import sleep
from typing import Dict, List, Union

from pypom import Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from pages.tutor.base import TutorBase
from pages.tutor.calendar import Calendar
from pages.tutor.preview import StudentPreview
from pages.tutor.reference import ReferenceBook
from pages.tutor.settings import CourseSettings
from regions.tutor.assessment import Assessment
from utils.tutor import TutorException
from utils.utilities import Utility, go_to_

# -------------------------------------------------------- #
# Javascript page requests
# -------------------------------------------------------- #

# return True if the field error message is displayed
DISPLAYED = 'return getComputedStyle(arguments[0]).display != none;'
# get the modal and tooltip root that is a neighbor of the React root element
GET_ROOT = 'return document.querySelector("[role={0}]");'
# wait until the loading animation (bouncing books) is gone
ANIMATION = 'return document.querySelector(".loading-animation");'


# -------------------------------------------------------- #
# Page dialog boxes and tooltips
# -------------------------------------------------------- #

class ButtonTooltip(Region):
    """The card button explanation tooltip."""

    _explanation_locator = (By.CSS_SELECTOR, 'p')

    @property
    def root(self) -> WebElement:
        """Locate the tooltip trunk.

        :return: the root element for a tooltip
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.driver.execute_script(GET_ROOT.format('tooltip'))

    @property
    def description(self) -> str:
        """Return the tooltip content.

        :return: the form buttons and there purpose
        :rtype: str

        """
        return ' '.join(list(
            [line.get_attribute('textContent')
             for line in self.find_elements(*self._explanation_locator)]))


class CancelConfirm(Region):
    """The unsaved changes confirmation dialog."""

    _modal_title_locator = (By.CSS_SELECTOR, '.modal-title')
    _close_x_locator = (By.CSS_SELECTOR, '.close')
    _explanation_locator = (By.CSS_SELECTOR, '.modal-body')
    _yes_button_locator = (By.CSS_SELECTOR, '.ok')
    _no_button_locator = (By.CSS_SELECTOR, '.cancel')

    @property
    def title(self) -> str:
        """Return the dialog box title.

        :return: the modal title
        :rtype: str

        """
        return self.find_element(*self._modal_title_locator).text

    def close(self, no_button=False) -> Assignment:
        """Click on the close 'x' button.

        :param bool no_button: (optional) use the 'No' button instead of the
            'x' button
        :return: the assignment page
        :rtype: :py:class:`Assignment`

        """
        locator = self._no_button_locator if no_button \
            else self._close_x_locator
        button = self.find_element(*locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.25)
        return self.page

    @property
    def explanation(self) -> str:
        """Return the modal explanation text.

        :return: the modal explaining unsaved changes
        :rtype: str

        """
        return self.find_element(*self._explanation_locator).text

    def yes(self) -> Calendar:
        """Click on the 'Yes' button.

        :return: the instructor's calendar
        :rtype: :py:class:`~pages.tutor.calendar.Calendar`

        """
        button = self.find_element(*self._yes_button_locator)
        Utility.click_option(self.driver, element=button)
        return go_to_(Calendar(self.driver, base_url=self.page.base_url))

    def no(self) -> Assignment:
        """Click on the 'No' button.

        :return: the assignment page
        :rtype: :py:class:`Assignment`

        """
        return self.close(no_button=True)


class ReadingQuestionTooltip(ButtonTooltip):
    """The reading questions informational tooltip."""

    pass


class HomeworkTutorSelectionsTooltip(ButtonTooltip):
    """The 'What are these?' Tutor selections tooltip."""

    pass


# -------------------------------------------------------- #
# Assignment shared properties
# -------------------------------------------------------- #

class OpenToClose(Region):
    """The open and close dates and times rows."""

    _open_date_time_locator = (By.CSS_SELECTOR, '.col-md-6:nth-child(1)')
    _close_date_time_locator = (By.CSS_SELECTOR, '.col-md-6:nth-child(2)')

    @property
    def open(self) -> OpenToClose.DateTime:
        """Access the open date and time.

        :return: a date and time set
        :rtype: :py:class:`~OpenToClose.DateTime`

        """
        open_root = self.find_element(*self._open_date_time_locator)
        return self.DateTime(self, open_root)

    @property
    def close(self) -> OpenToClose.DateTime:
        """Access the due date and time.

        :return: a date and time set
        :rtype: :py:class:`~OpenToClose.DateTime`

        """
        due_root = self.find_element(*self._close_date_time_locator)
        return self.DateTime(self, due_root)

    class DateTime(Region):
        """A assignment date and time set."""

        _date_locator = (
            By.CSS_SELECTOR, '.-assignment-open-date , .-assignment-due-date')
        _time_locator = (
            By.CSS_SELECTOR, '.-assignment-open-time , .-assignment-due-time')

        @property
        def date(self) -> OpenToClose.DateTime.Date:
            """Access the date field.

            :return: the date portion of a date time set
            :rtype: :py:class:`~OpenToClose.DateTime.Date`

            """
            date_root = self.find_element(*self._date_locator)
            return self.Date(self, date_root)

        @property
        def time(self) -> OpenToClose.DateTime.Time:
            """Access the time field.

            :return: the time portion of a date time set
            :rtype: :py:class:`~OpenToClose.DateTime.Time`

            """
            time_root = self.find_element(*self._time_locator)
            return self.Time(self, time_root)

        class Date(Region):
            """An assignment date."""

            class Calendar(Region):
                """A mini-calendar to select a date."""

                _current_month_locator = (
                    By.CSS_SELECTOR, '[class*="current-month"]')
                _month_year_locator = (
                    By.CSS_SELECTOR, '.react-datepicker__month')
                _previous_month_arrow_locator = (
                    By.CSS_SELECTOR, '[class*="navigation--previous"]')
                _next_month_arrow_locator = (
                    By.CSS_SELECTOR, '[class*="navigation--next"]')
                _day_locator = (
                    By.CSS_SELECTOR,
                    '.react-datepicker__day:not([class*=disabled])')

                @property
                def current(self) -> str:
                    """Return the calendar's current month and year.

                    :return: the mini-calendar's month and year
                    :rtype: str

                    """
                    return self.find_element(*self._current_month_locator).text

                @property
                def year(self) -> int:
                    """Return the calendar year.

                    :return: the calendar year
                    :rtype: int

                    """
                    return int(self.find_element(*self._month_year_locator)
                               .get_attribute('aria-label')
                               .split('-')[1])

                @property
                def month(self) -> int:
                    """Return the calendar month.

                    :return: the calendar month as a number
                    :rtype: int

                    """
                    return int(self.find_element(*self._month_year_locator)
                               .get_attribute('aria-label')
                               .split('-')[2])

                def previous_month(self) -> OpenToClose.DateTime.Date.Calendar:
                    """Click on the left arrow to view the previous month.

                    :return: the mini-calendar with the previous month, if the
                        previous month is an option
                    :rtype: :py:class:`~OpenToClose.DateTime.Date.Calendar`

                    """
                    arrow = self.find_elements(
                        *self._previous_month_arrow_locator)
                    if arrow:
                        Utility.click_option(self.driver, element=arrow)
                        sleep(0.5)
                    return self

                def next_month(self) -> OpenToClose.DateTime.Date.Calendar:
                    """Click on the right arrow to view the next month.

                    :return: the mini-calendar with the following month, if the
                        next month is an option
                    :rtype: :py:class:`~OpenToClose.DateTime.Date.Calendar`

                    """
                    arrow = self.find_elements(
                        *self._next_month_arrow_locator)
                    if arrow:
                        Utility.click_option(self.driver, element=arrow)
                        sleep(0.5)
                    return self

                @property
                def days(self) -> List[WebElement]:
                    r"""Return the list of valid, selectable days.

                    :return: the days available for selection
                    :rtype: list(:py:class:`~selenium.webdriver.remote \
                                            .webelement.WebElement`)

                    """
                    return self.find_elements(*self._day_locator)

                def select(self, day: Union[str, int]) -> Assignment:
                    """Select a calendar date by clicking on the day.

                    :param day: the single day to select
                    :type day: str or int
                    :return: the assignment
                    :rtype: :py:class:`Assignment`
                    :raise :py:class:`utils.tutor.TutorException`: if the
                        specified day is not an option

                    """
                    for date in self.days:
                        if date.text == str(day):
                            Utility.click_option(self.driver, element=date)
                            sleep(0.25)
                            return self.page.page.page.page
                    raise TutorException('"{0}" is not an available option'
                                         .format(day))

        class Time(Region):
            """An assignment time."""

            _label_locator = (By.CSS_SELECTOR, '.floating-label')
            _current_time_locator = (By.CSS_SELECTOR, 'input')
            _set_as_default_locator = (By.CSS_SELECTOR, 'button')

            @property
            def label(self) -> str:
                """Return the floating label.

                :return: the floating input label
                :rtype: str

                """
                return self.find_element(*self._label_locator).text

            @property
            def time(self) -> str:
                """Return the currently assigned time.

                :return: the current value for the time input box
                :rtype: str

                """
                return (self.find_element(*self._current_time_locator)
                        .get_attribute('value'))

            @time.setter
            def time(self, new_time: str) -> None:
                """Set the time value.

                .. note::

                   The time should be given as a string formatted to
                   'HH:MM(a/p)'. Some valid options: '9:21a', '11:59p'

                :param str new_time: the new time to assign
                :return: None

                """
                time_field = self.find_element(*self._current_time_locator)
                Utility.click_option(self.driver, element=time_field)
                for _ in range(8):
                    time_field.send_keys(Keys.RIGHT)
                from platform import system
                KEY = Keys.BACKSPACE if system() != 'Darwin' else Keys.DELETE
                for _ in range(8):
                    time_field.send_keys(KEY)
                time_field.send_keys(new_time)

            def set_as_default(self) -> Assignment:
                """Click the 'Set as default' button.

                :return: the assignment page
                :rtype: :py:class:`Assignment`
                :raise TutorException: if the current time is already the
                    default value

                """
                try:
                    link = self.find_element(*self._set_as_default_locator)
                    Utility.click_option(self.driver, element=link)
                    return self.page.page.page
                except NoSuchElementException:
                    raise TutorException(
                        'The current time is already the default')


class SectionSelector(Region):
    """A chapter and section selector for readings and homeworks."""

    _title_locator = (By.CSS_SELECTOR, '.card-header')
    _close_x_locator = (By.CSS_SELECTOR, '.close')
    _chapter_locator = (By.CSS_SELECTOR, '.chapter')
    _add_readings_button_locator = (By.CSS_SELECTOR, '.show-problems')
    _cancel_button_locator = (By.CSS_SELECTOR, '.btn-default')

    _exercise_selection_selector = '.homework-builder-view'

    @property
    def loaded(self) -> bool:
        """Wait until the loading animation is done.

        :return: ``True`` when the loading animation is not found, otherwise
            ``False``
        :rtype: bool

        """
        sleep(0.25)
        return self.execute_script(ANIMATION) is None

    @property
    def title(self) -> str:
        """Return the card heading.

        :return: the card heading
        :rtype: str

        """
        return self.find_element(*self._title_locator).text

    def close(self) -> Assignment:
        """Click on the close 'x' button.

        :return: close the selector and return to the assignment
        :rtype: :py:class:`Assignment`

        """
        button = self.find_element(*self._close_x_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.5)
        return self.page

    @property
    def chapters(self) -> List[SectionSelector.Chapter]:
        """Access the book chapters.

        :return: the list of book chapters
        :rtype: list(:py:class:`~SectionSelector.Chapter`)

        """
        return [self.Chapter(self, chapter)
                for chapter in self.find_elements(*self._chapter_locator)]

    def add_readings(self) -> Union[Assignment, ExerciseSelector]:
        """Click the 'Add Readings' / 'Show Problems' button.

        :return: the assignment creation wizard with the new readings added to
            the assignment or the exercise selector for homeworks
        :rtype: :py:class:`Assignment` or :py:class:`ExerciseSelector`

        """
        button = self.find_element(*self._add_readings_button_locator)
        destination = button.text
        Utility.click_option(self.driver, element=button)
        sleep(0.5)
        if 'Reading' in destination:
            return self.page
        selector_root = self.driver.execute_script(
            'return document.querySelector("{0}");'
            .format(self._exercise_selection_selector))
        return ExerciseSelector(self, selector_root)

    show_problems = add_readings

    def cancel(self) -> Assignment:
        """Click the 'Cancel' button and return to the assignment wizard.

        :return: the assignment creation page
        :rtype: :py:class:`Assignment`

        """
        button = self.find_element(*self._cancel_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.5)
        return self.page

    class Chapter(Region):
        """A book selection chapter."""

        _section_checkbox_locator = (By.CSS_SELECTOR, '[role=button] button')
        _check_state_locator = (By.CSS_SELECTOR, '.tri-state-checkbox')
        _chapter_number_locator = (By.CSS_SELECTOR, '.chapter-number span')
        _chapter_title_locator = (By.CSS_SELECTOR, '.chapter-title')
        _browse_the_book_link_locator = (By.CSS_SELECTOR, '.browse-the-book')
        _section_locator = (By.CSS_SELECTOR, '.section')

        def toggle(self) -> SectionSelector:
            """Click on the chapter bar to open or close the chapter.

            :return: the book section selector
            :rtype: :py:class:`SectionSelector`

            """
            Utility.click_option(self.driver, element=self.root)
            sleep(0.75)
            return self.page

        @property
        def is_open(self) -> bool:
            """Return True if the chapter sections are displayed.

            :return: ``True`` if the chapter is open and ``False`` if it is not
            :rtype: bool

            """
            return self.root.get_attribute('data-is-expanded') == 'true'

        def select(self) -> SectionSelector:
            """Click on the chapter check box.

            :return: the book section selector
            :rtype: :py:class:`SectionSelector`

            """
            checkbox = self.find_element(*self._section_checkbox_locator)
            Utility.click_option(self.driver, element=checkbox)
            sleep(0.75)
            return self.page

        @property
        def checked(self) -> bool:
            """Return True if the checkbox is selected.

            :return: ``True`` if the chapter checkbox is checked and ``False``
                if it is not
            :rtype: bool

            """
            checkbox = self.find_element(*self._check_state_locator)
            return 'checked' in checkbox.get_attribute('class')

        @property
        def number(self) -> str:
            """Return the chapter number.

            :return: the chapter number
            :rtype: str

            """
            return self.find_element(*self._chapter_number_locator).text

        @property
        def title(self) -> str:
            """Return the chapter title.

            :return: the chapter title
            :rtype: str

            """
            return self.find_element(*self._chapter_title_locator).text

        def browse_the_book(self) -> ReferenceBook:
            """Click on the 'Browse the Book' link to view the chapter.

            :return: the reference view for the selected chapter in a new tab
            :rtype: :py:class:`~pages.tutor.reference.ReferenceBook`

            """
            link = self.find_element(*self._browse_the_book_link_locator)
            Utility.switch_to(self.driver, element=link)
            return go_to_(
                ReferenceBook(self.driver, base_url=self.page.page.base_url))

        @property
        def sections(self) -> List[SectionSelector.Chapter.Section]:
            """Access the chapter sections.

            :return: the list of chapter sections
            :rtype: list(:py:class:`~SectionSelector.Chapter.Section`)

            """
            return [self.Section(self, section)
                    for section in self.find_elements(*self._section_locator)]

        class Section(Region):
            """A book section within a chapter."""

            _section_checkbox_locator = (By.CSS_SELECTOR, '[type=checkbox]')
            _section_number_locator = (By.CSS_SELECTOR, '.chapter-section')
            _section_title_locator = (By.CSS_SELECTOR, '.section-title')

            def select(self) -> SectionSelector:
                """Click on the section check box.

                :return: the book section selector
                :rtype: :py:class:`SectionSelector`

                """
                checkbox = self.find_element(*self._section_checkbox_locator)
                Utility.click_option(self.driver, element=checkbox)
                sleep(0.75)
                return self.page.page

            @property
            def checked(self) -> bool:
                """Return True if the checkbox is selected.

                :return: ``True`` if the section checkbox is checked and
                    ``False`` if it is not
                :rtype: bool

                """
                return 'checked' in self.root.get_attribute('class')

            @property
            def is_unnumbered(self) -> bool:
                """Return True if the section is not numbered.

                :return: ``True`` if the section does not have a section
                    number, ``False`` if it does
                :rtype: bool

                """
                return bool(self.find_elements(*self._section_number_locator))

            @property
            def number(self) -> str:
                """Return the section number.

                :return: the section number if it exists or an empty string if
                    it does not exist
                :rtype: str

                """
                if self.is_unnumbered:
                    return ''
                return self.find_element(*self._section_number_locator).text

            @property
            def title(self) -> str:
                """Return the section title.

                :return: the section title
                :rtype: str

                """
                return self.find_element(*self._section_title_locator).text


class ExerciseSelector(Region):
    """A section-grouped exercise selector and display."""

    _book_section_locator = (By.CSS_SELECTOR, '.exercise-sections')

    _secondary_toolbar_root_selector = '.exercise-controls-bar'

    @property
    def toolbar(self) -> ExerciseSelector.Toolbar:
        """Access the secondary toolbar buttons for exercise selection.

        :return: the exercise selection toolbar
        :rtype: :py:class:`~ExerciseSelector.Toolbar`

        """
        toolbar_root = self.driver.execute_script(
            'return document.querySelector("{0}");'
            .format(self._secondary_toolbar_root_selector))
        return self.Toolbar(self, toolbar_root)

    @property
    def sections(self) -> List[ExerciseSelector.BookSection]:
        """Access the book sections within the assessment selector pane.

        :return: the list of book sections that have available assessments
        :rtype: list(:py:class:`ExerciseSelector.BookSection`)

        """
        return [self.BookSection(self, section)
                for section in self.find_elements(*self._book_section_locator)]

    class Toolbar(Region):
        """The assessment selection toolbar."""

        _previous_section_arrow_locator = (By.CSS_SELECTOR, '.prev')
        _sections_list_locator = (By.CSS_SELECTOR, '.section')
        _next_section_arrow_locator = (By.CSS_SELECTOR, '.next')
        _total_problems_locator = (By.CSS_SELECTOR, '.num.total h2')
        _my_selections_locator = (By.CSS_SELECTOR, '.num.mine h2')
        _tutor_selections_locator = (By.CSS_SELECTOR, '.num.tutor h2')
        _more_tutor_selections_locator = (By.CSS_SELECTOR, '')
        _add_more_sections_button_locator = (
            By.CSS_SELECTOR, '.sectionizer ~ button')
        _exercise_selection_root_locator = (
            By.CSS_SELECTOR, '.homework-plan-exercise-select-topics')

        def previous_section(self) -> ExerciseSelector:
            """Click on the previous section left arrow.

            :return: the exercise selector with the previous section displayed
                if the arrow is not inactive
            :rtype: :py:class:`ExerciseSelector`

            """
            button = self.find_element(*self._previous_section_arrow_locator)
            if 'disabled' not in button.get_attribute('class'):
                Utility.click_option(self.driver, element=button)
            return self.page

        def next_section(self) -> ExerciseSelector:
            """Click on the next section right arrow.

            :return: the exercise selector with the subsequent section
                displayed if the arrow is not inactive
            :rtype: :py:class:`ExerciseSelector`

            """
            button = self.find_element(*self._next_section_arrow_locator)
            if 'disabled' not in button.get_attribute('class'):
                Utility.click_option(self.driver, element=button)
            return self.page

        @property
        def sections(self) -> List[ExerciseSelector.Toolbar.Section]:
            """Return the list of available section buttons.

            :return: the list of currently displayed sections that have at
                least one available assessment
            :rtype: list(:py:class:`~ExerciseSelector.Toolbar.Section`)

            """
            return [self.Section(self, section)
                    for section
                    in self.find_elements(*self._sections_list_locator)]

        @property
        def total_problems(self) -> int:
            """Return the total number of problems selected.

            Return the total number of assessments selected for this
            assignment (My Selections + Tutor Selections).

            :return: the total number of selected problems
            :rtype: int

            """
            return int(self.find_element(*self._total_problems_locator).text)

        @property
        def my_selections(self) -> int:
            """Return the number of user-selected problems.

            Return the number of assessments selected by the teacher for this
            assignment.

            :return: the number of user-selected problems
            :rtype: int

            """
            return int(self.find_element(*self._my_selections_locator).text)

        @property
        def tutor_selections(self) -> int:
            """Return the number of Tutor-selected problems.

            Return the number of assessments selected by Tutor for this
            assignment.

            :return: the number of Tutor-selected problems
            :rtype: int

            """
            return int(self.find_element(*self._tutor_selections_locator).text)

        def fewer_tutor_selections(self) -> ExerciseSelector:
            """Click the down arrow to reduce the number of Tutor questions.

            :return: the exercise selector
            :rtype: :py:class:`ExerciseSelector`

            """
            try:
                button = self.find_element(
                    *self._fewer_tutor_selections_locator)
                Utility.click_option(self.driver, element=button)
            except NoSuchElementException:
                # cannot have fewer than zero (0) Tutor-selected problems
                pass
            return self.page

        def more_tutor_selections(self) -> ExerciseSelector:
            """Click the up arrow to increase the number of Tutor questions.

            :return: the exercise selector
            :rtype: :py:class:`ExerciseSelector`

            """
            try:
                button = self.find_element(
                    *self._more_tutor_selections_locator)
                Utility.click_option(self.driver, element=button)
            except NoSuchElementException:
                # cannot have more than four (4) Tutor-selected problems
                pass
            return self.page

        def what_are_these(self) -> HomeworkTutorSelectionsTooltip:
            """Click on the 'What are these?' link.

            :return: the Tutor-selected problem explanation tooltip
            :rtype: :py:class:`HomeworkTutorSelectionsTooltip`

            """
            link = self.find_element(*self._what_are_these_link_locator)
            Utility.click_option(self.driver, element=link)
            return HomeworkTutorSelectionsTooltip(self.page)

        def add_more_sections(self) -> SectionSelector:
            """Click on the '+ Add More Sections' button.

            :return: the book section selector
            :rtype: :py:class:`SectionSelector`

            """
            button = self.find_element(*self._add_more_sections_button_locator)
            Utility.click_option(self.driver, element=button)
            sleep(1)
            selection_root = self.find_element(
                *self._exercise_selection_root_locator)
            return SectionSelector(self.page.page, selection_root)

        class Section(Region):
            """A selected book section button in the toolbar."""

            @property
            def number(self) -> str:
                """Return the section number.

                :return: the section number
                :rtype: str

                """
                return self.root.text

            @property
            def is_active(self) -> bool:
                """Return True if the section is currently displayed.

                :return: ``True`` if the section or its assessments are
                    currently displayed in the main window
                :rtype: bool

                """
                return 'active' in self.root.get_attribute('class')

            def select(self) -> ExerciseSelector:
                """Click on the section number button.

                :return: the exercise selector with the section displayed in
                    the main window
                :rtype: :py:class:`ExerciseSelector`

                """
                Utility.click_option(self.driver, element=self.root)
                return self.page.page

    class BookSection(Region):
        """All assessments within a specific book section."""

        _section_number_locator = (By.CSS_SELECTOR, '.chapter-section')
        _section_title_locator = (By.CSS_SELECTOR, '.exercises-section-label')
        _assessment_card_locator = (By.CSS_SELECTOR, '.exercise-card')

        @property
        def number(self) -> str:
            """Return the section number including the chapter.

            :return: the section number
            :rtype: str

            """
            return self.find_element(*self._section_number_locator).text

        @property
        def title(self) -> str:
            """Return the section title.

            :return: the section title
            :rtype: str

            """
            return self.find_element(*self._section_title_locator).text

        @property
        def assessments(self) -> List[Assessment]:
            """Access the available assessments within the book section.

            :return: the list of assessments available within the section
            :rtype: list(:py:class:`Assessment`)

            """
            return [Assessment(self, exercise)
                    for exercise
                    in self.find_elements(*self._assessment_card_locator)]


class ExerciseTableReview(Region):
    """The exercise selection review."""

    _total_problems_locator = (By.CSS_SELECTOR, '.total h2')
    _my_selections_locator = (By.CSS_SELECTOR, '.mine h2')
    _tutor_selections_locator = (By.CSS_SELECTOR, '.tutor-selections h2')
    _fewer_tutor_selections_locator = (
        By.CSS_SELECTOR, '.ox-icon-chevron-down')
    _more_tutor_selections_locator = (
        By.CSS_SELECTOR, '.ox-icon-chevron-up')
    _what_are_these_link_locator = (
        By.CSS_SELECTOR, '#homework-selections-trigger')
    _add_more_sections_button_locator = (By.CSS_SELECTOR, '.add-sections')
    _question_overview_locator = (By.CSS_SELECTOR, '.exercise-table tbody tr')
    _assessment_card_locator = (By.CSS_SELECTOR, '.exercise-wrapper')

    @property
    def loaded(self) -> bool:
        """Wait until the loading animation is done.

        :return: ``True`` when the loading animation is not found, otherwise
            ``False``
        :rtype: bool

        """
        sleep(0.25)
        return self.execute_script(ANIMATION) is None

    @property
    def total_problems(self) -> int:
        """Return the total number of assignment problems selected.

        :return: the number of user-selected assessments plus the number of
            Tutor-selected assessments
        :rtype: int

        """
        return int(self.find_element(*self._total_problems_locator).text)

    @property
    def my_selections(self) -> int:
        """Return the number of user-selected assessments.

        :return: the number of user-selected assessments
        :rtype: int

        """
        return int(self.find_element(*self._my_selections_locator).text)

    @property
    def tutor_selections(self) -> int:
        """Return the number of Tutor-selected assessments.

        :return: the number of Tutor-selected assessments
        :rtype: int

        """
        return int(self.find_element(*self._tutor_selections_locator).text)

    def fewer_tutor_selections(self) -> ExerciseTableReview:
        """Click the down arrow to reduce the number of Tutor selections.

        :return: the assessment review table
        :rtype: :py:class:`ExerciseTableReview`

        """
        try:
            arrow_down = self.find_element(
                *self._fewer_tutor_selections_locator)
        except NoSuchElementException:
            raise TutorException(
                "Cannot have fewer than zero (0) Tutor-selected assessments")
        Utility.click_option(self.driver, element=arrow_down)
        sleep(0.25)
        return self

    def more_tutor_selections(self) -> ExerciseTableReview:
        """Click the up arrow to increase the number of Tutor selections.

        :return: the assessment review table
        :rtype: :py:class:`ExerciseTableReview`

        """
        try:
            arrow_up = self.find_element(
                *self._more_tutor_selections_locator)
        except NoSuchElementException:
            raise TutorException(
                "Cannot have more than four (4) Tutor-selected assessments")
        Utility.click_option(self.driver, element=arrow_up)
        sleep(0.25)
        return self

    def what_are_these(self) -> HomeworkTutorSelectionsTooltip:
        """Click the 'What are these?' link.

        :return: the homework Tutor selections explanation tooltip
        :rtype: :py:class:`HomeworkTutorSelectionsTooltip`

        """
        link = self.find_element(*self._what_are_these_link_locator)
        Utility.click_option(self.driver, element=link)
        sleep(0.25)
        return HomeworkTutorSelectionsTooltip(self)

    def add_more_sections(self) -> SectionSelector:
        """Click the '+ Add More Sections' button.

        :return: the homework section selector
        :rtype: :py:class:`SectionSelector`

        """
        button = self.find_element(*self._add_more_sections_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.25)
        return SectionSelector(self.page)

    @property
    def problem_questions(self) -> List[ExerciseTableReview.OverviewRow]:
        """Access the Problem Questions assessment overview table.

        :return: the overview table row data
        :rtype: list(:py:class:`~ExerciseTableReview.OverviewRow`)

        """
        return [self.OverviewRow(self, row)
                for row
                in self.find_elements(*self._question_overview_locator)]

    @property
    def cards(self) -> List[ExerciseTableReview.Assessment]:
        """Access the assessment cards in the assignment review.

        :return: the assessment cards
        :rtype: list(:py:class:`~ExerciseTableReview.Assessment`)

        """
        return [self.Assessment(self, card)
                for card
                in self.find_elements(*self._assessment_card_locator)]

    class OverviewRow(Region):
        """An exercise table assessment overview row."""

        _position_column_locator = (By.CSS_SELECTOR, 'td:nth-child(1)')
        _section_column_locator = (By.CSS_SELECTOR, 'td:nth-child(2)')
        _assessment_column_locator = (By.CSS_SELECTOR, 'td:nth-child(3)')
        _lo_column_locator = (By.CSS_SELECTOR, 'td:nth-child(4)')
        _details_column_locator = (By.CSS_SELECTOR, 'td:nth-child(5)')

        @property
        def position(self) -> int:
            """Return the assessment position within the table.

            :return: the position of the assessment within the review table
            :rtype: int

            """
            return int(self.find_element(*self._position_column_locator).text)

        @property
        def section(self) -> str:
            """Return the book section containing the assessment, if known.

            :return: the book section for known locations, an empty string for
                unaffiliated assessments, or a '-' for Tutor selections
            :rtype: str

            """
            return self.find_element(*self._section_column_locator).text

        @property
        def question(self) -> str:
            """Return the first question in the assessment.

            :return: the question stem for normal assessments or the first
                question stem for multipart assessments
            :rtype: str

            """
            return (self.find_element(*self._assessment_column_locator)
                    .get_attribute('textContent'))

        @property
        def learning_objective(self) -> str:
            """Return the learning objective tag.

            :return: the learning objective tag
            :rtype: str

            """
            return self.find_element(*self._lo_column_locator).text

        @property
        def details(self) -> str:
            """Return the addition detail tags.

            :return: assessment detail tags
            :rtype: str

            """
            return self.find_element(*self._details_column_locator).text

    class Assessment(Region):
        """An exercise review card."""

        _position_locator = (By.CSS_SELECTOR, '.exercise-number')
        _move_up_arrow_locator = (By.CSS_SELECTOR, '.-move-exercise-up')
        _move_down_arrow_locator = (By.CSS_SELECTOR, '.-move-exercise-down')
        _remove_exercise_locator = (By.CSS_SELECTOR, '.-remove-exercise')
        _multipart_stimulus_locator = (By.CSS_SELECTOR, '.stimulus')
        _question_locator = (By.CSS_SELECTOR, '.openstax-question')
        _exercise_tag_locator = (By.CSS_SELECTOR, '.exercise-tag')

        @property
        def position(self) -> int:
            """Return the position of the assessment in the assignment.

            :return: the position of the assessment within the homework
                assignment
            :rtype: int

            """
            return int(self.find_element(*self._position_locator).text)

        def move_up(self) -> ExerciseTableReview:
            """Move the selected assessment earlier in the assignment.

            .. note::

               If the assessment is in position 1, the move up arrow is not
               available.

            :return: the review table
            :rtype: :py:class:`ExerciseTableReview`

            """
            try:
                button = self.find_element(*self._move_up_arrow_locator)
                Utility.click_option(self.driver, element=button)
                sleep(0.25)
            except NoSuchElementException:
                pass
            return self.page

        def move_down(self) -> ExerciseTableReview:
            """Move the selected assessment later in the assignment.

            .. note::

               If the assessment is in the last position, the move down arrow
               is not available.

            :return: the review table
            :rtype: :py:class:`ExerciseTableReview`

            """
            try:
                button = self.find_element(*self._move_down_arrow_locator)
                Utility.click_option(self.driver, element=button)
                sleep(0.25)
            except NoSuchElementException:
                pass
            return self.page

        def remove(self) -> ExerciseTableReview:
            """Remove the assessment from the assignment.

            :return: the review table
            :rtype: :py:class:`ExerciseTableReview`

            """
            button = self.find_element(*self._remove_exercise_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.5)
            return self.page

        @property
        def stimulus(self) -> str:
            """Return the introductory stimulus for a multipart question.

            :return: the introductory stimulus if the assessment is a multi-
                part question, otherwise return an empty string
            :rtype: str

            """
            try:
                return (self.find_element(*self._multipart_stimulus_locator)
                        .get_attribute('textContent'))
            except NoSuchElementException:
                return ''

        @property
        def question(self) -> str:
            """Access the assessment(s).

            :return: the question or list of questions
            :rtype: :py:class:`~ExerciseTableReview.Assessment.Question` or
                list(:py:class:`~ExerciseTableReview.Assessment.Question`)

            """
            questions = self.find_elements(*self._question_locator)
            if len(questions) == 1:
                return self.Question(self, questions[0])
            return [self.Question(self, question)
                    for question in questions]

        @property
        def tags(self) -> Dict[str, str]:
            """Return the tag key/value pairs.

            :return: the group of tag key:value pairs
            :rtype: dict(str, str)

            """
            tags = {}
            for tag in self.find_elements(*self._exercise_tag_locator):
                key, value = tag.split(':', 1)
                tags[key] = value
            return tags

        class Question(Region):
            """An individual question within an assessment item."""

            _question_stem_locator = (By.CSS_SELECTOR, '.question-stem')
            _exercise_answer_locator = (By.CSS_SELECTOR, '.openstax-answer')
            _detailed_solution_locator = (By.CSS_SELECTOR, '.solution')
            _tutor_label_locator = (By.CSS_SELECTOR, '.openstax-answer label')

            @property
            def stem(self) -> str:
                """Return the exercise question stem.

                :return: the assessment question stem
                :rtype: str

                """
                return (self.find_element(*self._question_stem_locator)
                        .get_attribute('textContent'))

            @property
            def answers(self) \
                    -> List[ExerciseTableReview.OverviewRow.Question.Answer]:
                r"""Access the list of answers for the current question.

                :return: the list of answer options for the current assessment
                :rtype: list(:py:class:`~ExerciseTableReview.OverviewRow \
                                        .Question.Answer`)

                """
                return [self.Answer(self, answer)
                        for answer
                        in self.find_elements(*self._exercise_answer_locator)]

            @property
            def detailed_solution(self) -> str:
                """Return the detailed solution.

                :return: the detailed solution, if present
                :rtype: str

                """
                return (self.find_element(*self._detailed_solution_locator)
                        .get_attribute('textContent'))

            @property
            def tutor_label(self) -> str:
                """Return the Tutor exercise reference number for the question.

                :return: the Tutor exercise reference ID for the question
                    within this assignment
                :rtype: str

                """
                return (self.find_element(*self._tutor_label_locator)
                        .get_attribute('for')
                        .split('-')[0])

            class Answer(Region):
                """An exercise answer."""

                _is_correct_locator = (
                    By.CSS_SELECTOR, '.correct-incorrect svg')
                _answer_letter_locator = (By.CSS_SELECTOR, '.answer-letter')
                _answer_content_locator = (By.CSS_SELECTOR, '.answer-content')

                @property
                def is_correct(self) -> bool:
                    """Return True if the answer is correct.

                    :return: ``True`` if the answer is correct, ``False`` if it
                        is incorrect
                    :rtype: bool

                    """
                    return bool(self.find_elements(*self._is_correct_locator))

                @property
                def letter(self) -> str:
                    """Return the answer letter.

                    :return: the letter representing the answer
                    :rtype: str

                    """
                    return self.find_element(*self._answer_letter_locator).text

                @property
                def answer(self) -> str:
                    """Return the answer content.

                    .. note::

                       The content may not be clear when the answer includes
                       LaTeX.

                    :return: the answer text including sub-elements
                    :rtype: str

                    """
                    return (self.find_element(*self._answer_content_locator)
                            .get_attribute('textContent'))


# -------------------------------------------------------- #
# Assignment shared properties
# -------------------------------------------------------- #

class Assignment(TutorBase):
    """An assignment creation or modification."""

    _assignment_heading_locator = (By.CSS_SELECTOR, '.card-header span')
    _close_x_locator = (By.CSS_SELECTOR, '.card-header .openstax-close-x')

    _assignment_name_locator = (
        By.CSS_SELECTOR, '#reading-title')
    _assignment_name_description_locator = (
        By.CSS_SELECTOR, '#reading-title ~ div .instructions')
    _assignment_name_required_locator = (
        By.CSS_SELECTOR, '#reading-title ~ .hint')

    _description_locator = (
        By.CSS_SELECTOR, '.assignment-description textarea')
    _description_required_locator = (
        By.CSS_SELECTOR, '.assignment-description .hint')

    _change_timezone_locator = (By.CSS_SELECTOR, '.course-time-zone')
    _current_timezone_locator = (By.CSS_SELECTOR, '.course-time-zone span')

    _assign_to_all_sections_locator = (By.CSS_SELECTOR, '#hide-periods-radio')
    _assign_by_section_locator = (By.CSS_SELECTOR, '#show-periods-radio')
    _all_sections_tasking_plan_locator = (
        By.CSS_SELECTOR, '.tasking-date-times')
    _section_tasking_plan_locator = (
        By.CSS_SELECTOR, '.tasking-plan')
    _tasking_date_time_error_locator = (
        By.CSS_SELECTOR, '.tasking-date-times .hint')

    # ---------------------------------------------------- #
    # Heading
    # ---------------------------------------------------- #

    @property
    def title(self) -> str:
        """Return the current card title.

        :return: the assignment creation or modification title
        :rtype: str

        """
        return self.find_element(*self._assignment_heading_locator).text

    def close(self) -> Calendar:
        """Click on the card 'x' button.

        :return: the instructor's calendar
        :rtype: :py:class:`~pages.tutor.calendar.Calendar`

        """
        button = self.find_element(*self._close_x_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.25)
        confirm = self.driver.execute_script(GET_ROOT.format('dialog'))
        if confirm:
            unsaved_changes = CancelConfirm(self, confirm)
            unsaved_changes.yes()
            sleep(0.25)
        return go_to_(Calendar(self.driver, base_url=self.base_url))

    # ---------------------------------------------------- #
    # Body
    # ---------------------------------------------------- #

    @property
    def name(self) -> str:
        """Return the current assignment name.

        :return: the current value in the assignment name field
        :rtype: str

        """
        return (self.find_element(*self._assignment_name_locator)
                .get_attribute('value'))

    @name.setter
    def name(self, assignment_name: str) -> None:
        """Set the assignment name.

        :param str assignment_name: the new assignment name
        :return: None

        """
        name_box = self.find_element(*self._assignment_name_locator)
        if name_box.get_attribute('value'):
            Utility.clear_field(self.driver, field=name_box)
        name_box.send_keys(assignment_name)

    @property
    def name_description(self) -> str:
        """Return the field descriptor.

        :return: the additional field descriptor text
        :rtype: str

        """
        return (self.find_element(*self._assignment_name_description_locator)
                .text)

    @property
    def name_error(self) -> str:
        """Return the name error text.

        :return: the name field error text
        :rtype: str

        """
        return self.find_element(*self._assignment_name_required_locator).text

    @property
    def description(self) -> str:
        """Return the current assignment description.

        :return: the current value in the assignment description field
        :rtype: str

        """
        return self.find_element(*self._description_locator).text

    @description.setter
    def description(self, description: str) -> None:
        """Set the assignment description.

        :param str description: the new assignment description
        :return: None

        """
        description_box = self.find_element(*self._description_locator)
        if description_box.get_attribute('textContent'):
            Utility.clear_field(self.driver, field=description_box)
        description_box.send_keys(description)

    @property
    def description_error(self) -> str:
        """Return the description error text.

        :return: the description field error text
        :rtype: str

        """
        return self.find_element(*self._description_required_locator).text

    @property
    def timezone(self) -> str:
        """Return the current timezone.

        :return: the course's assigned timezone
        :rtype: str

        """
        return self.find_element(*self._current_timezone_locator).text

    def change_timezone(self) -> CourseSettings:
        """Click on the current course timezone.

        :return: the course settings page
        :rtype: :py:class:`~pages.tutor.settings.CourseSettings`

        """
        link = self.find_element(*self._change_timezone_locator)
        Utility.click_option(self.driver, element=link)
        return go_to_(CourseSettings(self.driver, base_url=self.base_url))

    def all_sections(self) -> Assignment:
        """Click on the 'All Sections' radio button.

        :return: the current page
        :rtype: :py:class:`Assignment`

        """
        radio_option = self.find_element(*self._assign_to_all_sections_locator)
        Utility.click_option(self.driver, element=radio_option)
        sleep(0.25)
        return self

    def individual_sections(self) -> Assignment:
        """Click on the 'Individual Sections' radio button.

        :return: the current page
        :rtype: :py:class:`Assignment`

        """
        radio_option = self.find_element(*self._assign_by_section_locator)
        Utility.click_option(self.driver, element=radio_option)
        sleep(0.25)
        return self

    @property
    def open_and_due(self) \
            -> Union[OpenToClose, List[Assignment.SectionOpenToClose]]:
        """Access the open and due dates and times.

        :return: the all sections open and due dates and times or the list of
            sections and their open and due dates and times
        :rtype: :py:class:`OpenToClose` or
            list(:py:class:`~Assignment.SectionOpenToClose`)

        """
        sections = self.find_elements(*self._section_tasking_plan_locator)
        if sections:
            return [self.SectionOpenToClose(self, section)
                    for section in sections]
        all_sections = self.find_element(
            *self._all_sections_tasking_plan_locator)
        return OpenToClose(self, all_sections)

    @property
    def errors(self) -> List[str]:
        """Return any error messages.

        :return: a list of error messages
        :rtype: list(str)

        """
        errors = []
        name = self.find_elements(*self._assignment_name_required_locator)
        if name and self.driver.execute_script(DISPLAYED, name[0]):
            errors.append('Name: {0}'.format(name[0].text))
        description = self.find_elements(*self._description_required_locator)
        if description and self.driver.execute_script(DISPLAYED,
                                                      description[0]):
            errors.append('Description: {0}'.format(description[0].text))
        date_time_errors = (
            self.find_elements(*self._tasking_date_time_error_locator))
        for issue in date_time_errors:
            if self.driver.execute_script(DISPLAYED, issue):
                errors.append('DateTime: {0}'.format(issue.text))
        return errors

    class SectionOpenToClose(Region):
        """Open and due dates and times for a particular course section."""

        _section_checkbox_locator = (By.CSS_SELECTOR, '[type=checkbox]')
        _section_id_locator = (By.CSS_SELECTOR, '.period')
        _open_date_time_locator = (By.CSS_SELECTOR, '.tasking-date-times')

        @property
        def section(self) -> str:
            """Return the section name.

            :return: the section name
            :rtype: str

            """
            return self.find_element(*self._section_id_locator).text

        def select(self) -> Assignment:
            """Click on the section checkbox.

            :return: the assignment page
            :rtype: :py:class:`Assignment`

            """
            checkbox = self.find_element(*self._section_checkbox_locator)
            Utility.click_option(self.driver, element=checkbox)
            sleep(0.25)
            return self.page

        @property
        def checked(self) -> bool:
            """Return True if the section checkbox is checked.

            :return: ``True`` if the checkbox is checked, otherwise ``False``
            :rtype: bool

            """
            checkbox = self.find_element(*self._section_checkbox_locator)
            return self.driver.execute_script(
                'return arguments[0].checked;', checkbox)

        @property
        def open_to_close(self) -> OpenToClose:
            """Access the open and due dates and times.

            :return: the date and time controls for the section
            :rtype: :py:class:`OpenToClose`

            """
            datetime_root = self.find_element(*self._open_date_time_locator)
            return OpenToClose(self, datetime_root)


# -------------------------------------------------------- #
# Assignments
# -------------------------------------------------------- #

class Event(Assignment):
    """An event creation or modification."""

    pass


class External(Assignment):
    """An external assignment creation or modification."""

    _assignment_url_locator = (
        By.CSS_SELECTOR, '#external-url')
    _assignment_url_required_locator = (
        By.CSS_SELECTOR, '#external-url ~ .hint')

    @property
    def assignment_url(self) -> str:
        """Return the current URL value.

        :return: the current assignment URL
        :rtype: str

        """
        return (self.find_element(*self._assignment_url_locator)
                .get_attribute('value'))

    @assignment_url.setter
    def assignment_url(self, url: str) -> External:
        """Set the assignment URL.

        :param str url: the new assignment URL
        :return: the assignment wizard
        :rtype: :py:class:`External`

        """
        url_input = self.find_element(*self._assignment_url_locator)
        if self.assignment_url:
            Utility.clear_field(self.driver, field=url_input)
            sleep(0.25)
        url_input.send_keys(url)
        sleep(0.25)
        return self.page

    @property
    def url_error(self) -> str:
        """Return the assignment URL error text.

        :return: the assignment URL field error text
        :rtype: str

        """
        return self.find_element(*self._assignment_url_required_locator).text

    @property
    def errors(self) -> List[str]:
        """Return any error messages.

        :return: a list of error messages
        :rtype: list(str)

        """
        errors = super().errors()
        url = self.find_elements(*self._assignment_url_required_locator)
        if url and self.driver.execute_script(DISPLAYED, url[0]):
            errors.append('URL: {0}'.format(url[0].text))
        return errors


class Homework(Assignment):
    """A homework assignment creation or modification."""

    _feedback_select_menu_locator = (By.CSS_SELECTOR, '#feedback-select')
    _select_problems_button_locator = (By.CSS_SELECTOR, '#problem-select')
    _problems_required_locator = (By.CSS_SELECTOR, '.problems-required')
    _homework_plan_root_locator = (
        By.CSS_SELECTOR, '.homework-plan-select-topics')
    _what_do_students_see_button_locator = (By.CSS_SELECTOR, '.preview-btn')

    def select_problems(self) -> SectionSelector:
        """Click on the 'Select Problems' button.

        :return: the section selector
        :rtype: :py:class:`SectionSelector`

        """
        button = self.find_element(*self._add_readings_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(1)
        selector_root = self.find_element(*self._reading_plan_root_locator)
        return SectionSelector(self, selector_root)

    @property
    def problem_error(self) -> str:
        """Return the questions required error message.

        :return: the questions required field error text
        :rtype: str

        """
        return self.find_element(*self._readings_required_locator).text

    @property
    def errors(self) -> List[str]:
        """Return any error messages.

        :return: a list of error messages
        :rtype: list(str)

        """
        errors = super().errors()
        url = self.find_elements(*self._readings_required_locator)
        if url and self.driver.execute_script(DISPLAYED, url[0]):
            errors.append('Readings: {0}'.format(url[0].text))
        return errors

    def what_do_students_see(self) -> StudentPreview:
        """Click the 'What do students see?' button.

        :return: the student preview video pop up
        :rtype: :py:class:`~pages.tutor.preview.StudentPreview`

        """
        button = self.find_element(*self._what_do_students_see_button_locator)
        Utility.switch_to(self.driver, element=button)
        return StudentPreview(self.driver)


class Reading(Assignment):
    """A reading assignment creation or modification."""

    _selected_reading_list_locator = (
        By.CSS_SELECTOR, '.selected-reading-list .selected-section')
    _readings_required_locator = (By.CSS_SELECTOR, '.readings-required')
    _add_readings_button_locator = (
        By.CSS_SELECTOR, '#reading-select')
    _reading_plan_root_locator = (
        By.CSS_SELECTOR, '.reading-plan-select-topics')
    _see_questions_tooltip_locator = (
        By.CSS_SELECTOR, '#reading-select ~ button')
    _what_do_students_see_button_locator = (By.CSS_SELECTOR, '.preview-btn')

    @property
    def reading_list(self) -> List[Reading.ReadingSelection]:
        """Access the selected readings list.

        :return: a list of reading sections for the assignment
        :rtype: list(:py:class:`~Reading.ReadingSelection`)

        """
        return [self.ReadingSelection(self, item)
                for item
                in self.find_elements(*self._selected_reading_list_locator)]

    def add_readings(self) -> SectionSelector:
        """Click on the 'Add Readings' button.

        :return: the section selector
        :rtype: :py:class:`SectionSelector`

        """
        button = self.find_element(*self._add_readings_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(1)
        selector_root = self.find_element(*self._reading_plan_root_locator)
        return SectionSelector(self, selector_root)

    @property
    def readings_error(self) -> str:
        """Return the readings required error message.

        :return: the readings required field error text
        :rtype: str

        """
        return self.find_element(*self._readings_required_locator).text

    @property
    def errors(self) -> List[str]:
        """Return any error messages.

        :return: a list of error messages
        :rtype: list(str)

        """
        errors = super().errors()
        url = self.find_elements(*self._readings_required_locator)
        if url and self.driver.execute_script(DISPLAYED, url[0]):
            errors.append('Readings: {0}'.format(url[0].text))
        return errors

    def why_cant_i_see_the_questions(self) -> ReadingQuestionTooltip:
        """Click on the 'see the questions' FAQ question link.

        :return: the reading question FAQ tooltip
        :rtype: :py:class:`ReadingQuestionTooltip`

        """
        link = self.find_element(*self._see_questions_tooltip_locator)
        Utility.click_option(self.driver, element=link)
        sleep(0.25)
        return ReadingQuestionTooltip(self)

    def what_do_students_see(self) -> StudentPreview:
        """Click the 'What do students see?' button.

        :return: the student preview video pop up
        :rtype: :py:class:`~pages.tutor.preview.StudentPreview`

        """
        button = self.find_element(*self._what_do_students_see_button_locator)
        Utility.switch_to(self.driver, element=button)
        return StudentPreview(self.driver)

    class ReadingSelection(Region):
        """The reading order list."""

        _chapter_section_number_locator = (By.CSS_SELECTOR, '.chapter-section')
        _selection_title_locator = (By.CSS_SELECTOR, '.section-title')
        _move_up_arrow_locator = (By.CSS_SELECTOR, '.arrow-up')
        _move_down_arrow_locator = (By.CSS_SELECTOR, '.arrow-down')
        _delete_section_locator = (By.CSS_SELECTOR, '.close')

        @property
        def number(self) -> str:
            """Return the section number.

            :return: the chapter and section number for the reading
            :rtype: str

            """
            return (self.find_element(*self._chapter_section_number_locator)
                    .text)

        @property
        def title(self) -> str:
            """Return the section title.

            :return: the section title
            :rtype: str

            """
            return self.find_element(*self._selection_title_locator).text

        def move_up(self) -> Reading.ReadingSelection:
            """Move the section higher in the reading order, if possible.

            :return: the reading selection pane
            :rtype: :py:class:`~Reading.ReadingSelection`

            """
            try:
                button = self.find_element(*self._move_up_arrow_locator)
                Utility.click_option(self.driver, element=button)
                sleep(0.25)
            except NoSuchElementException:
                pass
            return self

        def move_down(self) -> Reading.ReadingSelection:
            """Move the section later in the reading order, if possible.

            :return: the reading selection pane
            :rtype: :py:class:`~Reading.ReadingSelection`

            """
            try:
                button = self.find_element(*self._move_down_arrow_locator)
                Utility.click_option(self.driver, element=button)
                sleep(0.25)
            except NoSuchElementException:
                pass
            return self

        def delete(self) -> Reading.ReadingSelection:
            """Remove the section from the reading assignment.

            :return: the reading selection pane
            :rtype: :py:class:`~Reading.ReadingSelection`

            """
            button = self.find_element(*self._delete_section_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.5)
            return self
