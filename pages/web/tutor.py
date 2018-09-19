"""The OpenStax Tutor Beta marketing page."""

from selenium.webdriver.common.by import By

from pages.web.home import WebHome


class TutorMarketing(WebHome):
    """The Tutor marketing page."""

    URL_TEMPLATE = '/openstax-tutor'

    _student_viewer_locator = (By.CSS_SELECTOR, '.viewport img')
    _canvas_locator = (By.CSS_SELECTOR, '#particles canvas')

    @property
    def loaded(self):
        """Override the base loader."""
        return (self.find_element(*self._student_viewer_locator).is_displayed()
                and self.find_element(*self._canvas_locator).is_displayed())
