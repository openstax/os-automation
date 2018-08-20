"""OpenStax payment admin email logs page object."""

from selenium.webdriver.common.by import By

from pages.payments.base import PaymentsBase
from regions.payments.nav import PaymentsNav
from regions.payments.section import PaymentsListSection


class EmailLogs(PaymentsBase):
    """OpenStax payment admin email logs page object."""

    _section_locator = (By.CSS_SELECTOR, '.results tbody')

    @property
    def nav(self):
        """Return the nav bar region."""
        return PaymentsNav(self)

    @property
    def email_list(self):
        """Return the email list region."""
        return self.EmailList(self, self.find_element(*self._section_locator))

    class EmailList(PaymentsListSection):
        """The section of email lists."""

        class Item(PaymentsListSection.Item):
            """The section of email items."""

            _email_type_locator = (By.CSS_SELECTOR, '.field-email_type a')
            _email_locator = (By.CLASS_NAME, 'field-to_emails')
            _time_locator = (By.CLASS_NAME, 'field-sent')
            _success_locator = (By.CSS_SELECTOR, '.field-success img')

            @property
            def get_email_type(self):
                """Return the type of an email entry."""
                return self.find_element(*self._email_type_locator).text

            @property
            def get_email_address(self):
                """Return the email address of an email entry."""
                return self.find_element(*self._email_locator).text

            @property
            def get_email_time(self):
                """Return the sent time of an email entry."""
                return self.find_element(*self._time_locator).text

            @property
            def get_email_status(self):
                """Return the email status of a an email entry."""
                return self.find_element(
                    *self._success_locator).get_attribute('alt')
