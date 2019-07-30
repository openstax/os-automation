"""Student enrollment."""

from __future__ import annotations

from time import sleep
from typing import List, Tuple, Union

from pypom import Page, Region
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.accounts.signup import Signup as AccountSignup
from pages.tutor.course import StudentCourse
from utils.tutor import Tutor, TutorException
from utils.utilities import Utility, go_to_

# get the modal and tooltip root that is a neighbor of the React root element
GET_ROOT = 'return document.querySelector("[role={0}]");'
# A By-styled selector
Selector = Tuple[str, str]


# -------------------------------------------------------- #
# Page dialog boxes
# -------------------------------------------------------- #

class Modal(Region):
    """A page modal."""

    @property
    def root(self) -> WebElement:
        """Return the root element for a page modal.

        :return: the root element for a page modal
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.driver.execute_script(GET_ROOT.format('dialog'))


class BuyAccess(Modal):
    """The product purchase modal."""

    _buy_access_now_button_locator = (By.CSS_SELECTOR, '.now')
    _try_free_button_locator = (By.CSS_SELECTOR, '.later')

    def buy_access_now(self) -> PurchaseForm:
        """Click the 'Buy access now' button.

        :return: the purchase form modal
        :rtype: :py:class:`~pages.tutor.enrollment.PurchaseForm`

        """
        button = self.find_element(*self._buy_access_now_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(1)
        return PurchaseForm(self.page)

    def try_free(self) -> FreeTrial:
        """Click the 'Try free' button.

        :return: the free trial modal
        :rtype: :py:class:`~pages.tutor.enrollment.FreeTrial`

        """
        button = self.find_element(*self._try_free_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(1)
        return FreeTrial(self.page)


class FreeTrial(Modal):
    """The free product trial notice modal."""

    _modal_content_locator = (By.CSS_SELECTOR, '.body')
    _access_your_course_button_locator = (By.CSS_SELECTOR, '.now')

    @property
    def content(self) -> str:
        """Return the modal content text.

        :return: the modal content
        :rtype: str

        """
        return (self.find_element(*self._modal_content_locator)
                .get_attribute('textContent'))

    def access_your_course(self) -> StudentCourse:
        """Click the 'Access your course' button.

        :return: the student course page
        :rtype: :py:class:`~pages.tutor.course.StudentCourse`

        """
        button = self.find_element(*self._access_your_course_button_locator)
        Utility.click_option(self.driver, element=button)
        return go_to_(StudentCourse(self.driver, base_url=self.page.base_url))


class PrivacyPolicy(Modal):
    """The privacy policy enrollment modal."""

    _modal_heading_locator = (By.CSS_SELECTOR, '.modal-header')
    _modal_title_locator = (By.CSS_SELECTOR, '.title')
    _modal_content_locator = (By.CSS_SELECTOR, '.title ~ div')
    _i_agree_button_locator = (By.CSS_SELECTOR, '.btn-primary')

    @property
    def loaded(self) -> bool:
        """Return True when 'Terms of Service' is found on the page.

        :return: ``True`` when the terms of service is found in the page text
        :rtype: bool

        """
        return ('Terms of Service'
                in (self.find_element(*self._modal_content_locator)
                    .get_attribute('textContent')))

    @property
    def heading(self) -> str:
        """Return the modal heading.

        :return: the privacy policy modal heading
        :rtype: str

        """
        return (self.find_element(*self._modal_heading_locator)
                .get_attribute('textContent'))

    @property
    def title(self) -> str:
        """Return the modal title.

        :return: the privacy policy modal title
        :rtype: str

        """
        return self.find_element(*self._modal_title_locator).text

    @property
    def content(self) -> str:
        """Return the modal body text.

        :return: the modal body text
        :rtype: str

        """
        return (self.find_element(*self._modal_content_locator)
                .get_attribute('textContent'))

    def i_agree(self) -> Union[BuyAccess, StudentCourse]:
        """Click on the 'I agree' button.

        After clicking on the I agree button, one of two destinations are
        possible:
            1) the student course page with the product purchase modal open for
               paid courses
            2) the student course page without a modal open for existing
               students in a free course

        :return: the course page with the product purchase modal displayed
        :rtype: :py:class:`~pages.tutor.enrollment.BuyAccess` or
            :py:class:`~pages.tutor.course.StudentCourse`

        """
        button = self.find_element(*self._i_agree_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(1.25)
        course = StudentCourse(self.driver, base_url=self.page.base_url)
        dialog_root = self.driver.execute_script(GET_ROOT.format('dialog'))
        if (dialog_root and
                'pay-now-or-later' in dialog_root.get_attribute('class')):
            return BuyAccess(course, dialog_root)
        return go_to_(course)


class IframeModal(Modal):
    """A dialog box with internal iFrames."""

    _base_iframe_locator = (By.CSS_SELECTOR, 'iframe')

    def _get_value(self, locator: Selector, field: str = 'value',
                   inner_frame: Selector = None) -> str:
        """Return a purchase form value.

        :param locator: a By-styled element selector for the requested element
            field
        :type locator: (str, str)
        :param str field: (optional) the element field to read, default is to
            return the input ``value`` field
        :param inner_frame: (optional) a By-styled element selector for the
            inner (second-order) iframe
        :return: a form input's current value
        :rtype: str

        :noindex:

        """
        purchase = self.find_element(*self._base_iframe_locator)
        self.driver.switch_to.frame(purchase)
        if inner_frame:
            second_frame = self.find_element(*inner_frame)
            self.driver.switch_to.frame(second_frame)
        value = self.find_element(*locator).get_attribute(field)
        if inner_frame:
            self.driver.switch_to.default_content()
        self.driver.switch_to.default_content()
        return value

    def _set_value(self, locator: Selector, value: str,
                   inner_frame: Selector = None) -> None:
        """Assign a value to a purchase form field.

        :param locator: a By-styled element selector for the requested element
            field
        :type locator: (str, str)
        :param str value: the value to assign
        :param inner_frame: (optional) a By-styled element selector for the
            inner (second-order) iframe
        :return: None

        :noindex:

        """
        purchase = self.find_element(*self._base_iframe_locator)
        self.driver.switch_to.frame(purchase)
        if inner_frame:
            second_frame = self.wait.until(
                lambda _: self.find_element(*inner_frame))
            self.driver.switch_to.frame(second_frame)
        self.find_element(*locator).send_keys(value)
        if inner_frame:
            self.driver.switch_to.default_content()
        self.driver.switch_to.default_content()


class PurchaseConfirmation(IframeModal):
    """The Tutor product purchase confirmation."""

    _content_locator = (By.CSS_SELECTOR, 'h3 , p')
    _order_date_locator = (By.CSS_SELECTOR, '.date span:last-child')
    _order_number_locator = (By.CSS_SELECTOR, '.number span:last-child')
    _product_name_locator = (By.CSS_SELECTOR, '.price span:first-child')
    _product_price_locator = (By.CSS_SELECTOR, '.price span:last-child')
    _tax_type_locator = (By.CSS_SELECTOR, '.tax span:first-child')
    _tax_total_locator = (By.CSS_SELECTOR, '.tax span:last-child')
    _sales_total_locator = (By.CSS_SELECTOR, '.total span:last-child')
    _access_your_course_button_locator = (By.CSS_SELECTOR, 'button')

    @property
    def loaded(self) -> bool:
        """Return True when the content is present in the iframe.

        :return: ``True`` when the content in the payment confirmation iframe
            is present
        :rtype: bool

        """
        # Intermittant load failures due to timing; check vals below until the
        # root cause is found.
        try:
            number = self.order_number
        except Exception:
            number = None
        try:
            total = self.total
        except Exception:
            total = None
        print(f'Order number: {number}\nTotal: {total}')
        # return bool(self.order_number) and bool(self.total)
        return bool(number) and bool(total)

    @property
    def content(self) -> str:
        """Return the order completion text.

        :return: the text content at the top of the order confirmation pane
        :rtype: str

        """
        confirmation = self.find_element(*self._base_iframe_locator)
        self.driver.switch_to.frame(confirmation)
        text = '\n'.join(list([
            line.text
            for line
            in self.find_elements(*self._content_locator)]))
        self.driver.switch_to.default_content()
        return text

    @property
    def order_date(self) -> str:
        """Return the order date.

        :return: the order date
        :rtype: str

        """
        return self._get_value(
            locator=self._order_date_locator,
            field='textContent')

    @property
    def order_number(self) -> str:
        """Return the order identification number.

        :return: the order number
        :rtype: str

        """
        return self._get_value(
            locator=self._order_number_locator,
            field='textContent')

    @property
    def product(self) -> str:
        """Return the purchased product name.

        :return: the product name
        :rtype: str

        """
        return self._get_value(
            locator=self._product_name_locator,
            field='textContent')

    @property
    def price(self) -> str:
        """Return the product price.

        :return: the product price
        :rtype: str

        """
        return self._get_value(
            locator=self._product_price_locator,
            field='textContent')

    @property
    def tax_type(self) -> str:
        """Return the tax type.

        :return: the type of tax being applied
        :rtype: str

        """
        return self._get_value(
            locator=self._tax_type_locator,
            field='textContent')

    @property
    def tax(self) -> str:
        """Return the tax total.

        :return: the total tax applied to the order
        :rtype: str

        """
        return self._get_value(
            locator=self._tax_total_locator,
            field='textContent')

    @property
    def total(self) -> str:
        """Return the order's total cost.

        :return: the total cost of the purchase
        :rtype: str

        """
        return self._get_value(
            locator=self._sales_total_locator,
            field='textContent')

    def access_your_course(self) -> StudentCourse:
        """Click the 'Access your course' continuation button.

        :return: the student course page
        :rtype: :py:class:`~pages.tutor.course.StudentCourse`

        """
        confirmation = self.find_element(*self._base_iframe_locator)
        self.driver.switch_to.frame(confirmation)
        button = self.find_element(*self._access_your_course_button_locator)
        Utility.click_option(self.driver, element=button)
        self.driver.switch_to.default_content()
        return go_to_(StudentCourse(self.driver, base_url=self.page.base_url))


class PurchaseForm(IframeModal):
    """The Tutor product purchase form."""

    # form nested iframes
    _card_number_iframe_locator = (By.CSS_SELECTOR, '.number iframe')
    _expiration_date_iframe_locator = (
                                    By.CSS_SELECTOR, '.expirationDate iframe')
    _cvv_code_iframe_locator = (By.CSS_SELECTOR, '.cvv iframe')
    _billing_zip_code_iframe_locator = (By.CSS_SELECTOR, '.postalCode iframe')

    # form fields
    _product_title_locator = (By.CSS_SELECTOR, '.heading h3')
    _address_locator = (By.CSS_SELECTOR, '[name=street_address]')
    _city_locator = (By.CSS_SELECTOR, '[name=city]')
    _state_locator = (By.CSS_SELECTOR, '[name=state]')
    _state_option_locator = (By.CSS_SELECTOR, '[name=state] option')
    _state_option_value_selector = '[value={0}]'
    _address_zip_code_locator = (By.CSS_SELECTOR, '[name=zip_code]')
    _card_number_locator = (By.CSS_SELECTOR, '#credit-card-number')
    _expiration_date_locator = (By.CSS_SELECTOR, '#expiration')
    _card_verification_number_locator = (By.CSS_SELECTOR, '.cvv')
    _billing_zip_code_locator = (By.CSS_SELECTOR, '#postal-code')
    _product_name_locator = (By.CSS_SELECTOR, '.price span:first-child')
    _product_price_locator = (By.CSS_SELECTOR, '.price span:last-child')
    _tax_type_locator = (By.CSS_SELECTOR, '.tax span:first-child')
    _tax_total_locator = (By.CSS_SELECTOR, '.tax span:last-child')
    _sales_total_locator = (By.CSS_SELECTOR, '.total span:last-child')
    _error_message_locator = (By.CSS_SELECTOR, '.error-message')
    _purchase_button_locator = (By.CSS_SELECTOR, '.purchase')
    _cancel_purchase_button_locator = (By.CSS_SELECTOR, '.cancel')

    @property
    def loaded(self) -> bool:
        """Return True when the form fields are found.

        :return: ``True`` when the form fields and iframes are found
        :rtype: bool

        """
        return (sleep(1) or self.find_elements(By.TAG_NAME, 'iframe'))

    @property
    def product_title(self) -> str:
        """Return the product title being purchased.

        :return: the product title
        :rtype: str

        """
        return self._get_value(self._product_title_locator, 'textContent')

    @property
    def address(self) -> str:
        """Return the current address.

        :return: the value in the address field
        :rtype: str

        """
        return self._get_value(self._address_locator)

    @address.setter
    def address(self, addr: str) -> None:
        """Set the street number and street name.

        :param str addr: the new street address
        :return: None

        """
        self._set_value(self._address_locator, addr)

    @property
    def city(self) -> str:
        """Return the current city.

        :return: the value in the city field
        :rtype: str

        """
        return self._get_value(self._city_locator)

    @city.setter
    def city(self, city_name: str) -> None:
        """Set the city name.

        :param str city_name: the new street city
        :return: None

        """
        self._set_value(self._city_locator, city_name)

    @property
    def state(self) -> str:
        """Return the current state.

        :return: the currently selected state
        :rtype: str

        """
        state_code = self._get_value(self._state_locator)
        if not state_code:
            return ''
        return self._get_value(
            locator=(By.CSS_SELECTOR,
                     self._state_option_value_selector.format(state_code)),
            field='textContent')

    @state.setter
    def state(self, state: str) -> None:
        """Set the district, state, or territory.

        :param str state: the state's select menu label for the district,
            state, or U.S. territory
        :return: None

        :raises :py:class:`~utils.tutor.TutorException`: if the state is not a
            valid state label

        """
        if state not in Tutor.states():
            raise TutorException(
                '"{0}" not a valid state; refer to '.format(state) +
                'utils.tutor.States for valid options')
        purchase = self.find_element(*self._base_iframe_locator)
        self.driver.switch_to.frame(purchase)
        Utility.select(self.driver, self._state_locator, state)
        self.driver.switch_to.default_content()

    @property
    def mailing_zip(self) -> str:
        """Return the current mailing zip code.

        :return: the value in the zip code field
        :rtype: str

        """
        return self._get_value(self._address_zip_code_locator)

    @mailing_zip.setter
    def mailing_zip(self, zip_code: Union[str, int]) -> None:
        """Set the mailing zip code.

        :param zip: the new mailing zip code
        :type zip: str or int
        :return: None

        """
        self._set_value(self._address_zip_code_locator, str(zip_code))

    @property
    def card_number(self) -> str:
        """Return the current credit card number.

        :return: the value in the credit card number field
        :rtype: str

        """
        return self._get_value(
            locator=self._card_number_locator,
            inner_frame=self._card_number_iframe_locator)

    @card_number.setter
    def card_number(self, number: Union[str, int]) -> None:
        """Set the credit card number.

        :param number: a credit card number
        :type number: str or int
        :return: None

        """
        self._set_value(
            locator=self._card_number_locator,
            value=str(number),
            inner_frame=self._card_number_iframe_locator)

    @property
    def expiration_date(self) -> str:
        """Return the current expiration date.

        :return: the value in the expiration date field
        :rtype: str

        """
        return self._get_value(
            locator=self._expiration_date_locator,
            inner_frame=self._expiration_date_iframe_locator)

    @expiration_date.setter
    def expiration_date(self, date: str) -> None:
        """Set the expiration date.

        :param str date: an expiration date in a "MM/YY" or "MMYY" format
        :return: None

        """
        self._set_value(
            locator=self._expiration_date_locator,
            value=date,
            inner_frame=self._expiration_date_iframe_locator)

    @property
    def cvv(self) -> str:
        """Return the current card verification number.

        :return: the value in the card verification field
        :rtype: str

        """
        return self._get_value(
            locator=self._card_verification_number_locator,
            inner_frame=self._cvv_code_iframe_locator)

    @cvv.setter
    def cvv(self, code: Union[str, int]) -> None:
        """Set the card verification number.

        :param code: a 3 or 4 digit credit card verification code number
            3-digit for VISA, MasterCard and Discover
            4-digit for American Express
        :type code: str or int
        :return: None

        """
        self._set_value(
            locator=self._card_verification_number_locator,
            value=str(code),
            inner_frame=self._cvv_code_iframe_locator)

    @property
    def billing_zip_code(self) -> str:
        """Return the current billing zip code.

        :return: the value in the billing zip code field
        :rtype: str

        """
        return self._get_value(
            locator=self._billing_zip_code_locator,
            inner_frame=self._billing_zip_code_iframe_locator)

    @billing_zip_code.setter
    def billing_zip_code(self, zip_code: Union[str, int]) -> None:
        """Set the billing zip code.

        :param zip_code: the billing zip code for the card
        :type zip_code: str or int
        :return: None

        """
        self._set_value(
            locator=self._billing_zip_code_locator,
            value=str(zip_code),
            inner_frame=self._billing_zip_code_iframe_locator)

    @property
    def product(self) -> str:
        """Return the product name.

        :return: the purchased product name
        :rtype: str

        """
        return self._get_value(
            locator=self._product_name_locator,
            field='textContent')

    @property
    def price(self) -> str:
        """Return the product price.

        :return: the product pre-tax price
        :rtype: str

        """
        return self._get_value(
            locator=self._product_price_locator,
            field='textContent')

    @property
    def tax_type(self) -> str:
        """Return the tax type.

        :return: the type of tax being applied
        :rtype: str

        """
        return self._get_value(
            locator=self._tax_type_locator,
            field='textContent')

    @property
    def tax(self) -> str:
        """Return the tax amount.

        :return: the tax amount, if applicable, otherwise '--'
        :rtype: str

        """
        return self._get_value(
            locator=self._tax_total_locator,
            field='textContent')

    @property
    def total(self) -> str:
        """Return the total post-tax price.

        :return: the total amount due (product price + tax amount)
        :rtype: str

        """
        return self._get_value(
            locator=self._sales_total_locator,
            field='textContent')

    @property
    def error_messages(self) -> List[str]:
        """Return any active input field error messages.

        :return: a list of error messages present in the purchase form
        :rtype: list(str)

        """
        purchase = self.find_element(*self._base_iframe_locator)
        self.driver.switch_to.frame(purchase)
        errors = [message.get_attribute('textContent')
                  for message
                  in self.find_elements(*self._error_message_locator)]
        self.driver.switch_to.default_content()
        return errors

    def purchase(self) -> Union[PurchaseConfirmation, List[str]]:
        """Click on the 'Purchase' Tutor button.

        :return: the purchase confirmation modal or the error message for a
            failed transaction
        :rtype: :py:class:`~pages.tutor.enrollment.PurchaseConfirmation` or
            list(str)

        """
        purchase = self.find_element(*self._base_iframe_locator)
        self.driver.switch_to.frame(purchase)
        button = self.wait.until(
            lambda _: self.find_element(*self._purchase_button_locator))
        Utility.click_option(self.driver, element=button)
        sleep(1)
        self.driver.switch_to.default_content()
        errors = self.error_messages
        if errors:
            return errors
        return PurchaseConfirmation(self.page)

    def cancel(self) -> FreeTrial:
        """Click on the 'Cancel' purchase button.

        :return: the free trial activation modal
        :rtype: :py:class:`~pages.tutor.enrollment.FreeTrial`

        """
        purchase = self.find_element(*self._base_iframe_locator)
        self.driver.switch_to.frame(purchase)
        button = self.find_element(*self._cancel_purchase_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.5)
        self.driver.switch_to.default_content()
        return FreeTrial(self.page)


# -------------------------------------------------------- #
# Assignment shared properties
# -------------------------------------------------------- #

class Enrollment(Page):
    """The standard student course enrollment (direct URL signup)."""

    URL_TEMPLATE = '/enroll/{enrollment_code}/{course_name}-{term}-{year}'

    _splash_content_locator = (By.CSS_SELECTOR, '.splash')
    _get_started_button_locator = (By.CSS_SELECTOR, 'a')

    @property
    def loaded(self) -> bool:
        """Return True if the enrollment introduction is loaded.

        :return: ``True`` if the enrollment introduction is loaded, otherwise
            ``False``
        :rtype: bool

        """
        return bool(self.content)

    @property
    def content(self) -> str:
        """Return the splash text content.

        :return: the enrollment introductory text
        :rtype: str

        """
        return (self.find_element(*self._splash_content_locator)
                .get_attribute('textContent'))

    def get_started(self) -> Union[AccountSignup, Enrollment.StudentID]:
        """Click on the 'Get Started' button to begin enrollment.

        :return: the account signup flow for new users or the student ID
            assignment for logged in users
        :rtype: :py:class:`~pages.accounts.signup.Signup` or
            :py:class:`~pages.tutor.enrollment.Enrollment.StudentID`

        """
        button = self.find_element(*self._get_started_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(1)
        if 'accounts' in self.driver.current_url:
            return AccountSignup(self.driver)
        return StudentID(self.driver, base_url=self.base_url)


class StudentID(Page):
    """Enter the student's identification number."""

    URL_TEMPLATE = '/enroll/start/{enrollment_code}'

    _student_id_icon_locator = (By.CSS_SELECTOR, '.student-id-icon')
    _course_name_locator = (By.CSS_SELECTOR, '.title h4')
    _student_id_input_locator = (By.CSS_SELECTOR, '.inputs input')
    _continue_button_locator = (By.CSS_SELECTOR, '.btn-success')
    _add_it_later_link_locator = (By.CSS_SELECTOR, '.cancel')

    @property
    def loaded(self) -> bool:
        """Return True when the student ID badge element is found.

        :return: ``True`` when the student ID icon is found
        :rtype: bool

        """
        return bool(self.find_elements(*self._student_id_icon_locator))

    @property
    def course_name(self) -> str:
        """Return the course name associated with the enrollment code.

        :return: the course name
        :rtype: str

        """
        return self.find_element(*self._course_name_locator).text

    @property
    def student_id(self) -> WebElement:
        """Return the student ID field.

        :return: the student ID field
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._student_id_input_locator)

    @student_id.setter
    def student_id(self, _id: str) -> None:
        """Set the student ID.

        :param str _id: the student's identification number
        :return: None

        """
        return self.student_id.send_keys(_id)

    def _continue(self, add_it_later: bool = False) \
            -> Union[PrivacyPolicy, BuyAccess, StudentCourse]:
        """Click on the 'Continue' button.

        After clicking on the continue button, one of three destinations are
        possible:
            1) the student course page with the privacy policy modal open when
               the student is new or has not accepted the privacy policy
            2) the student course page with the product purchase modal open for
               paid courses
            3) the student course page without a modal open for existing
               students in a free course

        :param bool add_it_later: (optional) click the 'Add it later' link
            instead of the 'Continue' button
        :return: the course page with the privacy policy or product purchase
            modal displayed
        :rtype: :py:class:`~pages.tutor.enrollment.PrivacyPolicy` or
            :py:class:`~pages.tutor.enrollment.BuyAccess` or
            :py:class:`~pages.tutor.course.StudentCourse`

        """
        locator = self._continue_button_locator if not add_it_later \
            else self._add_it_later_link_locator
        button = self.find_element(*locator)
        Utility.click_option(self.driver, element=button)
        sleep(1.25)
        course = StudentCourse(self.driver, base_url=self.base_url)
        for _ in range(5):
            dialog_root = self.driver.execute_script(GET_ROOT.format('dialog'))
            sleep(1)
            if dialog_root:
                break
        sleep(1)
        if 'Privacy Policy' in self.driver.page_source:
            return PrivacyPolicy(course, dialog_root)
        elif dialog_root:
            return BuyAccess(course, dialog_root)
        return go_to_(course)

    def add_it_later(self) -> Union[PrivacyPolicy, BuyAccess]:
        """Click on the 'Add it later' link.

        After clicking on the add it later button, one of two destinations are
        possible:
            1) the student course page with the privacy policy modal open
            2) the student course page with the product purchse modal open

        :return: the course page with the privacy policy or product purchse
            modal displayed
        :rtype: :py:class:`PrivacyPolicy` or :py:class:`BuyAccess`

        """
        return self._continue(add_it_later=True)
