"""Web nav region."""

from time import sleep

from pypom import Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class WebNav(Region):
    """Website navbar region."""

    _root_locator = (By.CLASS_NAME, 'nav')
    _openstax_logo_locator = (By.CSS_SELECTOR, '.os-logo > a')
    _subjects_dropdown_locator = (By.CLASS_NAME, 'subjects-dropdown')
    _technology_dropdown_locator = (By.CLASS_NAME, 'technology-dropdown')
    _what_we_do_dropdown_locator = (By.CLASS_NAME, 'what-we-do-dropdown')
    _user_menu_locator = (By.CLASS_NAME, 'login')

    @property
    def is_displayed(self):
        """Return True if the site navigation bar is visible."""
        return self.find_element(*self._openstax_logo_locator).is_displayed

    def go_home(self):
        """Return to the home page by clicking on the OpenStax logo."""
        self.find_element(*self._openstax_logo_locator).click()
        sleep(1.0)
        from pages.web.home import WebHome
        return WebHome(self.driver)

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
        return self.Login(self)

    class Subjects(Region):
        """The Subject navigation menu dropdown."""

        _open_menu_locator = (By.CSS_SELECTOR, '[href="."]')
        _menu_expand_locator = (By.CSS_SELECTOR, 'nav.dropdown-menu')
        _all_option_locator = (By.CSS_SELECTOR, '[href$=view-all]')
        _math_option_locator = (By.CSS_SELECTOR, '[href$=math]')
        _science_option_locator = (By.CSS_SELECTOR, '[href$=science]')
        _social_sciences_option_locator = (By.CSS_SELECTOR,
                                           '[href$=social-sciences]')
        _humanities_option_locator = (By.CSS_SELECTOR, '[href$=humanities]')
        _ap_option_locator = (By.CSS_SELECTOR, '[href$=AP]')

        @property
        def open(self):
            """Select the Subjects menu."""
            menu = self.find_element(*self._open_menu_locator)
            menu_state = self.find_element(*self._menu_expand_locator)
            print(menu_state.get_attribute('aria-expanded'))
            if menu_state.get_attribute('aria-expanded') != 'true':
                menu.click()
            sleep(0.5)
            return self

        @property
        def all(self):
            """Return the all subjects link."""
            return self.find_element(*self._all_option_locator)

        def view_all(self):
            """View all book subjects."""
            return self.open._selection_helper(
                self._all_option_locator)

        @property
        def math(self):
            """Return the math subjects link."""
            return self.find_element(*self._math_option_locator)

        def view_math(self):
            """View all math books."""
            return self.open._selection_helper(
                self._math_option_locator)

        @property
        def science(self):
            """Return the science subjects link."""
            return self.find_element(*self._science_option_locator)

        def view_science(self):
            """View all science books."""
            return self.open._selection_helper(
                self._science_option_locator)

        @property
        def social_science(self):
            """Return the social science subjects link."""
            return self.find_element(*self._social_science_option_locator)

        def view_social_science(self):
            """View all social science books."""
            return self.open._selection_helper(
                self._social_sciences_option_locator)

        @property
        def ap(self):
            """Return the AP subjects link."""
            return self.find_element(*self._ap_option_locator)

        def view_ap(self):
            """View all AP books."""
            return self.open._selection_helper(
                self._ap_option_locator)

        def _selection_helper(self, locator):
            """Select the corresponding option."""
            self.open.find_element(*locator).click()
            sleep(1.0)
            from pages.web.subjects import Subjects
            return Subjects(self.driver)

    class Technology(Region):
        """The Technology navigation menu dropdown."""

        _open_menu_locator = (By.CSS_SELECTOR, '[href="."]')
        _technology_option_locator = (By.CSS_SELECTOR, '[href$=technology]')
        _tutor_option_locator = (By.CSS_SELECTOR, '[href$=openstax-tutor]')
        _partners_option_locator = (By.CSS_SELECTOR, '[href$=partners]')

        @property
        def open(self):
            """Select the Technology menu."""
            self.find_element(*self._open_menu_locator).click()
            sleep(0.5)
            return self

        @property
        def technology(self):
            """Return the technology link."""
            return self.find_element(*self._technology_option_locator)

        def view_technology(self):
            """View the technology page."""
            self.open.technology.click()
            sleep(1.0)
            from pages.web.technology import Technology
            return Technology(self.driver)

        @property
        def tutor(self):
            """Return the OpenStax Tutor link."""
            return self.find_element(*self._tutor_option_locator)

        def view_tutor(self):
            """View the OpenStax Tutor beta marketing page."""
            self.open.tutor.click()
            sleep(1.0)
            from pages.web.tutor_marketing import TutorMarketing
            return TutorMarketing(self.driver)

        @property
        def partners(self):
            """Return the OpenStax partners link."""
            return self.find_element(*self._partners_option_locator)

        def view_partners(self):
            """View the OpenStax partners page."""
            self.open.partners.click()
            sleep(1.0)
            from pages.web.partners import Partners
            return Partners(self.driver)

    class WhatWeDo(Region):
        """The What we do navigation menu dropdown."""

        _open_menu_locator = (By.CSS_SELECTOR, '[href="."]')
        _about_us_option_locator = (By.CSS_SELECTOR, '[href$=about]')
        _team_option_locator = (By.CSS_SELECTOR, '[href$=team]')
        _research_option_locator = (By.CSS_SELECTOR, '[href$=research]')

        @property
        def open(self):
            """Select the What we do menu."""
            self.find_element(*self._open_menu_locator).click()
            sleep(0.5)
            return self

        @property
        def about_us(self):
            """Return the About Us link."""
            return self.find_element(*self._about_us_option_locator)

        def view_about_us(self):
            """View the About Us page."""
            self.open.about_us.click()
            sleep(1.0)
            from pages.web.about_us import AboutUs
            return AboutUs(self.driver)

        @property
        def team(self):
            """Return the OpenStax team link."""
            return self.find_element(*self._team_option_locator)

        def view_team(self):
            """View the OpenStax team page."""
            self.open.team.click()
            sleep(1.0)
            from pages.web.team import Team
            return Team(self.driver)

        @property
        def research(self):
            """Return the research team link."""
            return self.find_element(*self._research_option_locator)

        def view_research(self):
            """View the OpenStax researcher page."""
            self.open.research.click()
            sleep(1.0)
            from pages.web.research import Research
            return Research(self.driver)

    class Login(Region):
        """The login option and menu."""

        _log_in_link_locator = (By.LINK_TEXT, 'Login')
        _logged_in_locator = (By.CLASS_NAME, 'login-dropdown')
        _open_menu_locator = (By.CSS_SELECTOR, '[href="."]')
        _user_name_locator = (By.PARTIAL_LINK_TEXT, 'Hi ')
        _profile_link_locator = (By.CSS_SELECTOR, '[href$=profile]')
        _openstax_tutor_link_locator = (By.LINK_TEXT, 'OpenStax Tutor')
        _log_out_link_locator = (By.CSS_SELECTOR, '[href*=logout]')

        @property
        def login(self):
            """Return the log in link."""
            return self.find_element(*self._log_in_link_locator)

        def log_in(self, user, password):
            """Log a user into the website."""
            accounts = self.login.click()
            sleep(1.0)
            accounts.log_in(user, password)
            from pages.web.home import WebHome
            return WebHome(accounts.driver)

        @property
        def logged_in(self):
            """Return True if a user is logged into Web."""
            try:
                self.find_element(*self._logged_in_locator)
            except NoSuchElementException:
                return False
            return True

        @property
        def open(self):
            """Select the user menu."""
            self.find_element(*self._open_menu_locator).click()
            sleep(0.5)
            return self

        @property
        def name(self):
            """Return the user's first name as shown in the menu bar."""
            return self.find_element(*self._user_name_locator).text[3:].strip()

        @property
        def profile(self):
            """Return the user profile link."""
            return self.find_element(*self._profile_link_locator)

        def view_profile(self):
            """View the user's account profile on Accounts."""
            self.open.profile.click()
            sleep(1.0)
            from pages.accounts.profile import Profile
            return Profile(self.driver)

        @property
        def tutor(self):
            """Return the OpenStax Tutor Beta link."""
            return self.find_element(*self._tutor_option_locator)

        def view_tutor(self):
            """View OpenStax Tutor Beta for the current user."""
            self.open.tutor.click()
            sleep(1.0)
            from pages.tutor.dashboard import Dashboard
            return Dashboard(self.driver)

        @property
        def logout(self):
            """Return the log out link."""
            return self.find_element(*self._log_out_link_locator)

        def log_out(self):
            """Log the current user out."""
            self.open.logout.click()
            sleep(1.0)
            from pages.web.home import WebHome
            return WebHome(self.driver)
