"""OpenStax Web's microsurvey note region."""

from __future__ import annotations

from time import sleep
from typing import List

from pypom import Page, Region
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from utils.utilities import Utility


class MicroSurvey(Region):
    """OpenStax Web's microsurvey region."""

    _root_locator = (
        By.CSS_SELECTOR, '#microsurvey')

    _answer_option_locator = (
        By.CSS_SELECTOR, '.control-group label')
    _close_button_locator = (
        By.CSS_SELECTOR, '.put-away')
    _question_locator = (
        By.CSS_SELECTOR, 'h1')
    _submit_button_locator = (
        By.CSS_SELECTOR, 'button')

    @property
    def options(self) -> List[MicroSurvey.Option]:
        """Return the survey response options.

        :return: the survey responses
        :rtype: list(:py:class:`~regions.web.survey.MicroSurvey.Option`)

        """
        return [self.Option(self, response)
                for response
                in self.find_elements(*self._answer_option_locator)]

    @property
    def question(self) -> str:
        """Return the microsurvey question text.

        :return: the microsurvey question
        :rtype: str

        """
        return self.find_element(*self._question_locator).text

    def close(self) -> Page:
        """Close the survey box without answering the question.

        :return: the parent Web page
        :rtype: :py:class:`~pypom.Page`

        """
        button = self.find_element(*self._close_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.25)
        return self.page

    def is_displayed(self) -> bool:
        """Return True if the microsurvey box is displayed.

        :return: ``True`` if the microsurvey box height is greater than zero
        :rtype: bool

        """
        has_height = ('return window.getComputedStyle(arguments[0]).'
                      'height != "0px";')
        return self.driver.execute_script(has_height, self.root)

    def submit(self) -> Page:
        """Click the 'Submit' button.

        :return: the parent Web page
        :rtype: :py:class:`~pypom.Page`

        """
        button = self.find_element(*self._submit_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.25)
        return self.page

    class Option(Region):
        """A survey response option."""

        _checkbox_locator = (
            By.CSS_SELECTOR, 'input')

        @property
        def box(self) -> WebElement:
            """Return the checkbox input element.

            :return: the option checkbox
            :rtype: :py:class:`selenium.webdriver.remote.webelement.WebElement`

            """
            return self.find_element(*self._checkbox_locator)

        @property
        def is_checked(self) -> bool:
            """Return True when the checkbox is checked.

            :return: ``True`` if the checkbox is currently checked
            :rtype: bool

            """
            checked = 'return arguments[0].checked == true;'
            return self.driver.execute_script(checked, self.box)

        @property
        def option(self) -> str:
            """Return the option response.

            :return: the survey response text, name or title
            :rtype: str

            """
            return self.root.text

        def select(self):
            """Click the option checkbox.

            :return: None

            """
            Utility.click_option(self.driver, element=self.box)
