"""The New Course page object."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from pages.tutor.course import TutorCourse


class TutorNewCourse(TutorBase):
    """Tutor newcourse page object."""

    _continue_locator = (By.CSS_SELECTOR, 'button.next.btn.btn-primary')
    _select_course_locator = (
        By.CSS_SELECTOR,
        'div.list-group-item.choice.active')
    _select_semester_locator = (
        By.CSS_SELECTOR,
        'div.panel-body > div > div > div:nth-child(1)')
    _estimated_number_locator = (By.CSS_SELECTOR,
                                 'div.course-details-numbers.form-group input')
    _cancel_locator = (By.CSS_SELECTOR, 'button.cancel.btn.btn-default')
    _close_locator = (By.PARTIAL_LINK_TEXT, "I'll get them later")
    _get_locator = (By.PARTIAL_LINK_TEXT, "Got It")


    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    def create_new_course(self):
        """Create a new course"""
        self.find_element(*self._select_course_locator).click()
        self.find_element(*self._continue_locator).click()
        self.find_element(*self._select_semester_locator).click()
        self.find_element(*self._continue_locator).click()
        self.find_element(*self._continue_locator).click()
        self.find_element(*self._continue_locator).click()
        self.find_element(*self._estimated_number_locator).sendKeys("1")
        self.find_element(*self._continue_locator).click()
        self.find_element(*self._close_locator).click()
        self.find_element(*self._get_locator).click()
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

