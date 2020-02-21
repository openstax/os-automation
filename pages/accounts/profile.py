"""Profile page for logged in users."""

from __future__ import annotations

from time import sleep
from typing import List, Union

from pypom import Page, Region
from selenium.common.exceptions import (  # NOQA
    ElementNotVisibleException,  # NOQA
    NoSuchElementException,  # NOQA
    TimeoutException)  # NOQA
from selenium.webdriver.common.by import By

from pages.accounts.admin.base import AccountsAdmin
from pages.accounts.admin.contracts import Contracts
from pages.accounts.admin.docs import APIDocumentation
from pages.accounts.admin.security import Doorkeeper, Security
from pages.accounts.admin.users import Details
from pages.accounts.base import AccountsBase
from pages.accounts.reset import ChangePassword
from pages.web.home import WebHome
from utils.accounts import AccountsException, Name as UserName, Selector  # NOQA
from utils.utilities import Utility, go_to_


class Alert(Region):
    """A fade alert."""

    _root_locator = (
        By.CSS_SELECTOR, '.ox-alert')

    _close_button_locator = (
        By.CSS_SELECTOR, '.close')
    _content_message_locator = (
        By.CSS_SELECTOR, '.msg')

    @property
    def message(self) -> str:
        """Return the alert message.

        :return: the alert message text
        :rtype: str

        """
        return self.find_element(*self._content_message_locator).text

    def close(self) -> Union[Page, Region]:
        """Click the alert close 'x' button.

        :return: the alert box's parent object
        :rtype: :py:class:`~pypom.Page` or :py:class:`~pypom.Region`

        """
        button = self.find_element(*self._close_button_locator)
        Utility.click_option(self.driver, element=button)
        return self.page


class FieldEdit(Region):
    """Accept and cancel field edit buttons."""

    _accept_button_locator = (
        By.CSS_SELECTOR, '.editable-submit')
    _cancel_button_locator = (
        By.CSS_SELECTOR, '.editable-cancel')
    _error_field_locator = (
        By.CSS_SELECTOR, '[class*=error-block]')

    @property
    def error(self) -> str:
        """Return the error message.

        :return: the field error message, if found
        :rtype: str

        """
        try:
            return (self.find_element(*self._error_field_locator)
                    .get_attribute('textContent'))
        except NoSuchElementException:
            return ''

    def accept(self) -> Profile:
        """Click the accept checkmark button.

        :return: the user profile
        :rtype: :py:class:`~pages.accounts.profile.Profile`

        """
        button = self.find_element(*self._accept_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(1.0)
        return Utility.parent_page(self)

    def cancel(self) -> Profile:
        """Click the cancel x button.

        :return: the user profile
        :rtype: :py:class:`~pages.accounts.profile.Profile`

        """
        button = self.find_element(*self._cancel_button_locator)
        Utility.click_option(self.driver, element=button)
        return Utility.parent_page(self)


class GroupedProviders(Region):
    """The available or in use log in options pane."""

    _provider_locator = (
        By.CSS_SELECTOR, '.authentication')

    @property
    def providers(self) -> List[Provider]:
        """Return the list of enabled providers.

        :return: the list of currently enabled providers
        :rtype: list(:py:class:`~pages.accounts.profile.Provider`)

        """
        return [Provider(self, option)
                for option
                in self.find_elements(*self._provider_locator)]


class Popup(Region):
    """A confirmation pop up."""

    _root_locator = (
        By.CSS_SELECTOR, '[role=tooltip]')

    _content_message_locator = (
        By.CSS_SELECTOR, '.message')
    _cancel_button_locator = (
        By.CSS_SELECTOR, '.confirm-dialog-btn-abort')
    _ok_button_locator = (
        By.CSS_SELECTOR, '.confirm-dialog-btn-confirm')

    @property
    def message(self) -> str:
        """Return the pop up box message.

        :return: the pop up box text content
        :rtype: str

        """
        return self.find_element(*self._content_message_locator).text

    def cancel(self) -> Page:
        """Click the 'Cancel' button.

        :return: the current page
        :rtype: :py:class:`~pypom.Page`

        """
        button = self.find_element(*self._cancel_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.1)
        return Utility.parent_page(self)

    def ok(self) -> Page:
        """Click the 'OK' button.

        :return: the current page
        :rtype: :py:class:`~pypom.Page`

        """
        button = self.find_element(*self._ok_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.5)
        return Utility.parent_page(self)


class Provider(Region):
    """A log in provider."""

    _add_button_locator = (
        By.CSS_SELECTOR, '.mod-holder [class*=add]')
    _delete_button_locator = (
        By.CSS_SELECTOR, '.mod-holder [class*=delete]')
    _edit_button_locator = (
        By.CSS_SELECTOR, '.mod-holder [class*=edit]')
    _provider_name_locator = (
        By.CSS_SELECTOR, '.name')

    @property
    def name(self) -> str:
        """Return the provider name.

        :return: the provider name
        :rtype: str

        """
        return self.find_element(*self._provider_name_locator).text

    def add(self) -> Page:
        """Add a new log in method to the account.

        :return: the password setup page, the Facebook log in page or the
            Google log in page
        :rtype: :py:class:`~pages.accounts.reset.SetPassword`,
            :py:class:`~pages.facebook.home.Facebook`, or
            :py:class:`~pages.google.home.Google`

        """
        provider = self.name.lower()
        base_url = None
        if 'password' in provider:
            from pages.accounts.reset import SetPassword
            Destination = SetPassword
            base_url = Utility.parent_page(self).base_url
        elif 'facebook' in provider:
            from pages.facebook.home import Facebook
            Destination = Facebook
        else:
            from pages.google.home import Google
            Destination = Google
        button = self.find_element(*self._add_button_locator)
        Utility.click_option(self.driver, element=button)
        return go_to_(Destination(self.driver, base_url=base_url))

    def delete(self) -> Provider.Popup:
        """Remove the log in method from the account.

        :return: the confirmation pop up box
        :rtype: :py:class:`~pages.accounts.profile.Popup`

        """
        button = self.find_element(*self._delete_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.1)
        return Popup(self)

    def edit(self) -> ChangePassword:
        """Edit the password log in method.

        :return: the change password form
        :rtype: :py:class:`~pages.accounts.reset.ChangePassword`

        """
        base_url = Utility.parent_page(self).base_url
        button = self.find_element(*self._edit_button_locator)
        Utility.click_option(self.driver, element=button)
        return go_to_(ChangePassword(self.driver, base_url=base_url))


class Profile(AccountsBase):
    """A user profile."""

    URL_TEMPLATE = '/i/profile'

    _console_panel_locator = (
        By.CSS_SELECTOR, '#upper-corner-console')

    @property
    def console(self) -> Profile.Console:
        """Access the admin console links.

        :return: the admin console links
        :rtype: :py:class:`~pages.accounts.profile.Profile.Console`

        """
        console_root = self.find_element(*self._console_panel_locator)
        return self.Console(self, console_root)

    class Console(Region):
        """The admin console links."""

        _full_console_link_locator = (
            By.CSS_SELECTOR, '[href$=console]')
        _popup_console_link_locator = (
            By.CSS_SELECTOR, '[href$=admin]')

        _popup_console_root_selector = '#admin_console_dialog'

        @property
        def is_admin(self) -> bool:
            """Return True if the user is a site administrator.

            :return: ``True`` if the console links are found
            :rtype: bool

            """
            return bool(self.find_elements(*self._popup_console_link_locator))

        def view_popup_console(self) -> Profile.Console.PopupConsole:
            """Click the 'Popup Console' link.

            :return: the pop up console
            :rtype: :py:class:`~pages.accounts.profile.Profile.Console`

            """
            if not self.is_admin:
                raise AccountsException('user is not an administrator')
            link = self.find_element(*self._popup_console_link_locator)
            Utility.click_option(self.driver, element=link)
            sleep(0.2)
            modal_root = self.driver.execute_script(
                'return document.querySelector' +
                f'("{self._popup_console_root_selector}");')
            return self.PopupConsole(self, modal_root)

        def view_full_console(self) -> AccountsAdmin:
            """Open the full admin console.

            :return: the full administrator console
            :rtype: :py:class:`~pages.accounts.admin.base.AccountsAdmin`

            """
            if not self.is_admin:
                raise AccountsException('user is not an administrator')
            link = self.find_element(*self._full_console_link_locator)
            Utility.click_option(self.driver, element=link)
            return go_to_(
                AccountsAdmin(self.driver, base_url=self.page.base_url))

        class PopupConsole(Region):
            """The quick-links admin pop up console control."""

            _full_console_link_locator = (
                By.CSS_SELECTOR, '[href$=console]')
            _links_body_locator = (
                By.CSS_SELECTOR, '#links-tab')
            _links_tab_locator = (
                By.CSS_SELECTOR, f'[href$={_links_body_locator[1][1:]}]')
            _misc_body_locator = (
                By.CSS_SELECTOR, '#misc-tab')
            _misc_tab_locator = (
                By.CSS_SELECTOR, f'[href$={_misc_body_locator[1][1:]}]')
            _users_body_locator = (
                By.CSS_SELECTOR, '#users-tab')
            _users_tab_locator = (
                By.CSS_SELECTOR, f'[href$={_users_body_locator[1][1:]}]')

            def view_full_console(self) -> AccountsAdmin:
                """Click the 'Full Console >>' link.

                :return: the full administrator console
                :rtype: :py:class:`~pages.accounts.admin.base.AccountsAdmin`

                """
                full_console = self.find_element(
                    *self._full_console_link_locator)
                Utility.click_option(self.driver, element=full_console)
                return go_to_(
                    AccountsAdmin(self.driver, base_url=self.page.base_url))

            def view_links(self) -> Profile.Console.PopupConsole.Links:
                r"""Access the pop up console links tab.

                :return: the pop up console displaying the miscellaneous tab
                :rtype: :py:class:`~pages.accounts.profile.
                                    Profile.Console.PopupConsole.Links`

                """
                links_root = self.find_element(*self._links_body_locator)
                links_tab = self.find_element(*self._links_tab_locator)
                Utility.click_option(self.driver, element=links_tab)
                return self.Misc(self, links_root)

            def view_misc(self) -> Profile.Console.PopupConsole.Misc:
                r"""Access the pop up console misc tab.

                :return: the pop up console displaying the miscellaneous tab
                :rtype: :py:class:`~pages.accounts.profile.
                                    Profile.Console.PopupConsole.Misc`

                """
                misc_root = self.find_element(*self._misc_body_locator)
                misc_tab = self.find_element(*self._misc_tab_locator)
                Utility.click_option(self.driver, element=misc_tab)
                return self.Misc(self, misc_root)

            def view_users(self) -> Profile.Console.PopupConsole.Users:
                r"""Access the pop up console users tab.

                :return: the pop up console displaying the users tab
                :rtype: :py:class:`~pages.accounts.profile.
                                    Profile.Console.PopupConsole.Users`

                """
                users_root = self.find_element(*self._users_body_locator)
                users_tab = self.find_element(*self._users_locator)
                Utility.click_option(self.driver, element=users_tab)
                return self.Users(self, users_root)

            class Misc(Region):
                """Miscellaneous tasks section."""

            class Users(Region):
                """User section."""

                _results_list_root_locator = (
                    By.CSS_SELECTOR, '#search-results-list')
                _search_bar_locator = (
                    By.CSS_SELECTOR, '#search_terms')
                _search_button_locator = (
                    By.CSS_SELECTOR, '[type=submit]')
                _search_result_row_locator = (
                    By.CSS_SELECTOR, "tr.action-list-data-row")

                def search_for(self, topic: str) \
                        -> List[Profile.Console.PopupConsole.Users.Result]:
                    r"""Use the pop up console to search for a given string.

                    :param str topic: the search string
                    :return: the list of users matching the search string
                    :rtype: list(:py:class:`~pages.accounts.profile. \
                                            Profile.Console.PopupConsole. \
                                            Users.Result`)

                    """
                    results_list = self.find_element(
                        *self._results_list_root_locator)
                    self.find_element(*self._search_bar_locator) \
                        .send_keys(topic)
                    search_button = self.find_element(
                        *self._search_button_locator)
                    Utility.click_option(self.driver, element=search_button)
                    try:
                        self.wait.until(
                            lambda _: Utility.has_children(results_list))
                    except TimeoutException:
                        raise AccountsException('search not completed')
                    return [self.Result(self, line)
                            for line
                            in self.find_elements(
                                *self._search_result_row_locator)]

                class Result(Region):
                    """class for the search list column."""

                    _id_locator = (
                        By.CSS_SELECTOR, '.action-list-col-6:nth-child(1)')
                    _username_locator = (
                        By.CSS_SELECTOR, '.action-list-col-6 a')
                    _first_name_locator = (
                        By.CSS_SELECTOR, '.action-list-col-6:nth-child(3)')
                    _last_name_locator = (
                        By.CSS_SELECTOR, '.action-list-col-6:nth-child(4)')
                    _is_admin = (
                        By.CSS_SELECTOR, '.action-list-col-6:nth-child(5)')
                    _is_test = (
                        By.CSS_SELECTOR, '.action-list-col-6:nth-child(6)')
                    _sign_in_locator = (
                        By.LINK_TEXT, 'Sign in as')
                    _edit_locator = (
                        By.LINK_TEXT, 'Edit')

                    @property
                    def first_name(self) -> str:
                        """Return the user's first name.

                        :return: the user's first name
                        :rtype: str

                        """
                        return self.find_element(*self._first_name_locator) \
                                   .text

                    @property
                    def id(self) -> str:
                        """Return the user id.

                        :return: the user identification number
                        :rtype: str

                        """
                        return self.find_element(*self._id_locator) \
                                   .text

                    @property
                    def is_admin(self) -> bool:
                        """Return True if the user is an administrator.

                        :return: ``True`` if the user is an Accounts
                            administrator
                        :rtype: bool

                        """
                        is_admin = self.find_element(*self._is_admin).text
                        return is_admin.lower() == 'yes'

                    @property
                    def is_test(self) -> bool:
                        """Return True if the user is a test user.

                        :return: ``True`` if the user is marked as a test
                            account
                        :rtype: bool

                        """
                        is_test = self.find_element(*self._is_test).text
                        return is_test.lower() == "yes"

                    @property
                    def last_name(self) -> str:
                        """Return the user's last name.

                        :return: the user's last name
                        :rtype: str

                        """
                        return self.find_element(*self._last_name_locator) \
                                   .text

                    @property
                    def username(self) -> str:
                        """Return the username.

                        :return: the username
                        :rtype: str

                        """
                        return self.find_element(*self._username_locator) \
                                   .text

                    def edit(self) -> Details:
                        """Edit the selected user.

                        :return: the user details page for the selected user
                        :rtype: :py:class:`~pages.accounts.admin.users.Details`

                        """
                        link = self.find_element(*self._edit_locator)
                        base_url = Utility.parent_page(self).base_url
                        user_id = self.id
                        Utility.switch_to(self.driver, element=link)
                        return go_to_(
                            Details(self.driver,
                                    base_url=base_url,
                                    user_id=user_id))

                    def sign_in_as(self) -> Profile:
                        """Sign in to Accounts as the user.

                        :return: the selected user's profile
                        :rtype: :py:class:`~pages.accounts.profile.Profile`

                        """
                        sign_in = self.find_element(*self._sign_in_locator)
                        base_url = Utility.parent_page(self).base_url
                        Utility.click_option(self.driver, element=sign_in)
                        self.driver.get(f'{base_url}{Profile.URL_TEMPLATE}')
                        return go_to_(
                            Profile(self.driver, base_url=base_url))

                    def view_security_log(self) -> Security:
                        r"""Return the security log for the user.

                        :return: the security log for the user
                        :rtype: :py:class:`~pages.accounts.admin.security. \
                                            Security`

                        """
                        link = self.find_element(*self._username_locator)
                        base_url = Utility.parent_page(self).base_url
                        query = link.get_attribute('href') \
                                    .split('/security_log')[-1]
                        Utility.click_option(self.driver, element=link)
                        return go_to_(
                            Security(self.driver,
                                     base_url=base_url,
                                     query_string=query))

            class Links(Region):
                """Accounts program links section."""

                _security_log_link_locator = (
                    By.CSS_SELECTOR, '[href$=security_log]')
                _oauth_application_link_locator = (
                    By.CSS_SELECTOR, '[href*=oauth]')
                _fine_print_link_locator = (
                    By.CSS_SELECTOR, '[href$=fine_print]')
                _accounts_api_link_locator = (
                    By.CSS_SELECTOR, '[href*="/api"]')

                def view_api_documentation(self) -> APIDocumentation:
                    r"""View the Accounts API v1 documentation.

                    :return: the API v1 documentation
                    :rtype: :py:class:`~pages.accounts.admin.docs. \
                                        APIDocumentation`

                    """
                    return self._link_loader(
                        self._accounts_api_link_locator, APIDocumentation)

                def view_contracts(self) -> Contracts:
                    r"""View the FinePrint contracts.

                    :return: the FinePrint terms of use and privacy policy
                        contracts page
                    :rtype: :py:class:`~pages.accounts.admin.contracts. \
                                        Contracts`

                    """
                    return self._link_loader(
                        self._fine_print_link_locator, Contracts)

                def view_oauth_applications(self) -> Doorkeeper:
                    r"""View the OAuth applications.

                    :return: the Doorkeeper application list page
                    :rtype: :py:class:`~pages.accounts.admin.security. \
                                        Doorkeeper`

                    """
                    return self._link_loader(
                        self._oauth_application_link_locator, Doorkeeper)

                def view_security_log(self) -> Security:
                    """View the Accounts security log.

                    :return: the Accounts security log page
                    :rtype: :py:class:`~pages.accounts.admin.security.Security`

                    """
                    return self._link_loader(
                        self._security_log_link_locator, Security)

                def _link_loader(self, locator: Selector, destination: Page) \
                        -> Page:
                    """Click a link and return the destination page.

                    :param locator: a By-styled element selector
                    :param destination: the link destination page
                    :type locator: tuple(str, str)
                    :type destination: :py:class:`~pypom.Page`
                    :return: the destination page
                    :rtype: :py:class:`~pypom.Page`

                    """
                    link = self.find_element(*locator)
                    base_url = Utility.parent_page(self).base_url
                    Utility.click_option(self.driver, element=link)
                    return go_to_(destination(self.driver, base_url=base_url))

    class Content(Region):
        """The profile data pane."""

        _logo_link_locator = (
            By.CSS_SELECTOR, '.logo-wrapper a')
        _log_out_link_locator = (
            By.CSS_SELECTOR, '.sign-out')
        _redirect_back_button_locator = (
            By.CSS_SELECTOR, '#exit-icon a')
        _title_locator = (
            By.CSS_SELECTOR, '.title')

        _email_section_locator = (
            By.XPATH, '//div[div[contains(text(),"Email addresses")]]')
        _enabled_providers_section_locator = (
            By.CSS_SELECTOR, '.row.enabled-providers')
        _name_section_locator = (
            By.CSS_SELECTOR, '.row.name')
        _other_providers_section_locator = (
            By.CSS_SELECTOR, '.row.other-sign-in')
        _username_section_locator = (
            By.XPATH, '//div[div[contains(text(),"Username")]]')

        @property
        def emails(self) -> Profile.Content.Emails:
            """Access the user emails section.

            :return: the user emails section
            :rtype: :py:class:`~pages.accounts.profile.Profile.Content.Emails`

            """
            email_root = self.find_element(*self._email_section_locator)
            return self.Emails(self, email_root)

        @property
        def enabled_providers(self) -> Profile.Content.EnabledProviders:
            r"""Access the enabled log in providers section.

            :return: the enabled log in providers section
            :rtype: :py:class:`~pages.accounts.profile. \
                                Profile.Content.EnabledProviders`

            """
            provider_root = self.find_element(
                *self._enabled_providers_section_locator)
            return self.EnabledProviders(self, provider_root)

        @property
        def has_username(self) -> bool:
            """Return True if the current user has an assigned username.

            :return: ``True`` if the account has a username
            :rtype: bool

            """
            return bool(self.find_elements(*self._username_section_locator))

        @property
        def name(self) -> Profile.Content.Name:
            """Access the user name section.

            :return: the name section
            :rtype: :py:class:`~pages.accounts.profile.Profile.Content.Name`

            """
            name_root = self.find_element(*self._name_section_locator)
            return self.Name(self, name_root)

        @property
        def other_providers(self) -> Profile.Content.OtherProviders:
            r"""Access the available log in providers section.

            :return: the available log in providers section
            :rtype: :py:class:`~pages.accounts.profile. \
                                Profile.Content.OtherProviders`

            """
            provider_root = self.find_element(
                *self._other_providers_section_locator)
            return self.OtherProviders(self, provider_root)

        @property
        def title(self) -> str:
            """Return the page title.

            :return: the page title
            :rtype: str

            """
            return self.find_element(*self._title_locator).text

        @property
        def username(self) -> Profile.Content.Username:
            r"""Access the username section.

            :return: the username section
            :rtype: :py:class:`~pages.accounts.profile. \
                                Profile.Content.Username`

            """
            username_root = self.find_element(*self._username_section_locator)
            return self.Username(self, username_root)

        def home(self) -> WebHome:
            """Click on the OpenStax logo.

            :return: the OpenStax.org web page
            :rtype: :py:class:`~pages.web.home.WebHome`

            """
            logo = self.find_element(*self._logo_link_locator)
            Utility.click_option(self.driver, element=logo)
            return go_to_(WebHome(self.driver))

        def log_out(self) -> Page:
            """Click the 'Log out' link.

            :return: the Accounts sign in page
            :rtype: :py:class:`~pages.accounts.home.AccountsHome`

            """
            link = self.find_element(*self._log_out_link_locator)
            Utility.click_option(self.driver, element=link)
            from pages.accounts.home import AccountsHome
            return go_to_(
                AccountsHome(self.driver, base_url=self.page.base_url))

        def redirect(self) -> Page:
            """Click the redirect 'x' button.

            :return: the originating page or the user profile if the originator
                is Accounts
            :rtype: :py:class:`~pypom.Page` or
                :py:class:`~pages.accounts.profile.Profile`

            """
            button = self.find_element(*self._redirect_back_button_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.5)
            if 'profile' in self.driver.current_url:
                return self.page
            return Page(self.driver)

        class Emails(Region):
            """Account emails."""

            _current_email_locator = (
                By.CSS_SELECTOR, '.email-entry:not(.new)')
            _add_email_address_link_locator = (
                By.CSS_SELECTOR, '#add-an-email')
            _new_email_entry_locator = (
                By.CSS_SELECTOR, '.email-entry.new')

            @property
            def emails(self) -> List[Profile.Content.Emails.Email]:
                r"""Access the current emails list.

                :return: the account emails
                :rtype: list(:py:class:`~pages.accounts.profile. \
                                         Profile.Content.Emails.Email`)

                """
                return [self.Email(self, email)
                        for email
                        in self.find_elements(*self._current_email_locator)]

            @property
            def new_email(self) -> Profile.Content.Emails.Email:
                r"""Access the new email entry.

                :return: the new account email entry form
                :rtype: :py:class:`~pages.accounts.profile. \
                                    Profile.Content.Emails.Email`

                """
                new_email_root = self.find_element(
                    *self._new_email_entry_locator)
                return self.Email(self, new_email_root)

            def add_email_address(self) -> Profile.Content.Emails.Email:
                r"""Click the 'Add email address' link.

                :return: the new account email entry form
                :rtype: :py:class:`~pages.accounts.profile. \
                                    Profile.Content.Emails.Email`

                """
                link = self.find_element(*self._add_email_address_link_locator)
                Utility.click_option(self.driver, element=link)
                return self.new_email

            class Email(FieldEdit):
                """An individual account email."""

                _email_field_locator = (
                    By.CSS_SELECTOR, '.editable-input input')
                _email_locator = (
                    By.CSS_SELECTOR, '.value')
                _email_open_close_toggle_locator = (
                    By.CSS_SELECTOR, '.editable-click')
                _resend_confirmation_link_locator = (
                    By.CSS_SELECTOR, '[type=submit]')
                _delete_email_button_locator = (
                    By.CSS_SELECTOR, '.delete a')
                _searchable_checkbox_locator = (
                    By.CSS_SELECTOR, '[type=checkbox]')
                _unconfirmed_email_locator = (
                    By.CSS_SELECTOR, '.unconfirmed-warning')

                @property
                def email(self) -> str:
                    """Return the email address.

                    :return: the email address
                    :rtype: str

                    """
                    return self.find_element(*self._email_locator).text

                @email.setter
                def email(self, email: str):
                    """Set the new email address.

                    :param str email: the new email address
                    :return: None

                    """
                    self.find_element(*self._email_field_locator) \
                        .send_keys(email)

                @property
                def is_confirmed(self) -> bool:
                    """Return True if the email address is confirmed.

                    :return: ``True`` if the unconfirmed warning is not found
                    :rtype: bool

                    """
                    return not bool(
                        self.find_elements(*self._unconfirmed_email_locator))

                @property
                def is_expanded(self) -> bool:
                    """Return True if the email pane is expanded.

                    :return: ``True`` when the ``expanded`` class is found on
                        the email root element
                    :rtype: bool

                    """
                    return 'expanded' in self.root.get_attribute('class')

                def delete(self) -> Popup:
                    """Click the 'Delete' link.

                    :return: the delete confirmation pop up
                    :rtype: :py:class:`~pages.accounts.profile.Popup`

                    """
                    button = self.find_element(
                        *self._delete_email_button_locator)
                    Utility.click_option(self.driver, element=button)
                    sleep(0.1)
                    return Popup(self)

                def let_other_users_find_me_by_this_email(self) \
                        -> Profile.Content.Emails.Email:
                    r"""Click the 'Let other users find me...' checkbox.

                    :return: the email address section
                    :rtype: :py:class:`~pages.accounts.profile. \
                                        Profile.Content.Emails.Email`

                    """
                    checkbox = self.find_element(
                        *self._searchable_checkbox_locator)
                    Utility.click_option(self.driver, element=checkbox)
                    sleep(0.1)
                    return self

                def resend_confirmation_email(self) -> Alert:
                    """Click the 'Resend confirmation email' link.

                    :return: the alert box for the email line
                    :rtype: :py:class:`~pages.accounts.profile.Alert`

                    """
                    if not self.is_expanded:
                        raise AccountsException(
                            'link not visible; control pane not expanded')
                    link = self.find_element(
                        *self._resend_confirmation_link_locator)
                    Utility.click_option(self.driver, element=link)
                    sleep(0.25)
                    return Alert(self)

                def toggle(self) -> Profile.Content.Emails.Email:
                    r"""Click the email address to open or close the pane.

                    :return: the email address section
                    :rtype: :py:class:`~pages.accounts.profile. \
                                        Profile.Content.Emails.Email`

                    """
                    toggle = self.find_element(
                        *self._email_open_close_toggle_locator)
                    Utility.click_option(self.driver, element=toggle)
                    sleep(0.33)
                    return self

        class EnabledProviders(GroupedProviders):
            """Enabled log in providers."""

        class Name(FieldEdit):
            """The user name."""

            _name_field_locator = (
                By.CSS_SELECTOR, '#name')
            _title_field_locator = (
                By.CSS_SELECTOR, '[name=title]')
            _first_name_field_locator = (
                By.CSS_SELECTOR, '[name=first_name]')
            _last_name_field_locator = (
                By.CSS_SELECTOR, '[name=last_name]')
            _suffix_field_locator = (
                By.CSS_SELECTOR, '[name=suffix]')

            @property
            def first_name(self) -> str:
                """Return the current first name value.

                :return: the current user's first name
                :rtype: str

                """
                return (self.find_element(*self._first_name_field_locator)
                        .get_attribute('value'))

            @first_name.setter
            def first_name(self, first_name: str):
                """Set the first name field.

                :param str first_name: the new user first name
                :return: None

                """
                field = self.find_element(*self._first_name_field_locator)
                Utility.clear_field(self.driver, field=field)
                field.send_keys(first_name)

            @property
            def full_name(self) -> str:
                """Return the current name value.

                :return: the current user's name
                :rtype: str

                """
                return self.find_element(*self._name_field_locator).text

            @property
            def last_name(self) -> str:
                """Return the current last name value.

                :return: the current user's last name
                :rtype: str

                """
                return (self.find_element(*self._last_name_field_locator)
                        .get_attribute('value'))

            @last_name.setter
            def last_name(self, last_name: str):
                """Set the last name field.

                :param str last_name: the new user last name
                :return: None

                """
                field = self.find_element(*self._last_name_field_locator)
                Utility.clear_field(self.driver, field=field)
                field.send_keys(last_name)

            @property
            def suffix(self) -> str:
                """Return the current suffix value.

                :return: the current user's suffix
                :rtype: str

                """
                return (self.find_element(*self._suffix_field_locator)
                        .get_attribute('value'))

            @suffix.setter
            def suffix(self, suffix: str):
                """Set the suffix field.

                :param str suffix: the new user suffix
                :return: None

                """
                field = self.find_element(*self._suffix_field_locator)
                Utility.clear_field(self.driver, field=field)
                field.send_keys(suffix)

            @property
            def title(self) -> str:
                """Return the current title value.

                :return: the current user's title
                :rtype: str

                """
                return (self.find_element(*self._title_field_locator)
                        .get_attribute('value'))

            @title.setter
            def title(self, title: str):
                """Set the title field.

                :param str title: the new user title
                :return: None

                """
                field = self.find_element(*self._title_field_locator)
                Utility.clear_field(self.driver, field=field)
                field.send_keys(title)

            def change_name(self) -> Profile.Content.Name:
                r"""Click the user's name.

                :return: the user's name pane
                :rtype: :py:class:`~pages.accounts.profile. \
                                    Profile.Content.Name`

                """
                field = self.find_element(*self._name_field_locator)
                Utility.click_option(self.driver, element=field)
                sleep(0.1)
                return self

            def get_name_parts(self) -> UserName:
                """Return the four name parts.

                :return: the four parts of a user profile name (title, first
                    name, last name and suffix)
                :rtype: tuple(str, str, str, str)

                """
                self.change_name()
                name = [self.title,
                        self.first_name,
                        self.last_name,
                        self.suffix]
                self.cancel()
                return name

        class OtherProviders(GroupedProviders):
            """Other provider options."""

        class Username(FieldEdit):
            """The username."""

            _clear_username_button_locator = (
                By.CSS_SELECTOR, '.editable-clear-x')
            _username_field_locator = (
                By.CSS_SELECTOR, '#username')
            _username_input_field_locator = (
                By.CSS_SELECTOR, '.editable-input input')

            @property
            def username(self) -> str:
                """Return the current username.

                :return: the current username
                :rtype: str

                """
                return self.find_element(*self._username_field_locator).text

            @username.setter
            def username(self, username: str):
                """Set the new username.

                :param str username: the new username
                :return: None

                """
                field = self.find_element(*self._username_input_field_locator)
                Utility.clear_field(self.driver, field=field)
                field.send_keys(username)

            def change_username(self) -> Profile.Content.Username:
                r"""Click the username.

                :return: the username pane
                :rtype: :py:class:`~pages.accounts.profile. \
                                    Profile.Content.Username`

                """
                field = self.find_element(*self._username_field_locator)
                Utility.click_option(self.driver, element=field)
                sleep(0.1)
                return self

            def clear_username(self) -> Profile.Content.Username:
                r"""Click the clear field 'x' button.

                :return: the username pane
                :rtype: :py:class:`~pages.accounts.profile. \
                                    Profile.Content.Username`

                """
                button = self.find_element(
                    *self._clear_username_button_locator)
                Utility.click_option(self.driver, element=button)
                sleep(0.1)
                return self
