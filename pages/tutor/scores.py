"""The Scores page object."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from pages.tutor.course import TutorCourse


class TutorScores(TutorBase):
    """Scores page object."""

    _change_display_locator = (By.CSS_SELECTOR, 'div > label:nth-child(2)')
    _export_locator = (By.CSS_SELECTOR, '#scores-export-button > button')
    _review_locator = (By.CSS_SELECTOR, 'span.review-link > a')

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    def change_display(self):
        """Change way of display"""
        self.find_element(*self._change_display_locator).click()

    def export_scores(self):
        """Export Scores as spreadsheet"""
        self.find_element(*self._export_locator).click()

    def review_assignment(self):
        """Review assignment"""
        self.find_element(*self._review_locator).click()

    def set_weight(self):
        """Set weight for scores"""
        return self.Set_weight(self)

    class Set_weight(Region):
        """The Set Weight Region."""

        _set_weight_locator = (
            By.CSS_SELECTOR,
            'div.overall-header-cell > div > a')
        _first_locator = (
            By.CSS_SELECTOR,
            'label:nth-child(1) input[type="number"]')
        _second_locator = (
            By.CSS_SELECTOR,
            'label:nth-child(2) input[type="number"]')
        _confirm_locator = (
            By.CSS_SELECTOR,
            'button.async-button.btn.btn-primary')
        _why_locator = (
            By.CSS_SELECTOR,
            'div.page-loading.loadable.is-loading.modal-body > a')

        def modify_weight(self):
            """Modify weights"""
            self.find_element(*self._set_weight_locator).click()
            self.find_element(*self._first_locator).clear()
            self.find_element(*self._first_locator).sendKeys('90')
            self.find_element(*self._second_locator).sendKeys('10')
            self.find_element(*self._confirm_locator).click()

        def see_why(self):
            """Go to the see why link"""
            self.find_element(*self._set_weight_locator).click()
            self.find_element(*self._why_locator).click()
