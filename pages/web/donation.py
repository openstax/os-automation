"""The gift and donation page."""

from time import sleep

from pypom import Region
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility, go_to_


class Give(WebBase):
    """The give page and form."""

    URL_TEMPLATE = '/give'

    _give_background_selector = '.background-image'

    _banner_locator = (By.CSS_SELECTOR, '.hero h1')
    _description_locator = (By.CSS_SELECTOR, '.hero h1 ~ p')
    _form_locator = (By.CSS_SELECTOR, '.preform')
    _other_heading_locator = (By.CSS_SELECTOR, '.text-content h2')
    _options_locator = (By.CSS_SELECTOR, '.col')
    _contact_locator = (By.CSS_SELECTOR, '[href*=contact]')
    _amount_box_locator = (By.CSS_SELECTOR, '.box-row [role=button]')

    @property
    def loaded(self):
        """Return True when the banner heading is loaded."""
        return (self.banner.is_displayed() and
                Utility.load_background_images(
                    self.driver, self._give_background_selector) and
                len(self.find_elements(*self._amount_box_locator)) > 0)

    def is_displayed(self):
        """Return True if the heading and other give options are displayed."""
        return (self.banner.is_displayed() and
                self.options)

    @property
    def banner(self):
        """Return the heading element."""
        return self.find_element(*self._banner_locator)

    @property
    def title(self):
        """Return the banner text."""
        return self.banner.text.strip()

    @property
    def description(self):
        """Return the preform text."""
        return self.find_element(*self._description_locator).text.strip()

    @property
    def form(self):
        """Access the preform."""
        return self.Form(self)

    @property
    def other_options(self):
        """Return the other options heading element."""
        return self.find_element(*self._other_heading_locator)

    @property
    def options(self):
        """Access the other ways to give options."""
        return [self.Option(self, box)
                for box in self.find_elements(*self._options_locator)]

    def contact_us(self):
        """Click on the 'Contact us for help...' button."""
        Utility.click_option(self.driver, locator=self._contact_locator)
        from pages.web.contact import Contact
        return go_to_(Contact(self.driver, base_url=self.base_url))

    class Form(Region):
        """The preform."""

        _amount_locator = (By.CSS_SELECTOR, '.box-row [role=button]')
        _other_locator = (By.CSS_SELECTOR, '.box-row [type=number]')
        _donate_locator = (By.CSS_SELECTOR, '[type=submit]')

        @property
        def boxes(self):
            """Return the set amount boxes."""
            return [box for box in self.find_elements(*self._amount_locator)]

        @boxes.setter
        def boxes(self, amount):
            """Set the donation amount."""
            set_options = {10: 0, 25: 1, 50: 2, 100: 3, 500: 4, 1000: 5}
            if amount in set_options:
                Utility.click_option(
                    self.driver,
                    element=self.boxes[set_options.get(amount)])
            else:
                self.other = amount
            return self

        @property
        def other(self):
            """Return the other amount box."""
            return self.find_element(*self._other_locator)

        @other.setter
        def other(self, amount):
            """Set a specific donation amount."""
            self.other.send_keys(amount)
            if self.page.is_safari:
                sleep(0.5)
                from selenium.webdriver.common.keys import Keys
                self.other.send_keys(Keys.TAB)
            return self

        @property
        def other_validation(self):
            """Return the other amount field validation message."""
            return self.driver.execute_script(
                'return arguments[0].validationMessage;', self.other)

        @property
        def donate_button(self):
            """Return the donate button."""
            return self.find_element(*self._donate_locator)

        def donate(self):
            """Click the 'donate!' button."""
            Utility.click_option(self.driver, element=self.donate_button)
            return go_to_(Donate(self.driver, self.page.base_url))

    class Option(Region):
        """An other option donation box."""

        _title_locator = (By.CSS_SELECTOR, 'h3')
        _content_locator = (By.CSS_SELECTOR, 'p')

        @property
        def title(self):
            """Return the box heading."""
            return self.find_element(*self._title_locator).text.strip()

        @property
        def content(self):
            """Return the content paragraphs."""
            return [paragraph.text.strip()
                    for paragraph
                    in self.find_elements(*self._content_locator)
                    if len(paragraph.text.strip()) > 0]


class Donate(WebBase):
    """The full donation form."""

    URL_TEMPLATE = '/give/form'
    ERROR = ' ~ .invalid-message'

    _instructions_locator = (By.CSS_SELECTOR, '.instructions')
    _input_locator = (By.CSS_SELECTOR, 'input:not([type=hidden])')
    _is_test_locator = (By.CSS_SELECTOR, '#use-testing-site')
    _options_locator = (By.CSS_SELECTOR, '.options')

    # Fields
    _title_locator = (By.CSS_SELECTOR, '[name=Title]')
    _first_name_locator = (By.CSS_SELECTOR, '[name=First_Name]')
    _last_name_locator = (By.CSS_SELECTOR, '[name=Last_Name]')
    _suffix_locator = (By.CSS_SELECTOR, '[name=Suffix]')
    _email_locator = (By.CSS_SELECTOR, '[name=Email]')
    _phone_locator = (By.CSS_SELECTOR, '[name=Phone]')
    _phone_type_locator = (By.CSS_SELECTOR, '[name=Phone_Type]')
    _address_one_locator = (By.CSS_SELECTOR, '[name=Mailing_Address]')
    _address_two_locator = (By.CSS_SELECTOR, '[name=Mailing_Address2]')
    _city_locator = (By.CSS_SELECTOR, '[name=Mailing_City]')
    _state_locator = (By.CSS_SELECTOR, 'label:nth-child(3) .select')
    _zip_locator = (By.CSS_SELECTOR, '[name=Mailing_Zip]')
    _country_locator = (By.CSS_SELECTOR, 'label:nth-child(5) .select')
    _amount_locator = (By.CSS_SELECTOR, '[name=AMT]')
    _continue_button_locator = (By.CSS_SELECTOR, '[type=submit]')

    # Error messages
    _first_name_error_locator = (
        By.CSS_SELECTOR, _first_name_locator[1] + ERROR)
    _last_name_error_locator = (By.CSS_SELECTOR, _last_name_locator[1] + ERROR)
    _email_error_locator = (By.CSS_SELECTOR, _email_locator[1] + ERROR)
    _phone_error_locator = (By.CSS_SELECTOR, _phone_locator[1] + ERROR)
    _phone_type_error_locator = (
        By.CSS_SELECTOR, _phone_type_locator[1] + ERROR)
    _address_one_error_locator = (
        By.CSS_SELECTOR, _address_one_locator[1] + ERROR)
    _city_error_locator = (By.CSS_SELECTOR, _city_locator[1] + ERROR)
    _state_error_locator = (By.CSS_SELECTOR, _state_locator[1] + ERROR)
    _zip_error_locator = (By.CSS_SELECTOR, _zip_locator[1] + ERROR)
    _country_error_locator = (By.CSS_SELECTOR, _country_locator[1] + ERROR)
    _amount_error_locator = (By.CSS_SELECTOR, _amount_locator[1] + ERROR)

    @property
    def loaded(self):
        """Return True when the donation form input boxes are loaded."""
        return len(self.find_elements(*self._input_locator)) > 0

    def is_displayed(self):
        """Return True if the instructions are displayed."""
        return len(self.instructions) > 0

    @property
    def instructions(self):
        """Return the form instructions."""
        return self.find_element(*self._instructions_locator).text.strip()

    @property
    def is_test(self):
        """Return True if the testing checkbox is checked."""
        try:
            return self.driver.execute_script(
                'return arguments[0].checked;',
                self.find_element(*self._is_test_locator))
        except WebDriverException:
            return False

    def clear_test(self):
        """Uncheck the is_test checkbox."""
        if self.is_test:
            Utility.click_option(driver=self.driver,
                                 locator=self._is_test_locator)
        return self

    @property
    def title(self):
        """Return the title field."""
        return self.find_element(*self._title_locator)

    @title.setter
    def title(self, value):
        """Set the title field."""
        return self._set_value(self.title, value)

    @property
    def first(self):
        """Return the first name field."""
        return self.find_element(*self._first_name_locator)

    @first.setter
    def first(self, value):
        """Set the first name field."""
        return self._set_value(self.first, value)

    @property
    def last(self):
        """Return the last name field."""
        return self.find_element(*self._last_name_locator)

    @last.setter
    def last(self, value):
        """Set the last name field."""
        return self._set_value(self.last, value)

    @property
    def suffix(self):
        """Return the suffix field."""
        return self.find_element(*self._suffix_locator)

    @suffix.setter
    def suffix(self, value):
        """Set the suffix field."""
        return self._set_value(self.suffix, value)

    @property
    def email(self):
        """Return the email address field."""
        return self.find_element(*self._email_locator)

    @email.setter
    def email(self, value):
        """Set the email address field."""
        return self._set_value(self.email, value)

    @property
    def phone(self):
        """Return the phone number field."""
        return self.find_element(*self._phone_locator)

    @phone.setter
    def phone(self, value):
        """Set the telephone number field."""
        return self._set_value(self.phone, value)

    @property
    def phone_type(self):
        """Return the phone type field."""
        return self.find_element(*self._phone_type_locator)

    @phone_type.setter
    def phone_type(self, value):
        """Set the telephone number type field."""
        return self._set_value(self.phone_type, value)

    @property
    def address(self):
        """Return the address line 1 field."""
        return self.find_element(*self._address_one_locator)

    @address.setter
    def address(self, value):
        """Set the address line 1 field."""
        return self._set_value(self.address, value)

    @property
    def address_line_two(self):
        """Return the address line 2 field."""
        return self.find_element(*self._address_two_locator)

    @address_line_two.setter
    def address_line_two(self, value):
        """Set the address line 2 field."""
        return self._set_value(self.address_line_two, value)

    @property
    def city(self):
        """Return the city name field."""
        return self.find_element(*self._city_locator)

    @city.setter
    def city(self, value):
        """Set the city name field."""
        return self._set_value(self.city, value)

    @property
    def state(self):
        """Return the state selection field."""
        return self.find_element(*self._state_locator)

    @state.setter
    def state(self, option):
        """Set the state of residence."""
        return self._set_pull_down_menu(self.state, option)

    @property
    def zip_code(self):
        """Return the zip code field."""
        return self.find_element(*self._zip_locator)

    @zip_code.setter
    def zip_code(self, value):
        """Set the zip code field."""
        return self._set_value(self.zip_code, value)

    @property
    def country(self):
        """Return the country selection field."""
        return self.find_element(*self._country_locator)

    @country.setter
    def country(self, option):
        """Set the country of residence."""
        return self._set_pull_down_menu(self.country, option)

    @property
    def amount(self):
        """Return the donation amount field."""
        return self.find_element(*self._amount_locator)

    @property
    def current_amount(self):
        """Return the current donation value."""
        return int(self.amount.get_attribute('value'))

    @amount.setter
    def amount(self, value):
        """Set the donation amount field."""
        return self._set_value(self.amount, value)

    @property
    def continue_button(self):
        """Return the continue button."""
        return self.find_element(*self._continue_button_locator)

    def submit(self):
        """Click the Continue button."""
        Utility.click_option(self.driver, element=self.continue_button)
        sleep(1.5)
        if not self.get_errors:
            from pages.rice.ebank import EBank
            sleep(2)
            return go_to_(EBank(self.driver))
        return self

    def get_errors(self):
        """Return a list of validation errors found."""
        errors = []
        fields = [
            ('First Name', self._first_name_error_locator),
            ('Last Name', self._last_name_error_locator),
            ('Email', self._email_error_locator),
            ('Phone', self._phone_error_locator),
            ('Phone Type', self._phone_type_error_locator),
            ('Address', self._address_one_error_locator),
            ('City', self._city_error_locator),
            ('State', self._state_error_locator),
            ('Zip', self._zip_error_locator),
            ('Country', self._country_error_locator),
            ('Donation Amount', self._amount_error_locator)
        ]
        for field, locator in fields:
            try:
                issue = self.find_element(*locator).text
                errors.append('{0}: {1}'.format(field, issue.strip()))
            except WebDriverException:
                pass
        return errors

    def _set_value(self, field, value):
        """Set a field value."""
        Utility.scroll_to(self.driver, element=field, shift=-80)
        field.send_keys(value)
        sleep(0.5)
        return self

    def _set_pull_down_menu(self, field, option):
        """Set a pull down menu field."""
        Utility.scroll_to(driver=self.driver, element=field, shift=-80)
        if 'open' not in field.get_attribute('class'):
            Utility.click_option(self.driver, element=field)
        if len(option) > 2:
            # received a full option name
            locator = (By.XPATH, '//li[text()="{0}"]'.format(option))
        else:
            locator = (By.CSS_SELECTOR, '[data-value={0}]'.format(option))
        # find out how far we need to scroll to see the selected option
        offset = self.driver.execute_script(
            'return arguments[0].offsetTop;',
            field.find_element(*locator))
        # then scroll the option list to that position
        self.driver.execute_script(
            'arguments[0].scrollTop = {0}'.format(offset),
            field.find_element(*self._options_locator))
        Utility.click_option(driver=self.driver,
                             element=field.find_element(*locator))
        return self
