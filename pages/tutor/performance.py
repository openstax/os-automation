"""The Performance Forecast page object."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from pages.tutor.course import TutorCourse


class TutorPerformance(TutorBase):
    """Tutor Performance page object."""

    _info_icon_locator = (By.CSS_SELECTOR, 'div.guide-group-title > button')
    _back_locator = (By.CSS_SELECTOR, 'div.info > a')

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    def get_info(self):
        """Hover over info icon"""
        self.find_element(*self._info_icon_locator).click()

    def back_to_dashboard(self):
        """Go back to dashboard"""
        self.find_element(*self._back_locator).click()
        return self
