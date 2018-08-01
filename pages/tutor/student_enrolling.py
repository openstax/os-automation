"""The page object for student enrolling in a new course with url."""

from time import sleep

from pypom import Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect

from pages.tutor.purchase import TutorPurchase
from pages.tutor.tutor_calendar import TutorCalendar


class StudentEnroll(Page):
    """The page object for student enrolling in a new course with url."""

    _get_started_btn_locator = (By.PARTIAL_LINK_TEXT, 'started')
    _id_locator = (By.CSS_SELECTOR, '.modal-body .inputs input')
    _continue_locator = (By.CSS_SELECTOR, '.modal-footer .btn-primary')
    _buy_now_btn_locator = (By.CSS_SELECTOR, '.body .btn-primary')
    _trial_btn_locator = (By.PARTIAL_LINK_TEXT, 'Try')

    def logged_in_enroll_pay_now(self):
        self.wait.until(
            expect.presence_of_element_located(
                self._get_started_btn_locator)).click()
        try:
            self.wait.until(
                expect.presence_of_element_located(
                    self._id_locator)).send_keys('123')
            self.find_element(*self._continue_locator).click()
        except:
            pass

        self.wait.until(
            expect.presence_of_element_located(
                self._buy_now_btn_locator)).click()
        return TutorPurchase(self.driver)

    def logged_in_enroll_pay_later(self):
        self.wait.until(
            expect.presence_of_element_located(
                self._get_started_btn_locator)).click()
        self.wait.until(
            expect.presence_of_element_located(
                self._id_locator)).send_keys('123')
        self.find_element(*self._continue_locator).click()
        self.wait.until(
            expect.presence_of_element_located(
                self._trial_btn_locator)).click()
        return TutorCalendar(self.driver)
