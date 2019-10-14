"""OpenStax global reach information page."""

from pages.web.base import WebBase


class GlobalReach(WebBase):
    """The Global Reach information page."""

    URL_TEMPLATE = '/global-reach'

    def is_displayed(self):
        """Return True if the global reach page is loaded."""
        return self.loaded and 'global' in self.location
