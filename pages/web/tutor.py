"""The OpenStax Tutor Beta marketing page."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.web.home import WebHome


class TutorMarketing(WebHome):
    """The Tutor marketing page."""

    URL_TEMPLATE = '/openstax-tutor'

    _student_viewer_locator = (By.CSS_SELECTOR, '.viewport img')
    _canvas_locator = (By.CSS_SELECTOR, '#particles canvas')

    @property
    def loaded(self):
        return (self.find_element(*self._student_viewer_locator).is_displayed
                and self.find_element(*self._canvas_locator).is_displayed)

    def wait_for_page_to_load(self):
        """Override the default wait because it is too short."""
        WebDriverWait(self.driver, 90).until(
            lambda _: self.loaded
        )
