"""The frequently asked questions page."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility, go_to_external_


class FAQ(WebBase):
    """The OpenStax frequently asked questions."""

    URL_TEMPLATE = '/faq'

    _main_content_locator = (By.CSS_SELECTOR, '#main')
    _title_locator = (By.CSS_SELECTOR, '.boxed h1')
    _heading_locator = (By.CSS_SELECTOR, '[data-html=subhead] p')
    _support_locator = (By.CSS_SELECTOR, '.hero [href*=force]')
    _question_locator = (By.CSS_SELECTOR, '.qa')

    @property
    def loaded(self):
        """Return True if the hero banner is found."""
        content = self.find_elements(*self._main_content_locator)
        return super().loaded and bool(content)

    def is_displayed(self):
        """Return True if the main content is loaded."""
        return self.find_element(*self._main_content_locator).is_displayed()

    @property
    def title(self):
        """Return the page title."""
        return self.find_element(*self._title_locator).text.strip()

    @property
    def heading(self):
        """Return the heading text."""
        return self.find_element(*self._heading_locator).text.strip()

    def visit_support(self):
        """Click the 'support page' link."""
        link = self.wait.until(
            lambda _: self.find_element(*self._support_locator))
        url = link.get_attribute('href')
        Utility.switch_to(self.driver, element=link)
        from pages.salesforce.home import Salesforce
        return go_to_external_(Salesforce(self.driver), url)

    @property
    def questions(self):
        """Return the list of frequently asked questions."""
        return [self.Question(self, question)
                for question in self.find_elements(*self._question_locator)]

    class Question(Region):
        """A frequently asked question."""

        _question_locator = (By.CSS_SELECTOR, '.question p')
        _answer_locator = (By.CSS_SELECTOR, '.answer p')
        _toggle_locator = (By.CSS_SELECTOR, '.question')

        def toggle(self):
            """Open or close the question."""
            toggle = self.find_element(*self._toggle_locator)
            Utility.click_option(self.driver, element=toggle)
            return self.page

        @property
        def question(self):
            """Return the question text."""
            return self.find_element(*self._question_locator).text.strip()

        @property
        def answer(self):
            """Return the answer text."""
            text = ''
            for paragraph in self.find_elements(*self._answer_locator):
                text = text + '\n' + paragraph.text.strip()
            return text

        @property
        def answer_is_visible(self):
            """Return True if the answer is visible."""
            return 'open' in self.root.get_attribute('class')
