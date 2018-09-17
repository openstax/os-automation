"""The book adoption form."""

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Adoption(WebBase):
    """The adoption form."""

    URL_TEMPLATE = '/adoption'

    _loaded_locator = (By.CLASS_NAME, 'page-loaded')
    _drop_down_menu_locator = (By.CLASS_NAME, 'proxy-select')

    @property
    def loaded(self):
        """Wait until the form is displayed."""
        return (self.find_element(*self._loaded_locator).is_displayed and
                self.find_element(*self._drop_down_menu_locator).is_displayed)


class AdoptionConfirmation(WebBase):
    """The adoption confirmation page."""

    URL_TEMPLATE = '/adoption-confirmation'

    _confirmation_locator = (By.CLASS_NAME, 'adoption-confirmation')

    @property
    def loaded(self):
        """Wait until the confirmation is displayed."""
        return self.find_element(*self._confirmation_locator).is_displayed
