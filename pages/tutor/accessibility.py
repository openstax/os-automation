"""The accessiblity page object."""

from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase


class TutorAccessibility(TutorBase):
    """Tutor accessibility page."""

    _back_locator = (By.CSS_SELECTOR, 'header > a')

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    def go_back(self):
        """Click the back btn to back to question library, scores, etc."""
        self.find_element(*self._back_locator).click()
