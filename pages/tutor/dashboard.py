"""The dashboard (course picker) page object."""

from pypom import Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from utils.tutor import Tutor
from utils.utilities import Utility, go_to_


class Dashboard(TutorBase):
    """The OpenStax Tutor Beta dashboard."""

    URL_TEMPLATE = '/dashboard'

    _root_locator = (By.CLASS_NAME, 'tutor-root')
    _pending_verify_locator = (
                            By.CSS_SELECTOR, '.pending-faculty-verification')
    _create_tile_locator = (By.CSS_SELECTOR, '.my-courses-add-zone')
    _current_courses_locator = (By.CSS_SELECTOR, '.my-courses-current')
    _preview_courses_locator = (By.CSS_SELECTOR, '.my-courses-preview')
    _past_courses_locator = (By.CSS_SELECTOR, '.my-courses-past')

    @property
    def nav(self):
        """Access the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    @property
    def pending(self):
        """Access the pending verification section, if found."""
        try:
            root = self.find_element(*self._pending_verify_locator)
        except NoSuchElementException:
            return None
        return self.Pending(self, root)

    @property
    def current_courses(self):
        """Return the current courses section."""
        return self._get_section(self._current_courses_locator)

    def create_a_course(self):
        """Select the create course tile."""
        tile = self.find_elements(*self._create_tile_locator)
        assert(tile), (
            "Create a course tile not found - "
            "check user's faculty verification")
        link = tile[0].find_element(By.CSS_SELECTOR, 'a')
        Utility.scroll_to(self.driver, element=tile[0], shift=-80)
        Utility.click_option(self.driver, element=link)
        from pages.tutor.new_course import CloneCourse
        return go_to_(CloneCourse(self.driver, self.base_url))

    @property
    def preview_courses(self):
        """Return the preview courses section."""
        return self._get_section(self._preview_courses_locator)

    @property
    def past_courses(self):
        """Return the past courses section."""
        return self._get_section(self._past_courses_locator)

    @property
    def _get_section(self, locator):
        """Return the past courses section."""
        try:
            root = self.find_element(*locator)
        except NoSuchElementException:
            root = None
        cycle = locator[1].split('-')[-1]
        assert(root), "No {time} courses found".format(time=cycle)
        return Courses(self, root)

    def go_to_first_course(self):
        """Go to the first course."""
        course = self.courses_region.courses[0]
        is_teacher = course.is_teacher
        course.go_to_course()
        if is_teacher:
            from pages.tutor.calendar import Calendar
            return go_to_(Calendar(self.driver, self.base_url))
        from pages.tutor.course import StudentCourse
        return go_to_(StudentCourse(self.driver, self.base_url))

    class Pending(Region):
        """The pending faculty verification pane."""

        _title_locator = (By.CSS_SELECTOR, 'h4')
        _expanation_locator = (By.CSS_SELECTOR, '.lead')
        _chat_verify_locator = (By.CSS_SELECTOR, 'button')

        @property
        def title(self):
            """Return the pending title overlay text."""
            return self.find_element(*self._title_locator).text

        @property
        def explanation(self):
            """Return the explanation text."""
            return self.find_element(*self._expanation_locator).text

        @property
        def verify_button(self):
            """Return the verify now button."""
            return self.find_element(*self._chat_verify_locator)

        def verify_now(self):
            """Click the 'Verify now via chat' button."""
            Utility.switch_to(self.driver, element=self.verify_button)
            from pages.salesforce.chat import Chat
            return go_to_(Chat(self.driver))


class Courses(Region):
    """Courses sections."""

    _course_locator = (By.CSS_SELECTOR, '.my-courses-item-wrapper')

    @property
    def courses(self):
        """Return a list of course objects."""
        return [self.Course(self, element)
                for element in self.find_elements(*self._course_locator)]

    def select_course_by_name(self, name, ignore_case=False, latest=True):
        """Select a course by the course name.

        :param name: the course name to select
        :type name: str
        :param ignore_case: match the case-insensitive value
            default - use case-sensitive matching
        :type ignore_case: bool
        :param latest: use the most recent course in the option list
            default - select a random, matching course option
        :type latest: bool
        :returns: the calendar (teacher) or current week (student) page
            object for the selected course
        :rtype: pages.tutor.calendar.Calendar
            or pages.tutor.course.StudentCourse
        """
        return self._course_selection(
            Tutor.BY_TITLE, name, ignore_case, latest)

    def select_course_by_id(self, course_id):
        """Select a course by the course identification number.

        :param course_id: the course identification number to select
        :type course_id: str
        :returns: the calendar (teacher) or current week (student) page
            object for the selected course
        :rtype: pages.tutor.calendar.Calendar
            or pages.tutor.course.StudentCourse
        """
        return self._course_selection(Tutor.BY_ID, course_id)

    def select_course_by_subject(self, subject):
        """Select a random course by the book subject.

        :param subject: the course subject to select from
        :type subject: str
        :returns: the calendar (teacher) or current week (student) page
            object for the selected course
        :rtype: pages.tutor.calendar.Calendar
            or pages.tutor.course.StudentCourse
        """
        return self._course_selection(Tutor.BY_SUBJECT, subject)

    def select_course_by_term(self, term, year=None):
        """Select a random course by the term and year.

        :param term: the semester or quarter to select from
        :type term: str
        :param year: the 4-digit calendar year to select from
            default - use today's year
        :type year: str
        :returns: the calendar (teacher) or current week (student) page
            object for the selected course
        :rtype: pages.tutor.calendar.Calendar
            or pages.tutor.course.StudentCourse
        """
        if not year:
            from datetime import datetime
            year = datetime.now().year
        full_term = "{0} {1}".format(term, year)
        return self._course_selection(Tutor.BY_TERM, full_term)

    def _course_selection(self, option, value,
                          ignore_case=False, latest=False):
        """Select a specific or random course matching a particular option."""
        value = value.casefold() if ignore_case else value
        course_options = []
        for course in self.courses:
            if value == course._get_data_option(option):
                course_options.append(course)
        assert(course_options), \
            "No courses found for {0}:{1}".format(option, value)
        course = 0 if latest else Utility.random(end=len(course_options))
        return course_options[course].go_to_course()

    class Course(Region):
        """Individual course cards."""

        _course_info_locator = (By.CSS_SELECTOR, '[data-title]')
        _card_locator = (By.CSS_SELECTOR, '.my-courses-item-title')
        _preview_belt_locator = (By.CSS_SELECTOR, '.preview-belt p')
        _course_brand_locator = (By.CSS_SELECTOR, '.course-branding')
        _course_clone_locator = (By.CSS_SELECTOR, 'a')

        @property
        def course_info(self):
            """Return the course data element."""
            return self.find_element(*self._course_info_locator)

        @property
        def course_brand(self):
            """Return the course brand element."""
            return self.find_element(*self._course_brand_locator)

        @property
        def course_clone(self):
            """Return the course clone button."""
            return self.find_element(*self._course_clone_locator)

        @property
        def title(self):
            """Return the course title."""
            return self.course_info.get_attribute("data-title")

        @property
        def book_title(self):
            """Return the textbook title."""
            return self.course_info.get_attribute("data-book-title")

        @property
        def appearance(self):
            """Return the book tile appearance code."""
            return self.course_info.get_attribute("data-appearance")

        @property
        def is_preview(self):
            """Return True if the course is a preview course."""
            return (self.course_info
                    .get_attribute("data-is-preview").lower() == "true")

        @property
        def term(self):
            """Return the course term."""
            return self.course_info.get_attribute("data-term")

        @property
        def is_teacher(self):
            """Return True if the current user is a course instructor."""
            return (self.course_info
                    .get_attribute("data-is-teacher").lower() == "true")

        @property
        def course_id(self):
            """Return the course identification number."""
            return self.course_info.get_attribute("data-course-id")

        @property
        def course_type(self):
            """Return the course type.

            Most courses will be Tutor, but some Concept
            Coach courses may still show for old users.
            """
            return (self.course_info
                    .get_attribute("data-course-course-type"))

        def go_to_course(self):
            """Go to the course page for this course."""
            self.find_element(*self._card_locator).click()
            if self.is_teacher:
                from pages.tutor.calendar import Calendar
                return go_to_(Calendar(self.driver,
                                       self.page.page.base_url))
            from pages.tutor.course import StudentCourse
            return go_to_(StudentCourse(self.driver,
                                        self.page.page.base_url))

        def clone_course(self):
            """Clone the selected course."""
            assert(self.is_teacher), \
                "Only verified instructors may clone a course"
            assert(not self.is_preview), \
                "Preview courses may not be cloned"
            from selenium.webdriver.common.action_chains import ActionChains
            Utility.scroll_to(self.driver, element=self.root, shift=-80)
            ActionChains(self.driver) \
                .move_to_element(self.course_brand) \
                .pause(1) \
                .move_to_element(self.course_clone) \
                .click() \
                .perform()
            from pages.tutor.new_course import CloneCourse
            return go_to_(CloneCourse(self.driver, self.page.page.base_url))

        @property
        def preview_text(self):
            """Return the preview belt explanation text if found."""
            if self.is_preview:
                return self.find_element(*self._preview_belt_locator).text
            return ""

        def _get_data_option(self, option):
            """Return the property value by the option type."""
            if option == Tutor.BY_TITLE:
                return self.title
            elif option == Tutor.BY_SUBJECT:
                return self.book_title
            elif option == Tutor.BY_APPEARANCE:
                return self.appearance
            elif option == Tutor.IS_PREVIEW:
                return self.is_preview
            elif option == Tutor.BY_TERM:
                return self.term
            elif option == Tutor.IS_TEACHER:
                return self.is_teacher
            elif option == Tutor.BY_ID:
                return self.course_id
            elif option == Tutor.BY_TYPE:
                return self.course_type
            raise ValueError('"{option}" is not a valid course data selector'
                             .format(option=option))
