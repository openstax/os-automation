"""The page object for student enrolling in a new course with url."""

from time import sleep

from selenium.webdriver.common.by import By

from pages.accounts.home import AccountsHome
from pages.tutor.base import TutorBase
from pages.tutor.dashboard import TutorDashboard
from pages.tutor.purchase import TutorPurchase
from pages.tutor.student_calendar import StudentCalendar


class StudentEnroll(TutorBase):
    """The page object for student enrolling in a new course with url."""

    _get_started_btn_locator = (By.PARTIAL_LINK_TEXT, 'started')
    _later_btn_locator = (By.PARTIAL_LINK_TEXT, 'later')
    _buy_now_btn_locator = (By.PARTIAL_LINK_TEXT, 'Buy access now')
    _trial_btn_locator = (By.PARTIAL_LINK_TEXT, 'Try')

    def logged_in_enroll_pay_now(self):
        self.find_element(*self._get_started_btn_locator).click()
        sleep(1)
        self.find_element(*self._later_btn_locator).click()
        sleep(3)
        self.find_element(*self._buy_now_btn_locator).click()
        return TutorPurchase(self.driver)

    def logged_in_enroll_pay_later(self):
        self.find_element(*self._get_started_btn_locator).click()
        sleep(1)
        self.find_element(*self._later_btn_locator).click()
        sleep(3)
        self.find_element(*self._trial_btn_locator).click()
        return StudentCalendar(self.driver)
