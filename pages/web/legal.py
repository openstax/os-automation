"""The legal / intellectual property frequently asked questions page."""

from time import sleep

from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility, go_to_


class LegalBase(WebBase):
    """The base page for the legal document pages."""

    _heading_locator = (By.CSS_SELECTOR, '#main h1')
    _content_locator = (By.CSS_SELECTOR, '#main [data-html*=content]')
    _text_locator = (By.CSS_SELECTOR, 'p')

    @property
    def loaded(self):
        """Return True when the content is available."""
        return sleep(1) or Utility.has_children(self.content)

    @property
    def heading(self):
        """Return the heading."""
        return self.find_element(*self._heading_locator)

    @property
    def content(self):
        """Return the content wrapper."""
        return self.find_element(*self._content_locator)

    @property
    def title(self):
        """Return the heading text."""
        return self.heading.text.strip()

    @property
    def text(self):
        """Return the body text."""
        return [paragraph.text.strip()
                for paragraph
                in self.content.find_elements(*self._text_locator)]

    def is_displayed(self):
        """Return True if the heading is displayed."""
        return self.heading.is_displayed()


class License(LegalBase):
    """The OpenStax.org licensing overview page."""

    URL_TEMPLATE = '/license'

    _heading_locator = (By.CSS_SELECTOR, '#maincontent h2')


class Terms(LegalBase):
    """The OpenStax.org terms of use."""

    URL_TEMPLATE = '/tos'


class PrivacyPolicy(LegalBase):
    """The OpenStax.org terms of use."""

    URL_TEMPLATE = '/privacy-policy'

    _section_title_locator = (By.CSS_SELECTOR, 'h3')
    _privacy_content_locator = (By.CSS_SELECTOR, '[data-html=content] p')
    _gdpr_locator = (By.CSS_SELECTOR, '[href$=gdpr]')

    @property
    def sections(self):
        """Access the section headings."""
        return [section.text.strip().split('. ', 1)[-1]
                for section
                in self.find_elements(*self._section_title_locator)]

    @property
    def privacy_content(self):
        """Return the privacy policy content."""
        return [subsection.text.strip()
                for subsection
                in self.find_elements(*self._privacy_content_locator)
                if len(subsection.text.strip()) > 0]

    def view(self, section):
        """Scroll to the selected section heading."""
        target = self.find_elements(*self._section_title_locator)[section]
        Utility.scroll_to(self.driver, element=target, shift=-80)
        return self

    def view_gdpr(self):
        """View the Rice GDPR policy."""
        Utility.switch_to(self.driver, link_locator=self._gdpr_locator)
        from pages.rice.gdpr import GeneralDataPrivacyRegulation
        return go_to_(GeneralDataPrivacyRegulation(self.driver))
