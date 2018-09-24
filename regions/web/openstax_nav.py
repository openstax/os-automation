"""Openstax Web's shared company navigation."""

from time import sleep

from pypom import Region
from selenium.webdriver.common.by import By


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
        self.find_element(*self._our_impact_locator).click()
        sleep(1.0)
        from pages.web.impact import OurImpact
        return OurImpact(self.driver)

    def view_supporters(self):
        """Go to the supporters page."""
        self.find_element(*self._supporters_locator).click()
        sleep(1.0)
        from pages.web.supporters import Supporters
        return Supporters(self.driver)

    def view_the_blog(self):
        """Go to the blog."""
        self.find_element(*self._blog_locator).click()
        sleep(1.0)
        from pages.web.blog import Blog
        return Blog(self.driver)

    def view_donation_options(self):
        """Go to the donation page."""
        self.find_element(*self._give_locator).click()
        sleep(1.0)
        from pages.web.give import Donate
        return Donate(self.driver)

    def view_help_articles(self):
        """Go to the Salesforce help site."""
        self.find_element(*self._help_locator).click()
        sleep(1.0)
        from pages.salesforce.home import Salesforce
        return Salesforce(self.driver)

    def go_to_rice(self):
        """Go to the Rice University home page."""
        self.find_element(*self._rice_locator).click()
        sleep(1.0)
        from pages.rice.home import Rice
        return Rice(self.driver)
