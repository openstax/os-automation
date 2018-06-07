"""Home page objects."""
# from pypom import Region
# from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase


class TutorHome(TutorBase):
    """Home page base."""

    def log_in(self, user, password):
        """Log into the site with a specific user."""

    @property
    def logged_in(self):
        """Return user log in status."""
