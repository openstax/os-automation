"""The Question Library page object."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from pages.tutor.course import TutorCourse


class TutorQuestionLibrary(TutorBase):
    """Question library page object."""

    _back_locator = (By.CSS_SELECTOR, 'div.header > div > a')
    _browse_locator = (By.CSS_SELECTOR, 'div.panel-heading > div > a > div')

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    def show_questions(self):
        """Show questions for question library"""
        return self.Show_questions(self)

    def browse_chapter(self):
        """Browse the entire chapter"""
        self.find_element(*self._browse_locator).click()
        return self

    def back_to_dashboard(self):
        """Go back to dashboard"""
        self.find_element(*self._back_locator).click()
        return self

    def select_a_chapter(self):
        """Select a chapter"""
        _chapter_locator = (By.CSS_SELECTOR, 'span > i')
        self.find_element(*self._chapter_locator).click()

    class Show_questions(Region):
        """Show questions for the question library"""

        _show_locator = (By.CSS_SELECTOR, 'div > button.btn.btn-primary')
        _select_locator = (By.CSS_SELECTOR, 'div.pinned-header > div > button')
        _detail_locator = (By.CSS_SELECTOR, 'div > div.action.details')
        _exclude_locator = (By.CSS_SELECTOR, 'div.action.exclude > span')

        def select_more_questions(self):
            """Select more questions"""
            self.find_element(*self._select_locator).click()

        def show_question_details(self):
            """Show question details"""
            self.find_element(*self._detail_locator).click()

        def exclude_questions(self):
            """Exclude Questions"""
            self.find_element(*self._exclude_locator).click()
