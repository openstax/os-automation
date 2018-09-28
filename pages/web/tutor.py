"""The OpenStax Tutor Beta marketing page."""

from time import sleep

from selenium.webdriver.common.by import By

from pages.web.home import WebHome
from utils.utilities import Utility


class TutorMarketing(WebHome):
    """The Tutor marketing page."""

    URL_TEMPLATE = '/openstax-tutor'

    _image_locator = (By.CSS_SELECTOR, '.viewport img')
    _canvas_locator = (By.CSS_SELECTOR, '#particles canvas')
    _mountains_locator = (By.CLASS_NAME, 'middle-image')
    _image_locators = (By.CSS_SELECTOR, '#main img')

    @property
    def loaded(self):
        """Override the base loader."""
        sleep(1.0)
        visible = Utility.is_image_visible(
            self.driver,
            locator=self._image_locators)
        return visible

    def is_displayed(self):
        """Return True if the marketing page is displayed."""
        if self.URL_TEMPLATE not in self.location:
            return False
        return self.loaded
