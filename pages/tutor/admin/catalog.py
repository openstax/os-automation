"""The admin catalog page object."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.admin.base import TutorAdminBase


class TutorAdminCatalog(TutorAdminBase):
    """Tutor admin course page object."""

    _add_locator = (By.CSS_SELECTOR, 'body > div > a')
    _edit_locator = (
        By.CSS_SELECTOR,
        '#offering_32 > span:nth-child(2) > a:nth-child(2)')
    _title_locator = (By.CSS_SELECTOR, '#offering_title')
    _description_locator = (By.CSS_SELECTOR, '#offering_description')
    _sales_locator = (By.CSS_SELECTOR, '#offering_salesforce_book_name')
    _eco_locator = (By.CSS_SELECTOR, '#offering_content_ecosystem_id')
    _url_locator = (By.CSS_SELECTOR, '#offering_webview_url')
    _save_locator = (By.CSS_SELECTOR, '#offering_ > input')

    def add_catalog(self):
        """Add a catalog."""
        self.find_element(*self._add_locator).click()
        self.find_element(*self._title_locator).sendKeys('a')
        self.find_element(*self._description_locator).sendKeys('a')
        self.find_element(*self._sales_locator).sendKeys('a')
        self.find_element(*self._url_locator).sendKeys('www.baidu.com')
        select = Select(*self._eco_locator)
        select.select_by_value('1')
        self.find_element(*self._save_locator).click()

    def edit_catalog(self):
        """Edit a catalog."""
        self.find_element(*self._edit_locator).click()
        self.find_element(*self._title_locator).sendKeys('a')
        self.find_element(*self._save_locator).click()
