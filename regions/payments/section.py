"""The basic list section of payments page."""

from pypom import Region
from selenium.webdriver.common.by import By


class PaymentsListSection(Region):
    """The basic list section of payments page."""

    _item_locator = (By.CSS_SELECTOR, 'tr')

    @property
    def items(self):
        """Return a list of item objects."""
        return [self.Item(self, element)
                for element in self.find_elements(*self._item_locator)]

    @property
    def lastest_item(self):
        """Return the top item of the list"""
        return self.items[0]

    class Item(Region):
        """The item region."""

        _btn_locator = (By.CSS_SELECTOR, 'th a')

        def click_item(self):
            """Click into the current item."""
            self.find_element(*self._btn_locator).click()
