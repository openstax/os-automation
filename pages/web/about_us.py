"""OpenStax About Us Page."""

from time import sleep

from pypom import Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase


class AboutUs(WebBase):
    """About Us page."""

    _root_locator = (By.ID, 'main')
    _splash_locator = (By.CSS_SELECTOR, '.w-cards h1')
    _about_locator = (By.CLASS_NAME, 'meta')
    _people_locator = (By.CSS_SELECTOR, "#main .boxed")

    @property
    def splash(self):
        """Splash banner region."""
        return self.find_element(*self._splash_locator).text

    @property
    def about(self):
        """About text region."""
        el = self.find_element(*self._about_locator)
        return self.About(self, el)

    @property
    def people(self):
        """People region which includes both team members and advisors."""
        el = self.find_element(*self._people_locator)
        return self.People(self, el)

    class About(Region):
        """About region."""

        _mission_statement_locator = (By.CSS_SELECTOR, 'p:first-child')
        _promote_oer_locator = (By.CSS_SELECTOR, '[href*=".pdf"]')
        _support_link_locator = (By.PARTIAL_LINK_TEXT, 'Support')
        _faq_link_locator = (By.CSS_SELECTOR, '[href="/faq"]')

    class People(Region):
        """People region."""

        _team_headshots_locator = (
            By.CSS_SELECTOR, '.our-team .headshots .headshot')
        _advisors_headshots_locator = (
            By.CSS_SELECTOR, '.strategic-advisors .headshots .headshot')

        @property
        def team(self):
            """Team region."""
            items = self.find_elements(*self._team_headshots_locator)
            return [self.Headshot(self, el) for el in items]

        @property
        def advisors(self):
            """Advisors region."""
            items = self.find_elements(*self._advisors_headshots_locator)
            return [self.Headshot(self, el) for el in items]

        class Headshot(Region):
            """Headshot region."""

            _name_locator = (By.CSS_SELECTOR, '.picture-area .name')
            _description_locator = (By.CLASS_NAME, 'description')
            _photo_container_locator = (By.CLASS_NAME, 'picture-area')
            _photo_locator = (By.CSS_SELECTOR, 'img')
            _exit_locator = (By.CSS_SELECTOR, '.btn.dismiss')

            @property
            def name(self):
                """Return the team member's name."""
                return self.find_element(*self._name_locator).text

            @property
            def description(self):
                """Return the team member's biography."""
                return self.find_element(*self._description_locator).text

            @property
            def photo_present(self):
                """Return true if a photo is present."""
                el = self.find_element(*self._photo_container_locator)
                return 'has-picture' in el.get_attribute('class')

            @property
            def get_photo(self):
                """Return the team member's photo source URL."""
                el = self.find_element(*self._photo_locator)
                return el.get_attribute('src')

            def open_description(self):
                """Open the description box."""
                self.find_element(*self._photo_container_locator).click()
                sleep(0.25)
                return self

            def close_description(self):
                """Close the description box."""
                self.find_element(*self._exit_locator).click()
                sleep(0.25)
                return self
