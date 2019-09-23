"""Web nav region."""

from time import sleep

from pypom import Region
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from utils.utilities import Actions, Utility, go_to_
from utils.web import Web


class WebNavMenu(Region):
    """Shared nav menu functionality."""

    _menu_item_selector = r'[href=\".\"]'

    @property
    def loaded(self):
        """Return True if the subjects menu exist.

        :return: ``True`` if the subjects dropdown menu is found, else
            ``False``
        :rtype: bool

        """
        script = ('return document.querySelectorAll("{0}");'
                  .format(self._menu_item_selector))
        menus = ' '.join(list(
            menu.get_attribute('textContent')
            for menu
            in self.driver.execute_script(script)))
        return 'Subjects' in menus

    def is_displayed(self):
        """Return True if the region is displayed."""
        return self.root.is_displayed()

    def _is_available(self, label, menu, options):
        """Return True if the menu option is available."""
        locator = ('li.{menu}-dropdown {topic}'
                   .format(menu=menu, topic=options.get(label)))
        return Utility.has_height(self.driver, locator)

    def _hover(self, locator):
        """Return the CSS style of a hovered element."""
        menu = self.root
        option = locator[1]
        action = (
            Actions(self.driver)
            .move_to_element(menu)
            .pause(1)
            .get_js_data(option, 'height', 'auto')
        )
        # if the result is 'auto', the menu option isn't displayed
        return not action

    def open(self):
        """Select the menu."""
        sleep(0.5)
        try:
            is_expanded = self.find_element(*self._menu_expand_locator) \
                .get_attribute('aria-expanded') == 'true'
        except WebDriverException as ex:
            print('WebNav > open -- ', self.driver.current_url, str(ex))
            is_expanded = False
        if not is_expanded:
            target = (
                self._open_menu_locator[0],
                '.{parent} {menu_locator}'.format(
                    parent='.'.join(self.root.get_attribute('class').split()),
                    menu_locator=self._open_menu_locator[1]))
            Utility.click_option(driver=self.driver,
                                 locator=target,
                                 force_js_click=True)
        sleep(0.25)
        return self

    def _selection_helper(self, locator, destination, new_tab=False):
        """Select the corresponding option."""
        self.open()
        sleep(0.5)
        if new_tab:
            Utility.switch_to(driver=self.driver,
                              link_locator=locator,
                              force_js_click=True)
        else:
            Utility.click_option(driver=self.driver,
                                 locator=locator,
                                 force_js_click=True)
        sleep(1.0)
        return go_to_(destination(self.driver))


class WebNav(Region):
    """Website navbar region."""

    _root_locator = (By.CSS_SELECTOR, '.nav')
    _openstax_logo_locator = (By.CSS_SELECTOR, '.logo > a , a.logo')
    _slogan_locator = (By.CSS_SELECTOR, '.logo-quote')
    _subjects_dropdown_locator = (By.CSS_SELECTOR, '.subjects-dropdown')
    _technology_dropdown_locator = (By.CSS_SELECTOR, '.technology-dropdown')
    _what_we_do_dropdown_locator = (By.CSS_SELECTOR, '.what-we-do-dropdown')
    _user_menu_locator = (By.CSS_SELECTOR, '.login , .login-dropdown')
    _back_link_locator = (By.CSS_SELECTOR, 'a.close')
    _meta_menu_locator = (By.CSS_SELECTOR, '.expand')

    def is_displayed(self):
        """Return True if the nav bar is displayed."""
        if not self.root.is_displayed():
            return False
        current_width = self.driver.get_window_size().get('width')
        return (
            (current_width > 960) or
            (current_width <= 960 and self.meta.is_open)
        )

    def is_hidden(self):
        """Return True if the nav bar is not visible due to the mobile menu."""
        if (not self.meta.is_open and
                self.driver.get_window_size().get('width') <= 960):
            return True
        return False

    def go_home(self):
        """Return to the home page by clicking on the OpenStax logo."""
        logo = self.find_element(*self._openstax_logo_locator)
        Utility.safari_exception_click(self.driver, element=logo)
        from pages.web.home import WebHome
        return go_to_(WebHome(self.driver, self.page.base_url))

    @property
    def slogan(self):
        """Access the slogan."""
        return self.find_element(*self._slogan_locator).text

    def slogan_visible(self):
        """Return True if the text is displayed."""
        element_height = (
            'return window.getComputedStyle(document.querySelector'
            '("{selector}"))["height"]'
        ).format(selector=self._slogan_locator[1])
        return self.driver.execute_script(element_height) != '0px'

    @property
    def subjects(self):
        """Access the Subject dropdown menu."""
        region_root = self.find_element(*self._subjects_dropdown_locator)
        return self.Subjects(self, region_root)

    @property
    def technology(self):
        """Access the Technology dropdown menu."""
        region_root = self.find_element(*self._technology_dropdown_locator)
        return self.Technology(self, region_root)

    @property
    def openstax(self):
        """Access the What we do dropdown menu."""
        region_root = self.find_element(*self._what_we_do_dropdown_locator)
        return self.WhatWeDo(self, region_root)

    @property
    def login(self):
        """Access the Login option or menu."""
        region_root = self.find_element(*self._user_menu_locator)
        return self.Login(self, region_root)

    def back(self):
        """Click on the back link within the mobile menu.

        Use a document query because the back button and menu name are
        outside the scope of the Web Nav region but are only used in
        the nav.
        """
        sleep(0.5)
        self.driver.execute_script(
            'document.querySelector("%s").click()' %
            self._back_link_locator[1])
        sleep(1.0)
        return self

    @property
    def meta(self):
        """Access the meta menu for condensed views."""
        region_root = self.find_element(*self._meta_menu_locator)
        return self.Meta(self, region_root)

    class Meta(Region):
        """The meta menu control for non-full screen viewers."""

        def is_displayed(self):
            """Return True if the region is displayed."""
            return self.root.is_displayed()

        @property
        def is_open(self):
            """Return True if the meta menu for mobile displays is open."""
            status = self.driver.execute_script(
                'return document.querySelector("body.no-scroll");')
            return bool(status)

        def toggle_menu(self):
            """Click the menu to open or close it.

            If the page overlay is still in place, wait and retry.
            """
            Utility.wait_for_overlay_then(self.root.click)
            return self

    class Subjects(WebNavMenu):
        """The Subject navigation menu dropdown."""

        _open_menu_locator = (By.CSS_SELECTOR, '[href="."]')
        _menu_expand_locator = (By.CSS_SELECTOR, 'nav.dropdown-menu')
        _all_option_locator = (By.CSS_SELECTOR, '[href$=view-all]')
        _math_option_locator = (By.CSS_SELECTOR, '[href$=math]')
        _science_option_locator = (By.CSS_SELECTOR, '[href$=science]')
        _social_sciences_option_locator = (By.CSS_SELECTOR,
                                           '[href$=social-sciences]')
        _humanities_option_locator = (By.CSS_SELECTOR, '[href$=humanities]')
        _business_option_locator = (By.CSS_SELECTOR, '[href$=business]')
        _ap_option_locator = (By.CSS_SELECTOR, '[href$=ap]')

        def is_available(self, label):
            """Return True if the menu option is available."""
            sleep(0.5)
            subjects = {
                Web.VIEW_ALL: self._all_option_locator[1],
                Web.VIEW_MATH: self._math_option_locator[1],
                Web.VIEW_SCIENCE: self._science_option_locator[1],
                Web.VIEW_SOCIAL_SCIENCES: (
                    self._social_sciences_option_locator[1]),
                Web.VIEW_HUMANITIES: self._humanities_option_locator[1],
                Web.VIEW_BUSINESS: self._business_option_locator[1],
                Web.VIEW_AP: self._ap_option_locator[1],
            }
            return self._is_available(label, 'subjects', subjects)

        def hover(self):
            """Return the CSS style of a hovered element."""
            return self._hover(self._all_option_locator)

        @property
        def all(self):
            """Return the all subjects link."""
            return self.find_element(*self._all_option_locator)

        def view_all(self):
            """View all book subjects."""
            from pages.web.subjects import Subjects
            return self.open()._selection_helper(
                self._all_option_locator,
                Subjects)

        @property
        def math(self):
            """Return the math subjects link."""
            return self.find_element(*self._math_option_locator)

        def view_math(self):
            """View all math books."""
            from pages.web.subjects import Subjects
            return self.open()._selection_helper(
                self._math_option_locator,
                Subjects)

        @property
        def science(self):
            """Return the science subjects link."""
            return self.find_element(*self._science_option_locator)

        def view_science(self):
            """View all science books."""
            from pages.web.subjects import Subjects
            return self.open()._selection_helper(
                self._science_option_locator,
                Subjects)

        @property
        def social_sciences(self):
            """Return the social science subjects link."""
            return self.find_element(*self._social_sciences_option_locator)

        def view_social_sciences(self):
            """View all social science books."""
            from pages.web.subjects import Subjects
            return self.open()._selection_helper(
                self._social_sciences_option_locator,
                Subjects)

        @property
        def humanities(self):
            """Return the humanities subjects link."""
            return self.find_element(*self._humanities_option_locator)

        def view_humanities(self):
            """View all humanities books."""
            from pages.web.subjects import Subjects
            return self.open()._selection_helper(
                self._humanities_option_locator,
                Subjects)

        @property
        def business(self):
            """Return the business subjects link."""
            return self.find_element(*self._business_option_locator)

        def view_business(self):
            """View all business books."""
            from pages.web.subjects import Subjects
            return self.open()._selection_helper(
                self._business_option_locator,
                Subjects)

        @property
        def ap(self):
            """Return the AP subjects link."""
            return self.find_element(*self._ap_option_locator)

        def view_ap(self):
            """View all AP books."""
            from pages.web.subjects import Subjects
            return self.open()._selection_helper(
                self._ap_option_locator,
                Subjects)

    class Technology(WebNavMenu):
        """The Technology navigation menu dropdown."""

        _open_menu_locator = (By.CSS_SELECTOR, '[href="."]')
        _menu_expand_locator = (By.CSS_SELECTOR, 'nav.dropdown-menu')
        _technology_option_locator = (By.CSS_SELECTOR, '[href$=technology]')
        _tutor_option_locator = (By.CSS_SELECTOR, '[href$=openstax-tutor]')
        _partners_option_locator = (By.CSS_SELECTOR, '[href$=partners]')

        def hover(self):
            """Return the CSS style of a hovered element."""
            return self._hover(self._technology_option_locator)

        def is_available(self, label):
            """Return True if the menu option is available."""
            topics = {
                Web.VIEW_TECHNOLOGY: self._technology_option_locator[1],
                Web.VIEW_TUTOR: self._tutor_option_locator[1],
                Web.VIEW_PARTNERS: self._partners_option_locator[1],
            }
            return self._is_available(label, 'technology', topics)

        @property
        def technology(self):
            """Return the technology link."""
            return self.find_element(*self._technology_option_locator)

        def view_technology(self):
            """View the technology page."""
            from pages.web.technology import Technology
            return self.open()._selection_helper(
                self._technology_option_locator,
                Technology)

        @property
        def tutor(self):
            """Return the OpenStax Tutor link."""
            return self.find_element(*self._tutor_option_locator)

        def view_tutor(self):
            """View the OpenStax Tutor beta marketing page."""
            from pages.web.tutor import TutorMarketing
            return self.open()._selection_helper(
                self._tutor_option_locator,
                TutorMarketing)

        @property
        def partners(self):
            """Return the OpenStax partners link."""
            return self.find_element(*self._partners_option_locator)

        def view_partners(self):
            """View the OpenStax partners page."""
            from pages.web.partners import Partners
            return self.open()._selection_helper(
                self._partners_option_locator,
                Partners)

    class WhatWeDo(WebNavMenu):
        """The What we do navigation menu dropdown."""

        _open_menu_locator = (By.CSS_SELECTOR, '[href="."]')
        _menu_expand_locator = (By.CSS_SELECTOR, 'nav.dropdown-menu')
        _about_us_option_locator = (By.CSS_SELECTOR, '[href$=about]')
        _team_option_locator = (By.CSS_SELECTOR, '[href$=team]')
        _research_option_locator = (By.CSS_SELECTOR, '[href$=research]')

        def hover(self):
            """Return the CSS style of a hovered element."""
            return self._hover(self._about_us_option_locator)

        def is_available(self, label):
            """Return True if the menu option is available."""
            groups = {
                Web.VIEW_ABOUT_US: self._about_us_option_locator[1],
                Web.VIEW_TEAM: self._team_option_locator[1],
                Web.VIEW_RESEARCH: self._research_option_locator[1],
            }
            return self._is_available(label, 'what-we-do', groups)

        @property
        def about_us(self):
            """Return the About Us link."""
            return self.find_element(*self._about_us_option_locator)

        def view_about_us(self):
            """View the About Us page."""
            from pages.web.about import AboutUs
            return self.open()._selection_helper(
                self._about_us_option_locator,
                AboutUs)

        @property
        def team(self):
            """Return the OpenStax team link."""
            return self.find_element(*self._team_option_locator)

        def view_team(self):
            """View the OpenStax team page."""
            from pages.web.team import Team
            return self.open()._selection_helper(
                self._team_option_locator,
                Team)

        @property
        def research(self):
            """Return the research team link."""
            return self.find_element(*self._research_option_locator)

        def view_research(self):
            """View the OpenStax researcher page."""
            from pages.web.research import Research
            return self.open()._selection_helper(
                self._research_option_locator,
                Research)

    class Login(WebNavMenu):
        """The login option and menu."""

        _menu_expand_locator = (By.CSS_SELECTOR, 'nav.dropdown-menu')
        _log_in_link_locator = (By.CSS_SELECTOR, '.pardotTrackClick')
        _logged_in_locator = (By.CSS_SELECTOR, '.login-dropdown')
        _open_menu_locator = (By.CSS_SELECTOR, '[href="."]')
        _profile_link_locator = (By.CSS_SELECTOR, '[href$=profile]')
        _openstax_tutor_link_locator = (
            By.CSS_SELECTOR, f'{_logged_in_locator[1]} [href*=tutor]')
        _faculty_access_locator = (By.CSS_SELECTOR, '[href*=faculty]')
        _log_out_link_locator = (By.CSS_SELECTOR, '[href*=logout]')

        @property
        def login(self):
            """Return the log in link."""
            return self.find_element(*self._log_in_link_locator)

        def go_to_log_in(self):
            """Click on the login menu link."""
            return self.log_in(do_not_log_in=True)

        def is_displayed(self):
            """Return True if the log in link or user's name is displayed."""
            return self.login.is_displayed()

        def log_in(self, user=None, password=None,
                   do_not_log_in=False, destination=None, url=None):
            """Log a user into the website."""
            Utility.wait_for_overlay_then(self.login.click)
            from pages.accounts.home import AccountsHome
            if do_not_log_in:
                return go_to_(AccountsHome(self.driver, url))
            else:
                AccountsHome(self.driver).service_log_in(user, password)
            if destination:
                return go_to_(destination(self.driver, url))
            from pages.web.home import WebHome as Home
            return go_to_(Home(self.driver, url))

        @property
        def logged_in(self):
            """Return True if a user is logged into Web."""
            return 'dropdown' in self.root.get_attribute('class')

        @property
        def name(self):
            """Return the user's first name as shown in the menu bar."""
            if self.logged_in:
                return (' '.join(
                        self.find_element(*self._open_menu_locator)
                        .get_attribute('innerHTML')
                        .split('<')[0]
                        .split()[1:]))
            return self.find_element(*self._log_in_link_locator).text

        @property
        def profile(self):
            """Return the user profile link."""
            return self.find_element(*self._profile_link_locator)

        def view_profile(self):
            """View the user's account profile on Accounts."""
            from pages.accounts.profile import Profile
            return self.open()._selection_helper(
                self._profile_link_locator,
                Profile,
                new_tab=True)

        @property
        def tutor(self):
            """Return the OpenStax Tutor Beta link."""
            return self.find_element(*self._openstax_tutor_link_locator)

        def view_tutor(self):
            """View OpenStax Tutor Beta for the current user."""
            from pages.tutor.home import TutorHome
            tutor = self.open()._selection_helper(
                self._openstax_tutor_link_locator,
                TutorHome,
                new_tab=True)
            return tutor.service_pass_through()

        @property
        def instructor_access(self):
            """Return the link to apply for faculty access."""
            return self.find_element(*self._faculty_access_locator)

        def request_access(self):
            """Click the faculty access link to start the application."""
            from pages.accounts.signup import Signup
            return self.open()._selection_helper(
                self._faculty_access_locator,
                Signup,
                new_tab=True)

        @property
        def logout(self):
            """Return the log out link."""
            return self.find_element(*self._log_out_link_locator)

        def log_out(self):
            """Log the current user out."""
            from pages.web.home import WebHome as Home
            return self.open()._selection_helper(
                self._log_out_link_locator,
                Home)
