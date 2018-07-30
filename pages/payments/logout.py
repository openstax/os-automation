"""OpenStax payment log out transition page object."""

from selenium.webdriver.common.by import By

from pages.payments.base import PaymentsBase
from pages.payments.login import PaymentsLogin


class PaymentsLogOut(PaymentsBase):
    """OpenStax payment log out transition page object."""

    _log_in_again_btn_locator = (By.PARTIAL_LINK_TEXT, 'again')

    def click_log_in_again(self):
        """Click the log in again button to return to log in page."""
        self.find_element(*self._log_in_again_btn_locator).click()
        return PaymentsLogin(self.driver)
