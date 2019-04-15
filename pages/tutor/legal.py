"""Tutor externally available terms of use and privacy policy."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorLoginBase
from pages.utils import go_to_


class Policies(TutorLoginBase):
    """The Tutor site general legal policies."""

    @property
    def policies(self):
        """Access the main page text."""
        return self.Policies(self)

    @property
    def title(self):
        """Return the policy page title."""
        return self.policies.title

    @property
    def description(self):
        """Return the policy page explanation text."""
        return self.policies.description

    @property
    def terms_of_use(self):
        """Return the terms of use policy text."""
        return self.policies.terms_of_use

    @property
    def privacy_policy(self):
        """Return the privacy policy text."""
        return self.policies.privacy_policy

    class Policies(Region):
        """The body containing the OpenStax policies."""

        TERMS_OF_USE = 0
        PRIVACY_POLICY = 1

        _root_locator = (By.CSS_SELECTOR,
                         '.container .row .container:nth-child(2)')
        _title_locator = (By.CSS_SELECTOR, 'h2')
        _description_locator = (By.CSS_SELECTOR, '.row:nth-child(2)')
        _policy_locator = (By.CSS_SELECTOR, '.well')
        _section_locator = (By.CSS_SELECTOR, 'p , h3')

        @property
        def title(self):
            """Return the policy page title."""
            return self.find_element(*self._title_locator).text

        @property
        def description(self):
            """Return the policy explanation."""
            return self.find_element(*self._description_locator).text

        @property
        def policies(self):
            """Return the policy sections."""
            return self.find_elements(*self._policy_locator)

        @property
        def terms_of_use(self):
            """Return the terms of use."""
            return self._policy_text(self.TERMS_OF_USE)

        @property
        def privacy_policy(self):
            """Return the privacy policy."""
            return self._policy_text(self.PRIVACY_POLICY)

        def _policy_text(self, section):
            """Return the text list for a particular policy."""
            parts = self.policies[section]
            lines = [line.text
                     for line in parts.find_elements(*self._section_locator)]
            return '\n'.join(lines)

    class Nav(TutorLoginBase.Nav):
        """The terms base navigation."""

        _log_in_locator = (By.CSS_SELECTOR, '.btn')

        def go_to_log_in(self):
            """Click the 'LOG IN' button."""
            self.find_element(*self._log_in_locator).click()
            from pages.accounts.home import AccountsHome
            return go_to_(AccountsHome(self.driver))
