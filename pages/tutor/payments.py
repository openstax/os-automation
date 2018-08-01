"""The Payment page object."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from pages.utils.utilities import Utility


class TutorPayment(TutorBase):
    """Tutor Payment page object."""

    _item_locator = (By.CSS_SELECTOR, 'div.manage-payments')
    _support_locator = (By.PARTIAL_LINK_TEXT, 'Contact Support')
    _refund_policy_locator = (By.CLASS_NAME, 'refund-policy')

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    def contact_support(self):
        """Go to support page"""
        self.find_element(*self._support_locator).click()

    def refund_policy(self):
        """Go to refund policies"""
        self.find_element(*self._refund_policy_locator).click()

    @property
    def items(self):
        print(self.find_elements(*self._support_locator))
        print(self.find_elements(*self._refund_policy_locator))
        print(self.find_element(*self._item_locator).get_attribute(
            'innerHTML'))
        Utility.scroll_to(self.driver, self._item_locator)
        return [self.Item(self, element) for element in
                self.find_elements(*self._item_locator)]

    @property
    def get_latest_order(self):
        print(self.items)
        print(len(self.items))
        return self.items[-1]

    class Item(Region):

        _invoice_locator = (By.CSS_SELECTOR, '.btn-link')
        _refund_locator = (By.CSS_SELECTOR, '.refund button')
        _continue_locator = (By.CSS_SELECTOR, '.modal-footer .btn-primary')
        _skip_locator = (By.CSS_SELECTOR, '.modal-footer .btn-default')

        def view_invoice(self):
            self.find_element(*self._invoice_locator).click()

        def request_refund(self):
            self.find_element(*self._refund_locator).click()
            self.find_element(*self._continue_locator).click()
            self.find_element(*self._skip_locator).click()
            self.find_element(*self._continue_locator).click()
            return self


