"""The accessiblity page object."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from pages.tutor.course import TutorCourse


class TutorAccessibility(TutorBase):
    """Tutor accessiblity page."""

    _back_locator = (By.CSS_SELECTOR, 'header > a')

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    def go_to_library(self):
        """Go back to question library"""
        self.find_element(*self._back_locator).click()
        return self
