"""The book highlight summary modal."""

from __future__ import annotations

from time import sleep
from typing import List

from pypom import Page, Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as expect

from utils.utilities import Utility, go_to_


class DeleteConfirmation(Region):
    """The delete highlight confirmation dialog box."""

    _cancel_button_locator = (
        By.CSS_SELECTOR, '.btn-default')
    _delete_button_locator = (
        By.CSS_SELECTOR, '.btn-primary')
    _heading_content_locator = (
        By.CSS_SELECTOR, '.popover-header')
    _message_content_locator = (
        By.CSS_SELECTOR, '.message')

    @property
    def heading(self) -> str:
        """Return the dialog box header.

        :return: the dialog box header text
        :rtype: str

        """
        return self.find_element(*self._heading_content_locator).text

    @property
    def message(self) -> str:
        """Return the dialog box message.

        :return: the dialog box message text
        :rtype: str

        """
        return self.find_element(*self._message_content_locator).text

    def cancel(self) -> MyHighlights:
        """Click the dialog box cancel button.

        :return: the My Highlights dialog box
        :rtype: :py:class:`~regions.tutor.my_highlights.MyHighlights`

        """
        button = self.find_element(*self._cancel_button_locator)
        Utility.click_option(self.driver, element=button)
        self.wait.until(expect.staleness_of(self.root))
        return self.page

    def delete(self) -> MyHighlights:
        """Click the dialog box delete button.

        :return: the My Highlights dialog box
        :rtype: :py:class:`~regions.tutor.my_highlights.MyHighlights`

        """
        button = self.find_element(*self._delete_button_locator)
        Utility.click_option(self.driver, element=button)
        self.wait.until(expect.staleness_of(self.root))
        return self.page


class MyHighlights(Region):
    """The My Highlights dialog box."""

    _root_locator = (
        By.CSS_SELECTOR, '[role=dialog]')

    _back_to_top_of_modal_button_locator = (
        By.CSS_SELECTOR, '.modal-scroll-btn')
    _close_modal_button_locator = (
        By.CSS_SELECTOR, '.close')
    _filter_pane_locator = (
        By.CSS_SELECTOR, '.filter-area')
    _modal_title_locator = (
        By.CSS_SELECTOR, '.modal-title')
    _my_highlights_pane_locator = (
        By.CSS_SELECTOR, '.notes')

    @property
    def all_highlights(self) \
            -> List[MyHighlights.Highlights.Section.Highlight]:
        r"""Return all available highlights.

        :return: a list of all currently displayed highlights
        :rtype: list(:py:class:`~regions.tutor.my_highlights \
                                .MyHighlights.Highlights.Section.Highlight`)

        """
        highlights = []
        for section in self.highlights.sections:
            highlights
        highlights = highlights + section.highlights
        return self._all_highlights

    @property
    def back_to_top(self):
        """Click the scroll to the top of the dialog box button.

        :return: None

        """
        button = self.find_element(*self._back_to_top_of_modal_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.5)

    @property
    def close(self) -> Page:
        """Close the My Highlights dialog box.

        :return: the parent page
        :rtype: :py:class:`~pypom.Page`

        """
        button = self.find_element(*self._close_modal_button_locator)
        Utility.click_option(self.driver, element=button)
        self.wait.until(expect.staleness_of(self.root))
        return self.page

    @property
    def filter_bar(self) -> MyHighlights.FilterBar:
        """Access the section filter options control bar.

        :return: the My Highlights filter bar
        :rtype: :py:class:`~regions.tutor.my_highlights.MyHighlights.FilterBar`

        """
        filter_bar_root = self.find_element(*self._filter_pane_locator)
        return self.FilterBar(self, filter_bar_root)

    @property
    def highlights(self) -> MyHighlights.Highlights:
        r"""Access the filtered highlights pane.

        :return: the highlights pane
        :rtype: :py:class:`~regions.tutor.my_highlights. \
                            MyHighlights.Highlights`

        """
        highlights_pane_root = self.find_element(
            *self._my_highlights_pane_locator)
        return self.Highlights(self, highlights_pane_root)

    @property
    def loaded(self) -> bool:
        """Return True when the My Highlights panes are found.

        :return: ``True`` when the title, filter bar and highlights pane are
            found within the dialog box
        :rtype: bool

        """
        return self.title and self.filter_bar and self.highlights

    @property
    def root(self) -> WebElement:
        """Access the root element for the My Highlights region.

        .. note:
           Override the default root method because the dialog box is outside
           of the main content (neighbor element).

        :return: the dialog root element
        :rtype: :py:class:

        """
        if self._root is None and self._root_locator is not None:
            script = ('return document.querySelector('
                      f'"{self._root_locator[1]}");')
            return self.driver.execute_script(script)
        return self._root

    @property
    def title(self) -> str:
        """Return the dialog title.

        :return: the My Highlights modal title
        :rtype: str

        """
        return self.find_element(*self._modal_title_locator).text

    def is_displayed(self) -> bool:
        """Return True if the dialog is displayed.

        :return: ``True`` if the My Highlights dialog box root is displayed
        :rtype: bool

        """
        return self.root.is_displayed()

    class FilterBar(Region):
        """The My Highlights section filter bar and controls."""

        _section_selector_locator = (
            By.CSS_SELECTOR, '#multi-select')
        _select_all_sections_link_locator = (
            By.CSS_SELECTOR, '.select-all')
        _clear_all_sections_link_locator = (
            By.CSS_SELECTOR, '.select-none')
        _available_section_options_locator = (
            By.CSS_SELECTOR, '[class*=MultiSelectItems]')
        _active_filter_selections_locator = (
            By.CSS_SELECTOR, '[class*=TagListItem]')
        _clear_all_filters_link_locator = (
            By.CSS_SELECTOR, '[class*=ClearAllButton]')
        _print_highlights_button_locator = (
            By.CSS_SELECTOR, '.filter-widget ~ div > button')

        @property
        def filtered_by(self) -> List[MyHighlights.FilterBar.Filter]:
            r"""Access the current book filters.

            :return: the list of currently selected book section filters
            :rtype: list(:py:class:`~regions.tutor.my_highlights \
                                    .MyHighlights.FilterBar.Filter`)

            """
            return [self.Filter(self, option)
                    for option
                    in self.find_elements(
                        *self._active_filter_selections_locator)]

        @property
        def sections(self) -> List[MyHighlights.FilterBar.Section]:
            r"""Access the list of available book section options.

            :return: the list of book sections with at least one highlight
            :rtype: list(:py:class:`~regions.tutor.my_highlights \
                                    .MyHighlights.FilterBar.Section`)

            """
            return [self.Section(self, option)
                    for option
                    in self.find_elements(
                        *self._available_section_options_locator)]

        def print(self):
            """Click the 'Print' highlights buttn.

            :return: None

            """
            button = self.find_element(*self._print_highlights_button_locator)
            Utility.click_option(self.driver, element=button)

        def sections_menu(self):
            """Toggle the 'Sections' multi-choice menu.

            :return: None

            """
            toggle = self.find_element(*self._section_selector_locator)
            Utility.click_option(self.driver, element=toggle)

        def select_all(self):
            """Click the 'All' sections selector.

            :return: None

            """
            link = self.find_element(*self._select_all_sections_link_locator)
            Utility.click_option(self.driver, element=link)

        def select_none(self):
            """Click the no sections ('None') selector.

            :return: None

            """
            link = self.find_element(*self._clear_all_filters_link_locator)
            Utility.click_option(self.driver, element=link)

        class Filter(Region):
            """An active book section filter."""

            _chapter_section_label_locator = (
                By.CSS_SELECTOR, '.chapter-section')
            _remove_filter_locator = (
                By.CSS_SELECTOR, '.remove-tag')
            _section_name_locator = (
                By.CSS_SELECTOR, '.remove-tag ~ span')

            @property
            def section(self) -> str:
                """Return the chapter and section number.

                :return: the chapter and section number, if available
                :rtype: str

                """
                try:
                    return self.find_element(
                        *self._chapter_section_label_locator).text
                except NoSuchElementException:
                    return ''

            @property
            def title(self) -> str:
                """Return the section title.

                :return: the section title
                :rtype: str

                """
                return self.find_element(*self._section_name_locator).text

            def remove(self):
                """Remove an active section filter.

                :return: None

                """
                button = self.find_element(*self._remove_filter_locator)
                Utility.click_option(self.driver, element=button)
                sleep(0.25)

        class Section(Region):
            """A book section with highlights."""

            _checkbox_select_locator = (
                By.CSS_SELECTOR, 'a')
            _filter_section_title_locator = (
                By.CSS_SELECTOR, '.title')
            _is_active_locator = (
                By.CSS_SELECTOR, '[data-icon=check-square]')

            @property
            def selected(self) -> bool:
                """Return True if the section filter is currently selected.

                :return: ``True`` if the checkbox is checked
                :rtype: bool

                """
                return bool(self.find_elements(*self._is_active_locator))

            @property
            def title(self) -> str:
                """Return the filter section title.

                :return: the filter section title
                :rtype: bool

                """
                return (self.find_element(*self._filter_section_title_locator)
                        .text)

            def select(self):
                """Toggle the highlight filter section checkbox.

                :return: None

                """
                checkbox = self.find_element(*self._checkbox_select_locator)
                Utility.click_option(self.driver, element=checkbox)
                sleep(0.1)

    class Highlights(Region):
        """The pane displaying highlights for selected book sections."""

        _section_locator = (
            By.CSS_SELECTOR, '.section')

        @property
        def sections(self) -> List[MyHighlights.Highlights.Section]:
            r"""Return the list of sections with highlights.

            :return: the list of currently filtered book sections with at
                least one highlight
            :rtype: list(:py:class:`regions.tutor.my_highlights
                                    .MyHighlights.Highlights.Section`)

            """
            return [self.Section(self, section)
                    for section
                    in self.find_elements(*self._section_locator)]

        class Section(Region):
            """Highlights within an individual book section."""

            _highlight_locator = (
                By.CSS_SELECTOR, '.note-card')
            _section_number_locator = (
                By.CSS_SELECTOR, '.chapter-section')
            _section_title_locator = (
                By.CSS_SELECTOR, '.section-title div')

            @property
            def highlights(self) \
                    -> List[MyHighlights.Highlights.Section.Highlight]:
                r"""Access the book section highlights.

                :return: the list of highlights found in the book section
                :rtype: list(
                    :py:class:`~regions.tutor.my_highlights.MyHighlights \
                               .Highlights.Section.Highlight)

                """
                return [self.Highlight(self, highlight)
                        for highlight
                        in self.find_elements(*self._highlight_locator)]

            @property
            def section(self) -> str:
                """Return the book chapter and section number.

                :return: the book chapter and section number, if available
                :rtype: str

                """
                try:
                    return (self.find_element(*self._section_number_locator)
                            .text)
                except NoSuchElementException:
                    return ''

            @property
            def title(self) -> str:
                """Return the book section title.

                :return: the book section title
                :rtype: str

                """
                return self.find_element(*self._section_title_locator).text

            class Highlight(Region):
                """A single highlight or annotation."""

                _cancel_note_changes_button_locator = (
                    By.CSS_SELECTOR, '[title=Cancel]')
                _delete_highlight_button_locator = (
                    By.CSS_SELECTOR, '[title=Delete]')
                _edit_note_button_locator = (
                    By.CSS_SELECTOR, '[title=Edit]')
                _edit_note_text_box_locator = (
                    By.CSS_SELECTOR, 'textarea')
                _highlight_content_locator = (
                    By.CSS_SELECTOR, 'blockquote')
                _highlight_note_locator = (
                    By.CSS_SELECTOR, '.plain-text')
                _save_note_changes_button_locator = (
                    By.CSS_SELECTOR, '[title=Save]')
                _view_highlight_in_book_button_locator = (
                    By.CSS_SELECTOR, '.controls a')

                _confirmation_box_selector = '#confirmation-alert'

                @property
                def content(self) -> str:
                    """Return the text content of the highlight.

                    :return: the highlighted text content
                    :rtype: str

                    """
                    return (self.find_element(*self._highlight_content_locator)
                            .get_attribute('textContent'))

                @property
                def note(self) -> str:
                    """Return the highlight's note or annotation text.

                    :return: the note attached to the highlighed text
                    :rtype: str

                    """
                    return (self.find_element(*self._highlight_note_locator)
                            .get_attribute('textContent'))

                @note.setter
                def note(self, content: str):
                    """Edit the highlight's note or annotation text.

                    :param str content: the new note content
                    :return: None

                    """
                    textarea = self.find_element(
                        *self._edit_note_text_box_locator)
                    Utility.clear_field(self.driver, textarea)
                    textarea.send_keys(content)
                    sleep(0.15)

                def delete(self):
                    r"""Click the delete highlight button.

                    :return: the confirmation dialog box
                    :rtype: :py:class:`~regions.tutor.my_highlights \
                                        .Confirmation`

                    """
                    button = self.find_element(
                        *self._delete_highlight_button_locator)
                    Utility.click_option(self.driver, element=button)
                    dialog_box = ('return document.querySelector('
                                  f'"{self._confirmation_box_selector}");')
                    box_root = self.wait.until(
                        lambda _: self.driver.execute_script(dialog_box))
                    return DeleteConfirmation(self, box_root)

                def edit(self):
                    """Click the edit note button.

                    :return: None

                    """
                    button = self.find_element(*self._edit_note_button_locator)
                    Utility.click_option(self.driver, element=button)
                    sleep(0.15)

                def view(self) -> Page:
                    """View the reference book at the highlight's location.

                    :return: the reference book view scrolled to the location
                        of the highlight
                    :rtype: :py:class:`~pages.tutor.reference.ReferenceBook`

                    """
                    url = Utility.parent_page(self).base_url
                    from pages.tutor.reference import ReferenceBook
                    button = self.find_element(
                        *self._view_highlight_in_book_button_locator)
                    Utility.switch_to(self.driver, element=button)
                    return go_to_(ReferenceBook(self, base_url=url))
