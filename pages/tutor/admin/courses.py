"""The admin course page object."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.admin.base import TutorAdminBase


class TutorAdminCourse(TutorAdminBase):
    """Tutor admin course page object."""

    _edit_locator = (By.CSS_SELECTOR, 'a:nth-child(2)')
    _year_locator = (By.CSS_SELECTOR, '#course_year')
    _save_locator = (By.CSS_SELECTOR, '#edit-save')
    _name_locator = (By.CSS_SELECTOR, '#course_name')
    _add_locator = (By.CSS_SELECTOR, 'body > div > a')
    _imcomplete_locator = (By.CSS_SELECTOR,
                           'body > div > ul > li:nth-child(2) > a')
    _fail_locator = (By.CSS_SELECTOR, 'body > div > ul > li:nth-child(3) > a')

    def edit_course(self):
        """Edit a course."""
        self.find_element(*self._edit_locator).click()
        self.find_element(*self._year_locator).clear()
        self.find_element(*self._year_locator).send_keys('2016')
        self.find_element(*self._save_locator).click()

    def add_course_to_imcomplete(self):
        """Add an course to imcomplete ecosystem."""
        self.find_element(*self._imcomplete_locator).click()
        self.find_element(*self._add_locator).click()
        self.find_element(*self._imcomplete_locator).sendKeys('course')
        self.find_element(*self._save_locator).click()

    def add_course_to_failed(self):
        """Add course to failed ecosystem."""
        self.find_element(*self._fail_locator).click()
        self.find_element(*self._add_locator).click()
        self.find_element(*self._fail_locator).send_keys('course')
        self.find_element(*self._save_locator).click()
