"""The interest form page."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Interest(WebBase):
    """The book interest form."""

    URL_TEMPLATE = '/interest'

    _loaded_locator = (By.CLASS_NAME, 'page-loaded')
    _drop_down_menu_locator = (By.CLASS_NAME, 'proxy-select')
    _adoption_form_link_locator = (By.CSS_SELECTOR, '[href$=adoption]')

    @property
    def loaded(self):
        """Wait until the form is displayed."""
        return (self.find_element(*self._loaded_locator).is_displayed() and
                self.find_element(*self._drop_down_menu_locator).is_displayed()
                )

    def is_displayed(self):
        """Return True if the interest form is displayed."""
        try:
            return self.loaded
        except Exception:
            return False
