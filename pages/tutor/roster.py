"""The roster page object."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase


class TutorRoster(TutorBase):
    """Tutor roster page object."""

    _instructor_locator = (By.CSS_SELECTOR, '.teachers-table table')
    _add_locator = (By.CSS_SELECTOR, '.teachers-table .control')
    _link_locator = (By.CSS_SELECTOR, '.modal-body .copy-on-focus')

    @property
    def instructors(self):
        """The Instructors Region."""
        print(self.find_elements(*self._instructor_locator)[0]
              .get_attribute('innerHTML'))
        return [self.Instructor(self, el)
                for el in self.find_elements(*self._instructor_locator)]

    @property
    def section(self):
        """The Sections Region."""
        return self.Sections(self)

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    @property
    def get_instructor_link(self):
        """Add an instructor."""
        self.find_element(*self._add_locator).click()
        link = self.find_element(*self._link_locator)
        return link

    class Instructor(Region):
        """The Instructors Region."""

        _remove_locator = (By.CSS_SELECTOR, '.actions a')
        _confirm_locator = (By.CSS_SELECTOR, '.popover-content .btn')

        def remove_instructor(self):
            """Remove an instructor."""
            self.find_element(*self._remove_locator).click()
            self.find_element(*self._confirm_locator).click()
            return self

    class Sections(Region):
        """The Sections Region."""
        _add_session_locator = (By.CSS_SELECTOR, '.periods .add-period')
        _enter_name_locator = (By.CSS_SELECTOR, 'div > input')
        _confirm_delete_locator = (By.CSS_SELECTOR, '.modal-footer .delete')
        _confirm_add_locator = (By.CSS_SELECTOR, '.modal-footer button')
        _remove_session_locator = (By.CSS_SELECTOR, '.periods .delete-period')
        _rename_session_locator = (By.CSS_SELECTOR, '.periods .rename-period')

        def add_session(self, section_name):
            """Add a session"""
            self.find_element(*self._add_session_locator).click()
            self.find_element(*self._enter_name_locator).sendKeys(section_name)
            self.find_element(*self._confirm_add_locator).click()

        def delete_session(self):
            """Delete a session."""
            self.find_element(*self._remove_session_locator).click()
            self.find_element(*self._confirm_delete_locator).click()

        def rename_session(self, section_name):
            """Rename a session"""
            self.find_element(*self._rename_session_locator).click()
            self.find_element(*self._enter_name_locator).sendKeys(section_name)
            self.find_element(*self._confirm_add_locator).click()
