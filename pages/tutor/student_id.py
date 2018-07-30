"""The Student ID page object."""

from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase


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

    def change_id(self, new_id):
        """Change the student id."""
        self.find_element(*self._enter_id_locator).sendKeys(new_id)
        self.find_element(*self._save_locator).click()

    def cancel_id(self, new_id):
        """Cancel changing student id"""
        self.find_element(*self._enter_id_locator).sendKeys(new_id)
        self.find_element(*self._cancel_locator).click()
