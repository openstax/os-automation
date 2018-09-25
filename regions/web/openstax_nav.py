"""Openstax Web's shared company navigation."""

from time import sleep

from pypom import Region
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from utils.utilities import go_to_


class OpenStaxNav(Region):
    """OpenStax's website shared navigational control."""

    _root_locator = (By.CLASS_NAME, 'meta-nav')
    _our_impact_locator = (By.CSS_SELECTOR, '[href$=impact]')
    _supporters_locator = (By.CSS_SELECTOR, '[href$=foundation]')
    _blog_locator = (By.CSS_SELECTOR, '[href$=blog]')
    _give_locator = (By.CSS_SELECTOR, '[href$=give]')
    _help_locator = (By.CSS_SELECTOR, '[href$=help]')
    _rice_locator = (By.CLASS_NAME, '.rice-logo')

    def is_displayed(self):
        """Return True if the nav bar is displayed."""
        return self.root.is_displayed()

    def view_our_impact(self):
        """Go to the impact page."""
        self._click(self._our_impact_locator)
        sleep(1.0)
        from pages.web.impact import OurImpact
        return go_to_(OurImpact(self.driver))

    def view_supporters(self):
        """Go to the supporters page."""
        self._click(self._supporters_locator)
        sleep(1.0)
        from pages.web.supporters import Supporters
        return go_to_(Supporters(self.driver))

    def view_the_blog(self):
        """Go to the blog."""
        self._click(self._blog_locator)
        sleep(1.0)
        from pages.web.blog import Blog
        return go_to_(Blog(self.driver))

    def view_donation_options(self):
        """Go to the donation page."""
        self._click(self._give_locator)
        sleep(1.0)
        from pages.web.donation import Give
        return go_to_(Give(self.driver))

    def view_help_articles(self):
        """Go to the Salesforce help site."""
        self._click(self._help_locator)
        sleep(1.0)
        from pages.salesforce.home import Salesforce
        return go_to_(Salesforce(self.driver))

    def go_to_rice(self):
        """Go to the Rice University home page."""
        self._click(self._rice_locator)
        sleep(1.0)
        from pages.rice.home import Rice
        return go_to_(Rice(self.driver))

    def _click(self, locator):
        """Click on the navigation link."""
        for _ in range(30):
            try:
                self.find_element(*locator).click()
                break
            except WebDriverException:
                sleep(1.0)
