"""The Our Impact webpage."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility, go_to_


class OurImpact(WebBase):
    """The Our Impact page."""

    URL_TEMPLATE = '/impact'

    _banner_locator = (By.CSS_SELECTOR, '.header')
    _description_locator = (By.CSS_SELECTOR, '.blurb')
    _student_locator = (By.CSS_SELECTOR, '.student')
    _ip_heading_locator = (By.CSS_SELECTOR, '.affiliates h2')
    _ip_description_locator = (By.CSS_SELECTOR, 'html-block p:first-child')
    _contact_us_locator = (By.CSS_SELECTOR, '.cta .btn')
    _partners_locator = (By.CSS_SELECTOR, '.partners img')
    _adopters_locator = (By.CSS_SELECTOR, '.adopters a')

    @property
    def loaded(self):
        """Return True when the background image and partner images load."""
        return (
            Utility.load_background_images(self.driver,
                                           self._student_locator) and
            Utility.is_image_visible(self.driver,
                                     locator=self._partners_locator) and
            len(self.find_element(*self._description_locator)).text > 0)

    def is_displayed(self):
        """Return True if the heading statement is displayed."""
        return self.banner.is_displayed()

    @property
    def banner(self):
        """Return the banner element."""
        return self.find_element(*self._banner_locator)

    @property
    def title(self):
        """Return the banner text."""
        return self.banner.text

    @property
    def subheading(self):
        """Return the page description element."""
        return self.find_element(*self._description_locator)

    @property
    def description(self):
        """Return the banner subtext."""
        return self.subheading.text

    def view_partners(self):
        """Scroll to the partner logos."""
        Utility.scroll_to(self.driver, element=self.partners[0].logo)
        return self

    @property
    def partners_heading(self):
        """Return the Institutional Partners heading."""
        return self.find_element(*self._ip_heading_locator).text

    @property
    def institutional_partnership(self):
        """Return the IP/AS description."""
        return self.find_element(*self._ip_description_locator).text

    def contact_us(self):
        """Click the 'Contact us to learn more' button."""
        Utility.safari_exception_click(self.driver,
                                       locator=self._contact_us_locator)
        from pages.web.contact import Contact
        return go_to_(Contact(self.driver, base_url=self.base_url))

    @property
    def partners(self):
        """Access the list of current institutional partners."""
        return [self.Partner(self, partner)
                for partner in self.find_elements(*self._partners_locator)]

    def view_adopters(self):
        """Click the 'See a full list of institutions...' link."""
        Utility.safari_exception_click(self.driver,
                                       locator=self._adopters_locator)
        from pages.web.adopters import Adopters
        return go_to_(Adopters(self.driver, base_url=self.base_url))

    class Partner(Region):
        """An Institutional Partner or Affiliate School."""

        @property
        def name(self):
            """Return the institution's name."""
            return self.root.get_attribute('alt')

        @property
        def logo(self):
            """Return the image."""
            return self.root
