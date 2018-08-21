"""The Settings page object."""

from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase


class TutorSettings(TutorBase):
    """Tutor settings page object."""

    _edit_time_locator = (By.CSS_SELECTOR, 'div:nth-child(3) > button')
    _hawaii_time_locator = (By.CSS_SELECTOR, '#-hawaii')
    _confirm_time_locator = (By.CSS_SELECTOR, 'div.modal-footer > button')
    _edit_name_locator = (
        By.CSS_SELECTOR,
        'div.course-settings-title > button')
    _text_enter_locator = (By.CSS_SELECTOR, 'div > input')
    _confirm_name_locator = (By.CSS_SELECTOR, 'div.modal-footer > button')
    _url_locator = (By.CSS_SELECTOR, 'label:nth-child(3) > input')

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    def edit_time(self):
        """Edit the time zone."""
        self.find_element(*self._edit_time_locator).click()
        self.find_element(*self._hawaii_time_locator).click()
        self.find_element(*self._confirm_time_locator).click()

    def edit_course_name(self):
        """Edit course name."""
        self.find_element(*self._edit_name_locator).click()
        self.find_element(*self. _text_enter_locator).sendKeys("1")
        self.find_element(*self._confirm_name_locator).click()

    def get_access_url(self):
        """Get the student access url."""
        return self.find_element(*self._url_locator).get_attribute('value')
