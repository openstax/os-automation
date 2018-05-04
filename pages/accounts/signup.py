"""Break the signup process out of the base."""
from selenium.webdriver.common.by import By

from pages.accounts.base import AccountsBase


class Signup(AccountsBase):
    """Signup process."""

    URL_TEMPLATE = '/signup'

    _signup_role_locator = (By.ID, 'signup_role')
    _next_step_button_locator = (By.CSS_SELECTOR, '.primary')
    _email_locator = (By.ID, 'signup_email')
    _pin_entry_locator = (By.ID, 'pin_pin')
    _password_entry_locator = (By.ID, 'signup_password')
    _password_confirmation_locator = (By.ID, 'signup_password_confirmation')
    _social_signup_locator = (By.PARTIAL_LINK_TEXT, 'Google')

    def account_signup(self, _type='student', social=None, kwargs=None):
        """Single signup entry point."""
        if _type == 'student':
            return self._student_signup(_type, social, kwargs)
        return self._elevated_signup(_type, social, kwargs)

    def _student_signup(self, type='student', social=None, **kwargs):
        """Student signup."""
        return self

    def _elevated_signup(self, type='teacher', social=None, **kwargs):
        """Non-student signup."""
        return self
