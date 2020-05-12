"""Shared Account sign up form fields."""

from typing import Union

from pypom import Region
from selenium.webdriver.remote.webelement import WebElement

from utils.utilities import Utility

ERROR_SELECTOR = ' ~ .errors .invalid-message'


class Email(Region):
    """An email form field.

    .. note::
       Must define ``_email_locator`` and ``_email_error_message_locator``

    """

    @property
    def email(self) -> str:
        """Return the current value for the email field.

        :return: the email field content
        :rtype: str

        """
        return self.email_field.get_attribute('value')

    @email.setter
    def email(self, email: str):
        """Set the first name field.

        :param str email: the user's email
        :return: None

        """
        self.email_field.send_keys(email)

    @property
    def email_error(self) -> str:
        """Return the error message for the email field.

        :return: the error message content for the email field, if found
        :rtype: str

        """
        if self.email_has_error:
            return self.find_element(
                *self._email_error_message_locator).text
        return ''

    @property
    def email_field(self) -> WebElement:
        """Return the email field.

        :return: the email field
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._email_locator)

    @property
    def email_has_error(self) -> bool:
        """Return True if there is an error on the email field.

        :return: ``True`` if an error exists under the email field
        :rtype: bool

        """
        return 'has-error' in self.email_field.get_attribute('class')


class FirstName(Region):
    """A first name form field.

    .. note::
       Must define ``_first_name_locator`` and
       ``_first_name_error_message_locator``

    """

    @property
    def first_name(self) -> str:
        """Return the current value for the first name field.

        :return: the first name field content
        :rtype: str

        """
        return self.first_name_field.get_attribute('value')

    @first_name.setter
    def first_name(self, first_name: str):
        """Set the first name field.

        :param str first_name: the user's first name
        :return: None

        """
        self.first_name_field.send_keys(first_name)

    @property
    def first_name_error(self) -> str:
        """Return the error message for the first name field.

        :return: the error message content for the first name field, if found
        :rtype: str

        """
        if self.first_name_has_error:
            return self.find_element(
                *self._first_name_error_message_locator).text
        return ''

    @property
    def first_name_field(self) -> WebElement:
        """Return the first name field.

        :return: the first name field
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._first_name_locator)

    @property
    def first_name_has_error(self) -> bool:
        """Return True if there is an error on the first name field.

        :return: ``True`` if an error exists under the first name field
        :rtype: bool

        """
        return 'has-error' in self.first_name_field.get_attribute('class')


class LastName(Region):
    """A last name form field.

    .. note::
       Must define ``_last_name_locator`` and
       ``_last_name_error_message_locator``

    """

    @property
    def last_name(self) -> str:
        """Return the current value for the last name field.

        :return: the last name field content
        :rtype: str

        """
        return self.last_name_field.get_attribute('value')

    @last_name.setter
    def last_name(self, last_name: str):
        """Set the last name field.

        :param str last_name: the user's last name
        :return: None

        """
        self.last_name_field.send_keys(last_name)

    @property
    def last_name_error(self) -> str:
        """Return the error message for the last name field.

        :return: the error message content for the last name field, if found
        :rtype: str

        """
        if self.last_name_has_error:
            return self.find_element(
                *self._last_name_error_message_locator).text
        return ''

    @property
    def last_name_field(self) -> WebElement:
        """Return the last name field.

        :return: the last name field
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._last_name_locator)

    @property
    def last_name_has_error(self) -> bool:
        """Return True if there is an error on the last name field.

        :return: ``True`` if an error exists under the last name field
        :rtype: bool

        """
        return 'has-error' in self.last_name_field.get_attribute('class')


class Password(Region):
    """A first name form field.

    .. note::
       Must define ``_password_locator`` and
       ``_password_error_message_locator``

    """

    @property
    def password(self) -> str:
        """Return the current value for the password field.

        :return: the password field content
        :rtype: str

        """
        return self.password_field.get_attribute('value')

    @password.setter
    def password(self, password: str):
        """Set the password field.

        :param str password: the user's password
        :return: None

        """
        self.password_field.send_keys(password)

    @property
    def password_error(self) -> str:
        """Return the error message for the password field.

        :return: the error message content for the password field, if found
        :rtype: str

        """
        if self.password_has_error:
            return self.find_element(
                *self._password_error_message_locator).text
        return ''

    @property
    def password_field(self) -> WebElement:
        """Return the password field.

        :return: the password field
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._password_locator)

    @property
    def password_has_error(self) -> bool:
        """Return True if there is an error on the password field.

        :return: ``True`` if an error exists under the password field
        :rtype: bool

        """
        return 'has-error' in self.password_field.get_attribute('class')


class Phone(Region):
    """A telephone form field.

    .. note::
       Must define ``_phone_locator`` and ``_phone_error_message_locator``

    """

    @property
    def phone(self) -> str:
        """Return the current value for the telephone field.

        :return: the phone field content
        :rtype: str

        """
        return self.phone_field.get_attribute('value')

    @phone.setter
    def phone(self, number: Union[int, str]):
        """Set the pin field.

        :param number: the user's telephone number
        :type number: int or str
        :return: None

        """
        Utility.click_option(self.driver, element=self.phone_field)
        self.phone_field.send_keys(str(number))

    @property
    def phone_error(self) -> str:
        """Return the error message for the telephone number field.

        :return: the error message content for the telephone field, if found
        :rtype: str

        """
        if self.phone_has_error:
            return self.find_element(
                *self._phone_error_message_locator).text
        return ''

    @property
    def phone_field(self) -> WebElement:
        """Return the telephone number field.

        :return: the telephone number field
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._phone_locator)

    @property
    def phone_has_error(self) -> bool:
        """Return True if there is an error on the telephone number field.

        :return: ``True`` if an error exists under the telephone number field
        :rtype: bool

        """
        return 'has-error' in self.phone_field.get_attribute('class')


class Pin(Region):
    """A PIN form field.

    .. note::
       Must define ``_pin_locator`` and ``_pin_error_message_locator``

    """

    @property
    def pin(self) -> str:
        """Return the current value for the pin verification field.

        :return: the pin verification field content
        :rtype: str

        """
        return self.pin_field.get_attribute('value')

    @pin.setter
    def pin(self, pin: str):
        """Set the pin field.

        :param str pin: the user's verification pin number
        :return: None

        """
        self.pin_field.send_keys(pin)

    @property
    def pin_error(self) -> str:
        """Return the error message for the pin field.

        :return: the error message content for the pin verification field, if
            found
        :rtype: str

        """
        if self.pin_has_error:
            return self.find_element(
                *self._pin_error_message_locator).text
        return ''

    @property
    def pin_field(self) -> WebElement:
        """Return the pin confirmation field.

        :return: the pin confirmation field
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._pin_locator)

    @property
    def pin_has_error(self) -> bool:
        """Return True if there is an error on the pin field.

        :return: ``True`` if an error exists under the verification pin field
        :rtype: bool

        """
        return 'has-error' in self.pin_field.get_attribute('class')
