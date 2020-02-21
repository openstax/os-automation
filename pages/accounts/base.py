"""Basic page parent for all Accounts pages."""

from __future__ import annotations

from time import sleep
from typing import Union

from pypom import Page, Region
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

from pages.rice.home import Rice
from utils.accounts import AccountsException
from utils.utilities import Utility, go_to_


class AccountsBase(Page):
    """The base page for each Accounts class."""

    _body_tag_locator = (
        By.CSS_SELECTOR, 'body')
    _content_locator = (
        By.CSS_SELECTOR, '.main-menu ~ .content:not([id]), #application-body')
    _footer_locator = (
        By.CSS_SELECTOR, '.main-menu ~ [id*=footer], #application-footer')
    _main_menu_locator = (
        By.CSS_SELECTOR, '.main-menu, #application-header')

    @property
    def content(self) -> AccountsBase.Content:
        """Access the Accounts' page content.

        :return: the Accounts page content
        :rtype: :py:class:`~pages.accounts.base.AccountsBase.Content`

        """
        content_root = self.find_element(*self._content_locator)
        return self.Content(self, content_root)

    @property
    def footer(self) -> AccountsBase.Footer:
        """Access the Accounts' page footer.

        :return: the Accounts page footer
        :rtype: :py:class:`~pages.accounts.base.AccountsBase.Footer`

        """
        footer_root = self.find_element(*self._footer_locator)
        return self.Footer(self, footer_root)

    @property
    def is_displayed(self) -> bool:
        """Return True when the Accounts content is displayed.

        :return: ``True`` when the Accounts main body content is displayed
        :rtype: bool

        """
        try:
            return self.find_element(*self._content_locator).is_displayed()
        except NoSuchElementException:
            return False

    @property
    def is_safari(self) -> bool:
        """Return True if the browser in use is Safari.

        :return: ``True`` if the browser in use is Safari
        :rtype: bool

        """
        return self.driver.capabilities.get('browserName').lower() == 'safari'

    @property
    def loaded(self) -> bool:
        """Return True when the Accounts page is loaded.

        .. note::
           We delay the check by 1/2 second for Safari and Firefox to insure
           the page is loading prior to the full DOM ``load``.

        :return: ``True`` when the Accounts content is found
        :rtype: bool

        """
        self.wait.until(
            lambda _: self.find_elements(*self._body_tag_locator))
        script = (r'document.addEventListener("load", function(event) {});')
        sleep(0.5)
        return self.driver.execute_script(script) or self.content

    @property
    def location(self) -> str:
        """Return the current URL.

        :return: the current page URL
        :rtype: str

        """
        return self.driver.current_url

    @property
    def menu(self) -> Union[AccountsBase.MenuBar, None]:
        """Access the Accounts' page menu bar, if found.

        :return: the Accounts' menu bar or ``None`` if it is missing (Profile)
        :rtype: :py:class:`~pages.accounts.base.AccountsBase.MenuBar` or None

        """
        bar_root = self.find_element(*self._main_menu_locator)
        return self.MenuBar(self, bar_root)

    @property
    def page_source(self) -> str:
        """Return the current page source HTML.

        :return: the current page source
        :rtype: str

        """
        return self.driver.page_source

    @property
    def url(self) -> str:
        """Return the last segment of the current URL.

        :return: the final segment of the current URL (everything after the
            last '/')
        :rtype: str

        """
        return self.location.split('/')[-1]

    def back(self) -> Page:
        """Go to the previous page in the browser history.

        :return: the current page
        :rtype: :py:class:`~pages.accounts.base.AccountsBase`

        """
        self.driver.execute_script(
            'window.history.go(-1);'
            r'document.addEventListener("DOMContent", function(event) {});')
        return self

    def close_tab(self):
        """Close the current tab and switch to the remaining one.

        .. note::
           Assumes 2 browser tabs are open; switches the window handle to the
           remaining tab.

        :return: None

        """
        Utility.close_tab(self.driver)

    def reload(self) -> Page:
        """Reload the current page.

        :return: the current page
        :rtype: :py:class:`~pages.accounts.base.AccountsBase`

        """
        self.driver.refresh()
        self.wait_for_page_to_load()
        return self

    def resize_window(self, width: int = 1024, height: int = 768):
        """Set the browser window size.

        .. note::
           We default to a standard 4:3 ratio 1024px x 768px.

        :param int width: (optional) the desired browser window width
        :param int height: (optional) the desired browser window height
        :return: None

        """
        self.driver.set_window_size(width, height)
        sleep(1.0)

    class Content(Region):
        """The main content region."""

        _header_text_locator = (
            By.CSS_SELECTOR, '.page-header')
        _log_in_tab_locator = (
            By.CSS_SELECTOR, '.tab.login')
        _sign_up_tab_locator = (
            By.CSS_SELECTOR, '.tab.signup')

        @property
        def header(self) -> str:
            """Return the page heading.

            :return: the body content header
            :rtype: str

            """
            return self.find_element(*self._header_text_locator).text

        def view_log_in(self) -> Page:
            """Click the Log in tab.

            :return: the Accounts Log in page
            :rtype: :py:class:`~pages.accounts.home.AccountsHome`

            """
            tab = self.find_element(*self._log_in_tab_locator)
            Utility.click_option(self.driver, element=tab)
            from page.accounts.home import AccountsHome
            return go_to_(AccountsHome(self.driver, self.page.base_url))

        def view_sign_up(self) -> Page:
            """Click the Sign up tab.

            :return: the Accounts Log in page
            :rtype: :py:class:`~pages.accounts.home.AccountsHome`

            """
            tab = self.find_element(*self._sign_up_tab_locator)
            Utility.click_option(self.driver, element=tab)
            from pages.accounts.signup import Signup
            return go_to_(Signup(self.driver, self.page.base_url))

    class Footer(Region):
        """The Accounts footer."""

        _rice_link_locator = (
            By.CSS_SELECTOR, '[href*=rice]')
        _copyright_locator = (
            By.CSS_SELECTOR, '[href*=copyright]')
        _terms_locator = (
            By.CSS_SELECTOR, '[href*=terms]')

        @property
        def copyright(self) -> str:
            """Return the brief copyright message.

            :return: the short copyright message displayed on Accounts pages
            :rtype: str

            """
            return self.find_element(*self._copyright_locator).text

        @property
        def is_displayed(self) -> bool:
            """Return True if the footer is displayed.

            :return: ``True`` if the Accounts footer is displayed
            :rtype: bool

            """
            return self.root.is_displayed()

        def go_to_rice(self) -> Rice:
            """Click the Rice University logo.

            :return: the Rice University home page
            :rtype: :py:class:`~pages.rice.home.Rice`
            :raises :py:class:`~utils.accounts.AccountsException`: if the Rice
                webpage is not loaded

            """
            rice = self.find_element(*self._rice_link_locator)
            Utility.click_option(self.driver, element=rice)
            try:
                self.wait.until(
                    lambda _: 'rice.edu' in self.driver.current_url)
            except TimeoutException:
                raise AccountsException('Rice webpage did not load')
            return go_to_(Rice(self.driver))

        def view_copyright(self) -> Page:
            """Display the OpenStax Accounts copyright and licensing notice.

            :return: the copyright notice
            :rtype: :py:class:`~pages.accounts.legal.Copyright`

            """
            copyright = self.find_element(*self._copyright_locator)
            Utility.click_option(self.driver, element=copyright)
            from pages.accounts.legal import Copyright
            return go_to_(Copyright(self.driver, self.page.base_url))

        def view_terms_of_use(self) -> Page:
            """Display the OpenStax Accounts policies.

            :return: the terms of use and privacy policy page
            :rtype: :py:class:`~pages.accounts.legal.Terms`

            """
            terms = self.find_element(*self._terms_locator)
            Utility.click_option(self.driver, element=terms)
            from pages.accounts.legal import Terms
            return go_to_(Terms(self.driver, self.page.base_url))

        show_copyright = view_copyright
        show_terms_of_use = view_terms_of_use

    class MenuBar(Region):
        """The Accounts menu bar."""

        _logo_locator = (
            By.CSS_SELECTOR, 'a')

        @property
        def is_displayed(self) -> bool:
            """Return True if the menu bar is displayed.

            :return: ``True`` if the Accounts menu bar is displayed
            :rtype: bool

            """
            return self.root.is_displayed()

        def go_home(self) -> Page:
            """Follow the OpenStax logo link back to the site home page.

            :return: the OpenStax.org web page
            :rtype: :py:class:`~pages.web.home.WebHome`

            """
            go_home = self.find_element(*self._logo_locator)
            Utility.click_option(self.driver, element=go_home)
            sleep(0.5)
            from pages.web.home import WebHome
            return go_to_(WebHome(self.driver, self.page.base_url))
