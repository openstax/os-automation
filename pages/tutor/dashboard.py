"""Dashboard objects"""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from pages.tutor.course import TutorCourse
from pages.accounts.home import AccountsHome


class TutorDashboard(TutorBase):

    URL_TEMPLATE = '/dashboard'
    _root_locator = (By.CLASS_NAME, 'tutor-root')

    @property
    def courses_region(self):
        return self.Courses(self)

    class Courses(Region):
        """Courses sections"""

        _root_locator = (By.CLASS_NAME, 'my-courses-current')
        _course_locator = (By.CSS_SELECTOR, '.my-courses-item-wrapper')

        @property
        def courses(self):
            """Return a list of course objects"""
            return [self.Course(self, element)
                    for element in self.find_elements(*self._course_locator)]

        class Course(Region):
            """Individual course cards"""

            _card_locator = (By.CSS_SELECTOR, '.my-courses-item-title')

            def go_to_course(self):
                self.find_element(*self._card_locator).click()
                return TutorCourse(self.driver)
