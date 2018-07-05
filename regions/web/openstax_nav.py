"""Openstax nav region."""

from pypom import Region
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class OpenStaxNav(Region):
    """OpenStax navbar region."""

    _openstax_logo_locator = (By.CLASS_NAME, 'logo-color')
    _subjects_dropdown_locator = (By.CSS_SELECTOR, "a[href*='subjects']")
    _all_subjects_locator = (By.PARTIAL_LINK_TEXT, "All")
    _math_subjects_locator = (By.CSS_SELECTOR, "a[href*='subjects/math']")
    _science_subjects_locator = (By.CSS_SELECTOR, "a[href*='subjects/science']")
    _social_sciences_subjects_locator = (By.CSS_SELECTOR, "a[href*='subjects/social-sciences']")
    _humanities_subjects_locator = (By.CSS_SELECTOR, "a[href*='subjects/humanities']")
    _ap_subjects_locator = (By.CSS_SELECTOR, "a[href*='subjects/AP']")
    _technology_dropdown_locator = (By.CSS_SELECTOR, "a[href*='technology']")
    _technology_options_locator = (By.PARTIAL_LINK_TEXT, "Technology Options")
    _openstax_tutor_locator = (By.CSS_SELECTOR, "a[href*='openstax-tutor']")
    _openstax_partners_locator = (By.CSS_SELECTOR, "a[href*='partners']")
    _our_impact_locator = (By.CSS_SELECTOR, "a[href*='impact']")
    _login_locator = (By.CLASS_NAME, 'pardotTrackClick')

    def go_to_web_home(self):
        """Goes to OpenStax home page."""
        self.find_element(*self._openstax_logo_locator).click()
        sleep(1)
        return self

    def go_to_subjects_all(self):
        """Goes to the all section fo the subjects page."""
        ActionChains(self.driver).move_to_element(*self._subjects_dropdown_locator).click(*self._all_subjects_locator).perform()
        sleep(1)
        return Subjects(self.driver)

    def go_to_subjects_math(self):
        """Goes to the math section of the subjects page."""
        ActionChains(self.driver).move_to_element(*self._subjects_dropdown_locator).click(*self._math_subjects_locator).perform()
        sleep(1)
        return Subjects(self.driver)

    def go_to_subjects_science(self):
        """Goes to the science section of the subjects page."""
        ActionChains(self.driver).move_to_element(*self._subjects_dropdown_locator).click(*self._science_subjects_locator).perform()
        sleep(1)
        return Subjects(self.driver)

    def go_to_subjects_science(self):
        """Goes to the science section of the subjects page."""
        ActionChains(self.driver).move_to_element(*self._subjects_dropdown_locator).click(*self._science_subjects_locator).perform()
        sleep(1)
        return Subjects(self.driver)

    def go_to_subjects_social_sciences(self):
        """Goes to the social science section of the subjects page."""
        ActionChains(self.driver).move_to_element(*self._subjects_dropdown_locator).click(*self._social_sciences_subjects_locator).perform()
        sleep(1)
        return Subjects(self.driver)

    def go_to_subjects_humanities(self):
        """Goes to the humanities section of the subjects page."""
        ActionChains(self.driver).move_to_element(*self._subjects_dropdown_locator).click(*self._humanities_subjects_locator).perform()
        sleep(1)
        return Subjects(self.driver)

    def go_to_subjects_ap(self):
        """Goes to the ap section of the subjects page."""
        ActionChains(self.driver).move_to_element(*self._subjects_dropdown_locator).click(*self._ap_subjects_locator).perform()
        sleep(1)
        return Subjects(self.driver)

    def go_to_technology_options(self):
        """Goes to the technology options page."""
        ActionChains(self.driver).move_to_element(*self._technology_dropdown_locator).click(*self._technology_options_locator).perform()
        sleep(1)
        return Technology(self.driver)

    def go_to_about_tutor(self):
        """Goes to the about tutor page."""
        ActionChains(self.driver).move_to_element(*self._technology_dropdown_locator).click(*self._about_tutor_locator).perform()
        sleep(1)
        return About_Tutor(self.driver)

    def go_to_partners(self):
        """Goes to the partners page."""
        ActionChains(self.driver).move_to_element(*self._technology_dropdown_locator).click(*self._openstax_partners_locator).perform()
        sleep(1)
        return Partners(self.driver)

    def go_to_our_impact(self):
        """Goes to the our impact page."""
        self.find_element(*self._our_impact_locator).click()
        sleep(1)
        return Our_Impact(self.driver)

    def go_to_login(self):
        """Goes to the our impact page."""
        self.find_element(*self._login_locator).click()
        sleep(1)
        return AccountsHome(self.driver)
