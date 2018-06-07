"""Rice GDPR."""

from pypom import Page


class GeneralDataPrivacyRegulation(Page):
    """Rice GDPR."""

    URL_TEMPLATE = 'https://vpit.rice.edu/policies/regulatory-compliance/gpdr'

    @property
    def at_rice(self):
        """Return True if at Rice's homepage root."""
        return 'regulatory' in self.selenium.current_url
