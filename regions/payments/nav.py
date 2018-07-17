"""OpenStax payment nav bar region object."""

from pypom import Region
from selenium.webdriver.common.by import By


class PaymentsNav(Region):
    """OpenStax payment nav bar region object."""

    _root_locator = (By.ID, 'header')
    _logo_locator = (By.ID, 'branding')
    _view_site_locator = (By.PARTIAL_LINK_TEXT, 'SITE')
    _log_out_locator = (By.PARTIAL_LINK_TEXT, 'OUT')

    def click_logo(self):
        self.find_element(*self._logo_locator).click()
        from pages.payments.home import PaymentsHome
        return PaymentsHome(self.driver)

    def log_out(self):
        self.find_element(*self._log_out_locator).click()
        from pages.payments.logout import PaymentsLogOut
        return PaymentsLogOut(self.driver)
