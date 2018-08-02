"""The Question Library page object."""

from pypom import Region
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from pages.tutor.base import TutorBase


class TutorQuestionLibrary(TutorBase):
    """Question library page object."""

    _back_locator = (By.CSS_SELECTOR, '.header .btn')
    _cancel_locator = (By.CSS_SELECTOR, 'button.cancel')
    _show_question_btn_locator = (By.CSS_SELECTOR, 'button.btn-primary')
    _chapter_locator = (By.CSS_SELECTOR, '[role="tablist"]')
    _question_locator = (By.CSS_SELECTOR, '#exercise-preview')
    _select_locator = (By.CSS_SELECTOR, 'div.pinned-header > div > button')

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    @property
    def chapters(self):
        """Return a list of all the chapters."""
        return [self.Chapter(self, element) for element in
                self.find_elements(*self._chapter_locator)]

    @property
    def questions(self):
        """Return the Question Region after clicking show questions."""
        return [self.Question(self, element) for element in
                self.find_elements(*self._question_locator)]

    def click_back(self):
        """Go back to dashboard/scores/etc."""
        self.find_element(*self._back_locator).click()

    def click_show_questions(self):
        """Show questions for question library."""
        self.find_element(*self._show_question_btn_locator).click()

    def click_cancel(self):
        """Click cancel button to cancel selection."""
        self.find_element(*self._cancel_locator)

    class Chapter(Region):
        """Chapter list of question library."""

        _panel_locator = (By.CSS_SELECTOR, '.panel')
        _checkbox_locator = (By.CSS_SELECTOR, '.chapter-checkbox i')
        _section_locator = (By.CSS_SELECTOR, '.in .section')
        _browse_locator = (By.CSS_SELECTOR, '.browse-the-book')

        def expand_chapter(self):
            """Click to expand the current chapter."""
            self.find_element(*self._panel_locator).click()

        def select_chapter(self):
            """Select current chapter."""
            self.find_element(*self._checkbox_locator).click()

        def browse_book(self):
            """Browse the book of current chapter."""
            self.find_element(*self._browse_locator).click()

        def sections(self):
            """Return a list of the sections."""
            try:
                self.find_element(*self._section_locator)
            except NoSuchElementException:
                self.expand_chapter()
            return [self.Section(self, element) for element in
                    self.find_elements(*self._section_locator)]

        class Section(Region):
            """The sections in a chapter."""

            _checkbox_locator = (By.CSS_SELECTOR, '.section-checkbox input')

            def select_section(self):
                """Select current session."""
                self.find_element(*self._checkbox_locator).click()

    class Question(Region):
        """Show questions for the question library."""

        _detail_locator = (By.CSS_SELECTOR, 'div > div.action.details')
        _exclude_locator = (By.CSS_SELECTOR, 'div.action.exclude > span')

        def select_more_questions(self):
            """Select more questions."""
            self.find_element(*self._select_locator).click()

        def show_question_details(self):
            """Show question details."""
            self.find_element(*self._detail_locator).click()

        def exclude_questions(self):
            """Exclude Questions."""
            self.find_element(*self._exclude_locator).click()
