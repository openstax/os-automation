"""The Payment page object."""

from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase


class TutorPayment(TutorBase):
    """Tutor Payment page object."""

    _invoice_locator = (By.CSS_SELECTOR, 'td:nth-child(5) > a')
    _support_locator = (
        By.CSS_SELECTOR,
        'div.manage-payments.container > div > div > a')
    _refund_locator = (
        By.CSS_SELECTOR,
        'div.manage-payments.container > div > a')

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    def invoice(self):
        """Go to invoice"""
        self.find_element(*self._invoice_locator).click()

    def contact_support(self):
        """Go to support page"""
        self.find_element(*self._support_locator).click()

    def refund_policy(self):
        """Go to refund policies"""
        self.find_element(*self._refund_locator).click()
