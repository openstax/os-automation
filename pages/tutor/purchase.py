"""The Course purchase page object."""

from time import sleep
from pypom import Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect

from pages.tutor.base import TutorBase
from pages.tutor.dashboard import TutorDashboard
from pages.utils.utilities import Utility


class TutorPurchase(TutorBase):
    """Tutor purchase page object."""
    _payment_iframe_locator = (By.ID, 'iFrameResizer0')
    _card_iframe_locator = (By.ID, 'braintree-hosted-field-number')
    _exp_iframe_locator = (By.ID, 'braintree-hosted-field-expirationDate')
    _cvv_iframe_locator = (By.ID, 'braintree-hosted-field-cvv')
    _zip_iframe_locator = (By.ID, 'braintree-hosted-field-postalCode')
    _address_locator = (By.CSS_SELECTOR, '.street_address input')
    _city_locator = (By.CSS_SELECTOR, '.city input')
    _state_locator = (By.CSS_SELECTOR, '.state select')
    _zip_locator = (By.CSS_SELECTOR, '.zip_code input')
    _card_locator = (By.CSS_SELECTOR, '#credit-card-number')
    _exp_locator = (By.CSS_SELECTOR, '#expiration')
    _cvv_locator = (By.CSS_SELECTOR, '#cvv')
    _bil_locator = (By.CSS_SELECTOR, '#postal-code')
    _first_state_locator = (By.CSS_SELECTOR, 'select > option:nth-child(2)')
    _purchase_locator = (By.CSS_SELECTOR, 'button.purchase')
    _cancel_locator = (By.CSS_SELECTOR, 'button.cancel')
    _order_number_locator = (By.CSS_SELECTOR,
                             '.summary-lines .number span:nth-child(2)')
    _continue_locator = (By.CSS_SELECTOR, 'body .controls button')

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    def make_purchase(self, address, city, zip_code,
                        visa, exp_date, cvv, billing_zip):
        """Successfully proceed payment."""
        sleep(5)
        self.wait.until(
            expect.presence_of_element_located(self._payment_iframe_locator))
        self.driver.switch_to.frame(
            self.find_element(*self._payment_iframe_locator))
        self.find_element(*self._address_locator).send_keys(address)
        self.find_element(*self._city_locator).send_keys(city)
        self.find_element(*self._state_locator).click()
        self.find_element(*self._first_state_locator).click()
        self.find_element(*self._zip_locator).send_keys(zip_code)
        self.driver.switch_to.frame(
            self.find_element(*self._card_iframe_locator))
        Utility.scroll_to(self.driver, self._card_locator)
        self.find_element(*self._card_locator).send_keys(visa)
        self.driver.switch_to_default_content()
        self.driver.switch_to.frame(
            self.find_element(*self._payment_iframe_locator))
        self.driver.switch_to.frame(
            self.find_element(*self._exp_iframe_locator))
        self.find_element(*self._exp_locator).send_keys(exp_date)
        self.driver.switch_to_default_content()
        self.driver.switch_to.frame(
            self.find_element(*self._payment_iframe_locator))
        self.driver.switch_to.frame(
            self.find_element(*self._cvv_iframe_locator))
        self.find_element(*self._cvv_locator).send_keys(cvv)
        self.driver.switch_to_default_content()
        self.driver.switch_to.frame(
            self.find_element(*self._payment_iframe_locator))
        self.driver.switch_to.frame(
            self.find_element(*self._zip_iframe_locator))
        self.find_element(*self._bil_locator).send_keys(billing_zip)
        self.driver.switch_to_default_content()
        self.driver.switch_to.frame(
            self.find_element(*self._payment_iframe_locator))
        self.find_element(*self._purchase_locator).click()
        self.wait.until(
            expect.presence_of_element_located(self._order_number_locator))
        number = self.find_element(*self._order_number_locator).text
        self.find_element(*self._continue_locator).click()
        return TutorDashboard(self.driver), number

    def attempt_payment_with_blank(self):
        """Attempt to pay with required fields blank"""
        self.driver.switch_to.frame(*self._payment_iframe_locator)
        self.find_element(*self._purchase_locator).click()
        self.driver.switch_to_default_content()

    def cancel_purchase(self):
        """Cancel purchase."""
        self.driver.switch_to.frame(*self._payment_iframe_locator)
        self.find_element(*self._cancel_locator).click()
        self.driver.switch_to_default_content()


