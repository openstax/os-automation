"""The Google Play app store."""

from pypom import Page
from selenium.webdriver.common.by import By


class GooglePlay(Page):
    """The OpenStax + SE page within the Google Play app store."""

    URL_TEMPLATE = ('https://play.google.com/store/apps/details'
                    '?id=com.openstax.openstax&hl=en'
                    '&pcampaignid='
                    'MKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1')

    _app_title_locator = (By.CSS_SELECTOR, 'h1 span')
    _app_description_text_locator = (
        By.CSS_SELECTOR, '[itemprop=description] [jsname]:not([class])')

    @property
    def loaded(self) -> bool:
        """Return True when the app title and description are found.

        :return: ``True`` when the OpenStax + SE app title and description are
            found within the page
        :rtype: bool

        """
        return self.title and self.description

    def is_displayed(self) -> bool:
        """Return True when the app store page is loaded.

        :return: ``True`` when the app store page for the OpenStax + SE app is
            loaded
        :rtype: bool

        """
        return self.loaded

    @property
    def title(self) -> str:
        """Return the app title.

        :return: the app title
        :rtype: str

        """
        return self.find_element(*self._app_title_locator).text

    @property
    def description(self) -> str:
        """Return the app description.

        :return: the app description
        :rtype: str

        """
        return self.find_element(*self._app_description_text_locator).text
