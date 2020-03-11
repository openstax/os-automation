"""Social login control for the main content pane."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.facebook.home import Facebook
from pages.google.home import Google
from utils.utilities import Utility, go_to_


class SocialLogins(Region):
    """Social logins found in the Accounts main content region."""

    _facebook_button_locator = (
        By.CSS_SELECTOR, '.facebook.btn')
    _google_button_locator = (
        By.CSS_SELECTOR, '.google.btn')

    def log_in_with_facebook(self) -> Facebook:
        """Click the Facebook button.

        :return: the Facebook log in page
        :rtype: :py:class:`~pages.facebook.home.Facebook`

        """
        button = self.find_element(*self._facebook_button_locator)
        Utility.click_option(self.driver, element=button)
        return go_to_(Facebook(self.driver))

    def log_in_with_google(self) -> Google:
        """Click the Google button.

        :return: the Google log in page
        :rtype: :py:class:`~pages.google.home.Google`

        """
        button = self.find_element(*self._google_button_locator)
        Utility.click_option(self.driver, element=button)
        return go_to_(Google(self.driver))
