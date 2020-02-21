"""Accounts password control forms."""

from __future__ import annotations

from time import sleep

from pypom import Page
from selenium.webdriver.common.by import By

from pages.accounts.base import AccountsBase
from pages.salesforce.home import Salesforce
from regions.accounts.fields import ERROR_SELECTOR, Email, Password
from utils.utilities import Utility, go_to_


class ChangePassword(AccountsBase):
    """Change the password for a currently logged in user."""

    URL_TEMPLATE = '/i/change_password_form'

    class Content(AccountsBase.Content, Password):
        """The change password form."""

        _content_message_locator = (
            By.CSS_SELECTOR, '.info-message')
        _log_in_button_locator = (
            By.CSS_SELECTOR, '[type=submit]')
        _password_locator = (
            By.CSS_SELECTOR, '#change_password_form_password')
        _show_password_toggle_locator = (
            By.CSS_SELECTOR, '#password-show-hide-button')

        _password_error_message_locator = (
            By.CSS_SELECTOR, _password_locator[1] + ERROR_SELECTOR)

        @property
        def message(self) -> str:
            """Return the change password explanation text.

            :return: the page expanation text
            :rtype: str

            """
            return self.find_element(*self._content_message_locator).text

        def log_in(self) -> Page:
            """Click the 'Log in' button.

            :return: the change password page if an error occurs or the user
                profile if the new password is accepted
            :rtype: :py:class:`~pages.accounts.reset.ChangePassword` or
                :py:class:`~pages.accounts.profile.Profile`

            """
            button = self.find_element(*self._log_in_button_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.25)
            if 'password' in self.driver.current_url:
                return self.page
            from pages.accounts.profile import Profile
            return go_to_(Profile(self.driver, base_url=self.page.base_url))

        def toggle_password_display(self) -> ChangePassword:
            """Toggle the password field to show or hide the value.

            :return: the Accounts log in page
            :rtype: :py:class:`~pages.accounts.home.AccountsHome`

            """
            toggle = self.find_element(*self._show_password_toggle_locator)
            Utility.click_option(self.driver, element=toggle)
            sleep(0.1)
            return self.page


class PasswordResetLinkSent(AccountsBase):
    """Reset link email sent confirmation page."""

    URL_TEMPLATE = '/i/reset_password'

    class Content(AccountsBase.Content):
        """Confirmation information pane."""

        _contact_support_link_locator = (
            By.CSS_SELECTOR, '[href*="force.com"]')
        _content_message_locator = (
            By.CSS_SELECTOR, '.info-message')
        _email_locator = (
            By.CSS_SELECTOR, '.info-message b')

        @property
        def email(self) -> str:
            """Return the email receiving the reset link.

            :return: the email receiving the password reset email and link
            :rtype: str

            """
            return self.find_element(*self._email_locator).text

        @property
        def message(self) -> str:
            """Return the password reset message including the email.

            :return: the explanation text including the email address
            :rtype: str

            """
            return (self.find_element(*self._content_message_locator)
                    .get_attribute('textContent'))

        def contact_us(self) -> Salesforce:
            """Click the 'Contact us' link.

            :return: the Salesforce support page
            :rtype: :py:class:`~pages.salesforce.home.Salesforce`

            """
            link = self.find_element(*self._contact_support_link_locator)
            Utility.click_option(self.driver, element=link)
            return go_to_(Salesforce(self.driver))


class ResetPassword(AccountsBase):
    """Reset an unknown password for a logged out user."""

    URL_TEMPLATE = '/i/reset_password_form'

    class Content(AccountsBase.Content, Email):
        """The password reset form."""

        _contact_support_link_locator = (
            By.CSS_SELECTOR, '[href*="force.com"]')
        _email_locator = (
            By.CSS_SELECTOR, '#reset_password_form_email')
        _reset_my_password_button_locator = (
            By.CSS_SELECTOR, '[type=submit]')

        _email_error_message_locator = (
            By.CSS_SELECTOR, _email_locator[1] + ERROR_SELECTOR)

        def contact_us(self) -> Salesforce:
            """Click the 'Contact us' link.

            :return: the Salesforce support page
            :rtype: :py:class:`~pages.salesforce.home.Salesforce`

            """
            link = self.find_element(*self._contact_support_link_locator)
            Utility.click_option(self.driver, element=link)
            return go_to_(Salesforce(self.driver))

        def reset_my_password(self) -> Page:
            """Click the 'Reset my password' button.

            :return: the reset password page if there is an error or the
                password reset message sent page if the password is accepted
            :rtype: :py:class:`~pages.accounts.reset.ResetPassword` or
                :py:class:`~pages.accounts.reset.PasswordResetLinkSent`

            """
            button = self.find_element(*self._reset_my_password_button_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.25)
            if '_form' in self.driver.current_url:
                return self.page
            return go_to_(
                PasswordResetLinkSent(
                    self.driver, base_url=self.page.base_url))


class SetPassword(ChangePassword):
    """Set a password for an account missing one."""

    URL_TEMPLATE = '/i/setup_password'
