"""The page object for student enrolling in a new course with url."""

from pypom import Page
from selenium.webdriver.common.by import By


class StudentEnroll(Page):
    """The page object for student enrolling in a new course with url."""

    _get_started_btn_locator = (By.PARTIAL_LINK_TEXT, 'started')
    _id_locator = (By.CSS_SELECTOR, '.modal-body .inputs input')
    _continue_locator = (By.CSS_SELECTOR, '.modal-footer .btn-primary')
    _buy_now_btn_locator = (By.CSS_SELECTOR, '.body .btn-primary')
    _trial_btn_locator = (By.PARTIAL_LINK_TEXT, 'Try')
