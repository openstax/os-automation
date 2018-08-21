"""The admin school page object."""

from selenium.webdriver.common.by import By

from pages.tutor.admin.base import TutorAdminBase


class TutorAdminSchool(TutorAdminBase):
    """Tutor admin course page object."""

    _delete_locator = (By.CSS_SELECTOR, 'a.btn.btn-xs.btn-secondary')
    _edit_locator = (By.CSS_SELECTOR, 'a.btn.btn-xs.btn-primary')
    _name_locator = (By.CSS_SELECTOR, '#school_name')
    _save_locator = (By.CSS_SELECTOR, 'input.btn.btn-primary')
    _add_locator = (By.CSS_SELECTOR, 'body > div > a')
