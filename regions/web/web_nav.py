"""Web nav region."""

from pypom import Region
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class WebNav(Region):
    """Website navbar region."""

    _about_us_locator = (By.CSS_SELECTOR, "a[href*='about']")
    _supporters_locator = (By.CSS_SELECTOR, "a[href*='foundation']")
    _blog_locator = (By.CSS_SELECTOR, "a[href*='blog']")
    _give_locator = (By.CSS_SELECTOR, "a[href*='give']")
    _help_locator = (By.CSS_SELECTOR, "a[href*='help']")
    _rice_locator = (By.CLASS_NAME, "rice-logo")

    def go_to_about_us(self):
        """Goes to the about us page."""
        self.find_element(*self._about_us_locator).click()
        sleep(1)
        return AboutUs(self.driver)

    def go_to_supporters(self):
        """Goes to the supporters page."""
        self.find_element(*self._supporters_locator).click()
        sleep(1)
        return Supporters(self.driver)

    def go_to_blog(self):
        """Goes to the blog page."""
        self.find_element(*self._blog_locator).click()
        sleep(1)
        return Blog(self.driver)

    def go_to_give(self):
        """Goes to the give page."""
        self.find_element(*self._give_locator).click()
        sleep(1)
        return Give(self.driver)

    def go_to_help(self):
        """Goes to the help page."""
        self.find_element(*self._help_locator).click()
        sleep(1)
        return Help(self.driver)

    def go_to_rice(self):
        """Goes to the rice home page."""
        self.find_element(*self._rice_locator).click()
        sleep(1)
        return Rice(self.driver)
