"""The admin district page object."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.admin.base import TutorAdminBase


class TutorAdminDistrict(TutorAdminBase):
    """Tutor admin course page object."""

    _delete_locator = (By.CSS_SELECTOR, 'a.btn.btn-xs.btn-secondary')
    _edit_locator = (By.CSS_SELECTOR, 'a.btn.btn-xs.btn-primary')
    _name_locator = (By.CSS_SELECTOR, '#district_name')
    _save_locator = (By.CSS_SELECTOR, 'input.btn.btn-primary')
    _add_locator = (By.CSS_SELECTOR, 'body > div > a')

    def delete_district(self):
        """Delete a district."""
        self.find_element(*self._delete_locator).click()
        self.driver.switch_to.alert.accept()

    def edit_district(self):
        """Edit a district."""
        self.find_element(*self._edit_locator).click()
        self.find_element(*self._name_locator).clear()
        self.find_element(*self._delete_locator).sendKeys('district')
        self.find_element(*self._save_locator).click()

    def add_district(self):
        """Add a district."""
        self.find_element(*self._add_locator).click()
        self.find_element(*self._name_locator).sendKeys('district')
        self.find_element(*self._save_locator).click()
