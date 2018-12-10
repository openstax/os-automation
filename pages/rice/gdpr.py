"""Rice GDPR."""

from pypom import Page


class GeneralDataPrivacyRegulation(Page):
    """Rice GDPR."""

    URL_TEMPLATE = 'https://privacy.rice.edu/gdpr'

    @property
    def at_rice(self):
        """Return True if at Rice's homepage root."""
        return 'gdpr' in self.selenium.current_url
