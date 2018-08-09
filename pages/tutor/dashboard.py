"""The dashboard (course picker) page object."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from pages.tutor.tutor_calendar import TutorCalendar


class TutorDashboard(TutorBase):
    """Tutor dashboard page object."""

    URL_TEMPLATE = '/dashboard'

    _root_locator = (By.CLASS_NAME, 'tutor-root')

    @property
    def courses_region(self):
        """Return all courses region."""
        return self.Courses(self)

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    def go_to_first_course(self, user):
        """Go to the first course."""
        self.courses_region.courses[0].go_to_course()
        return TutorCalendar(self.driver)

    class Courses(Region):
        """Courses sections."""

        _root_locator = (By.CLASS_NAME, 'my-courses-current')
        _course_locator = (By.CSS_SELECTOR, '.my-courses-item-wrapper')

        @property
        def courses(self):
            """Return a list of course objects."""
            return [self.Course(self, element)
                    for element in self.find_elements(*self._course_locator)]

        class Course(Region):
            """Individual course cards."""

            _card_locator = (By.CSS_SELECTOR, '.my-courses-item-title')

            def go_to_course(self):
                """Go to the course page for this course."""
                self.find_element(*self._card_locator).click()
                return TutorCalendar(self.driver)

