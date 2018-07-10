"""OpenStax About Us Page."""

from pypom import Region
from selenium.webdriver.common.by import By
from pages.web.base import WebBase


class AboutUs(WebBase):
    """About us page."""

    _root_locator = (By.ID, 'main')
    _splash_locator = (By.CLASS_NAME, 'w-cards')
    _about_locator = (By.CLASS_NAME, 'meta')
    _people_locator = (By.XPATH, "//*[@id='main']/div/div[3]")

    @property
    def splash(self):
        """Splash banner region."""
        return self.find_element(*self._splash_locator)

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

        _about_links_locator = (By.CSS_SELECTOR, 'a')

        def get_links(self):
            """Gets all the links in this section."""
            return self.find_elements(*self._about_links_locator)

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
        _photo_locator = (By.CSS_SELECTOR, 'img')
        _click_headshot_locator = (By.CLASS_NAME, 'picture-area')
        _exit_locator = (By.CSS_SELECTOR, '.btn.dismiss')

        @property
        def name(self):
            """Name of the person."""
            return self.find_element(*self._name_locator).text

        @property
        def description(self):
            """Description of the person."""
            return self.find_element(*self._description_locator).text

        @property
        def photo_present(self):
            """Returns true/false depening on if photo is present or not."""
            if self.find_element(*self._photo_locator):
                return True
            else:
                return False

        @property
        def get_photo(self):
            """Photo of the person if present."""
            return self.find_element(*self._photo_locator)

        def click_headshot(self):
            """Clicks the headshot to view description."""
            self.find_element(*self._click_headshot_locator).click()

        def close_description(self):
            """Closes the description box."""
            self.find_element(*self._exit_locator).click()
