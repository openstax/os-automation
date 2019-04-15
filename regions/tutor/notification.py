"""Tutor notification bars."""

from pypom import Region
from selenium.webdriver.common.by import By

from utils.tutor import Tutor
from utils.utilities import Utility, go_to_


class Notifications(Region):
    """User notifications."""

    _notification_locator = (By.CSS_SELECTOR, '.notification')

    @property
    def displayed(self):
        """Return True if a notification bar is displayed."""
        return 'viewable' in self.root.get_attribute('class')

    @property
    def notifications(self):
        """Access the individual notification bars."""
        return [self.Notification(self, note)
                for note
                in self.find_elements(*self._notification_locator)]

    class Notification(Region):
        """A single notification bar."""

        _content_locator = (
            By.CSS_SELECTOR,
            'div:not(.system) > .body > span , .system > span')
        _add_student_id_locator = (By.CSS_SELECTOR, 'a')
        _dismiss_locator = (By.CSS_SELECTOR, 'button')

        @property
        def type(self):
            """Return the notification type."""
            root_style = self.root.get_attribute('class')
            if Tutor.EMAIL in root_style:
                return Tutor.EMAIL
            elif Tutor.END_OF_COURSE in root_style:
                return Tutor.END_OF_COURSE
            elif Tutor.STUDENT_ID in root_style:
                return Tutor.STUDENT_ID
            elif Tutor.SYSTEM in root_style:
                return Tutor.SYSTEM
            else:
                raise ValueError(
                    '"{0}" does not contain a known notification type'
                    .format(root_style))

        @property
        def content(self):
            """Return the notification text."""
            return self.find_element(*self._content_locator).text

        @property
        def add_student_id_button(self):
            """Return the 'Add Student ID' button."""
            button = self.find_elements(*self._add_student_id_locator)
            if button:
                return button[0]

        def add_student_id(self):
            """Click on the 'Add Student ID' button."""
            Utility.click_option(self.driver,
                                 element=self.add_student_id_button)
            from pages.tutor.student_id import TutorID
            return go_to_(TutorID(self.driver, self.page.page.base_url))

        @property
        def dismiss_button(self):
            """Return the dismiss notification 'x'."""
            button = self.find_elements(*self._dismiss_locator)
            if button:
                return button[0]

        def dismiss_notification(self):
            """Click on the dismiss 'x'."""
            Utility.click_option(self.driver, element=self.dismiss_button)
            return self.page.page
