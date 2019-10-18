"""The OpenStax Creator Fest information page."""

from pages.web.base import WebBase


class CreatorFest(WebBase):
    """The OpenStax Creator Fest information page."""

    URL_TEMPLATE = '/creator-fest'

    def is_displayed(self):
        """Return True if the Creator Fest page is loaded."""
        return self.loaded and 'creator' in self.location
