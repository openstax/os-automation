"""Openstax Web's shared company navigation."""

from time import sleep

from pypom import Region
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from utils.utilities import Utility, go_to_, go_to_external_


class OpenStaxNav(Region):
    """OpenStax's website shared navigational control."""

    _root_locator = (By.CSS_SELECTOR, 'nav.meta-nav')
    _bookstore_suppliers_locator = (By.CSS_SELECTOR, '[href$=suppliers]')
    _our_impact_locator = (By.CSS_SELECTOR, '[href$=impact]')
    _supporters_locator = (By.CSS_SELECTOR, '[href$=foundation]')
    _blog_locator = (By.CSS_SELECTOR, '[href$=blog]')
    _give_locator = (By.CSS_SELECTOR, '[href$=give]')
    _help_locator = (By.CSS_SELECTOR, '[href$=help]')
    _rice_locator = (By.CLASS_NAME, 'rice-logo')

    def is_displayed(self):
        """Return True if the nav bar is displayed."""
        return self.root.is_displayed()

    def view_bookstores(self):
        """Go to the bookstore suppliers page."""
        self._click(self._bookstore_suppliers_locator)
        sleep(1.0)
        from pages.web.bookstore_suppliers import Bookstore
        return go_to_(Bookstore(self.driver, base_url=self.page.base_url))

    def view_our_impact(self):
        """Go to the impact or annual report page."""
        self._click(self._our_impact_locator)
        sleep(1.0)
        if 'impact' in self._our_impact_locator[1]:
            from pages.web.impact import Impact as Destination
        else:
            from pages.web.annual import AnnualReport as Destination
        return go_to_(Destination(self.driver, base_url=self.page.base_url))

    def view_supporters(self):
        """Go to the supporters page."""
        self._click(self._supporters_locator)
        sleep(1.0)
        from pages.web.supporters import Supporters
        return go_to_(Supporters(self.driver, base_url=self.page.base_url))

    def view_the_blog(self):
        """Go to the blog."""
        self._click(self._blog_locator)
        sleep(1.0)
        from pages.web.blog import Blog
        return go_to_(Blog(self.driver, base_url=self.page.base_url))

    def view_donation_options(self):
        """Go to the donation page."""
        link = self.find_element(*self._give_locator)
        url = link.get_attribute('href')
        Utility.switch_to(self.driver, element=link)
        from pages.rice.riceconnect import RiceConnect
        return go_to_(RiceConnect(self.driver, url))

    def view_help_articles(self):
        """Go to the Salesforce help site."""
        link = self.find_element(*self._help_locator)
        url = link.get_attribute('href')
        Utility.switch_to(self.driver, element=link)
        from pages.salesforce.home import Salesforce
        return go_to_external_(Salesforce(self.driver), url)

    def go_to_rice(self):
        """Go to the Rice University home page."""
        # if the screen is set for mobile use, wait for the logo animation
        if self.driver.get_window_size().get('width') <= 960:
            sleep(0.5)
        Utility.switch_to(self.driver, self._rice_locator)
        from pages.rice.home import Rice
        return go_to_(Rice(self.driver))

    def _click(self, locator):
        """Click on the navigation link."""
        for _ in range(30):
            try:
                link = self.find_element(*locator)
                Utility.click_option(self.driver, element=link)
                break
            except WebDriverException:
                sleep(1.0)
