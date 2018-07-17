"""OpenStax payment orders page object."""

from selenium.webdriver.common.by import By

from pages.payments.base import PaymentsBase
from regions.payments.nav import PaymentsNav
from regions.payments.section import PaymentsListSection


class PaymentOrders(PaymentsBase):
    """OpenStax payment orders page object."""

    _section_locator = (By.CSS_SELECTOR, '.results tbody')

    @property
    def nav(self):
        """Return the nav bar region."""
        return PaymentsNav(self)

    @property
    def orders_list(self):
        """Return the order list region."""
        return self.OrdersList(self, self.find_element(*self._section_locator))

    class OrdersList(PaymentsListSection):
        """The section of order lists."""

        class Item(PaymentsListSection.Item):
            """The section of order items."""

            _time_locator = (By.CLASS_NAME, 'field-created')
            _identifier_locator = (By.CLASS_NAME, 'field-identifier')
            _product_locator = (By.CLASS_NAME, 'field-product')
            _uuid_locator = (By.CLASS_NAME, 'field-student_account_uuid')

            @property
            def get_order_time(self):
                """Return the sent time of an order entry."""
                return self.find_element(*self._time_locator).text

            @property
            def get_order_identifier(self):
                """Return the identifier of an order entry."""
                return self.find_element(*self._identifier_locator).text

            @property
            def get_order_product(self):
                """Return the product of an order entry."""
                return self.find_element(*self._product_locator).text

            @property
            def get_order_uuid(self):
                """Return the uuid of an order entry."""
                return self.find_element(*self._uuid_locator).text
