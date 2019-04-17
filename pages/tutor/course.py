"""The student course view."""

import re
from datetime import datetime
from time import sleep

from pypom import Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from regions.tutor.notification import Notifications
from utils.tutor import Tutor, TutorException
from utils.utilities import Utility, go_to_


class StudentCourse(TutorBase):
    """The weekly course view for students."""

    _notification_bar_locator = (
                                By.CSS_SELECTOR, '.openstax-notifications-bar')
    _banner_locator = (By.CSS_SELECTOR, '.course-title-banner')
    _this_week_locator = (By.CSS_SELECTOR, '.nav-tabs li:first-child a')
    _all_past_work_locator = (By.CSS_SELECTOR, '.nav-tabs li:last-child a')
    _weekly_work_locator = (By.CSS_SELECTOR, '.row div:first-child')
    _period_locator = (By.CSS_SELECTOR, '.active .card')
    _survey_locator = (By.CSS_SELECTOR, '.research-surveys')
    _performance_guide_locator = (By.CSS_SELECTOR, '.progress-guide')
    _reference_book_locator = (By.CSS_SELECTOR, 'a.browse-the-book')

    # ---------------------------------------------------- #
    # Notifications
    # ---------------------------------------------------- #

    @property
    def notes(self):
        """Access the notifications.

        :return: the notification region
        :rtype: :py:class:`~regions.tutor.notification.Notifications`

        """
        notes = self.find_element(*self._notification_bar_locator)
        return Notifications(self, notes)

    # ---------------------------------------------------- #
    # Course overview
    # ---------------------------------------------------- #

    @property
    def banner(self):
        """Access the course banner.

        :return: the course banner region
        :rtype: :py:class:`~StudentCourse.Banner`

        """
        banner = self.find_element(*self._banner_locator)
        return self.Banner(self, banner)

    @property
    def course_title(self):
        """Return the course title.

        :return: the course title
        :rtype: str

        """
        return self.banner.course_name

    @property
    def course_term(self):
        """Return the course term.

        :return: the course semester or quarter
        :rtype: str

        """
        return self.banner.course_term

    # ---------------------------------------------------- #
    # Assignments
    # ---------------------------------------------------- #

    def view_this_week(self):
        """Click on the 'THIS WEEK' toggle to view current work.

        :return: the course page with the This Week view active
        :rtype: :py:class:`StudentCourse`

        """
        toggle = self.find_element(*self._this_week_locator)
        Utility.click_option(self.driver, element=toggle)
        sleep(0.5)
        return self

    def view_all_past_work(self):
        """Click on the 'ALL PAST WORK' toggle to view previous work.

        :return: the course page with the Past Work view active
        :rtype: :py:class:`StudentCourse`

        """
        toggle = self.find_element(*self._all_past_work_locator)
        Utility.click_option(self.driver, element=toggle)
        sleep(0.5)
        return self.page

    @property
    def weeks(self):
        """Access the assignment weeks.

        :return: the list of assignment weeks
        :rtype: list(:py:class:`~StudentCourse.Week`)

        """
        return [self.Week(self, period)
                for period in self.find_elements(*self._period_locator)]

    # ---------------------------------------------------- #
    # Sidebar
    # ---------------------------------------------------- #

    @property
    def survey(self):
        """Access the research surveys.

        :return: the research survey region
        :rtype: :py:class:`~StudentCourse.Survey`

        """
        survey_card = self.find_element(*self._survey_locator)
        return self.Survey(self, survey_card)

    @property
    def performance_sidebar(self):
        """Access the performance forecast sidebar.

        :return: the performance forecast recent work sidebar
        :rtype: :py:class:`~StudentCourse.Performance`

        """
        forecast_sidebar = self.find_element(*self._performance_guide_locator)
        return self.Performance(self, forecast_sidebar)

    @property
    def reference_book(self):
        """Return the reference book link element.

        :return: the reference book element
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._reference_book_locator)

    @property
    def book_cover(self):
        """Return the reference book cover image URL.

        :return: the book cover image URL
        :rtype: str

        """
        script = ('return window.getComputedStyle(arguments[0], ":before")'
                  '.backgroundImage;')
        url = self.driver.execute_script(script, self.reference_book)
        return url[5:-2]

    def browse_the_book(self):
        """Click on the 'Browse the Book' link.

        :return: the reference book view in a new tab
        :rtype: :py:class:`~pages.tutor.reference.ReferenceBook`

        """
        Utility.switch_to(self.driver, element=self.reference_book)
        from pages.tutor.reference import ReferenceBook
        return go_to_(ReferenceBook(self.driver, self.base_url))

    # ---------------------------------------------------- #
    # Student Course Regions
    # ---------------------------------------------------- #

    class Banner(Region):
        """The course banner."""

        _course_title_locator = (By.CSS_SELECTOR, '.book-title-text')
        _course_term_locator = (By.CSS_SELECTOR, '.course-term')

        @property
        def course_data(self):
            """Return the course data stored in the course banner element.

            :return: the course data overview provided by the banner
            :rtype: dict(str, str)

            """
            return {
                "title": self.root.get_attribute("data-title"),
                "book-title": self.root.get_attribute("data-book-title"),
                "appearance": self.root.get_attribute("data-appearance"),
                "is-preview": self.root.get_attribute("data-is-preview"),
                "term": self.root.get_attribute("data-term"), }

        @property
        def course_name(self):
            """Return the course name.

            :return: the course title
            :rtype: str

            """
            return self.find_element(*self._course_title_locator).text

        @property
        def course_term(self):
            """Return the course term.

            :return: the course semester or quarter
            :rtype: str

            """
            return self.find_element(*self._course_term_locator).text

    class Weeks(Region):
        """Assignments listed by week."""

        _banner_locator = (By.CSS_SELECTOR, '.row:first-child')
        _assignments_locator = (By.CSS_SELECTOR, '.row:not(:first-child)')
        _key_guide_locator = (By.CSS_SELECTOR, '[class*="Wrapper-sc"] span')

        @property
        def banner(self):
            """Access the period bar.

            :return: the title bar for a particular week
            :rtype: :py:class:`~StudentCourse.Weeks.Banner`

            """
            banner_root = self.find_element(*self._banner_locator)
            return self.Banner(self, banner_root)

        @property
        def assignments(self):
            """Access the assignment bars.

            :return: the list of assignments
            :rtype: list(:py:class:`~StudentCourse.Weeks.Assignment`)

            """
            return [self.Assignment(self, line)
                    for line in self.find_elements(*self._assignments_locator)]

        @property
        def guide(self):
            """Access the key icons.

            :return: the list of guide icon descriptions
            :rtype: list(:py:class:`~StudentCourse.Weeks.Key`)

            """
            return [self.Key(self, icon)
                    for icon in self.find_elements(*self._key_guide_locator)]

        class Banner(Region):
            """The title bar for an assignment set."""

            _start_date_locator = (By.CSS_SELECTOR, '.time:first-child')
            _end_date_locator = (By.CSS_SELECTOR, '.time:li:last-child')
            _title_locator = (By.CSS_SELECTOR, '.title')

            def is_upcoming(self):
                """Return True if a title element is present.

                :return: ``True`` if the title is found, else ``False``
                :rtype: bool

                """
                return bool(self.find_elements(*self._title_locator))

            def start(self):
                """Return the week's starting date.

                :return: the start date for the week
                :rtype: :py:class:`~datetime.datetime`

                """
                date = self.find_element(*self._start_date_locator).text
                return datetime.strptime(date, "%b %d, %Y")

            def end(self):
                """Return the week's ending date.

                :return: the end date for the week
                :rtype: :py:class:`~datetime.datetime`

                """
                date = self.find_element(*self._end_date_locator).text
                return datetime.strptime(date, "%b %d, %Y")

            def title(self):
                """Return the title or week date information.

                :return: title or week information for the week
                :rtype: str

                """
                if self.is_upcoming:
                    return self.find_element(*self._title_locator).text
                return "{start}–{end}".format(start=self.start, end=self.end)

        class Assignment(Region):
            """A student assignment."""

            _title_locator = (By.CSS_SELECTOR, '.title')
            _due_date_time_locator = (By.CSS_SELECTOR, '.due-at time')
            _status_locator = (
                            By.CSS_SELECTOR, '[data-tour-anchor-id*=progress]')
            _secondary_status_locator = (
                                    By.CSS_SELECTOR, '[class*=LateCaption]')
            _lateness_locator = (By.CSS_SELECTOR, '.feedback svg')

            _course_term_selector = '.course-title-banner'

            @property
            def title(self):
                """Return the assignment name.

                :return: the assignment name
                :rtype: str

                """
                return self.find_element(*self._title_locator).text

            @property
            def style(self):
                """Return the assignment type.

                :return: the assignment type
                :rtype: str
                :raises :py:class:`~utils.tutor.TutorException`: if a known
                    assignment type is not found within the assignment class

                """
                assignment_type = self.root.get_attribute('class')
                if Tutor.EVENT in assignment_type:
                    return Tutor.EVENT
                elif Tutor.EXTERNAL in assignment_type:
                    return Tutor.EXTERNAL
                elif Tutor.HOMEWORK in assignment_type:
                    return Tutor.HOMEWORK
                elif Tutor.READING in assignment_type:
                    return Tutor.READING
                else:
                    raise TutorException(
                        '"{0}" does not contain a known assignment type'
                        .format(assignment_type))

            @property
            def url(self):
                """Return the assignment access URL.

                :return: the assignment URL
                :rtype: str

                """
                return self.root.get_attribute('href')

            @property
            def due(self):
                """Return the assignment due date and time.

                :return: the assignment due date and time, timezone-aware
                :rtype: :py:class:`~datetime.datetime`

                """
                date_and_time = self.find_element(
                    *self._due_date_time_locator).text
                script = ('return document.querySelector("{0}")'
                          .format(self._course_term_selector))
                term, year = (self.driver.execute_script(script)
                              .get_attribute("data-term").split())
                year = int(year)
                if term.lower() == "winter":
                    date = date_and_time.split(",")[0].lower()
                    if "jan" in date or "feb" in date or "mar" in date:
                        year = year + 1
                date_time = ("{date} {year}, {time} {timezone}"
                             .format(date=date_and_time[3:].split(",")[0],
                                     year=year,
                                     time=date_and_time.split()[-1],
                                     timezone="CST"))
                return datetime.strptime(date_time, "%b %d %Y, %I:%M%p %Z")

            @property
            def progress(self):
                """Return the assignment progress status.

                :return: the student's progress on the assignment
                :rtype: str

                """
                return self.find_element(*self._status_locator).text

            @property
            def late_work(self):
                """Return the homework secondary status line.

                :return: the secondary status line text for homeworks
                :rtype: str

                """
                return self.find_element(*self._secondary_status_locator).text

            @property
            def lateness(self):
                """Return the assignment on time or late status.

                :return: whether the assignment is on time or late
                :rtype: str
                :raises ValueError: if the icon color for the clock does not
                    match the color for a late assignment or the color for a
                    late assignment with accepted work

                """
                try:
                    late = self.find_element(*self._lateness_locator)
                except NoSuchElementException:
                    return Tutor.ON_TIME
                icon = late.get_attribute('class')
                if 'exclamation-circle' in icon:
                    return Tutor.DUE_SOON
                elif 'clock' in icon:
                    color = icon.get_attribute('color')
                    if color == Tutor.LATE_COLOR:
                        return Tutor.LATE
                    elif color == Tutor.ACCEPTED_COLOR:
                        return Tutor.ACCEPTED_LATE
                    else:
                        error = ('"{color}" not {late} ({late_color}) '
                                 'nor {accepted} ({accepted_color})')
                        ValueError(
                            error.format(color=color,
                                         late=Tutor.LATE,
                                         late_color=Tutor.LATE_COLOR,
                                         accepted=Tutor.ACCEPTED_LATE,
                                         accepted_color=Tutor.ACCEPTED_COLOR))

        class Key(Region):
            """An icon and descriptor for assignment lateness."""

            _icon_locator = (By.CSS_SELECTOR, 'svg')

            @property
            def icon(self):
                """Return the key icon.

                :return: the guide icon
                :rtype: \
                    :py:class:`~selenium.webdriver.remote.webelement.WebElement`

                """
                return self.find_element(*self._icon_locator)

            @property
            def description(self):
                """Return the icon description.

                :return: the guide description for the icon
                :rtype: str

                """
                return self.root.text

    class Survey(Region):
        """A course research survey access card."""

        _title_locator = (By.CSS_SELECTOR, 'p:nth-child(2)')
        _content_locator = (By.CSS_SELECTOR, 'p')
        _button_locator = (By.CSS_SELECTOR, 'button')

        @property
        def title(self):
            """Return the survey title.

                :return: the survey title
                :rtype: str

                """
            title_text = self.find_element(*self._title_locator).text
            match = re.search(r'(["“][\w\ \.\-]+["”])', title_text)
            assert(match is not None), \
                'Survey title not located in "{0}"'.format(title_text)
            return match.group(0)[1:-1]

        @property
        def content(self):
            """Return the text content of the survey card.

                :return: the survey card text
                :rtype: str

                """
            content = [line.text
                       for line in self.find_elements(*self._content_locator)]
            return '\n'.join(list(content))

        def take_survey(self):
            """Click on the 'Take Survey' button.

                :return: the form for a research study
                :rtype: :py:class:`~pages.tutor.research.ResearchSurvey`

                """
            button = self.find_element(*self._button_locator)
            Utility.click_option(self.driver, element=button)
            from pages.tutor.survey import ResearchSurvey
            return go_to_(ResearchSurvey(self.driver, self.page.base_url))

    class Performance(Region):
        """The performance forecast sidebar."""

        _title_locator = (By.CSS_SELECTOR, '.h2')
        _empty_description_locator = (By.CSS_SELECTOR, '.actions-box p')
        _section_locator = (By.CSS_SELECTOR, '.section')
        _key_guide_locator = (By.CSS_SELECTOR, '.guide-key .item')
        _practice_weakest_locator = (By.CSS_SELECTOR, '.weakest')
        _view_full_forecast_locator = (
                                By.CSS_SELECTOR, '.view-performance-forecast')

        @property
        def title(self):
            """Return the forecast sidebar title.

                :return: the performance forecast sidebar title
                :rtype: str

                """
            return self.find_element(*self._title_locator).text

        @property
        def is_empty(self):
            """Return True if the forecast has not been populated.

                :return: ``True`` if the forecast is empty, else ``False``
                :rtype: bool

                """
            return 'empty' in self.root.get_attribute('class')

        @property
        def empty_description(self):
            """Return the forecast explanation if the sidebar is empty.

                :return: ``True`` if the forecast explanation is empty, else
                    ``False``
                :rtype: bool

                """
            if self.is_empty:
                lines = [
                    line.text for line
                    in self.find_elements(*self._empty_description_locator)]
                return "\n".join(list(lines))
            return ""

        @property
        def sections(self):
            """Access the section forecasts.

                :return: the list of sections in the recent forecast
                :rtype: list(:py:class:`~StudentCourse.Performance.Section`)
                :raises :py:class:`~utils.tutor.TutorException`: if the
                    recent topics forecast is empty

                """
            if self.is_empty:
                raise TutorException("Forecast is not populated")
            return [self.Section(self, section)
                    for section in self.find_elements(*self._section_locator)]

        @property
        def key_guide(self):
            """Access the color guide for the performance bars.

                :return: the color guide keys for the performance bars
                :rtype: list(:py:class:`~StudentCourse.Performance.Key`)

                """
            return [self.Key(self, guide)
                    for guide in self.find_elements(*self._key_guide_locator)]

        class Section(Region):
            """A recent performance forecast section information."""

            _section_number_locator = (By.CSS_SELECTOR, '.number')
            _section_title_locator = (By.CSS_SELECTOR, '.title')
            _no_data_locator = (By.CSS_SELECTOR, '.no-data')
            _progress_bar_locator = (By.CSS_SELECTOR, '.progress-bar')
            _clue_data_locator = (By.CSS_SELECTOR, 'li')
            _problem_count_locator = (By.CSS_SELECTOR, '.count')
            _practice_section_locator = (By.CSS_SELECTOR, 'button')

            @property
            def number(self):
                """Return the book chapter and section number.

                :return: book chapter and section number for the bar
                :rtype: str

                """
                return self.find_element(*self._section_number_locator).text

            @property
            def title(self):
                """Return the book section title.

                :return: the section title for the bar
                :rtype: str

                """
                return self.find_element(*self._section_title_locator).text

            @property
            def not_enough_data(self):
                """Return True if a forecast CLUE is not available.

                :return: ``True`` if not enough assessments have been worked
                    from the section to generate a BigLearn CLUe, else
                    ``False``
                :rtype: bool

                """
                return bool(self.find_elements(*self._no_data_locator))

            @property
            def practice_more(self):
                """Return the button text if a CLUE is not available.

                :return: the button text if a CLUe is not available for the
                    section or an empty string if the bar is displayed
                :rtype: str

                """
                if self.not_enough_data:
                    return self.find_element(*self._no_data_locator).text
                return ""

            @property
            def progress_bar(self):
                """Return the progress bar element.

                :return: the progress bar
                :rtype: \
                    :py:class:`~selenium.webdriver.remote.webelement.WebElement`

                """
                return self.find_element(*self._progress_bar_locator)

            @property
            def progress_data(self):
                """Return the progress bar data attributes.

                :return: the progress bar data attributes
                :rtype: dict(str, int or float)

                """
                bar = self.progress_bar
                return {
                    "minimum": int(bar.get_attribute("aria-valuemin")),
                    "value": int(bar.get_attribute("aria-valuenow")),
                    "maximum": int(bar.get_attribute("aria-valuemax")),
                    "width": float(bar.get_attribute("style")
                                   .split(": ")[-1].split("%")[0]), }

            @property
            def data(self):
                """Return the CLUE data values.

                :return: the CLUe data values
                :rtype: dict(str, float or bool or str)

                """
                options = list(
                    [line.text.split(": ")[-1]
                     for line in self.find_elements(*self._clue_data_locator)])
                return {
                    "minimum": float(options[0]),
                    "most_likely": float(options[1]),
                    "maximum": float(options[2]),
                    "is_real": options[3] == "true",
                    "uuid": options(4), }

            @property
            def worked(self):
                """Return the questions worked text.

                :return: the full text for the number of questions worked for
                    the section
                :rtype: str

                """
                return self.find_element(*self._problem_count_locator).text

            @property
            def count(self):
                """Return the number of questions worked.

                :return: the number of questions worked for the section
                :rtype: int

                """
                return int(self.worked.split()[0])

            def practice(self):
                """Request a practice session for this book section.

                :return: a practice session for the selected section
                :rtype: :py:class:`~pages.tutor.practice.Practice`

                """
                button = self.find_element(*self._practice_section_locator)
                Utility.click_option(self.driver, element=button)
                from pages.tutor.practice import Practice
                return go_to_(Practice(self.driver, self.page.page.base_url))

        class Key(Region):
            """The color guide for the performance forecast progress bars."""

            _color_locator = (By.CSS_SELECTOR, '.progress-bar')
            _title_locator = (By.CSS_SELECTOR, '.title')

            @property
            def progress_bar(self):
                """Return the progress bar color box.

                :return: the progress bar box
                :rtype: \
                    :py:class:`~selenium.webdriver.remote.webelement.WebElement`

                """
                return self.find_element(*self._color_locator)

            @property
            def color(self):
                """Return the bar color.

                :return: the color of the progress bar
                :rtype: str

                """
                script = ('return window.getComputedStyle(arguments[0])'
                          '.backgroundColor;')
                return self.driver.execute_script(script, self.progress_bar)

            @property
            def description(self):
                """Return the bar color description.

                :return: the description of the bar color
                :rtype: str

                """
                return self.find_element(*self._title_locator).text
