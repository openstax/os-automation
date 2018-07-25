"""Basic page parent for the tutor admin page."""

from time import sleep

from pypom import Page, Region
from selenium.webdriver.common.by import By

from pages.utils.utilities import Utility


class TutorAdminBase(Page):
	"""Base class."""

	_root_locator = (By.CSS_SELECTOR,'#ox-react-root-container')

	def wait_for_page_to_load(self):
        """Override page load."""
        self.wait.until(
            lambda _: self.find_element(*self._root_locator).is_displayed())

    @property
    def header(self):
        """Return initial Tutor header."""
        return self.Header(self)

    class Header(Region):
    	"""Header for tutor admin."""

    	_logo_locator = (By.CLASS_NAME, 'ui-brand-logo')
    	_help_link_locator = (By.LINK_TEXT, 'Help')

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