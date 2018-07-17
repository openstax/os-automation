"""The roster page object."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from pages.tutor.course import TutorCourse


class TutorRoster(TutorBase):
    """Tutor roster page object."""

    @property
    def instructors(self):
        """The Instructors Region."""
        return self.Instructors(self)

    @property
    def section(self):
        """The Sections Region."""
        return self.Section(self)

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    class Instructors(Region):
        """The Instructors Region."""
        _add_locator = (
            By.CSS_SELECTOR,
            'div.settings-section.teachers > div > div > button')
        _remove_locator = (By.CSS_SELECTOR, 'td.actions > a')
        _confirm_locator = (By.CSS_SELECTOR, 'div.popover-content > button')

        def add_instructor(self):
            """Add an instructor."""
            self.find_element(*self._add_locator).click()
            return self

        def remove_instructor(self):
            """Remove an instructor."""
            self.find_element(*self._remove_locator).click()
            self.find_element(*self._confirm_locator).click()
            return self

    class Sections(Region):
        """The Sections Region."""
        _add_session_locator = (
            By.CSS_SELECTOR,
            'div.roster > div > nav > button')
        _enter_name_locator = (By.CSS_SELECTOR, 'div > input')
        _confirm_delete_session_locator = (
            By.CSS_SELECTOR, 'button.async-button.delete.btn.btn-danger')
        _confirm_rename_session_locator = (
            By.CSS_SELECTOR, 'div.modal-body > div > input')
        _confirm_add_locator = (By.CSS_SELECTOR, 'div.modal-footer > button')
        _remove_session_locator = (By.CSS_SELECTOR,
                                   'button.control.delete-period.btn.btn-link')
        _rename_session_locator = (By.CSS_SELECTOR,
                                   'button.control.rename-period.btn.btn-link')

        def add_session(self):
            """Add a session"""
            self.find_element(*self._add_session_locator).click()
            self.find_element(
                *self._enter_name_locator).sendKeys("section thera")
            self.find_element(*self._confirm_add_locator).click()

        def delete_session(self):
            """Delete a session."""
            self.find_element(*self._remove_session_locator).click()
            self.find_element(*self._confirm_delete_session_locator).click()

        def rename_session(self):
            """Rename a session"""
            self.find_element(*self._rename_session_locator).click()
            self.find_element(*self._confirm_rename_session_locator).click()
