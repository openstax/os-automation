"""The book adoption form."""

from time import sleep

from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class Adoption(WebBase):
    """The adoption form."""

    URL_TEMPLATE = '/adoption'

    _loaded_locator = (By.CLASS_NAME, 'page-loaded')
    _drop_down_menu_locator = (By.CLASS_NAME, 'proxy-select')
    _interest_form_link_locator = (By.CSS_SELECTOR, '[href$=interest]')

    @property
    def loaded(self):
        """Wait until the form is displayed."""
        return (self.find_element(*self._loaded_locator).is_displayed and
                self.find_element(*self._drop_down_menu_locator).is_displayed)

    def go_to_interest(self):
        """Switch to the interest form."""
        self.wait.until(
            lambda _: self.find_element(*self._interest_form_link_locator)
        ).click()
        sleep(1.0)
        from pages.web.interest import Interest
        return Interest(self.driver)


class AdoptionConfirmation(WebBase):
    """The adoption confirmation page."""

    URL_TEMPLATE = '/adoption-confirmation'

    _confirmation_locator = (By.CLASS_NAME, 'adoption-confirmation')

    @property
    def loaded(self):
        """Wait until the confirmation is displayed."""
        return self.find_element(*self._confirmation_locator).is_displayed
