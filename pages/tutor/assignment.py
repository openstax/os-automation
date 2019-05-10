"""The instructor's assignment control pages.

Add/Edit/Delete Event
Add/Edit/Delete External
Add/Edit/Delete Homework
Add/Edit/Delete Reading

"""

from time import sleep

from pypom import Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.tutor.base import TutorBase
from utils.tutor import TutorException
from utils.utilities import Utility, go_to_

# return True if the error message is displayed
DISPLAYED = 'return getComputedStyle(arguments[0]).display != none;'
# get the modal and tooltip root that is a neighbor of the React root element
GET_ROOT = 'return document.querySelector("[role={0}]");'


# -------------------------------------------------------- #
# Page dialog boxes and tooltips
# -------------------------------------------------------- #

class ButtonTooltip(Region):
    """The card button explanation tooltip."""

    _explanation_locator = (By.CSS_SELECTOR, 'p')

    @property
    def description(self):
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
    def title(self):
        """Return the dialog box title.

        :return: the modal title
        :rtype: str

        """
        return self.find_element(*self._modal_title_locator).text

    def close(self, no_button=False):
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
    def explanation(self):
        """Return the modal explanation text.

        :return: the modal explaining unsaved changes
        :rtype: str

        """
        return self.find_element(*self._explanation_locator).text

    def yes(self):
        """Click on the 'Yes' button.

        :return: the instructor's calendar
        :rtype: :py:class:`~pages.tutor.calendar.Calendar`

        """
        button = self.find_element(*self._yes_button_locator)
        Utility.click_option(self.driver, element=button)
        from pages.tutor.calendar import Calendar
        return go_to_(Calendar(self.driver, base_url=self.page.base_url))

    def no(self):
        """Click on the 'No' button.

        :return: the assignment page
        :rtype: :py:class:`Assignment`

        """
        return self.close(no_button=True)


class ReadingQuestionTooltip(ButtonTooltip):
    """The reading questions informational tooltip."""

    pass


# -------------------------------------------------------- #
# Assignment shared properties
# -------------------------------------------------------- #

class OpenToClose(Region):
    """The open and close dates and times rows."""

    _open_date_time_locator = (By.CSS_SELECTOR, '.col-md-6:nth-child(1)')
    _close_date_time_locator = (By.CSS_SELECTOR, '.col-md-6:nth-child(2)')

    @property
    def open(self):
        """Access the open date and time.

        :return: a date and time set
        :rtype: :py:class:`~OpenToClose.DateTime`

        """
        open_root = self.find_element(*self._open_date_time_locator)
        return self.DateTime(self, open_root)

    @property
    def close(self):
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
        def date(self):
            """Access the date field.

            :return: the date portion of a date time set
            :rtype: :py:class:`~OpenToClose.DateTime.Date`

            """
            date_root = self.find_element(*self._date_locator)
            return self.Date(self, date_root)

        @property
        def time(self):
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
                def current(self):
                    """Return the calendar's current month and year.

                    :return: the mini-calendar's month and year
                    :rtype: str

                    """
                    return self.find_element(*self._current_month_locator).text

                @property
                def year(self):
                    """Return the calendar year.

                    :return: the calendar year
                    :rtype: int

                    """
                    return int(self.find_element(*self._month_year_locator)
                               .get_attribute('aria-label')
                               .split('-')[1])

                @property
                def month(self):
                    """Return the calendar month.

                    :return: the calendar month as a number
                    :rtype: int

                    """
                    return int(self.find_element(*self._month_year_locator)
                               .get_attribute('aria-label')
                               .split('-')[2])

                def previous_month(self):
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

                def next_month(self):
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
                def days(self):
                    r"""Return the list of valid, selectable days.

                    :return: the days available for selection
                    :rtype: list(:py:class:`~selenium.webdriver.remote \
                                            .webelement.WebElement`)

                    """
                    return self.find_elements(*self._day_locator)

                def select(self, day):
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
            def label(self):
                """Return the floating label.

                :return: the floating input label
                :rtype: str

                """
                return self.find_element(*self._label_locator).text

            @property
            def time(self):
                """Return the currently assigned time.

                :return: the current value for the time input box
                :rtype: str

                """
                return (self.find_element(*self._current_time_locator)
                        .get_attribute('value'))

            @time.setter
            def time(self, new_time):
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

            def set_as_default(self):
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

    @property
    def title(self):
        """Return the card heading.

        :return: the card heading
        :rtype: str

        """
        return self.find_element(*self._title_locator).text

    def close(self):
        """Click on the close 'x' button.

        :return: close the selector and return to the assignment
        :rtype: :py:class:`Assignment`

        """
        button = self.find_element(*self._close_x_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.5)
        return self.page

    @property
    def chapters(self):
        """Access the book chapters.

        :return: the list of book chapters
        :rtype: list(:py:class:`~SectionSelector.Chapter`)

        """
        return [self.Chapter(self, chapter)
                for chapter in self.find_elements(*self._chapter_locator)]

    def add_readings(self):
        """Click the 'Add Readings' button.

        :return: the assignment creation wizard with the new readings added to
            the assignment
        :rtype: :py:class:`Assignment`

        """
        button = self.find_element(*self._add_readings_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.5)
        return self.page

    def cancel(self):
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

        def toggle(self):
            """Click on the chapter bar to open or close the chapter.

            :return: the book section selector
            :rtype: :py:class:`SectionSelector`

            """
            Utility.click_option(self.driver, element=self.root)
            sleep(0.75)
            return self.page

        @property
        def is_open(self):
            """Return True if the chapter sections are displayed.

            :return: ``True`` if the chapter is open and ``False`` if it is not
            :rtype: bool

            """
            return self.root.get_attribute('data-is-expanded') == 'true'

        def select(self):
            """Click on the chapter check box.

            :return: the book section selector
            :rtype: :py:class:`SectionSelector`

            """
            checkbox = self.find_element(*self._section_checkbox_locator)
            Utility.click_option(self.driver, element=checkbox)
            sleep(0.75)
            return self.page

        @property
        def checked(self):
            """Return True if the checkbox is selected.

            :return: ``True`` if the chapter checkbox is checked and ``False``
                if it is not
            :rtype: bool

            """
            checkbox = self.find_element(*self._check_state_locator)
            return 'checked' in checkbox.get_attribute('class')

        @property
        def number(self):
            """Return the chapter number.

            :return: the chapter number
            :rtype: str

            """
            return self.find_element(*self._chapter_number_locator).text

        @property
        def title(self):
            """Return the chapter title.

            :return: the chapter title
            :rtype: str

            """
            return self.find_element(*self._chapter_title_locator).text

        def browse_the_book(self):
            """Click on the 'Browse the Book' link to view the chapter.

            :return: the reference view for the selected chapter in a new tab
            :rtype: :py:class:`~pages.tutor.reference.ReferenceBook`

            """
            link = self.find_element(*self._browse_the_book_link_locator)
            Utility.switch_to(self.driver, element=link)
            from pages.tutor.reference import ReferenceBook
            return go_to_(
                ReferenceBook(self.driver, base_url=self.page.page.base_url))

        @property
        def sections(self):
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

            def select(self):
                """Click on the section check box.

                :return: the book section selector
                :rtype: :py:class:`SectionSelector`

                """
                checkbox = self.find_element(*self._section_checkbox_locator)
                Utility.click_option(self.driver, element=checkbox)
                sleep(0.75)
                return self.page.page

            @property
            def checked(self):
                """Return True if the checkbox is selected.

                :return: ``True`` if the section checkbox is checked and
                    ``False`` if it is not
                :rtype: bool

                """
                return 'checked' in self.root.get_attribute('class')

            @property
            def is_unnumbered(self):
                """Return True if the section is not numbered.

                :return: ``True`` if the section does not have a section
                    number, ``False`` if it does
                :rtype: bool

                """
                return bool(self.find_elements(*self._section_number_locator))

            @property
            def number(self):
                """Return the section number.

                :return: the section number if it exists or an empty string if
                    it does not exist
                :rtype: str

                """
                if self.is_unnumbered:
                    return ''
                return self.find_element(*self._section_number_locator).text

            @property
            def title(self):
                """Return the section title.

                :return: the section title
                :rtype: str

                """
                return self.find_element(*self._section_title_locator).text


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
    def title(self):
        """Return the current card title.

        :return: the assignment creation or modification title
        :rtype: str

        """
        return self.find_element(*self._assignment_heading_locator).text

    def close(self):
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
        from pages.tutor.calendar import Calendar
        return go_to_(Calendar(self.driver, base_url=self.base_url))

    # ---------------------------------------------------- #
    # Body
    # ---------------------------------------------------- #

    @property
    def name(self):
        """Return the current assignment name.

        :return: the current value in the assignment name field
        :rtype: str

        """
        return (self.find_element(*self._assignment_name_locator)
                .get_attribute('value'))

    @name.setter
    def name(self, assignment_name):
        """Set the assignment name.

        :param str assignment_name: the new assignment name
        :return: None

        """
        name_box = self.find_element(*self._assignment_name_locator)
        if name_box.get_attribute('value'):
            Utility.clear_field(self.driver, field=name_box)
        name_box.send_keys(assignment_name)

    @property
    def name_description(self):
        """Return the field descriptor.

        :return: the additional field descriptor text
        :rtype: str

        """
        return (self.find_element(*self._assignment_name_description_locator)
                .text)

    @property
    def name_error(self):
        """Return the name error text.

        :return: the name field error text
        :rtype: str

        """
        return self.find_element(*self._assignment_name_required_locator).text

    @property
    def description(self):
        """Return the current assignment description.

        :return: the current value in the assignment description field
        :rtype: str

        """
        return self.find_element(*self._description_locator).text

    @description.setter
    def description(self, description):
        """Set the assignment description.

        :param str description: the new assignment description
        :return: None

        """
        description_box = self.find_element(*self._description_locator)
        if description_box.get_attribute('textContent'):
            Utility.clear_field(self.driver, field=description_box)
        description_box.send_keys(description)

    @property
    def description_error(self):
        """Return the description error text.

        :return: the description field error text
        :rtype: str

        """
        return self.find_element(*self._description_required_locator).text

    @property
    def timezone(self):
        """Return the current timezone.

        :return: the course's assigned timezone
        :rtype: str

        """
        return self.find_element(*self._current_timezone_locator).text

    def change_timezone(self):
        """Click on the current course timezone.

        :return: the course settings page
        :rtype: :py:class:`~pages.tutor.settings.CourseSettings`

        """
        link = self.find_element(*self._change_timezone_locator)
        Utility.click_option(self.driver, element=link)
        from pages.tutor.settings import CourseSettings
        return go_to_(CourseSettings(self.driver, base_url=self.base_url))

    def all_sections(self):
        """Click on the 'All Sections' radio button.

        :return: the current page
        :rtype: self

        """
        radio_option = self.find_element(*self._assign_to_all_sections_locator)
        Utility.click_option(self.driver, element=radio_option)
        sleep(0.25)
        return self

    def individual_sections(self):
        """Click on the 'Individual Sections' radio button.

        :return: the current page
        :rtype: self

        """
        radio_option = self.find_element(*self._assign_by_section_locator)
        Utility.click_option(self.driver, element=radio_option)
        sleep(0.25)
        return self

    @property
    def open_and_due(self):
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
    def errors(self):
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
        def section(self):
            """Return the section name.

            :return: the section name
            :rtype: str

            """
            return self.find_element(*self._section_id_locator).text

        def select(self):
            """Click on the section checkbox.

            :return: the assignment page
            :rtype: :py:class:`Assignment`

            """
            checkbox = self.find_element(*self._section_checkbox_locator)
            Utility.click_option(self.driver, element=checkbox)
            sleep(0.25)
            return self.page

        @property
        def checked(self):
            """Return True if the section checkbox is checked.

            :return: ``True`` if the checkbox is checked, otherwise ``False``
            :rtype: bool

            """
            checkbox = self.find_element(*self._section_checkbox_locator)
            return self.driver.execute_script(
                'return arguments[0].checked;', checkbox)

        @property
        def open_to_close(self):
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
    def assignment_url(self):
        """Return the current URL value.

        :return: the current assignment URL
        :rtype: str

        """
        return (self.find_element(*self._assignment_url_locator)
                .get_attribute('value'))

    @assignment_url.setter
    def assignment_url(self, url):
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
    def url_error(self):
        """Return the assignment URL error text.

        :return: the assignment URL field error text
        :rtype: str

        """
        return self.find_element(*self._assignment_url_required_locator).text

    @property
    def errors(self):
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
    def reading_list(self):
        """Access the selected readings list.

        :return: a list of reading sections for the assignment
        :rtype: list(:py:class:`~Reading.ReadingSelection`)

        """
        return [self.ReadingSelection(self, item)
                for item
                in self.find_elements(*self._selected_reading_list_locator)]

    def add_readings(self):
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
    def readings_error(self):
        """Return the readings required error message.

        :return: the readings required field error text
        :rtype: str

        """
        return self.find_element(*self._readings_required_locator).text

    @property
    def errors(self):
        """Return any error messages.

        :return: a list of error messages
        :rtype: list(str)

        """
        errors = super().errors()
        url = self.find_elements(*self._readings_required_locator)
        if url and self.driver.execute_script(DISPLAYED, url[0]):
            errors.append('Readings: {0}'.format(url[0].text))
        return errors

    def why_cant_i_see_the_questions(self):
        """Click on the 'see the questions' FAQ question link.

        :return: the reading question FAQ tooltip
        :rtype: :py:class:`ReadingQuestionTooltip`

        """
        link = self.find_element(*self._see_questions_tooltip_locator)
        Utility.click_option(self.driver, element=link)
        sleep(0.25)
        tooltip_root = self.driver.execute_script(GET_ROOT.format('tooltip'))
        return ReadingQuestionTooltip(self, tooltip_root)

    def what_do_students_see(self):
        """Click the 'What do students see?' button.

        :return: the student preview video pop up
        :rtype: :py:class:`~pages.tutor.preview.StudentPreview`

        """
        button = self.find_element(*self._what_do_students_see_button_locator)
        Utility.switch_to(self.driver, element=button)
        from pages.tutor.preview import StudentPreview
        return StudentPreview(self.driver)

    class ReadingSelection(Region):
        """The reading order list."""

        _chapter_section_number_locator = (By.CSS_SELECTOR, '.chapter-section')
        _selection_title_locator = (By.CSS_SELECTOR, '.section-title')
        _move_up_arrow_locator = (By.CSS_SELECTOR, '.arrow-up')
        _move_down_arrow_locator = (By.CSS_SELECTOR, '.arrow-down')
        _delete_section_locator = (By.CSS_SELECTOR, '.close')

        @property
        def number(self):
            """Return the section number.

            :return: the chapter and section number for the reading
            :rtype: str

            """
            return (self.find_element(*self._chapter_section_number_locator)
                    .text)

        @property
        def title(self):
            """Return the section title.

            :return: the section title
            :rtype: str

            """
            return self.find_element(*self._selection_title_locator).text

        def move_up(self):
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

        def move_down(self):
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

        def delete(self):
            """Remove the section from the reading assignment.

            :return: the reading selection pane
            :rtype: :py:class:`~Reading.ReadingSelection`

            """
            button = self.find_element(*self._delete_section_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.5)
            return self
