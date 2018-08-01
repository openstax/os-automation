"""OpenStax payment orders detail page object."""

from selenium.webdriver.common.by import By

from pages.payments.base import PaymentsBase
from regions.payments.nav import PaymentsNav
from regions.payments.section import PaymentsListSection


class PaymentOrdersDetail(PaymentsBase):
    """OpenStax payment orders detail page object."""

    _transactions_locator = (By.CSS_SELECTOR, '#transaction_set-group tbody')
    _identifier_locator = (By.CSS_SELECTOR, '.field-identifier input')

    @property
    def nav(self):
        """Return the nav bar region."""
        return PaymentsNav(self)

    @property
    def get_identifier(self):
        """Return the order identifier."""
        return self.find_element(*self._identifier_locator)\
            .get_attribute('value')

    @property
    def transactions_list(self):
        """Return the transaction list region."""
        return self.TransactionList(
            self, self.find_element(*self._transactions_locator))

    class TransactionList(PaymentsListSection):
        """The section of transactions lists."""

        class Item(PaymentsListSection.Item):
            """The section of order items."""

            _status_locator = (By.CSS_SELECTOR, 'select option[selected]')

            @property
            def get_status(self):
                """Return the status of an order."""
                return self.find_element(*self._status_locator).text
