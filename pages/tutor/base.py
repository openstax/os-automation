"""The Tutor base objects."""

from __future__ import annotations

from time import sleep

from pypom import Page, Region
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.rice.home import Rice
from pages.salesforce.home import Salesforce
from regions.tutor.nav import TutorNav
from utils.utilities import Utility, go_to_, go_to_external_


class TutorShared(Page):
    """Shared base page functions."""

    _root_locator = (By.CSS_SELECTOR, 'body')
    _nav_locator = (By.CSS_SELECTOR, '.tutor-navbar')

    def __init__(self, driver, base_url=None, timeout=60, **url_kwargs) \
            -> None:
        """Override the initialization to hold onto the Tutor timeout.

        :param driver: a web browser control
        :param base_url: (optional) the website base URL; required to use
            the :py:function:`~pypom.Page.open` function
        :param int timeout: (optional) the maximum number of seconds to before
            the WebDriverWait polling times out, default is 1 minute
        :param url_kwargs: (optional) keyword arguments used when generating
            the :py:attr:`seed_url`
        :type base_url: str or None
        :type driver: :py:class:`~selenium.webdriver.Chrome` or
            :py:class:`~selenium.webdriver.Edge` or
            :py:class:`~selenium.webdriver.Firefox` or
            :py:class:`~selenium.webdriver.Safari`

        :return: None

        """
        super(TutorShared, self) \
            .__init__(driver, base_url, timeout, **url_kwargs)

    @property
    def loaded(self) -> bool:
        """Override the default loaded function.

        Wait up to :py:attr:`timeout` seconds for the root element to be found
        within the DOM.

        :return: ``True`` when the root element is found
        :rtype: bool

        """
        return bool(self.find_elements(*self._root_locator))

    def is_displayed(self) -> bool:
        """Return True when the Tutor page is displayed.

        :return: ``True`` if the root element is currently displayed, otherwise
            ``False``
        :rtype: bool

        """
        return self.find_element(*self._root_locator).is_displayed()

    @property
    def nav(self) -> TutorShared.Nav:
        """Access the page nav.

        :return: the OpenStax Tutor navigation bar
        :rtype: :py:class:`~pages.tutor.base.TutorShared.Nav`

        """
        nav = self.find_element(*self._nav_locator)
        return self.Nav(self, nav)

    def reload(self) -> TutorShared:
        """Reload the current page.

        Ignore stale element issues because we're reloading the page;
        everything is going to be stale if accessed too quickly
        (multi-process Firefox issue).

        :return: the current page
        :rtype: :py:class:`~pages.tutor.base.TutorShared`

        """
        try:
            self.driver.execute_script('location.reload();')
            self.wait_for_page_to_load()
        except StaleElementReferenceException:
            pass
        sleep(3.0)
        return self

    def back(self) -> TutorShared:
        """Go back to the previous page.

        Execute a one history step backwards request.

        :return: the current page
        :rtype: :py:class:`~pages.tutor.base.TutorShared`

        """
        self.driver.execute_script('window.history.go(-1)')
        return self

    def close_tab(self) -> TutorShared:
        """Close the current tab and switch to the remaining one.

        Assumes 2 browser tabs are open.

        :return: the page on the previous tab
        :rtype: :py:class:`~pages.tutor.base.TutorShared`

        """
        Utility.close_tab(self.driver)
        return self

    @property
    def location(self) -> str:
        """Return the current URL.

        :return: the current website URL
        :rtype: str

        """
        return self.driver.current_url

    @property
    def url(self) -> str:
        """Return the last segment of the current URL.

        :return: the final route segment of the current URL
        :rtype: str

        """
        return self.location.split('/')[-1]

    def resize_window(self, width=1024, height=768) -> None:
        """Set the browser window size.

        :param int width: (optional) browser window width, default to a 4:3
            ration
        :param int height: (optional) browser window height, default to a 4:3
            ration
        :return: None

        """
        self.driver.set_window_size(width, height)
        sleep(1.5)

    @property
    def is_safari(self) -> bool:
        """Return True if the browser in use is Safari.

        :return: ``True`` if the current browser is Safari, else ``False``
        :rtype: bool

        """
        return self.driver.capabilities.get('browserName').lower() == 'safari'


class TutorLoginBase(TutorShared):
    """The base page for the Tutor URI root.

    Used for `/` and `/terms`
    """

    _footer_locator = (By.CSS_SELECTOR, 'footer')

    @property
    def footer(self) -> TutorLoginBase.Footer:
        """Access the page footer.

        :return: the page footer element
        :rtype: :py:class:`~pages.tutor.base.TutorLoginBase.Footer`

        """
        footer = self.find_element(*self._footer_locator)
        return self.Footer(self, footer)

    class Nav(Region):
        """The log in base navigation."""

        _home_locator = (By.CSS_SELECTOR, '.navbar-brand')
        _help_link_locator = (By.CSS_SELECTOR, '[href*="force.com"]')
        _rice_link_locator = (By.CSS_SELECTOR, '.navbar-brand-rice')

        @property
        def logo(self) -> WebElement:
            r"""Return the Tutor Beta logo.

            :return: the OpenStax Tutor Beta logo element
            :rtype: \
                :py:class:`~selenium.webdriver.remote.webelement.WebElement`

            """
            return self.find_element(*self._home_locator)

        def go_home(self) -> TutorLoginBase:
            """Click on the logo.

            :return: the OpenStax Tutor Beta home page
            :rtype: :py:class:`TutorLoginBase`

            """
            Utility.click_option(self.driver, element=self.logo)
            return go_to_(TutorLoginBase(self.page.driver, self.page.base_url))

        def view_help_articles(self) -> Salesforce:
            """Click on the Help link to view Salesforce articles.

            :return: the OpenStax knowledge base webpage
            :rtype: :py:class:`~pages.salesforce.home.Salesforce`

            """
            link = self.find_element(*self._help_link_locator)
            url = link.get_attribute('href')
            Utility.switch_to(self.driver, element=link)
            return go_to_external_(Salesforce(self.driver), url)

        @property
        def rice_logo(self) -> WebElement:
            r"""Return the Rice University logo.

            :return: the Rice University logo
            :rtype: \
                :py:class:`~selenium.webdriver.remote.webelement.WebElement`

            """
            return self.find_element(*self._rice_link_locator)

        def go_to_rice(self) -> Rice:
            """Click on the Rice logo to view the Rice University home page.

            :return: the Rice University home page
            :rtype: :py:class:`~pages.rice.home.Rice`

            """
            logo = self.rice_logo
            url = logo.get_attribute('href')
            Utility.switch_to(self.driver, element=logo)
            return go_to_external_(Rice(self.driver), url)

    class Footer(Region):
        """The log in base footer."""

        _rice_link_locator = (By.CSS_SELECTOR, 'a:first-child')
        _terms_link_locator = (By.CSS_SELECTOR, '[href$=terms]')

        def go_to_rice(self) -> Rice:
            """Click the Rice University link.

            :return: the Rice University home page
            :rtype: :py:class:`~pages.rice.home.Rice`

            """
            link = self.find_element(*self._rice_link_locator)
            url = link.get_attribute('href')
            Utility.switch_to(self.driver, element=link)
            return go_to_external_(Rice(self.driver), url)

        def view_terms(self):
            """View the general Tutor terms of service and privacy policy.

            :return: the OpenStax Tutor Beta terms and policy page
            :rtype: :py:class:`~pages.tutor.legal.Terms`

            """
            link = self.find_element(*self._terms_link_locator)
            Utility.click_option(self.driver, element=link)
            from pages.tutor.legal import Terms
            return go_to_(Terms(self.driver, base_url=self.page.base_url))


class TutorBase(TutorShared):
    """The base page for the Tutor app."""

    class Nav(TutorNav):
        """Use the shared region Tutor navigation."""

        pass
