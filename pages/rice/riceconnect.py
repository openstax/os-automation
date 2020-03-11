"""Rice's RiceConnect portal for OpenStax donations."""

from time import sleep

from pypom import Page
from selenium.webdriver.common.by import By


class RiceConnect(Page):
    """Rice's RiceConnect portal."""

    URL_TEMPLATE = 'https://riceconnect.rice.edu/donation/support-openstax'

    _main_content_locator = (
        By.CSS_SELECTOR, '#content #content-main')

    @property
    def at_rice(self) -> bool:
        """Return True if the opening RiceConnect content is found on the page.

        :return: ``True`` if the RiceConnect heading text is found on the page
        :rtype: bool

        """
        return ('Help us create a world where anyone can learn'
                in self.driver.page_source and
                'riceconnect' in self.driver.current_url)

    @property
    def loaded(self) -> bool:
        """Return True when the RiceConnect page is loaded.

        .. note::
           We delay the check by 1/2 second for Safari and Firefox to insure
           the page is loading prior to the full DOM ``load``.

        :return: ``True`` when the RiceConnect content is found
        :rtype: bool

        """
        self.wait.until(
            lambda _: self.find_elements(*self._main_content_locator))
        script = (r'document.addEventListener("load", function(event) {});')
        sleep(0.5)
        return self.driver.execute_script(script) or True

    def is_displayed(self):
        """Return True if the amount header is displayed."""
        return self.find_element(*self._main_content_locator).is_displayed()
