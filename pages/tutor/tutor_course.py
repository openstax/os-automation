"""Student calendar."""

from pypom import Page, Region
from selenium.webdriver.common.by import By


class TutorCourse(Page):
    """Tutor course page."""

    _banner_locator = (By.CLASS_NAME, "course-title-banner")
    _text_book_locator = (By.CLASS_NAME, 'browse-the-book')
    _past_work_locator = (By.XPATH, "//ul[contains(@class, 'nav')] /li[2]")

    def wait_for_page_to_load(self):
        """Wait until the page load."""
        self.wait.until(
            lambda _: self.find_element(*self._banner_locator).is_displayed())

    @property
    def weeks(self):
        """Pass main assignment dashboard."""
        return self.Weeks(self)

    @property
    def performance_forecast(self):
        """Pass performance forcast region."""
        return self.PerformanceForecast(self)

    def past_work(self):
        """Clicks the past_work tab."""
        self.find_element(*self._past_work_locator).click()
        return self

    class Weeks(Region):
        """The assignemnt dashboard."""

        _this_week_locator = (By.CLASS_NAME, "-this-week")
        _upcoming_locator = (By.CLASS_NAME, "-upcoming")
        _this_week_assignments_locator = (By.CSS_SELECTOR, '.-this-week .task')
        _upcoming_assignments_locator = (By.CSS_SELECTOR, '.-upcoming .task')

        def this_week_assignments(self):
            """Get all the this week's assignments."""
            return [self.Assignemnt(self, el)
                    for el in self.find_elements(
                        *self._this_week_assignments_locator)]

        def upcoming_assignments(self):
            """Get all the upcoming assignments."""
            return [self.Assignemnt(self, el)
                    for el in self.find_elements(
                        *self._upcoming_assignments_locator)]

        class Assignment(Region):
            """Individual assignment class."""

            _image_locator = (By.CLASS_NAME, "icon-lg")
            _chapter_locator = (By.CLASS_NAME, "col-sm-6")
            _progress_locator = (By.CLASS_NAME, "feedback")
            _due_date_locator = (By.CLASS_NAME, "due-at")

            def go_to_assignment(self):
                """Clicks the assignemnt."""
                self.find_element(*self._image_locator).click()
                return self

    class PerformanceForecast(Region):
        """Performance forcast region."""

        _practice_more_locator = (By.CLASS_NAME, "no-data")
        _weakest_topic_locator = (By.CLASS_NAME, "weakest")
        _view_all_topic_locator = (
            By.CSS_SELECTOR, 'button.view-performance-forecast')

        def practice_more(self):
            """Prcatice more buttons."""
            return self.find_elements(*self._practice_more_locator)

        def go_to_weakest_topic(self):
            """Weakest topic button."""
            self.find_element(*self._weakest_topic_locator).click()
            return self

        def go_to_view_all_topic_locator(self):
            """All topic button."""
            self.find_element(*self._view_all_topic_locator).click()
            return self
