"""The admin school page object."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.admin.base import TutorAdminBase


class TutorAdminSchool(TutorAdminBase):
    """Tutor admin course page object."""

    _delete_locator = (By.CSS_SELECTOR, 'a.btn.btn-xs.btn-secondary')
    _edit_locator = (By.CSS_SELECTOR, 'a.btn.btn-xs.btn-primary')
    _name_locator = (By.CSS_SELECTOR, '#school_name')
    _save_locator = (By.CSS_SELECTOR, 'input.btn.btn-primary')
    _add_locator = (By.CSS_SELECTOR, 'body > div > a')

    def add_school(self):
        """Add a school."""
        self.find_element(*self._add_locator).click()
        self.find_element(*self._name_locator).sendKeys('hello')
        self.find_element(*self._save_locator).click()

    def delete_school(self):
        """Delete a school."""
        self.find_element(*self._delete_locator).click()
        self.driver.switch_to.alert.accept()

    def edit_school(self):
        """Edit a school."""
        self.find_element(*self._edit_locator).click()
        self.find_element(*self._name_locator).clear()
        self.find_element(*self._delete_locator).sendKeys('district')
        self.find_element(*self._save_locator).click()
