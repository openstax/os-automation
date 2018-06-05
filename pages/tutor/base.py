"""Basic page parent for all Accounts pages."""
import os
from time import sleep

from pypom import Page, Region
from selenium.webdriver.common.by import By

# from pages.accounts import home
from pages.rice.gdpr import GeneralDataPrivacyRegulation
from pages.rice.home import Rice
from pages.salesforce.home import Salesforce
from pages.utils.utilities import Utility
from pages.web.tutor_marketing import TutorMarketing


class TutorBase(Page):
    """Base class."""

    URL_TEMPLATE = 'https://tutor{0}.openstax.org'.format(
        (os.getenv('INSTANCE', '-qa')))

    _root_locator = (By.ID, 'home')

    def wait_for_page_to_load(self):
        """Override page load."""
        self.wait.until(
            lambda _: self.find_element(*self._root_locator).is_displayed())

    @property
    def header(self):
        """Return initial Tutor header."""
        return self.Header(self)

    @property
    def footer(self):
        """Return initial Tutor footer."""
        return self.Footer(self)

    def go_to_web_overview(self):
        """Go to the OpenStax web Tutor overview page."""
        return TutorMarketing(self.driver)

    def go_to_log_in(self):
        """Go to the Accounts log in page for Tutor."""
        # return home.AccountsHome(self)

    def log_in(self, username, password):
        """Log into Tutor."""
        return

    class Header(Region):
        """Tutor landing page header."""

        _root_locator = (By.CLASS_NAME, 'container')
        _logo_locator = (By.CLASS_NAME, 'navbar-brand')
        _help_link_locator = (By.LINK_TEXT, 'Help')
        _rice_link_locator = (By.CLASS_NAME, 'navbar-brand-rice')

        @property
        def is_header_displayed(self):
            """Header display boolean."""
            return self.loaded

        @property
        def go_to_tutor_home(self):
            """Follow the OpenStax icon link back to the site root."""
            self.find_element(*self._logo_locator).click()
            sleep(1)
            return self

        @property
        def go_to_help(self):
            """Click the Salesforce help link."""
            Utility.switch_to(self.driver, self._help_link_locator)
            return Salesforce(self.driver)

        def go_to_rice(self):
            """Load the Rice webpage."""
            self.find_element(*self._rice_link_locator).click()
            sleep(1)
            return Rice(self.driver)

    class Footer(Region):
        """Tutor landing page footer."""

        _root_locator = (By.TAG_NAME, 'footer')
        _rice_link_locator = (By.TAG_NAME, 'a')
        _terms_link_locator = (By.LINK_TEXT, 'Terms')
        _gdpr_link_locator = (By.LINK_TEXT, 'GDPR')

        @property
        def is_footer_displayed(self):
            """Footer display boolean."""
            return self.loaded

        def go_to_rice(self):
            """Load the Rice webpage."""
            self.find_element(*self._rice_link_locator).click()
            sleep(1)
            return Rice(self.driver)

        @property
        def show_terms_of_use(self):
            """Display the terms of use."""
            self.find_element(*self._terms_locator).click()
            sleep(1)
            return self

        def go_to_gdpr(self):
            """Go to the Rice GPDR compliance page."""
            return GeneralDataPrivacyRegulation(self.driver)
