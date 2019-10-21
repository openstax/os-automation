"""An instructor course page with calendar."""

from __future__ import annotations

from datetime import datetime
from time import sleep
from typing import Dict, List, Tuple, Union

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from regions.tutor.notification import Notifications
from regions.tutor.tooltip import Float
from utils.tutor import Tutor, TutorException
from utils.utilities import Utility, go_to_

DateTime = Tuple[Union[str, datetime], str]
Timeframe = Dict[str, Tuple[DateTime, DateTime]]


class Assignment(Region):
    """An individual student assignment or event."""

    _plan_locator = (By.CSS_SELECTOR, '.plan')
    _title_locator = (By.CSS_SELECTOR, 'label')
    _edit_draft_locator = (By.CSS_SELECTOR, 'a')
    _flagged_assignment_locator = (By.CSS_SELECTOR, 'label svg')

    @property
    def style(self):
        """Return the assignment color display type.

        :returns: the assignment type
        :rtype: str

        """
        return (self.root.get_attribute('class')
                .split('type-')[-1]
                .split()[0])

    @property
    def span(self):
        """Return the number of days this week the event spans.

        :returns: the number of days in the week the assignment
            spans
        :rtype: int

        """
        return int(self.root.get_attribute('class')
                   .split('span-')[-1]
                   .split()[0])

    @property
    def plan(self):
        """Return the assignment plan element.

        :return: the assignment plan
        :rtype: :py:class:`selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._plan_locator)

    @property
    def is_published(self):
        """Return True if the assignment is published.

        :return: ``True`` if the assignment is published,
            else ``False``
        :rtype: bool

        """
        return 'is-published' in self.plan.get_attribute('class')

    @property
    def is_draft(self):
        """Return True if the assignment is a saved draft.

        :return: ``True`` if the assignment is a saved draft,
            else ``False``
        :rtype: bool

        """
        return 'is-draft' in self.plan.get_attribute('class')

    @property
    def is_open(self):
        """Return True if the assignment is open for work.

        :return: ``True`` if the assignment is currently open for
            work, else ``False``
        :rtype: bool

        """
        return 'is-open' in self.plan.get_attribute('class')

    @property
    def plan_id(self):
        """Return the assignment plan ID.

        :return: the assignment plan identification number
        :rtype: str

        """
        return self.plan.get_attribute('data-plan-id')

    @property
    def assignment_type(self):
        """Return the assignment type.

        :return: the assignment type
        :rtype: str

        """
        return self.plan.get_attribute('data-assignment-type')

    @property
    def opens_on(self):
        """Return the date the assignment opens on.

        :return: the date the assignment opens for work
        :rtype: str

        """
        return (self.find_element(*self._title_locator)
                .get_attribute('data-opens-at'))

    @property
    def title(self):
        """Return the assignment title.

        :return: the assignment title
        :rtype: str

        """
        return self.find_element(*self._title_locator).text

    def edit(self):
        """Edit the selected assignment.

        :return: an assignment creation page if the assignment is
                 a saved draft else display the quick look assignment modal
        :rtype: :py:class:`~pages.tutor.assignment.AddExternal` or
                :py:class:`~pages.tutor.assignment.AddEvent` or
                :py:class:`~pages.tutor.assignment.AddHomework` or
                :py:class:`~pages.tutor.assignment.AddReading` or
                :py:class:`~regions.tutor.quick_look.QuickLook`

        :raises :py:class:`~utils.tutor.TutorException`: if the
                assignment type does not match a known assignment
                type

        """
        if self.is_draft:
            assignment_type = self.assignment_type
            link = self.find_element(*self._edit_draft_locator)
            Utility.click_option(self.driver, element=link)
            if assignment_type == Tutor.EVENT:
                from pages.tutor.assignment import Event as Assignment
            elif assignment_type == Tutor.EXTERNAL:
                from pages.tutor.assignment import External as Assignment
            elif assignment_type == Tutor.HOMEWORK:
                from pages.tutor.assignment import Homework as Assignment
            elif assignment_type == Tutor.READING:
                from pages.tutor.assignment import Reading as Assignment
            else:
                raise TutorException(
                    f'"{assignment_type}" is not a known assignment type.')
            target = self
            from pypom import Page
            while not isinstance(target, Page):
                target = target.page
            return go_to_(Assignment(self.driver, target.base_url))
        Utility.click_option(self.driver, element=self.root)
        sleep(0.5)
        from regions.tutor.quick_look import QuickLook
        return QuickLook(self.page)

    @property
    def flagged(self):
        """Return True if the trouble flag is present.

        :return: ``True`` if the assignment has a trouble flag
            displayed on the calendar, else ``False``
        :rtype: bool

        """
        return bool(
            self.find_elements(*self._flagged_assignment_locator))


class Calendar(TutorBase):
    """The instructor course calendar."""

    _joyride_root_locator = (By.CSS_SELECTOR, '.joyride')
    _banner_locator = (By.CSS_SELECTOR, '.course-page header')
    _assignment_sidebar_locator = (By.CSS_SELECTOR, '.add-assignment-sidebar')
    _calendar_body_locator = (By.CSS_SELECTOR, '.month-body')
    _is_publishing_locator = (By.CSS_SELECTOR, '.is-publishing')
    _assignment_locator = (By.CSS_SELECTOR, '.event')

    _loading_message_selector = '.calendar-loading'

    # ---------------------------------------------------- #
    # Banner / Header
    # ---------------------------------------------------- #

    @property
    def banner(self):
        """Access the course page header.

        :return: the course banner region
        :rtype: :py:class:`~Calendar.Banner`

        """
        banner = self.find_element(*self._banner_locator)
        return self.Banner(self, banner)

    @property
    def title(self):
        """Return the course title.

        :return: the course name
        :rtype: str

        """
        return self.banner.title

    @property
    def term(self):
        """Return the course term.

        :return: the course semester or quarter
        :rtype: str

        """
        return self.banner.term

    @property
    def notifications(self):
        """Access the active notifications, if exists.

        :return: the list of currently active site notifications
        :rtype: list(:py:class:`~regions.tutor.notification.Notifications`)

        """
        if not self.banner.notes.displayed:
            return []
        return self.banner.notes.notifications

    # ---------------------------------------------------- #
    # Assignment sidebar
    # ---------------------------------------------------- #

    @property
    def sidebar(self):
        """Access the assignment sidebar.

        :return: the assignment creation and cloning sidebar region
        :rtype: :py:class:`~Calendar.Sidebar`

        """
        sidebar = self.find_element(*self._assignment_sidebar_locator)
        return self.Sidebar(self, sidebar)

    # ---------------------------------------------------- #
    # The monthly calendar
    # ---------------------------------------------------- #

    @property
    def calendar(self):
        """Access the calendar.

        :return: the assignment calendar region
        :rtype: :py:class:`~Calendar.Calendar`

        """
        calendar = self.find_element(*self._calendar_body_locator)
        return self.CalendarMonth(self, calendar)

    # ---------------------------------------------------- #
    # Calendar helper functions
    # ---------------------------------------------------- #

    @property
    def loaded(self) -> bool:
        """Return True when the loading message goes away.

        :return: ``True`` when the loading message goes away
        :rtype: bool

        :noindex:

        """
        return ((self.find_element(By.CSS_SELECTOR, '.calendar-container')
                 .is_displayed()) and
                'calendar-loading' not in (
                    self.find_element(By.CSS_SELECTOR, '.calendar-container')
                    .get_attribute('class')))

    def clear_training_wheels(self) -> None:
        """Clear any joyride modals.

        :return: None

        """
        while Float(self).is_open:
            Float(self).close()

    def add_assignment(self,
                       assignment: str,
                       name: str,
                       assign_to: Timeframe,
                       description: str = "",
                       action: str = Tutor.PUBLISH
                       ) -> None:
        """Create a new assignment.

        :TODO: fill parameter list
        :return: None

        :raises :py:class:`~utils.tutor.TutorException`: if the assignment type
            does not match existing assignment types

        """
        # Expand the assignment menu if it is not already open
        if not self.sidebar.is_open:
            self.banner.add_assignment()

        # Select the assignment type
        try:
            {Tutor.EVENT:    self.sidebar.add_event,
             Tutor.EXTERNAL: self.sidebar.add_external,
             Tutor.HOMEWORK: self.sidebar.add_homework,
             Tutor.READING:  self.sidebar.add_reading, }[assignment]()
        except KeyError:
            raise TutorException(f'"{assignment}" not a valid assignment type')

        # Wait for the assignment creation page to load
        if assignment == Tutor.EVENT:
            from pages.tutor.assignment import Event as Destination
        elif assignment == Tutor.EXTERNAL:
            from pages.tutor.assignment import External as Destination
        elif assignment == Tutor.HOMEWORK:
            from pages.tutor.assignment import Homework as Destination
        else:
            from pages.tutor.assignment import Reading as Destination
        assign = go_to_(Destination(self.driver, self.base_url))

        # Enter the assignment name
        assign.name = name

        # Enter the description, if included
        if description:
            assign.description = description

        # select the assignment open and due dates and times
        assign.set_assignment_dates(assign_to)

        # click the action
        try:
            {Tutor.PUBLISH: assign.publish,
             Tutor.DRAFT: assign.save_as_draft,
             Tutor.CANCEL: assign.cancel,
             Tutor.DELETE: assign.delete, }[action]()
        except KeyError:
            raise TutorException(f'"{action}" not a valid assignment action')

        # wait for the calendar to load
        calendar = go_to_(Calendar(self.driver, self.base_url))

        # wait for the assignment to complete publishing/saving
        calendar.wait.until(
            lambda _: not self.driver.find_elements(
                *self._is_publishing_locator))

    def assignments(self, by_name: bool = False) \
            -> Union[List[Assignment], List[str]]:
        r"""Return a list of assignments.

        :param bool by_name: (optional) request the list of assignment names
            currently displayed in the calendar
        :return: the list of assignments or assignment names
        :rtype: list(:py:class:`~pages.tutor.calendar \
                     .Calendar.CalendarMonth.Day.Assignment`) or list(str)

        """
        assignments = [Assignment(self, ribbon)
                       for ribbon
                       in self.find_elements(*self._assignment_locator)]
        if not by_name:
            return assignments
        return [assignment.title for assignment in assignments]

    def assignment(self, name: str) -> Assignment:
        """Return the assignment from its name.

        :param str name: the assignment name or title
        :return: the assignment
        :rtype: :py:class:`~pages.tutor.calendar.Assignment`

        :raises :py:class:`~utils.tutor.TutorException` if an assignment does
            not match ``name``

        """
        for assignment in self.assignments():
            if assignment.title == name:
                return assignment
        raise TutorException(f'No assignment found matching "{name}"')

    def assignments_on(self, date: datetime, by_name: bool = False) \
            -> Union[List[str], List[Assignment]]:
        """Return the assignments on a particular date.

        .. note:

            Only looks at the current month
            TODO: add a calendar rotation to pull the assignments for dates in
                  different months

        :param date: a specific date
        :param bool by_name: (optional) return the assignment names found on
            the date instead of the assignments
        :type date: :py:class:`~datetime.datetime`
        :return: the list of assignments on that date or the list of
            assignment names on that date
        :rtype: list(:py:class:`~pages.tutor.calendar.Assignment`)

        """
        selector = f'[data-date="{date.strftime("%Y%m%d")}"]'
        due_date = self.find_element(By.CSS_SELECTOR, selector)
        assignments = [Assignment(self, ribbon)
                       for ribbon
                       in due_date.find_elements(*self._assignment_locator)]
        if not by_name:
            return assignments
        return [assignment.title for assignment in assignments]

    # ---------------------------------------------------- #
    # Instructor course regions
    # ---------------------------------------------------- #

    class Banner(Region):
        """The header region of the course calendar."""

        _title_locator = (By.CSS_SELECTOR, '.title')
        _course_term_locator = (By.CSS_SELECTOR, '.subtitle')
        _notification_bar_locator = (By.CSS_SELECTOR,
                                     '.openstax-notifications-bar')
        _assignment_toggle_locator = (By.CSS_SELECTOR, '.sidebar-toggle')
        _browse_the_book_locator = (By.CSS_SELECTOR, '.reference')
        _question_library_locator = (By.CSS_SELECTOR, '[href$=questions]')
        _performance_forecast_locator = (By.CSS_SELECTOR, '[href$=guide]')
        _student_scores_locator = (By.CSS_SELECTOR, '[href$=scores]')

        @property
        def title(self):
            """Return the course title.

            :return: the course name
            :rtype: str

            """
            return self.find_element(*self._title_locator).text

        @property
        def term(self):
            """Return the course term.

            :return: the course semester or quarter
            :rtype: str

            """
            return self.find_element(*self._course_term_locator).text

        @property
        def notes(self):
            """Access the notifications.

            :return: the list of currently active site notifications
            :rtype: list(:py:class:`~regions.tutor.notification.Notifications`)

            """
            notes = self.find_element(*self._notification_bar_locator)
            return Notifications(self, notes)

        def add_assignment(self):
            """Click on the 'Add Assignment' toggle button.

            :return: the course calendar
            :rtype: :py:class:`Calendar`

            """
            button = self.find_element(*self._assignment_toggle_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.5)
            return self.page

        def browse_the_book(self):
            """Click on the 'Browse the Book' button.

            :return: the reference book view in a new tab
            :rtype: :py:class:`~pages.tutor.reference.ReferenceBook`

            """
            button = self.find_element(*self._browse_the_book_locator)
            Utility.switch_to(self.driver, element=button)
            from pages.tutor.reference import ReferenceBook
            return go_to_(ReferenceBook(self.driver, self.page.base_url))

        def question_library(self):
            """Click on the 'Question Library' button.

            :return: the course question library page
            :rtype: :py:class:`~pages.tutor.library.QuestionLibrary`

            """
            button = self.find_element(*self._question_library_locator)
            Utility.click_option(self.driver, element=button)
            from pages.tutor.question_library import QuestionLibrary
            return go_to_(QuestionLibrary(self.driver, self.page.base_url))

        def performance_forecast(self):
            """Click on the 'Performance Forecast' button.

            :return: the course performance overview page
            :rtype: :py:class:`~pages.tutor.performance.Performance`

            """
            button = self.find_element(*self._performance_forecast_locator)
            Utility.click_option(self.driver, element=button)
            from pages.tutor.performance import PerformanceForecast
            return go_to_(PerformanceForecast(self.driver, self.page.base_url))

        def student_scores(self):
            """Click on the 'Student Scores' button.

            :return: the instructor scores page
            :rtype: :py:class:`~pages.tutor.scores.Scores`

            """
            button = self.find_element(*self._student_scores_locator)
            Utility.click_option(self.driver, element=button)
            from pages.tutor.scores import Scores
            return go_to_(Scores(self.driver, self.page.base_url))

    class Sidebar(Region):
        """The assignment sidebar."""

        _reading_bar_locator = (
                            By.CSS_SELECTOR, '[data-assignment-type=reading]')
        _homework_bar_locator = (
                            By.CSS_SELECTOR, '[data-assignment-type=homework]')
        _external_bar_locator = (
                            By.CSS_SELECTOR, '[data-assignment-type=external]')
        _event_bar_locator = (By.CSS_SELECTOR, '[data-assignment-type=event]')

        _add_reading_locator = (By.CSS_SELECTOR, '[href$="reading/new"]')
        _add_homework_locator = (By.CSS_SELECTOR, '[href$="homework/new"]')
        _add_external_locator = (By.CSS_SELECTOR, '[href$="external/new"]')
        _add_event_locator = (By.CSS_SELECTOR, '[href$="event/new"]')
        _assignment_clone_locator = (By.CSS_SELECTOR, '.plans > div')

        @property
        def is_open(self):
            """Return True if the assignment sidebar menu is displayed.

            :return: ``True`` if the assignment sidebar is open and displayed,
                else ``False``
            :rtype: bool

            """
            return 'is-open' in self.root.get_attribute('class')

        @property
        def reading_bar(self):
            r"""Return the 'Add Reading' bar element.

            :return: the reading assignment bar
            :rtype: \
                :py:class:`~selenium.webdriver.remote.webelement.WebElement`

            """
            return self.find_element(*self._reading_bar_locator)

        @property
        def homework_bar(self):
            r"""Return the 'Add Homework' bar element.

            :return: the homework assignment bar
            :rtype: \
                :py:class:`~selenium.webdriver.remote.webelement.WebElement`

            """
            return self.find_element(*self._homework_bar_locator)

        @property
        def external_bar(self):
            r"""Return the 'Add External Assignment' bar element.

            :return: the external assignment bar
            :rtype: \
                :py:class:`~selenium.webdriver.remote.webelement.WebElement`

            """
            return self.find_element(*self._external_bar_locator)

        @property
        def event_bar(self):
            r"""Return the 'Add Event' bar element.

            :return: the event bar
            :rtype: \
                :py:class:`~selenium.webdriver.remote.webelement.WebElement`

            """
            return self.find_element(*self._event_bar_locator)

        def add_reading(self):
            """Click on the 'Add Reading' button.

            :return: the add assignment page for a reading
            :rtype: :py:class:`~pages.tutor.assignment.AddReading`

            """
            return self._add_assignment(Tutor.READING)

        def add_homework(self):
            """Click on the 'Add Homework' button.

            :return: the add assignment page for a homework
            :rtype: :py:class:`~pages.tutor.assignment.AddHomework`

            """
            return self._add_assignment(Tutor.HOMEWORK)

        def add_external(self):
            """Click on the 'Add External Assignment' button.

            :return: the add assignment page for an external task
            :rtype: :py:class:`~pages.tutor.assignment.AddExternal`

            """
            return self._add_assignment(Tutor.EXTERNAL)

        def add_event(self):
            """Click on the 'Add Event' button.

            :return: the add assignment page for an event
            :rtype: :py:class:`~pages.tutor.assignment.AddEvent`

            """
            return self._add_assignment(Tutor.EVENT)

        @property
        def copied_assignments(self):
            """Access the assignment clone options.

            :return: the list of previous-course assignments available for
                cloning
            :rtype: list(:py:class:`~Calendar.Sidebar.AssignmentCopy`)

            """
            return [self.AssignmentCopy(self, assignment)
                    for assignment
                    in self.find_elements(*self._assignment_clone_locator)]

        def _add_assignment(self, assignment_type):
            """Click on an add assignment button.

            An internal helper function to select a new assignment.

            :param str assignment_type: the type of assignment to add
            :return: an assignment creation page
            :rtype: :py:class:`~pages.tutor.assignment.AddExternal` or
                :py:class:`~pages.tutor.assignment.AddEvent` or
                :py:class:`~pages.tutor.assignment.AddHomework` or
                :py:class:`~pages.tutor.assignment.AddReading`
            :raises :py:class:`~utils.tutor.TutorException`: if the
                assignment_type does not match a known assignment type

            :noindex:

            """
            if assignment_type == Tutor.EXTERNAL:
                locator = self._add_external_locator
                from pages.tutor.assignment import External as Assignment
            elif assignment_type == Tutor.EVENT:
                locator = self._add_event_locator
                from pages.tutor.assignment import Event as Assignment
            elif assignment_type == Tutor.HOMEWORK:
                locator = self._add_homework_locator
                from pages.tutor.assignment import Homework as Assignment
            elif assignment_type == Tutor.READING:
                locator = self._add_reading_locator
                from pages.tutor.assignment import Reading as Assignment
            else:
                raise TutorException('"{0}" is not a known assignment type.'
                                     .format(assignment_type))
            button = self.find_element(*locator)
            Utility.click_option(self.driver, element=button)
            return go_to_(Assignment(self.driver, self.page.base_url))

        class AssignmentCopy(Region):
            """An assignment from a previous course."""

            _title_locator = (By.CSS_SELECTOR, 'div')

            @property
            def plan_id(self):
                """Return the assignment ID.

                :return: the past assignment identification number
                :rtype: int

                """
                return self.root.get_attribute('data-assignment-id')

            @property
            def assignment_type(self):
                """Return the assignment type.

                :return: the past assignment type
                :rtype: str

                """
                return self.root.get_attribute('data-assignment-type')

            @property
            def title(self):
                """Return the assignment name.

                :return: the past assignment title
                :rtype: str

                """
                return self.find_element(*self._title_locator).text

    class CalendarMonth(Region):
        """The instructor calendar."""

        _current_month_locator = (By.CSS_SELECTOR, '.calendar-header-label')
        _last_month_locator = (By.CSS_SELECTOR, '.previous')
        _next_month_locator = (By.CSS_SELECTOR, '.next')
        _day_locator = (By.CSS_SELECTOR, '.days > div')

        @property
        def month(self):
            """Return the currently displayed month.

            :return: the calendar's currently displayed month
            :rtype: str

            """
            return (self.find_element(*self._current_month_locator)
                    .text.split()[0])

        @property
        def year(self):
            """Return the currently displayed year.

            :return: the currently displayed month's year
            :rtype: str

            """
            return (self.find_element(*self._current_month_locator)
                    .text.split()[1])

        def previous_month(self):
            """Click on the left arrow to view the previous month.

            :return: the previous month's calendar view
            :rtype: :py:class:`Calendar`

            """
            button = self.find_element(*self._last_month_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.5)
            return Calendar(self.driver, self.page.base_url)

        def next_month(self):
            """Click on the right arrow to view the next month.

            :return: the next month's calendar view
            :rtype: :py:class:`Calendar`

            """
            button = self.find_element(*self._next_month_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.5)
            return Calendar(self.driver, self.page.base_url)

        @property
        def days(self):
            """Access the individual dates.

            :return: the list of visible days
            :rtype: list(:py:class:`~Calendar.CalendarMonth.Day`)

            """
            return [self.Day(self, date)
                    for date in self.find_elements(*self._day_locator)]

        class Day(Region):
            """A specific date."""

            _today_locator = (By.CSS_SELECTOR, '.today')
            _event_locator = (By.CSS_SELECTOR, '.events')
            _assignment_locator = (By.CSS_SELECTOR, '.event')
            _date_label_locator = (By.CSS_SELECTOR, '.label')

            _add_assignment_selector = 'a[data-assignment-type={0}]'

            @property
            def number(self):
                """Return the calendar day number element.

                :return: the day's label
                :rtype: WebElement

                """
                return self.find_element(*self._date_label_locator)

            @property
            def date(self) -> datetime:
                """Return the date.

                :return: the day as a date
                :rtype: :py:class:`~datetime.datetime`

                """
                return datetime.strptime(self.root.get_attribute('data-date'),
                                         "%Y%m%d")

            @property
            def term(self):
                """Return whether the date is in or out of the term.

                :return: the status of a date with respect to the course term
                :rtype: str

                """
                term = self.root.get_attribute('class')
                if Tutor.BEFORE_TERM in term:
                    return Tutor.BEFORE_TERM
                elif Tutor.IN_TERM in term:
                    return Tutor.IN_TERM
                elif Tutor.AFTER_TERM in term:
                    return Tutor.AFTER_TERM
                else:
                    raise TutorException('No term-status listed in "{0}"'
                                         .format(term.split()))

            @property
            def tense(self):
                """Return whether the date is before today, today, or after.

                :return: the status of the date with respect to today
                :rtype: str

                """
                term = self.root.get_attribute('class')
                if Tutor.IN_PAST in term:
                    return Tutor.IN_PAST
                elif Tutor.IN_FUTURE in term:
                    return Tutor.IN_FUTURE
                return Tutor.TODAY

            def add_assignment(self, assignment_type=None):
                """Click on the date number to add an assignment.

                :param str assignment_type: the type of assignment to add
                :return: an assignment creation page
                :rtype: :py:class:`~pages.tutor.assignment.AddExternal` or
                        :py:class:`~pages.tutor.assignment.AddEvent` or
                        :py:class:`~pages.tutor.assignment.AddHomework` or
                        :py:class:`~pages.tutor.assignment.AddReading`

                :raises :py:class:`~utils.tutor.TutorException`: if the
                        assignment_type does not match a known assignment type

                """
                label = self.find_element(*self._date_label_locator)
                Utility.click_option(self.driver, element=label)
                sleep(0.5)
                if assignment_type == Tutor.EVENT:
                    assignment = Tutor.EVENT
                    from pages.tutor.assignment import Event \
                        as Assignment
                elif assignment_type == Tutor.EXTERNAL:
                    assignment = Tutor.EXTERNAL
                    from pages.tutor.assignment import External \
                        as Assignment
                elif assignment_type == Tutor.HOMEWORK:
                    assignment = Tutor.HOMEWORK
                    from pages.tutor.assignment import Homework \
                        as Assignment
                elif assignment_type == Tutor.READING:
                    assignment = Tutor.READING
                    from pages.tutor.assignment import Reading \
                        as Assignment
                elif assignment_type is None:
                    # just open the pop up menu
                    return self.page.page
                else:
                    raise TutorException(
                        '"{0}" is not a known assignment type.'
                        .format(assignment_type))
                if assignment:
                    button = self.driver.execute_script(
                        'return document.querySelector("{}");'.format(
                            self._add_assignment_selector.format(assignment)))
                    Utility.click_option(self.driver, element=button)
                    return go_to_(Assignment(self.driver,
                                             self.page.page.base_url))

            @property
            def has_assignments(self):
                """Return True if any class assignments are found.

                :return: ``True`` if any assignments are due on this day, else
                    ``False``
                :rtype: bool

                """
                return bool(self.find_elements(*self._event_locator))

            @property
            def assignments(self):
                r"""Access the assignments listed as due today.

                :returns: the list of assignments due on this day
                :rtype: \
                    list(:py:class:`~Calendar.CalendarMonth.Day.Assignment`)

                """
                return [Assignment(self, event)
                        for event
                        in self.find_elements(*self._assignment_locator)]
