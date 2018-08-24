"""OpenStax payment login page object."""

from time import sleep

from selenium.webdriver.common.by import By

from pages.accounts.home import AccountsHome
from pages.payments.base import PaymentsBase
from pages.payments.home import PaymentsHome


class PaymentsLogin(PaymentsBase):
    """OpenStax payment login page object."""

    _os_btn_locator = (By.PARTIAL_LINK_TEXT, "OSAccounts")

    def login_with_osa(self, username, password):
        """Login with an os account."""
        self.find_element(*self._os_btn_locator).click()
        sleep(1.0)
        accounts = AccountsHome(self.driver)
        accounts.service_log_in(username, password)
        sleep(1.0)
        return PaymentsHome(self.driver)
