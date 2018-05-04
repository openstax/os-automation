"""Rice placeholder."""
from pypom import Page


class Rice(Page):
    """Rice homepage."""

    URL_TEMPLATE = 'http://www.rice.edu'

    @property
    def at_rice(self):
        """Return True if at Rice's homepage root."""
        return 'rice.edu' in self.selenium.current_url
