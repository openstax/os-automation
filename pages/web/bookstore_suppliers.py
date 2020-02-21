"""The textbook suppliers page."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility, go_to_


class Bookstore(WebBase):
    """The campus bookstore supplier page."""

    URL_TEMPLATE = '/bookstore-suppliers'

    _banner_heading_locator = (By.CSS_SELECTOR, '.hero h1')
    _subheading_locator = (By.CSS_SELECTOR, '[data-html=subhead]')
    _subjects_full_locator = (By.CSS_SELECTOR, '.larger-screen a')
    _subjects_phone_locator = (By.CSS_SELECTOR, '.smaller-screen a')
    _background_image_locator = (By.CSS_SELECTOR, '.images img')
    _isbn_pdf_locator = (By.CSS_SELECTOR, '.main-content .button-row a')
    _fulfillment_locator = (By.CSS_SELECTOR, '.featured .card')
    _publisher_locator = (By.CSS_SELECTOR, '.cards:not(.featured) .card')

    @property
    def loaded(self):
        """Return True when the backgrounds and text are loaded."""
        return (super().loaded and
                'order print copies' in self.driver.page_source and
                Utility.is_image_visible(
                    self.driver, locator=self._background_image_locator))

    def is_displayed(self):
        """Return True if the suppliers heading is displayed."""
        return self.banner.is_displayed()

    @property
    def banner(self):
        """Return the page heading element."""
        return self.find_element(*self._banner_heading_locator)

    @property
    def title(self):
        """Return the page title."""
        return self.banner.text.strip()

    @property
    def subheading(self):
        """Return the subhead text."""
        return self.find_element(*self._subheading_locator).text.strip()

    @property
    def subjects(self):
        """Return the screen-limited subjects link."""
        locator = (self._subjects_phone_locator
                   if self.is_phone
                   else self._subjects_full_locator)
        return self.find_element(*locator)

    def view_subjects(self):
        """Click on the visible subjects link."""
        Utility.click_option(self.driver, element=self.subjects)
        from pages.web.subjects import Subjects
        return go_to_(Subjects(driver=self.driver, base_url=self.base_url))

    @property
    def isbn_list(self):
        """Return the ISBN PDF button."""
        return self.find_element(*self._isbn_pdf_locator)

    @property
    def fulfillment(self):
        """Access the fulfillment company cards."""
        return [self.Company(self, card)
                for card in self.find_elements(*self._fulfillment_locator)]

    @property
    def publishers(self):
        """Access the publishing company cards."""
        return [self.Company(self, card)
                for card in self.find_elements(*self._publisher_locator)]

    class Company(Region):
        """A partner company."""

        _logo_locator = (By.CSS_SELECTOR, '.logo-dot img')
        _name_locator = (By.CSS_SELECTOR, 'h2')
        _description_locator = (By.CSS_SELECTOR, '.blurb')
        _button_locator = (By.CSS_SELECTOR, 'a')

        @property
        def logo(self):
            """Return the company logo."""
            return self.find_element(*self._logo_locator)

        @property
        def name(self):
            """Return the company name."""
            return self.find_element(*self._name_locator).text.strip()

        @property
        def description(self):
            """Return the company description."""
            return self.find_element(*self._description_locator).text.strip()

        @property
        def button(self):
            """Return the view company button."""
            return self.find_element(*self._button_locator)

        def view(self):
            """Click on the card button to view the company site."""
            Utility.switch_to(self.driver, element=self.button)
            return self.driver
