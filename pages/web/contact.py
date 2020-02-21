"""The Web contact form."""

from pypom import Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect

from pages.web.base import WebBase
from utils.utilities import Utility, go_to_, go_to_external_
from utils.web import Web


class Contact(WebBase):
    """The web contact form."""

    URL_TEMPLATE = '/contact'

    _form_locator = (By.CSS_SELECTOR, '.form')
    _topic_locator = (By.CSS_SELECTOR, '.select')
    _header_locator = (By.CSS_SELECTOR, '.hero h1')
    _address_locator = (By.CSS_SELECTOR, '[data-html=mailing_address] p')
    _support_locator = (By.CSS_SELECTOR, '#main [href*=force]')

    @property
    def loaded(self):
        """Return True when the form and sidebar text are found."""
        return (self.find_element(*self._form_locator) and
                self.find_element(*self._topic_locator) and
                self.find_element(*self._address_locator))

    def is_displayed(self):
        """Return True if the heading is displayed."""
        return self.find_element(*self._header_locator).is_displayed()

    @property
    def title(self):
        """Return the page title."""
        return self.find_element(*self._header_locator).text.strip()

    @property
    def address(self):
        """Return the OpenStax mailing address."""
        return (self.find_element(*self._address_locator)
                .get_attribute('innerHTML').replace('<br>', '\n').strip())

    @property
    def support(self):
        """Return the user support link."""
        return self.wait.until(
            expect.presence_of_element_located(self._support_locator))

    def visit_the_support_center(self):
        """Click on the support link."""
        link = self.find_element(*self._support_locator)
        url = link.get_attribute('href')
        Utility.switch_to(self.driver, self._support_locator,
                          force_js_click=self.is_safari)
        from pages.salesforce.home import Salesforce
        return go_to_external_(Salesforce(self.driver), url)

    @property
    def form(self):
        """Access the contact form."""
        form_root = self.find_element(*self._form_locator)
        return self.Form(self, form_root)

    class Form(Region):
        """The Contact Us form."""

        ERROR = ' ~ span'

        _topic_locator = (By.CSS_SELECTOR, '.select')
        _current_topic_locator = (By.CSS_SELECTOR, '.select > .item')
        _option_locator = (By.CSS_SELECTOR, '.select .option')
        _name_locator = (By.CSS_SELECTOR, '[name=name]')
        _email_locator = (By.CSS_SELECTOR, '[name=email]')
        _message_locator = (By.CSS_SELECTOR, '[name=description]')
        _send_locator = (By.CSS_SELECTOR, '[type=submit]')

        _name_error_locator = (By.CSS_SELECTOR, _name_locator[1] + ERROR)
        _email_error_locator = (By.CSS_SELECTOR, _email_locator[1] + ERROR)
        _message_error_locator = (By.CSS_SELECTOR, _message_locator[1] + ERROR)

        @property
        def topic_drop_down(self):
            """Return the contact message subject drop down menu."""
            return self.find_element(*self._topic_locator)

        @property
        def topic(self):
            """Return the current message topic."""
            return self.find_element(*self._current_topic_locator).text

        @topic.setter
        def topic(self, subject):
            """Set the message topic."""
            if subject not in Web.TOPICS:
                raise ValueError('{0} is not a recognized contact topic'
                                 .format(subject))
            if 'open' not in self.topic_drop_down.get_attribute('class'):
                Utility.click_option(self.driver, element=self.topic_drop_down)
            for option in self.find_elements(*self._option_locator):
                if subject == option.get_attribute('data-value'):
                    Utility.click_option(self.driver, element=option)
            return self

        @property
        def name(self):
            """Return the name input."""
            return self.find_element(*self._name_locator)

        @name.setter
        def name(self, name):
            """Set the user's name."""
            self.name.send_keys(name)
            return self

        @property
        def email(self):
            """Return the email input."""
            return self.find_element(*self._email_locator)

        @email.setter
        def email(self, email):
            """Set the user's email address."""
            self.email.send_keys(email)
            return self

        @property
        def message(self):
            """Return the message body text box."""
            return self.find_element(*self._message_locator)

        @message.setter
        def message(self, message):
            """Enter the message body."""
            self.message.send_keys(message)
            return self

        def send(self):
            """Submit the contact message."""
            button = self.find_element(*self._send_locator)
            Utility.click_option(self.driver, element=button)
            issues = self.errors
            if issues:
                return issues
            return go_to_(ContactConfirmation(self.driver, self.page.base_url))

        @property
        def errors(self):
            """Return any form validation errors."""
            issues = []
            name_error = self.find_element(*self._name_error_locator).text
            email_error = self.find_element(*self._email_error_locator).text
            message_error = (self.find_element(*self._message_error_locator)
                             .text)
            if name_error:
                issues.append('Name: {0}'.format(name_error))
            if email_error:
                issues.append('Email: {0}'.format(email_error))
            if message_error:
                issues.append('Message: {0}'.format(message_error))
            return issues


class ContactConfirmation(WebBase):
    """The post-contact form submission confirmation page."""

    _title_locator = (By.CSS_SELECTOR, '.subhead h1')
    _subjects_locator = (By.CSS_SELECTOR, '[href$=subjects]')

    @property
    def loaded(self):
        """Return True when the view subjects button is displayed."""
        return self.button.is_displayed()

    def is_displayed(self):
        """Return True when loaded."""
        return self.loaded

    @property
    def title(self):
        """Return the page title."""
        return self.find_element(*self._title_locator).text.strip()

    @property
    def button(self):
        """Return the subjects button."""
        return self.find_element(*self._subjects_locator)

    def view_subjects(self):
        """Click on the Subjects button."""
        Utility.click_option(self.driver, element=self.button)
        from pages.web.subjects import Subjects
        return go_to_(Subjects(self.driver, self.base_url))
