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
from utils.tutor import Tutor, TutorException, get_date_times
from utils.utilities import Utility, go_to_

# -------------------------------------------------------- #
# Javascript page requests
# -------------------------------------------------------- #

# return True if the field error message is displayed
DISPLAYED = 'return getComputedStyle(arguments[0]).display != "none";'
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

    _section_name_locator = (By.CSS_SELECTOR, '.period')
    _section_checkbox_locator = (By.CSS_SELECTOR, '[type=checkbox]')
    _open_date_locator = (
        By.CSS_SELECTOR, '.-assignment-open-date input:not([readonly])')
    _open_time_locator = (
        By.CSS_SELECTOR, '.-assignment-open-time input')
    _due_date_locator = (
        By.CSS_SELECTOR, '.-assignment-due-date input:not([readonly])')
    _due_time_locator = (
        By.CSS_SELECTOR, '.-assignment-due-time input')

    @property
    def name(self) -> str:
        """Return the section name.

        :return: the section name
        :rtype: str

        """
        return (self.find_element(*self._section_name_locator)
                .get_attribute('textContent'))

    @property
    def checkbox(self) -> WebElement:
        """Return the section checkbox.

        :return: the section checkbox
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._section_checkbox_locator)

    @property
    def is_checked(self) -> bool:
        """Return True if the section checkbox is currently checked.

        :return: ``True`` if the section checkbox is checked, otherwise
            ``False``
        :rtype: bool

        """
        return self.driver.execute_script(
            'return arguments[0].checked == "true";', self.checkbox)

    def toggle(self) -> None:
        """Click on the section checkbox.

        :return: None

        """
        Utility.click_option(self.driver, element=self.checkbox)

    @property
    def open_date(self) -> WebElement:
        """Return the 'Open Date' input box.

        :return: the open date input box
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._open_date_locator)

    @property
    def open_time(self) -> WebElement:
        """Return the 'Open Time' input box.

        :return: the open time input box
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._open_time_locator)

    @property
    def due_date(self) -> WebElement:
        """Return the 'Due Date' input box.

        :return: the due date input box
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._due_date_locator)

    @property
    def due_time(self) -> WebElement:
        """Return the 'Due Time' input box.

        :return: the due time input box
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._due_time_locator)

    def set(self, open_on: str, open_at: str, due_on: str, due_at: str) \
            -> None:
        """Set the open and close dates/times.

        :param str open_on: a ``MM/DD/YYYY`` date to open the assignment
        :param str open_at: a ``hh:mm xm`` time to open the assignment
        :param str due_on: a ``MM/DD/YYYY`` date the assignment is due
        :param str due_at: a ``hh:mm xm`` time the assignment is due
        :return: None

        """
        self._set_field(self.open_date, open_on)
        self._set_field(self.open_time, open_at)
        self._set_field(self.due_date, due_on)
        self._set_field(self.due_time, due_at)

    def _set_field(self, field: WebElement, value: str) -> None:
        r"""Set the requested form field to the new value.

        :param field: the form field to modify
        :param str value: the new field value
        :type field: :py:class:`~selenium.webdriver.remote \
                                .webelement.WebElement`
        :return: None

        """
        if not value:
            # No value was given so skip over the field (generally time values)
            return
        Utility.click_option(self.driver, element=field)
        # Clear the field first to prevent data appends
        field.send_keys(Keys.DELETE)
        for _ in range(len(field.get_attribute('value'))):
            field.send_keys(Keys.BACKSPACE)
        sleep(0.25)
        # Send the letters/numbers individually to deal with the form
        # validation controls
        for char in value:
            field.send_keys(char)
        sleep(0.25)


class SectionSelector(Region):
    """A chapter and section selector for readings and homeworks."""

    _title_locator = (By.CSS_SELECTOR, '.card-header')
    _close_x_locator = (By.CSS_SELECTOR, '.close')
    _chapter_locator = (By.CSS_SELECTOR, '.chapter')
    _section_locator = (By.CSS_SELECTOR, '[data-section-id]')
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
        return self.driver.execute_script(ANIMATION) is None

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

    @property
    def sections(self) -> List[SectionSelector.Chapter.Section]:
        r"""Access the individual book sections.

        :return: the list of book sections ignoring the chapters
        :rtype: list(:py:class:`~pages.tutor.assignment \
                                .SectionSelector.Chapter.Section`)

        """
        return [self.Chapter.Section(self, section)
                for section in self.find_elements(*self._section_locator)]

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
        return ExerciseSelector(self.page, selector_root)

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
            return 'unchecked' not in checkbox.get_attribute('class')

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
                visibility = (self.root.find_element(By.XPATH, './..')
                              .get_attribute('class'))
                if 'show' not in visibility:
                    chapter_bar = self.root.find_element(By.XPATH, './../..')
                    Utility.click_option(self.driver, element=chapter_bar)
                    sleep(0.4)
                checkbox = self.find_element(*self._section_checkbox_locator)
                Utility.click_option(self.driver, element=checkbox)
                sleep(0.75)
                # if viewing the section of a chapter, return the chapter's
                # parent page
                if isinstance(self.page, Region):
                    return self.page.page
                # if viewing the section individually, return the immediate
                # parent
                return self.page

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
                return not bool(self.find_elements(
                    *self._section_number_locator))

            @property
            def number(self) -> str:
                """Return the section number.

                :return: the section number if it exists, chapter number plus
                    '.0' if it is an introductory section, or an empty string
                    if it does not exist for an end-of-chapter object
                :rtype: str

                """
                if self.is_unnumbered:
                    if 'Introduction to' in self.title:
                        chapter_number = (
                            self.find_element(By.XPATH, './../..')
                            .find_element(By.CSS_SELECTOR, 'div:first-child')
                            .get_attribute('data-chapter-section'))
                        return f'{chapter_number}.0'
                    return ''
                return (self.find_element(*self._section_number_locator)
                        .get_attribute('textContent')
                        .strip())

            @property
            def title(self) -> str:
                """Return the section title.

                :return: the section title
                :rtype: str

                """
                return (self.find_element(*self._section_title_locator)
                        .get_attribute('textContent')
                        .strip())


class ExerciseSelector(Region):
    """A section-grouped exercise selector and display."""

    _book_section_locator = (By.CSS_SELECTOR, '.exercise-sections')

    _secondary_toolbar_root_selector = '.exercise-controls-bar'

    @property
    def loaded(self) -> bool:
        """Wait until the loading animation is done.

        :return: ``True`` when the loading animation is not found, otherwise
            ``False``
        :rtype: bool

        """
        sleep(0.25)
        return self.driver.execute_script(ANIMATION) is None

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
        _sections_list_locator = (By.CSS_SELECTOR, '.sectionizer .section')
        _next_section_arrow_locator = (By.CSS_SELECTOR, '.next')
        _total_problems_locator = (By.CSS_SELECTOR, '.num.total h2')
        _my_selections_locator = (By.CSS_SELECTOR, '.num.mine h2')
        _tutor_selections_locator = (By.CSS_SELECTOR, '.num.tutor h2')
        _more_tutor_selections_locator = (By.CSS_SELECTOR, '')
        _add_more_sections_button_locator = (
            By.CSS_SELECTOR, '.sectionizer ~ button')
        _exercise_selection_root_locator = (
            By.CSS_SELECTOR, '.homework-plan-exercise-select-topics')
        _next_button_locator = (By.CSS_SELECTOR, '.review-exercises')
        _cancel_button_locator = (By.CSS_SELECTOR, '.cancel-add')

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

        def next(self) -> Homework:
            """Click the 'Next' button.

            :return: the homework builder with the question review visible
            :rtype: :py:class:`~pages.tutor.assignment.Homework`

            """
            button = self.find_element(*self._next_button_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.3)
            return self.page.page

        def cancel(self) -> Homework:
            """Click the 'Cancel' button.

            :return: the homework builder
            :rtype: :py:class:`~pages.tutor.assignment.Homework`

            """
            button = self.find_element(*self._cancel_button_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.3)
            return self.page.page

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
        _include_assessment_locator = (
            By.CSS_SELECTOR, '.action.include , .action.exclude')
        _assessment_details_locator = (By.CSS_SELECTOR, '.action.details')

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

        def add_question(self) -> None:
            """Include the assessment in the selection.

            :return: None

            """
            self._selection_toggle('Add question')

        def remove_question(self) -> None:
            """Remove the assessment from the selection.

            :return: None

            """
            self._selection_toggle('Remove question')

        def _selection_toggle(self, option: str) -> None:
            """Add or remove an assessment from the selection.

            :param str option: the expected button content
            :return: None

            """
            button = self.find_element(*self._include_assessment_locator)
            if option == button.get_attribute('textContent'):
                Utility.click_option(self.driver, element=button)
            return

        def question_details(self) -> None:
            """View the assessment detailed card view.

            :return: the assessment card detailed view
            :rtype: QuestionDetails

            """
            button = self.find_element(*self._assessment_details_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.25)
            raise NotImplementedError()

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

    # Name
    _assignment_name_locator = (
        By.CSS_SELECTOR, '#reading-title')
    _assignment_name_description_locator = (
        By.CSS_SELECTOR, '#reading-title ~ div .instructions')
    _assignment_name_required_locator = (
        By.CSS_SELECTOR, '#reading-title ~ .hint')

    # Description
    _description_locator = (
        By.CSS_SELECTOR, '.assignment-description textarea')
    _description_required_locator = (
        By.CSS_SELECTOR, '.assignment-description .hint')

    # Timezone
    _change_timezone_locator = (
        By.CSS_SELECTOR, '.course-time-zone')
    _current_timezone_locator = (
        By.CSS_SELECTOR, '.course-time-zone span')

    # Section open and due dates and times
    _all_sections_radio_button_locator = (
        By.CSS_SELECTOR, '#hide-periods-radio')
    _all_sections_plan_locator = (
        By.CSS_SELECTOR, '.common')

    _individual_sections_radio_button_locator = (
        By.CSS_SELECTOR, '#show-periods-radio')
    _individual_sections_plan_locator = (
        By.CSS_SELECTOR, '.tasking-plan')
    _section_name_locator = (
        By.CSS_SELECTOR, '.period')
    _section_checkbox_locator = (
        By.CSS_SELECTOR, '[type=checkbox]')

    _tasking_date_time_error_locator = (
        By.CSS_SELECTOR, '.tasking-date-times .hint')

    # Assignment controls
    _publish_button_locator = (
        By.CSS_SELECTOR, '.-publish')
    _save_as_draft_button_locator = (
        By.CSS_SELECTOR, '.-save')
    _cancel_button_locator = (
        By.CSS_SELECTOR, '[data-tour-anchor-id*=cancel] button')
    _delete_button_locator = (
        By.CSS_SELECTOR, '.delete-assignment')

    @property
    def loaded(self) -> bool:
        """Return True when the assignment name field is found.

        :return: ``True`` when the assignment name field is located
        :rtype: bool

        """
        return bool(self.find_elements(*self._assignment_name_locator))

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
        radio_option = self.find_element(
            *self._all_sections_radio_button_locator)
        Utility.click_option(self.driver, element=radio_option)
        sleep(0.25)
        return self

    def individual_sections(self) -> Assignment:
        """Click on the 'Individual Sections' radio button.

        :return: the current page
        :rtype: :py:class:`Assignment`

        """
        radio_option = self.find_element(
            *self._individual_sections_radio_button_locator)
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
        sections = self.find_elements(*self._individual_sections_plan_locator)
        if sections:
            return [self.SectionOpenToClose(self, section)
                    for section in sections]
        all_sections = self.find_element(*self._all_sections_plan_locator)
        return OpenToClose(self, all_sections)

    def set_assignment_dates(self, data: dict) -> None:
        """Set the assignment open and close dates/times.

        :param dict data: the data package containing the section open and due
            date and time information
        :return: None

        """
        if Tutor.ALL in data:
            # override the rest of the data and use the 'All Sections' open/due
            open_on, open_at, due_on, due_at = get_date_times(
                self.driver, data.get(Tutor.ALL))
            # make sure all sections is selected
            self.all_sections()
            # set the dates and times
            self.open_and_due.set(open_on, open_at, due_on, due_at)

            return

        # Set each section
        self.individual_sections()

        for section in self.open_and_due:
            name = section.name
            if name not in data and section.is_checked:
                # uncheck the section and move on
                section.toggle()
                continue

            open_on, open_at, due_on, due_at = get_date_times(
                self.driver, data.get(name))
            # set the dates and times
            section.set(open_on, open_at, due_on, due_at)

    @property
    def errors(self) -> List[str]:
        """Return any error messages.

        :return: a list of error messages
        :rtype: list(str)

        """
        errors = []
        name = self.find_elements(*self._assignment_name_required_locator)
        if name:
            if self.driver.execute_script(DISPLAYED, name[0]):
                errors.append(f'Name: {name[0].text}')
        description = self.find_elements(*self._description_required_locator)
        if description:
            if self.driver.execute_script(DISPLAYED, description[0]):
                errors.append(f'Description: {description[0].text}')
        date_time_errors = (
            self.find_elements(*self._tasking_date_time_error_locator))
        for issue in date_time_errors:
            if self.driver.execute_script(DISPLAYED, issue):
                field = issue.find_element(
                    By.XPATH, '../div[@class="floating-label"]')
                errors.append(f'{field.text}: {issue.text}')
        return errors

    # ---------------------------------------------------- #
    # Footer
    # ---------------------------------------------------- #

    def publish(self) -> Calendar:
        """Click the 'Publish' assignment button.

        :return: the instructor's calendar
        :rtype: :py:class:`~pages.tutor.calendar.Calendar`

        """
        button = self.find_element(*self._publish_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.5)
        if self.errors:
            raise TutorException(f'Assignment error(s): {self.errors}')
        calendar = go_to_(Calendar(self.driver, self.base_url))
        calendar.wait.until(
            lambda _: not self.driver.find_elements(
                *calendar._is_publishing_locator))
        return calendar

    save = publish

    def save_as_draft(self) -> Calendar:
        """Click the 'Save as Draft' assignment button.

        :return: the instructor's calendar
        :rtype: :py:class:`~pages.tutor.calendar.Calendar`

        """
        name = self.name
        button = self.find_element(*self._save_as_draft_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.5)
        if self.errors:
            raise(TutorException(f'Assignment error(s): {self.errors}'))
        calendar = go_to_(Calendar(self.driver, self.base_url))
        calendar.wait.until(
            lambda _: (name in calendar.assignments(by_name=True) and
                       calendar.assignment(name).is_draft))
        return calendar

    def cancel(self) -> Calendar:
        """Click the 'Cancel' assignment button.

        :return: the instructor's calendar
        :rtype: :py:class:`~pages.tutor.calendar.Calendar`

        """
        raise NotImplementedError()

    def delete(self) -> Calendar:
        """Click the 'Delete' assignment button.

        :return: the instructor's calendar
        :rtype: :py:class:`~pages.tutor.calendar.Calendar`

        """
        raise NotImplementedError()

    # ---------------------------------------------------- #
    # Regions
    # ---------------------------------------------------- #

    class SectionOpenToClose(Region):
        """Open and due dates and times for a particular course section."""

        _section_checkbox_locator = (By.CSS_SELECTOR, '[type=checkbox]')
        _section_id_locator = (By.CSS_SELECTOR, '.period')
        _open_date_time_locator = (By.CSS_SELECTOR, '.tasking-date-times')

        @property
        def name(self) -> str:
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
            return OpenToClose(self, self.root)


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
        errors = super().errors
        url = self.find_elements(*self._assignment_url_required_locator)
        if url and self.driver.execute_script(DISPLAYED, url[0]):
            errors.append('URL: {0}'.format(url[0].text))
        return errors


class Homework(Assignment):
    """A homework assignment creation or modification."""

    _feedback_select_menu_locator = (By.CSS_SELECTOR, '#feedback-select')
    _select_problems_button_locator = (By.CSS_SELECTOR, '#problems-select')
    _problems_required_locator = (By.CSS_SELECTOR, '.problems-required')
    _homework_plan_root_locator = (
        By.CSS_SELECTOR, '.homework-plan-select-topics')
    _what_do_students_see_button_locator = (By.CSS_SELECTOR, '.preview-btn')

    def select_problems(self) -> SectionSelector:
        """Click on the 'Select Problems' button.

        :return: the section selector
        :rtype: :py:class:`SectionSelector`

        """
        button = self.find_element(*self._select_problems_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(1)
        selector_root = self.find_element(*self._homework_plan_root_locator)
        return SectionSelector(self, selector_root)

    def add_assessments_by(self,
                           chapters: Union[int, List[str], List[int]] = None,
                           sections: Union[int, List[str], List[float]] = None
                           ) -> List[str]:
        """Narrow assessment selection to certain chapters or sections.

        .. note:

            ``chapters`` and ``sections`` are exclusive; if ``chapters`` is
            set then ``sections`` is ignored

        :param chapters: a number of chapters or a list of specific chapters to
            select assessments from
        :param sections: a number of sections or a list of specific sections to
            select assessments from
        :type chapters: int or list(str) or list(int)
        :type sections: int or list(str) or list(float)
        :return: the list of chapters or sections selected as strings
        :rtype: list(str)

        """
        if chapters:
            # if chapters is set, ignore sections
            sections = None
        selector = self.select_problems()
        options = [option.number
                   for option
                   in (selector.chapters if chapters else selector.sections)]
        if isinstance(chapters, int) or isinstance(sections, int):
            # We need a random selection of chapters or sections so find a
            # random starting position that will keep us from running beyond
            # the end of the options list
            start = Utility.random(0, len(options) - (chapters or sections))
            selections = options[start:start + (chapters or sections)]
        else:
            selections = (chapters or sections)
        group = selector.chapters if chapters else selector.sections
        for selection in selections:
            try:
                # Get the position of a choice then click on its checkbox
                index = options.index(str(selection))
                group[index].select()
            except ValueError:
                raise TutorException(
                    f"{'Chapter' if chapters else 'Section'} " +
                    f'"{selection}" not a valid option')
            sleep(0.3)
        return selector.show_problems()

    @property
    def problem_error(self) -> str:
        """Return the questions required error message.

        :return: the questions required field error text
        :rtype: str

        """
        return self.find_element(*self._problems_required_locator).text

    @property
    def errors(self) -> List[str]:
        """Return any error messages.

        :return: a list of error messages
        :rtype: list(str)

        """
        errors = super().errors
        problems = self.find_elements(*self._problems_required_locator)
        if problems and self.driver.execute_script(DISPLAYED, problems[0]):
            errors.append('Problems: {0}'.format(problems[0].text))
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

    def add_readings_by(self,
                        chapters: Union[int, List[str], List[int]] = None,
                        sections: Union[int, List[str], List[float]] = None) \
            -> List[str]:
        """Add chapters or sections to a reading assignment.

        .. note:

            ``chapters`` and ``sections`` are exclusive; if ``chapters`` is
            set then ``sections`` is ignored

        :param chapters: a number of chapters or a list of specific chapters to
            add to the reading
        :param sections: a number of sections or a list of specific sections to
            add to the reading
        :type chapters: int or list(str) or list(int)
        :type sections: int or list(str) or list(float)
        :return: the list of chapters or sections selected as strings
        :rtype: list(str)

        """
        if chapters:
            # if chapters is set, ignore sections
            sections = None
        selector = self.add_readings()
        options = [option.number
                   for option
                   in (selector.chapters if chapters else selector.sections)]
        if isinstance(chapters, int) or isinstance(sections, int):
            # We need a random selection of chapters or sections so find a
            # random starting position that will keep us from running beyond
            # the end of the options list
            start = Utility.random(0, len(options) - (chapters or sections))
            selections = options[start:start + (chapters or sections)]
        else:
            selections = (chapters or sections)
        group = selector.chapters if chapters else selector.sections
        for selection in selections:
            try:
                # Get the position of a choice then click on its checkbox
                index = options.index(str(selection))
                group[index].select()
            except ValueError:
                raise TutorException(
                    f"{'Chapter' if chapters else 'Section'} " +
                    f'"{selection}" not a valid option')
            sleep(0.3)
        selector.add_readings()
        return [str(option) for option in selections]

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
        errors = super().errors
        readings = self.find_elements(*self._readings_required_locator)
        if readings and self.driver.execute_script(DISPLAYED, readings[0]):
            errors.append('Readings: {0}'.format(readings[0].text))
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
            number = (self.find_element(*self._chapter_section_number_locator)
                      .text)
            if 'Introduction to' in self.title:
                return f'{number}.0'
            return number

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
