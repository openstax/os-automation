"""Tutor Admin shared region nav bar."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.utils.utilities import Utility


class TutorAdminNav(Region):
    """Tutor admin nav bar region for logged in users."""

    _course_organization_locator = (By.CSS_SELECTOR, 'li.dropdown.open > a')
    _catalog_offerings_locator = (By.PARTIAL_LINK_TEXT, 'Catalog Offerings')
    _course_locator = (By.CSS_SELECTOR, 'li.dropdown.open > ul > li:nth-child(2) > a')
    _school_locator = (By.PARTIAL_LINK_TEXT, 'Schools')
    _districts_locator = (By.PARTIAL_LINK_TEXT, 'Districts')
    _content_locator = (By.CSS_SELECTOR, 'ul:nth-child(1) > li:nth-child(2) > a')
    _tag_locator = (By.PARTIAL_LINK_TEXT, 'Tags')
    _eco_locator = (By.PARTIAL_LINK_TEXT, 'Ecosystems')
    _legal_locator = (By.CSS_SELECTOR, 'ul:nth-child(1) > li:nth-child(3) > a')
    _term_locator = (By.PARTIAL_LINK_TEXT, 'Terms')
    _stat_locator = (By.CSS_SELECTOR, 'ul:nth-child(1) > li:nth-child(4) > a')
    _stat_course_locator = (By.CSS_SELECTOR, 'li.dropdown.open > ul > li:nth-child(1) > a')
    _user_locator = (By.PARTIAL_LINK_TEXT, 'Users')
    _job_locator = (By.PARTIAL_LINK_TEXT, 'Jobs')
    _payment_locator = (By.PARTIAL_LINK_TEXT, 'Payments')
    _data_locator = (By.PARTIAL_LINK_TEXT, 'Research Data')
    _system_setting_locator = (By.CSS_SELECTOR, 'ul:nth-child(1) > li:nth-child(10) > a')
    _setting_locator = (By.PARTIAL_LINK_TEXT, 'Settings')

    def go_to_catalog_offerings(self):
    	"""Go to catalog offerings."""
    	self.find_element(*self._course_organization_locator).click()
    	self.find_element(*self._catalog_offerings_locator).click()

    def go_to_course(self):
    	"""Go to course."""
    	self.find_element(*self._course_organization_locator).click()
    	self.find_element(*self._course_locator).click()

    def go_to_school(self):
    	"""Go to school."""
    	self.find_element(*self._course_organization_locator).click()
    	self.find_element(*self._school_locator).click()

    def go_to_district(self):
    	"""Go to district."""
    	self.find_element(*self._course_organization_locator).click()
    	self.find_element(*self._districts_locator).click()

    def go_to_tags(self):
    	"""Go to tags."""
    	self.find_element(*self._content_locator).click()
    	self.find_element(*self._tag_locator).click()

    def go_to_eco(self):
    	"""Go to ecosystems."""
    	self.find_element(*self._content_locator).click()
    	self.find_element(*self._eco_locator).click()

    def go_to_terms(self):
    	"""Go to terms."""
    	self.find_element(*self._legal_locator).click()
    	self.find_element(*self._term_locator).click()

    def go_to_stat(self):
    	"""Go to statistics."""
    	self.find_element(*self._stat_locator).click()
    	self.find_element(*self._stat_course_locator).click()

    def go_to_user(self):
    	"""Go to user."""
    	self.find_element(*self._user_locator).click()

    def go_to_job(self):
    	"""Go to job."""
    	self.find_element(*self._job_locator).click()

    def go_to_payments(self):
    	"""Go to payments."""
    	self.find_element(*self._payment_locator).click()

    def go_to_data(self):
    	"""Go to data."""
    	self.find_element(*self._data_locator).click()

    def go_to_settings(self):
    	"""Go to settings."""
    	self.find_element(*self._system_setting_locator).click()
    	self.find_element(*self._setting_locator).click()









