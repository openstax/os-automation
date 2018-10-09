"""The OpenStax marketing newsletter signup form."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility


class NewsletterSignup(WebBase):
    """The newsletter signup form."""

    URL_TEMPLATE = 'http://www2.openstax.org/l/218812/2016-10-04/lvk'

    _form_root_locator = (By.CSS_SELECTOR, '#pardot-form')
    _logo_locator = (By.CSS_SELECTOR, 'img')

    @property
    def loaded(self):
        """Return True when the form is displayed."""
        return (Utility.is_image_visible(driver=self.driver,
                                         locator=self._logo_locator) and
                self.find_element(*self._form_root_locator).is_displayed())

    def is_displayed(self):
        """Return True if the form is displayed."""
        return self.find_element(*self._form_root_locator).is_displayed()
