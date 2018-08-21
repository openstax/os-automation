"""The admin course page object."""

from selenium.webdriver.common.by import By

from pages.tutor.admin.base import TutorAdminBase


class TutorAdminCourse(TutorAdminBase):
    """Tutor admin course page object."""

    _edit_locator = (By.CSS_SELECTOR, 'a:nth-child(2)')
    _year_locator = (By.CSS_SELECTOR, '#course_year')
    _save_locator = (By.CSS_SELECTOR, '#edit-save')
    _name_locator = (By.CSS_SELECTOR, '#course_name')
    _add_locator = (By.CSS_SELECTOR, 'body > div > a')
    _imcomplete_locator = (By.CSS_SELECTOR,
                           'body > div > ul > li:nth-child(2) > a')
    _fail_locator = (By.CSS_SELECTOR, 'body > div > ul > li:nth-child(3) > a')
