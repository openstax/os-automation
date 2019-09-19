"""The Apple app store."""

from pypom import Page
from selenium.webdriver.common.by import By


class AppStore(Page):
    """The OpenStax + SE page within the Apple app store."""

    _app_title_locator = (By.CSS_SELECTOR, '.app-header__title')
    _app_description_text_locator = (
        By.CSS_SELECTOR, '.section__description p[data-test-bidi]:first-child')

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
