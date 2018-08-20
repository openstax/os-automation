"""The Scores page object."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase


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
        """Change display."""
        self.find_element(*self._change_display_locator).click()

    def export_scores(self):
        """Export student scores as a spreadsheet."""
        self.find_element(*self._export_locator).click()

    def review_assignment(self):
        """Review an assignment."""
        self.find_element(*self._review_locator).click()

    def set_weight(self):
        """Set score weights."""
        return self.SetWeight(self)

    class SetWeight(Region):
        """Set weights."""

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
            """Modify weights."""
            return NotImplemented

        def see_why(self):
            """Click the See why link."""
            self.find_element(*self._set_weight_locator).click()
            self.find_element(*self._why_locator).click()
