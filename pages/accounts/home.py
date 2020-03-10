"""Home page objects."""

from __future__ import annotations

from time import sleep

from pypom import Page
from selenium.webdriver.common.by import By

from pages.accounts.base import AccountsBase
from pages.accounts.profile import Profile
from pages.accounts.reset import ResetPassword
from regions.accounts.fields import ERROR_SELECTOR
from regions.accounts.social import SocialLogins
from utils.accounts import AccountsException
from utils.email import RestMail
from utils.utilities import Utility, go_to_


class AccountsHome(AccountsBase):
    """The Accounts log in page."""

    URL_TEMPLATE = '/i/login'

    def log_in(self, username: str, password: str,
               destination: Page = None, base_url: str = None, **kwargs) \
            -> Page:
        """Log a user into the site.

        :param str username: the username or email address for the user
        :param str password: the password for the user
        :param Page destination: (optional) a Page destination, if known
        :param str base_url: (optional) the base URL for the destination Page
        :param kwargs: (optional) additional keyword arguments for the Page
        :return: the user's profile, a legal page, or the originating page
        :rtype: :py:class:`~pypom.Page`

        """
        self.content.email = username
        self.content.password = password
        return self.content._continue(destination, base_url, **kwargs)

    def service_log_in(self, user: str, password: str,
                       destination: Page = None, url: str = None, **kwargs) \
            -> Page:
        """Log into the site with a specific user from another service.

        .. note::
           Included for backwards compatibility

        """
        return self.log_in(user, password, destination, url, **kwargs)

    def student_signup(self, first_name: str, last_name: str, password: str,
                       email: RestMail = None,
                       page: Page = None, base_url: str = None) -> Page:
        """Register a new student user.

        :param str first_name: the user's first name
        :param str last_name: the user's last name
        :param str password: the user's selected password
        :param email: (optional) a provided RestMail address; if one is not
            given, an automatically generated one will be used
        :type email: :py:class:`~utils.email.RestMail`
        :param page: (optional) the expected page return
        :type page: :py:class:`~pypom.Page`
        :param str base_url: the template base URL for the returned page
        :return: the sign up page if there is an error, the user profile if the
            user signed up from Accounts, or the originating page if redirected
            from another OpenStax product
        :rtype: :py:class:`~pypom.Page`

        """
        sign_up = self.content.view_sign_up()
        student_signup = sign_up.content.sign_up_as_a_student().content
        student_signup.first_name = first_name
        student_signup.last_name = last_name
        if not email:
            email_user = (
                f'{first_name}.{last_name}.'
                f'{Utility.random_hex(Utility.random(3, 7))}'
                ).lower()
            email = RestMail(email_user)
        student_signup.email = email.address
        student_signup.password = password
        student_signup.i_agree()
        confirm_email = student_signup._continue().content
        box = email.wait_for_mail()
        pin = box[-1].pin
        confirm_email.pin = pin
        complete_signup = confirm_email.confirm_my_account().content.finish()
        if page:
            return go_to_(page(self.driver, base_url=base_url))
        return complete_signup

    class Content(AccountsBase.Content, SocialLogins):
        """The log in pane."""

        _continue_button_locator = (
            By.CSS_SELECTOR, '[type=submit]')
        _email_field_locator = (
            By.CSS_SELECTOR, '#login_form_email')
        _forgot_your_password_link_locator = (
            By.CSS_SELECTOR, '#forgot-password-link, #forgot-passwork-link')
        _password_field_locator = (
            By.CSS_SELECTOR, '#login_form_password')
        _show_password_toggle_locator = (
            By.CSS_SELECTOR, '#show-hide-button')

        _email_error_message_locator = (
            By.CSS_SELECTOR, _email_field_locator[1] + ERROR_SELECTOR)
        _password_error_message_locator = (
            By.CSS_SELECTOR, _password_field_locator[1] + ERROR_SELECTOR)

        @property
        def email(self) -> str:
            """Return the current email field address.

            :return: the current email form field value
            :rtype: str

            """
            return (self.find_element(*self._email_field_locator)
                    .get_attribute('value'))

        @property
        def email_error(self) -> str:
            """Return the email error message.

            :return: the email field error message, if found
            :rtype: str

            """
            if self.email_has_error:
                return (self.find_element(*self._email_error_message_locator)
                            .text)
            return ''

        @property
        def email_has_error(self) -> bool:
            """Return True if the email field has an error.

            :return: ``True`` if an error message is displayed below the email
                field
            :rtype: bool

            """
            email = self.find_element(*self._email_field_locator)
            return 'has-error' in email.get_attribute('class')

        @property
        def password(self) -> str:
            """Return the current password field value.

            :return: the current password form field value
            :rtype: str

            """
            return (self.find_element(*self._password_field_locator)
                    .get_attribute('value'))

        @property
        def password_error(self) -> str:
            """Return the password error message.

            :return: the password field error message, if found
            :rtype: str

            """
            if self.password_has_error:
                return (
                    self.find_element(*self._password_error_message_locator)
                        .text)
            return ''

        @property
        def password_has_error(self) -> bool:
            """Return True if the password field has an error.

            :return: ``True`` if an error message is displayed below the
                password field
            :rtype: bool

            """
            password = self.find_element(*self._password_field_locator)
            return 'has-error' in password.get_attribute('class')

        @email.setter
        def email(self, email: str):
            """Set the email log in field.

            :param str email: the email log in value
            :return: None

            """
            self.find_element(*self._email_field_locator) \
                .send_keys(email)

        def forgot_your_password(self) -> ResetPassword:
            """Click the Forgot your password? link.

            :return: the Reset my password page
            :rtype: :py:class:`~pages.accounts.reset.ResetPassword`

            """
            link = self.find_element(*self._forgot_your_password_link_locator)
            Utility.click_option(self.driver, element=link)
            return go_to_(
                ResetPassword(self.driver, base_url=self.page.base_url))

        @password.setter
        def password(self, password: str):
            """Set the password log in field.

            :param str password: the log in password
            :return: None

            """
            self.find_element(*self._password_field_locator) \
                .send_keys(password)

        def toggle_password_display(self) -> AccountsHome:
            """Toggle the password field to show or hide the value.

            :return: the Accounts log in page
            :rtype: :py:class:`~pages.accounts.home.AccountsHome`

            """
            toggle = self.find_element(*self._show_password_toggle_locator)
            Utility.click_option(self.driver, element=toggle)
            sleep(0.1)
            return self.page

        def _continue(self, previous: Page = None, base_url: str = None,
                      **kwargs) \
                -> Page:
            """Click the Continue button.

            :param Page previous: (optional) the Page object for the initial
                page that sent the log in request
            :param str base_url: (optional) the base URL for the previous Page
            :param kwargs: (optional) additional keyword arguments for the Page
            :return: the log in page if there is an error, the profile page if
                remaining on Accounts, the terms of use or privacy policy if a
                new policy is available, or the previous page if logging on to
                another OpenStax resource (like Tutor or OpenStax.org)
            :rtype: :py:class:`~pypom.Page`

            """
            current_page = self.page.location
            button = self.find_element(*self._continue_button_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.75)
            if self.driver.current_url == current_page:
                raise AccountsException(
                    self.driver.execute_script(
                        'return document.querySelector(".invalid-message")'
                        '.textContent;'))
            if previous:
                return go_to_(previous(self.driver, base_url, **kwargs))
            source = self.driver.page_source
            policies = 'Terms of Use' in source or 'Privacy policy' in source
            if 'accounts' in self.page.location and policies:
                from pages.accounts.legal import AcceptTerms
                return go_to_(AcceptTerms(self.driver, self.page.base_url))
            return go_to_(Profile(self.driver, self.page.base_url))
