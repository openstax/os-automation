"""The teacher calendar page object."""

from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from pages.tutor.question_library import TutorQuestionLibrary
from pages.tutor.scores import TutorScores
from pages.tutor.performance import TutorPerformance


class TutorCalendar(TutorBase):
    """Tutor calendar page object."""
    _browse_locator = (By.PARTIAL_LINK_TEXT, 'Browse the Book')
    _library_locator = (By.PARTIAL_LINK_TEXT, 'Question Library')
    _forecast_locator = (By.PARTIAL_LINK_TEXT, 'Performance Forecast')
    _scores_locator = (By.PARTIAL_LINK_TEXT, 'Student Scores')
    _add_locator = (By.CSS_SELECTOR, 'div > button')
    _reading_locator = (
        By.CSS_SELECTOR,
        '#sidebar-add-reading-assignment > div > a')
    _hw_locator = (By.CSS_SELECTOR, '#sidebar-add-homework-assignment > div')
    _ex_locator = (
        By.CSS_SELECTOR,
        '#sidebar-add-external-assignment > div > a')
    _name_locator = (By.CSS_SELECTOR, '#reading-title')
    _date_locator = (By.CLASS_NAME, 'form-control empty')
    _date_select_locator = (
        By.CSS_SELECTOR,
        'div:nth-child(5) > div:nth-child(3)')
    _add_reading_locator = (By.CSS_SELECTOR, '#reading-select')
    _add_question_locator = (By.CSS_SELECTOR, '#problems-select')
    _check_locator = (By.CSS_SELECTOR, 'span.chapter-checkbox > span')
    _confirm_locator = (
        By.CSS_SELECTOR,
        'button.-show-problems.btn.btn-primary')
    _publish_locator = (By.CSS_SELECTOR, '#builder-save-button > button')
    _draft_locator = (By.CSS_SELECTOR, '#builder-draft-button > button')
    _cancel_locator = (By.CSS_SELECTOR, '#builder-cancel-button > button')
    _show_question_locator = (
        By.CSS_SELECTOR,
        'button.show-problems.btn.btn-primary')
    _add_lib_question_locator = (By.CSS_SELECTOR, 'div.action.include > span')
    _next_locator = (
        By.CSS_SELECTOR,
        'button.review-exercises.btn.btn-primary')
    _url_locator = (By.CSS_SELECTOR, '#external-url')

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    def browse_the_book(self):
        """Browse the book."""
        self.find_element(*self._browse_locator).click()

    def performance_forecast(self):
        """Performance forecast."""
        self.find_element(*self._forecast_locator).click()
        return TutorPerformance(self.driver)

    def question_library(self):
        """Question Library."""
        self.find_element(*self._library_locator).click()
        return TutorQuestionLibrary(self.driver)

    def student_scores(self):
        """Go to student scores."""
        self.find_element(*self._scores_locator).click()
        return TutorScores(self.driver)

    def add_reading(self, assignment_name):
        """Add an reading."""
        self.find_element(*self._add_locator).click()
        self.find_element(*self._reading_locator).click()
        self.find_element(*self._name_locator).sendKeys(assignment_name)
        self.find_element(*self._date_locator).click()
        self.find_element(*self._date_select_locator).click()
        self.find_element(*self._add_reading_locator).click()
        self.find_element(*self._check_locator).click()
        self.find_element(*self._confirm_locator).click()
        self.find_element(*self._publish_locator).click()

    def draft_reading(self, assignment_name):
        """Add a reading draft"""
        self.find_element(*self._add_locator).click()
        self.find_element(*self._reading_locator).click()
        self.find_element(*self._name_locator).sendKeys(assignment_name)
        self.find_element(*self._date_locator).click()
        self.find_element(*self._date_select_locator).click()
        self.find_element(*self._add_reading_locator).click()
        self.find_element(*self._check_locator).click()
        self.find_element(*self._confirm_locator).click()
        self.find_element(*self._draft_locator).click()

    def cancel_reading(self):
        """Cancel adding a reading"""
        self.find_element(*self._add_locator).click()
        self.find_element(*self._reading_locator).click()
        self.find_element(*self._cancel_locator).click()

    def add_hw(self, assignment_name):
        """Add a hw."""
        self.find_element(*self._add_locator).click()
        self.find_element(*self._hw_locator).click()
        self.find_element(*self._name_locator).sendKeys(assignment_name)
        self.find_element(*self._date_locator).click()
        self.find_element(*self._date_select_locator).click()
        self.find_element(*self._add_question_locator).click()
        self.find_element(*self._check_locator).click()
        self.find_element(*self._show_question_locator).click()
        self.find_element(*self._add_lib_question_locator).click()
        self.find_element(*self._next_locator).click()
        self.find_element(*self._publish_locator).click()

    def draft_hw(self, assignment_name):
        """Save a hw as draft."""
        self.find_element(*self._add_locator).click()
        self.find_element(*self._hw_locator).click()
        self.find_element(*self._name_locator).sendKeys(assignment_name)
        self.find_element(*self._date_locator).click()
        self.find_element(*self._date_select_locator).click()
        self.find_element(*self._add_question_locator).click()
        self.find_element(*self._check_locator).click()
        self.find_element(*self._show_question_locator).click()
        self.find_element(*self._add_lib_question_locator).click()
        self.find_element(*self._next_locator).click()
        self.find_element(*self._draft_locator).click()

    def add_external(self, assignment_name, url):
        """Add an external assignment."""
        self.find_element(*self._add_locator).click()
        self.find_element(*self._ex_locator).click()
        self.find_element(*self._name_locator).sendKeys(assignment_name)
        self.find_element(*self._date_locator).click()
        self.find_element(*self._date_select_locator).click()
        self.find_element(*self._url_locator).sendKeys(url)
        self.find_element(*self._publish_locator).click()

    def draft_external(self, assignment_name, url):
        """Save an external assignment as draft."""
        self.find_element(*self._add_locator).click()
        self.find_element(*self._ex_locator).click()
        self.find_element(*self._name_locator).sendKeys(assignment_name)
        self.find_element(*self._date_locator).click()
        self.find_element(*self._date_select_locator).click()
        self.find_element(*self._url_locator).sendKeys(url)
        self.find_element(*self._draft_locator).click()

    def cancel_external(self):
        """Cancel creating an external assignment."""
        self.find_element(*self._add_locator).click()
        self.find_element(*self._ex_locator).click()
        self.find_element(*self._cancel_locator).click()

    def add_event(self, assignment_name):
        """Add an event."""
        self.find_element(*self._add_locator).click()
        self.find_element(*self._ex_locator).click()
        self.find_element(*self._name_locator).sendKeys(assignment_name)
        self.find_element(*self._date_locator).click()
        self.find_element(*self._date_select_locator).click()
        self.find_element(*self._publish_locator).click()

    def draft_event(self, assignment_name):
        """Add an event as draft."""
        self.find_element(*self._add_locator).click()
        self.find_element(*self._ex_locator).click()
        self.find_element(*self._name_locator).sendKeys(assignment_name)
        self.find_element(*self._date_locator).click()
        self.find_element(*self._date_select_locator).click()
        self.find_element(*self._draft_locator).click()

    def cancel_event(self):
        """Cancel creating an event."""
        self.find_element(*self._add_locator).click()
        self.find_element(*self._ex_locator).click()
        self.find_element(*self._cancel_locator).click()
