"""Web's home page."""

from pypom import Page, Region
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.web.base import WebBase


class WebHome(WebBase):
    """OpenStax Web home page."""

    @property
    def subjects(self):
    	return self.Subjects(self)

    class Subjects(Region):
    	"""Subjects button on openstax homepage"""

    	_subject_loactor = (By.XPATH, '//li[1]/div/a')
    	_all_locator = (By.XPATH,'//li[1]/div/div/nav/div[1]/a')
    	_math_locator = (By.XPATH,'//li[1]/div/div/nav/div[2]/a')
    	_sci_locator = (By.XPATH,'//li[1]/div/div/nav/div[3]/a')
    	_soci_locator = (By.XPATH,'//li[1]/div/div/nav/div[4]/a')
    	_huma_locator = (By.XPATH,'//li[1]/div/div/nav/div[5]/a')
    	_ap_locaotr = (By.XPATH,'//li[1]/div/div/nav/div[6]/a')

    	def go_all(self):
    		"""Go to the all subjects page"""
    		self.find_element(*self._subject_loactor).click()
    		self.find_element(*self._all_loactor).click()
    		return self 

    	def go_math(self):
    		"""Go to the all subjects page"""
    		self.find_element(*self._subject_loactor).click()
    		self.find_element(*self._math_loactor).click()
    		return self 

    	def go_sci(self):
    		"""Go to the all subjects page"""
    		self.find_element(*self._subject_loactor).click()
    		self.find_element(*self._sci_loactor).click()
    		return self 

    	def go_soci(self):
    		"""Go to the all subjects page"""
    		self.find_element(*self._subject_loactor).click()
    		self.find_element(*self._soci_loactor).click()
    		return self 

    	def go_huma(self):
    		"""Go to the all subjects page"""
    		self.find_element(*self._subject_loactor).click()
    		self.find_element(*self._huma_loactor).click()
    		return self 

    	def go_ap(self):
    		"""Go to the all subjects page"""
    		self.find_element(*self._subject_loactor).click()
    		self.find_element(*self._ap_loactor).click()
    		return self 



    

  
