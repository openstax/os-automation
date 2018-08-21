"""The New Course page object."""

from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase


class TutorNewCourse(TutorBase):
    """Tutor create new course page object."""

    _continue_locator = (By.CSS_SELECTOR, 'button.next.btn.btn-primary')
    _select_course_locator = (
        By.CSS_SELECTOR,
        'div.list-group-item.choice.active')
    _select_semester_locator = (
        By.CSS_SELECTOR,
        'div.panel-body > div > div > div:nth-child(1)')
    _estimated_number_locator = (By.CSS_SELECTOR,
                                 'div.course-details-numbers.form-group input')
    _cancel_locator = (By.CSS_SELECTOR, 'button.cancel.btn.btn-default')
    _close_locator = (By.PARTIAL_LINK_TEXT, "I'll get them later")
    _get_locator = (By.PARTIAL_LINK_TEXT, "Got It")

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    def create_new_course(self):
        """Create a new course."""
        return NotImplemented
