"""The Student ID page object."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from pages.tutor.course import TutorCourse


class TutorID(TutorBase):
    """Student ID page object."""

    _enter_id_locator = (By.CSS_SELECTOR, 'div.inputs > input')
    _save_locator = (By.CSS_SELECTOR, 'button.btn.btn-success.btn.btn-primary')
    _cancel_locator = (By.CSS_SELECTOR, 'button.cancel.btn.btn-link')

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    def change_id(self):
        """Change the student id."""
        self.find_element(*self._enter_id_locator).sendKeys('111111')
        self.find_element(*self._save_locator).click()

    def cancel_id(self):
        """Cancel changing student id"""
        self.find_element(*self._enter_id_locator).sendKeys('111111')
        self.find_element(*self._cancel_locator).click()
