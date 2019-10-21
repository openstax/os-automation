"""An OpenStax Tutor Beta tooltip region."""

from __future__ import annotations

from time import sleep
from typing import List, Union

from pypom import Page, Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from utils.utilities import Utility, go_to_


class Float(Region):
    """The new student enrollment links pane."""

    _content_locator = (
        By.CSS_SELECTOR, '.body')
    _footer_next_and_close_button_locator = (
        By.CSS_SELECTOR, '.footer button:last-child, .welcome-to-tutor button')
    _get_new_links_button_locator = (
        By.CSS_SELECTOR, '.footer button:first-child')
    _heading_locator = (
        By.CSS_SELECTOR, '.header')
    _is_enrollment_class_locator = (
        By.CSS_SELECTOR, '.new-enrollment-link')
    is_welcome_to_openstax_class_locator = (
        By.CSS_SELECTOR, '.welcome-to-tutor')
    _x_close_button_locator = (
        By.CSS_SELECTOR, '.ox-icon-close')

    _floater_root_selector = '.__floater'

    @property
    def root(self) -> WebElement:
        """Return the secondary base element for the floating region.

        :return: the secondary element in the floating region as the base
            element is a z-index assignment
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.driver.execute_script(
            f'return document.querySelector("{self._floater_root_selector}");')

    @property
    def is_open(self) -> bool:
        """Return True when the new enrollment links pane is open.

        :return: ``True`` when the new enrollment links pane is open, else
            ``False``
        :rtype: bool

        """
        if not self.root:
            return False
        return '__open' in self.root.get_attribute('class')

    @property
    def is_enrollment(self) -> bool:
        """Return True if the floating modal is the enrollment links pane.

        :return: ``True`` if the pane contains the enrollment links view
        :rtype: bool

        """
        return bool(self.find_elements(
            *self._is_enrollment_class_locator))

    @property
    def is_welcome(self) -> bool:
        """Return True if the floating modal is the welcome to OpenStax pane.

        :return: ``True`` if the pane contains the Welcome to OpenStax Tutor
            Beta view
        :rtype: bool

        """
        return bool(self.find_elements(
            *self._is_welcome_to_openstax_class_locator))

    @property
    def title(self) -> str:
        """Return the modal heading text.

        :return: the floating region heading text
        :rtype: str

        """
        return self.find_element(*self._heading_locator).text

    def x(self) -> Page:
        """Click the 'x' close button.

        :return: the current page
        :rtype: :py:class:`~pypom.Page`

        """
        return self.close(use_x=True)

    @property
    def content(self) -> str:
        """Return the modal content text.

        :return: the floating region body content text
        :rtype: str

        """
        return (self.find_element(*self._content_locator)
                .get_attribute('textContent'))

    def go_to_the_new_links(self) -> Page:
        """Click the 'Go to the new links' button.

        :return: the course settings page if this is the enrollment links pane,
            otherwise return the current page
        :rtype: :py:class:`~pypom.Page`

        """
        if not self.is_enrollment:
            return self.page
        button = self.find_element(*self._get_new_links_button_locator)
        Utility.click_option(self.driver, element=button)
        from pages.tutor.settings import CourseSettings
        return go_to_(CourseSettings(self.driver, base_url=self.page.base_url))

    def get_them_later(self) -> Page:
        """Click the "I'll get them later" button.

        :return: the instructor's calendar
        :rtype: :py:class:`~pypom.Page`

        """
        return self.close()

    def next(self) -> Union[Float, Page]:
        """Click the 'Next X/Y' button.

        :return: the next floating tooltip or the current page if this is the
            last tooltip in a chain
        :rtype: :py:class:`~regions.tutor.tooltip.Float` or
            :py:class:`~pypom.Page`

        """
        return self.close()

    def close(self, use_x: bool = False) -> Union[Float, Page]:
        """Close the floating modal.

        :param bool use_x: use the 'x' button instead of the footer button
        :return: the instructor's calendar
        :rtype: :py:class:`~regions.tutor.tooltip.Float` or
            :py:class:`~pypom.Page`

        """
        if use_x:
            button = self.find_element(
                *self._x_close_button_locator)
        else:
            button = self.find_element(
                *self._footer_next_and_close_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.5)
        if self.root:
            # there is another tooltip
            return Float(self.page)
        # close the tooltip chain
        return self.page


class Tooltip(Region):
    """An individual tooltip pane."""

    _close_tooltip_locator = (
        By.CSS_SELECTOR, '[class*=close] , [data-type=close]')
    _column_locator = (
        By.CSS_SELECTOR, '.column')
    _content_locator = (
        By.CSS_SELECTOR, '[class*=main] p')
    _continue_button_locator = (
        By.CSS_SELECTOR, '[class*="--primary"] , [data-type=next]')
    _heading_locator = (
        By.CSS_SELECTOR, '.heading , [class*="__header"]')
    _previous_button_locator = (
        By.CSS_SELECTOR, '[class*="--secondary"] , [data-type=back]')
    _subheading_locator = (
        By.CSS_SELECTOR, '.sub-heading')
    _view_later_button_locator = (
        By.CSS_SELECTOR, '[class*="--skip"]')

    _joyride_root_selector = '.joyride'

    @property
    def title(self) -> str:
        """Return the heading text.

        :return: the tooltip region heading text
        :rtype: str

        """
        return self.find_element(*self._heading_locator).text

    @property
    def subtitle(self) -> str:
        """Return the subheading text.

        :return: the subheading text, if found, otherwise an empty string
        :rtype: str

        """
        try:
            return self.find_element(*self._subheading_locator).text
        except NoSuchElementException:
            return ""

    @property
    def content(self) -> str:
        """Return the standard tooltip content.

        :return: the tooltip content text, if found, otherwise an empty string
        :rtype: str

        """
        try:
            return self.find_element(*self._content_locator).text
        except NoSuchElementException:
            return ""

    @property
    def columns(self) -> List[Tooltip.Column]:
        """Access the tooltip columns.

        :return: the tooltip columns
        :rtype: list(:py:class:`~regions.tutor.tooltip.Tooltip.Column`)

        """
        return [self.Column(self, column)
                for column
                in self.find_elements(*self._column_locator)]

    def close(self) -> Page:
        """Click on the window close button.

        :return: the tooltip's parent page
        :rtype: :py:class:`~pypom.Page`

        """
        Page = self.page.__class__
        button = self.find_element(*self._close_tooltip_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.5)
        return Page(self.driver, self.page.base_url)

    def previous(self) -> Tooltip:
        """Click on the 'Back' button.

        :return: the previous tooltip
        :rtype: :py:class:`~regions.tutor.tooltip.Tooltip`

        """
        button = self.find_element(*self._previous_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.75)
        tooltip_root = self.driver.execute_script(
            f'return document.querySelector("{self._joyride_root_selector}");')
        sleep(0.33)
        return Tooltip(self.page, tooltip_root)

    def next(self) -> Union[Page, Tooltip]:
        """Click on the 'Continue', 'Next', or 'Got It' button.

        :return: the previous tooltip
        :rtype: :py:class:`~pypom.Page` or
            :py:class:`~regions.tutor.tooltip.Tooltip`

        """
        button = self.find_element(*self._continue_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.75)
        tooltip_root = self.driver.execute_script(
            f'return document.querySelector("{self._joyride_root_selector});')
        sleep(0.33)
        if tooltip_root:
            return Tooltip(self.page, tooltip_root)
        return self.page

    def view_later(self) -> Page:
        """Click on the 'View later' button.

        :return: the tooltip's parent page
        :rtype: :py:class:`~pypom.Page`

        """
        button = self.find_element(*self._view_later_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.25)
        return self.page

    class Column(Region):
        """A display column."""

        _title_locator = (By.CSS_SELECTOR, 'h3')
        _text_locator = (By.CSS_SELECTOR, 'p')

        @property
        def title(self) -> str:
            """Return the column title.

            :return: the column title
            :rtype: str

            """
            return self.find_element(*self._title_locator).text

        @property
        def text(self) -> str:
            """Return the explanation text.

            :return: the tooltip explanation text
            :rtype: str

            """
            return self.find_element(*self._text_locator).text
