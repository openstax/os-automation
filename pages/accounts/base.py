"""Basic page parent for all Accounts pages."""

from __future__ import annotations

from time import sleep
from typing import Union

from pypom import Page, Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.accounts.legal import Copyright, Terms
from pages.rice.home import Rice
from utils.utilities import Utility, go_to_


class AccountsBase(Page):
    """The base page for each Accounts class."""

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
           We delay the return by 2 seconds for Safari to insure the page is
           loaded and displayed.

        :return: ``True`` when the Accounts content is found
        :rtype: bool

        """
        return (self.find_element(*self._content_locator) and
                ((sleep(2.0) or True) if self.is_safari else True))

    @property
    def menu(self) -> Union[AccountsBase.MenuBar, None]:
        """Access the Accounts' page menu bar, if found.

        :return: the Accounts' menu bar or ``None`` if it is missing (Profile)
        :rtype: :py:class:`~pages.accounts.base.AccountsBase.MenuBar` or None

        """
        bar_root = self.find_element(*self._main_menu_locator)
        return self.MenuBar(self, bar_root)

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

    def close_tab(self) -> Page:
        """Close the current tab and switch to the remaining one.

        Assumes 2 browser tabs are open.
        """
        Utility.close_tab(self.driver)
        return self

    @property
    def location(self) -> str:
        """Return the current URL.

        :return: the current page URL
        :rtype: str

        """
        return self.driver.current_url

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
           We default to a standard 4:3 ration 1024px x 768px.

        :param int width: (optional) the desired browser window width
        :param int height: (optional) the desired browser window height
        :return: None

        """
        self.driver.set_window_size(width, height)
        sleep(1.0)

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

        @property
        def view_copyright(self) -> Copyright:
            """Display the OpenStax Accounts copyright and licensing notice.

            :return: the copyright notice
            :rtype: :py:class:`~pages.accounts.legal.Copyright`

            """
            copyright = self.find_element(*self._copyright_locator)
            Utility.click_option(self.driver, element=copyright)
            return go_to_(Copyright(self.driver, self.page.base_url))

        @property
        def view_terms_of_use(self) -> Terms:
            """Display the OpenStax Accounts policies.

            :return: the terms of use and privacy policy page
            :rtype: :py:class:`~pages.accounts.legal.Terms`

            """
            terms = self.find_element(*self._terms_locator)
            Utility.click_option(self.driver, element=terms)
            return go_to_(Terms(self.driver, self.page.base_url))

        def go_to_rice(self):
            """Load the Rice webpage."""
            rice = self.find_element(*self._rice_link_locator)
            Utility.click_option(self.driver, element=rice)
            return go_to_(Rice(self.driver))

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

            :return: the Accounts login page if a user is not logged in or the
                Profile page if a user is logged in
            :rtype: :py:class:`~pages.accounts.home.AccountsHome` or
                :py:class:`~pages.accounts.profile.Profile`

            """
            go_home = self.find_element(*self._logo_locator)
            Utility.click_option(self.driver, element=go_home)
            sleep(0.5)
            if 'profile' in self.page.location:
                from pages.accounts.profile import Profile
                return go_to_(Profile(self.driver, self.page.base_url))
            from pages.accounts.home import AccountsHome
            return go_to_(AccountsHome(self.driver, self.page.base_url))
