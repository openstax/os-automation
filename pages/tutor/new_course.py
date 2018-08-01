"""The New Course page object."""

from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect


from pages.tutor.base import TutorBase
from pages.tutor.tutor_calendar import TutorCalendar


class TutorNewCourse(TutorBase):
    """Tutor create new course page object."""

    _continue_locator = (By.CSS_SELECTOR, '.controls .next')
    _select_course_locator = (By.CSS_SELECTOR,
                              '.choices-listing [role="button"]')
    _select_semester_locator = (By.CSS_SELECTOR,
                                '.choices-listing [role="button"]')
    _estimated_number_locator = (By.CSS_SELECTOR,
                                 '.course-details-numbers input')
    _cancel_locator = (By.CSS_SELECTOR, 'button.cancel.btn.btn-default')
    _close_locator = (By.CSS_SELECTOR, "div.joyride-tooltip__footer")
    _got_it_locator = (By.CSS_SELECTOR, 'button.joyride-tooltip__close')

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    def create_new_course(self):
        """Create a new course"""
        self.wait.until(
            expect.presence_of_element_located(
                self._select_course_locator)).click()
        self.find_element(*self._continue_locator).click()
        self.find_element(*self._select_semester_locator).click()
        self.find_element(*self._continue_locator).click()
        self.find_element(*self._continue_locator).click()
        self.find_element(*self._continue_locator).click()
        self.find_element(*self._estimated_number_locator).send_keys('1')
        self.find_element(*self._continue_locator).click()
        self.wait.until(
            expect.presence_of_element_located(self._close_locator)).click()
        sleep(1)
        self.wait.until(
            expect.presence_of_element_located(self._got_it_locator)).click()
        return TutorCalendar(self.driver)

    def cancel_create_course(self):
        """Cancel creating a new course"""
        self.find_element(*self._select_course_locator).click()
        self.find_element(*self._cancel_locator).click()

    def create_course_without_student_amount(self):
        """Attempt to create course without entering student amount"""
        self.find_element(*self._select_course_locator).click()
        self.find_element(*self._continue_locator).click()
        self.find_element(*self._select_semester_locator).click()
        self.find_element(*self._continue_locator).click()
        self.find_element(*self._continue_locator).click()
        self.find_element(*self._continue_locator).click()
        self.find_element(*self._continue_locator).click()

