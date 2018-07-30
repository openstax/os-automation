"""The Course purchase page object."""

from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase


class TutorPurchase(TutorBase):
    """Tutor purchase page object."""
    _iframe_locator = (By.CSS_SELECTOR, '#iFrameResizer2')
    _address_locator = (
        By.CSS_SELECTOR,
        'div:nth-child(2) > label > input[type="text"]')
    _city_locator = (
        By.CSS_SELECTOR,
        'label.city.full.half-1000 > input[type="text"]')
    _state_locator = (By.CSS_SELECTOR, 'label.state.half.fourth-1000 > select')
    _zip_locator = (
        By.CSS_SELECTOR,
        'label.zip_code.half.fourth-1000 > input[type="text"]')
    _card_locator = (By.CSS_SELECTOR, '#credit-card-number')
    _exp_locator = (By.CSS_SELECTOR, '#expiration')
    _cvv_locator = (By.CSS_SELECTOR, '#cvv')
    _bil_locator = (By.CSS_SELECTOR, '#postal-code')
    _first_state_locator = (By.CSS_SELECTOR, 'select > option:nth-child(2)')
    _purchase_locator = (By.CSS_SELECTOR, 'button.purchase')
    _cancel_locator = (By.CSS_SELECTOR, 'button.cancel')

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    def payment_proceed(self, address, city, zipcode,
                        visa, exp_date, cvv, billing):
        """Successfully proceed payment."""
        self.driver.switch_to.frame(*self._iframe_locator)
        self.find_element(*self._address_locator).sendKeys(address)
        self.find_element(*self._city_locator).sendKeys(city)
        self.find_element(*self._state_locator).click()
        self.find_element(*self._first_state_locator).click()
        self.find_element(*self._zip_locator).sendKeys(zipcode)
        self.find_element(*self._card_locator).sendKeys(visa)
        self.find_element(*self._exp_locator).sendKeys(exp_date)
        self.find_element(*self._cvv_locator).sendKeys(cvv)
        self.find_element(*self._bil_locator).sendKeys(billing)
        self.find_element(*self._state_locator).click()
        self.find_element(*self._purchase_locator).click()
        self.driver.switch_to.defaultContent()

    def attempt_payment_with_blank(self):
        """Attempt to pay with required fields blank"""
        self.driver.switch_to.frame(*self._iframe_locator)
        self.find_element(*self._purchase_locator).click()
        self.driver.switch_to.defaultContent()

    def cancel_purchase(self):
        """Cancel purchase."""
        self.driver.switch_to.frame(*self._iframe_locator)
        self.find_element(*self._cancel_locator).click()
        self.driver.switch_to.defaultContent()
