"""The Tutor reference view of the textbook."""

from time import sleep

from pypom import Page, Region
from selenium.webdriver.common.by import By

from utils.utilities import Utility, go_to_


class ReferenceBook(Page):
    """The complete textbook reading experience."""

    _nav_bar_locator = (By.CSS_SELECTOR, '.tutor-navbar')
    _table_of_contents_locator = (By.CSS_SELECTOR, '.book-menu')
    _content_locator = (By.CSS_SELECTOR, '.book-page-wrapper')
    _highlights_summary_locator = (By.CSS_SELECTOR, '.notes-summary')

    @property
    def nav(self):
        """Access the reference book navigation bar."""
        nav_root = self.find_element(*self._nav_bar_locator)
        return self.Nav(self, nav_root)

    @property
    def table_of_contents(self):
        """Access the table of contents."""
        toc_root = self.find_element(*self._table_of_contents_locator)
        return self.TableOfContents(self, toc_root)

    @property
    def content(self):
        """Access the currently selected section's book content."""
        content_root = self.find_element(*self._content_locator)
        return self.Content(self, content_root)

    @property
    def highlights(self):
        """Access the highlighting summary page."""
        annotation_root = self.find_element(*self._highlights_summary_locator)
        return self.Highlights(self, annotation_root)

    class Nav(Region):
        """The reference book navigation controls."""

        _menu_toggle_locator = (By.CSS_SELECTOR, '.book-menu-toggle')
        _section_title_locator = (By.CSS_SELECTOR, '.section-title span')
        _notes_toggle_locator = (By.CSS_SELECTOR, '.note-summary-toggle')
        _teacher_content_locator = (By.CSS_SELECTOR, '.teacher-content-toggle')

        _pop_over_content_selector = '.popover-body'

        @property
        def menu_toggle(self):
            """Return the table of contents toggle button."""
            return self.find_element(*self._menu_toggle_locator)

        @property
        def menu_is_open(self):
            """Return True if the ToC is open."""
            return 'open' in self.menu_toggle.get_attribute('class')

        def click_menu_toggle(self):
            """Click on the ToC toggle button."""
            Utility.click_option(self.driver, element=self.menu_toggle)
            return self.page

        @property
        def section_title(self):
            """Return the currently displayed section title."""
            return self.find_element(*self._section_title_locator).text

        @property
        def notes_summary_toggle(self):
            """Return the highlighting summary toggle button."""
            return self.find_element(*self._notes_toggle_locator)

        @property
        def note_summary_is_open(self):
            """Return True if the highlight summary page is visible."""
            return 'active' in self.notes_summary_toggle.get_attribute('class')

        def click_notes_summary_toggle(self):
            """Click on the highlight summary page toggle."""
            Utility.click_option(self.driver,
                                 element=self.notes_summary_toggle)
            return self.page

        @property
        def is_teacher(self):
            """Return True if the instructor toggle is available."""
            return bool(self.find_elements(*self._teacher_content_locator))

        @property
        def teacher_content_toggle(self):
            """Return the instructor content display toggle."""
            if self.is_teacher:
                return self.find_element(*self._teacher_content_locator)
            return None

        def show_teacher_content(self):
            """Click on the teacher content toggle."""
            toggle = self.teacher_content_toggle
            if toggle:
                Utility.click_option(self.driver, element=toggle)
            return self.page

        @property
        def popover_content(self):
            """Return the pop over text if found or a blank string."""
            if self.is_teacher:
                script = 'return document.querySelector("arguments[0]");'
                content = self.driver.execute_script(
                    script, self._pop_over_content_selector)
                if content:
                    return content.text
            return ''

    class TableOfContents(Region):
        """The reference book table of contents."""

        _chapter_locator = (By.CSS_SELECTOR, 'ul[data-depth="1"]')

        @property
        def chapters(self):
            """Access the individual book chapters."""
            return [self.Chapter(self, chapter)
                    for chapter
                    in self.find_elements(*self._chapter_locator)]

        class Chapter(Region):
            """A single book chapter list in the table of contents."""

            _title_locator = (
                    By.CSS_SELECTOR, '.chapter-section-title span:last-child')
            _chapter_number_locator = (By.CSS_SELECTOR, '.section-number')
            _section_locator = (By.CSS_SELECTOR, 'li:not(:first-child)')

            @property
            def title(self):
                """Return the chapter title."""
                return self.find_element(*self._title_locator).text

            @property
            def number(self):
                """Return the chapter number."""
                return self.find_element(*self._chapter_number_locator).text

            @property
            def sections(self):
                """Access the chapter sections."""
                return [self.Section(self, section)
                        for section
                        in self.find_elements(*self._section_locator)]

            class Section(Region):
                """A single book section including unnumbered pieces."""

                _title_locator = (By.CSS_SELECTOR, 'span:not(.section-number)')
                _display_line_locator = (By.CSS_SELECTOR, 'span')
                _link_locator = (By.CSS_SELECTOR, 'a')

                @property
                def section_id(self):
                    """Return the section identification."""
                    return self.root.get_attribute('data-section')

                @property
                def title(self):
                    """Return the section title."""
                    return self.find_element(*self._title_locator).text

                @property
                def display_line(self):
                    """Return the entire section line text."""
                    return (' '.join([
                        segment.text
                        for segment
                        in self.find_elements(*self._display_line_locator)]))

                def view_section(self):
                    """Click the section link."""
                    link = self.find_element(*self._link_locator)
                    Utility.click_option(self.driver, element=link)
                    return self.page.page.page

    class Content(Region):
        """The selected section's content."""

        _next_page_locator = (By.CSS_SELECTOR, '.next')
        _previous_page_locator = (By.CSS_SELECTOR, '.prev')
        _content_locator = (By.CSS_SELECTOR, '#paged-content')
        _page_data_locator = (By.CSS_SELECTOR, '.ecosystem-info')

        @property
        def next_page_arrow(self):
            """Return the next page arrow button."""
            return self.find_element(*self._next_page_locator)

        def next(self):
            """Click on the next page button."""
            Utility.click_option(self.driver, element=self.next_page_arrow)
            return self.page

        @property
        def previous_page_arrow(self):
            """Return the previous page arrow button."""
            return self.find_element(*self._previous_page_locator)

        def previous(self):
            """Click on the previous page button."""
            Utility.click_option(self.driver, element=self.previous_page_arrow)
            return self.page

        @property
        def content(self):
            """Return the HTML book content."""
            return (self.find_element(*self._content_locator)
                    .get_attribute('innerHTML'))

        @property
        def page_data(self):
            """Return the ecosystem page data."""
            return self.find_element(*self._page_data_locator).text

    class Highlights(Region):
        """The highlighting summary page overlay."""

        _description_locator = (
                    By.CSS_SELECTOR, '.notes > h4 , .notes > h3 , .notes > p')
        _sections_toggle_locator = (By.CSS_SELECTOR, '.dropdown-toggle')
        _dropdown_menu_option_locator = (
                                    By.CSS_SELECTOR, '.multi-selection-option')
        _print_preview_locator = (By.CSS_SELECTOR, '.print-btn')
        _note_sections_locator = (By.CSS_SELECTOR, '.notes .section')

        @property
        def description(self):
            """Return the page description if no notes are available."""
            return '\n'.join(
                [line.text
                 for line
                 in self.find_elements(*self._description_locator)])

        @property
        def drop_down(self):
            """Return the section selector drop down menu."""
            return self.find_element(*self._sections_toggle_locator)

        @property
        def menu_is_open(self):
            """Return True if the section drop down menu is open."""
            return \
                self.drop_down.get_attribute('aria-expanded').lower() == 'true'

        def menu_toggle(self):
            """Click on the drop down menu."""
            Utility.click_option(self.driver, element=self.drop_down)
            return self.page

        @property
        def options(self):
            """Return the list of sections with highlights."""
            return [self.DisplaySection(self, section)
                    for section
                    in self.find_elements(*self._dropdown_menu_option_locator)]

        def show_sections(self, sections=[], show_all=False):
            """Select sections by section number."""
            for section in self.options:
                if not self.menu_is_open:
                    self.menu_toggle()
                option_is_checked = section.is_checked
                if show_all and not option_is_checked:
                    section.select()
                else:
                    option = section.section
                    if ((option in sections and not option_is_checked) or
                            (option not in sections and option_is_checked)):
                        section.select()
                sleep(0.25)
            return self.page

        def show_print_preview(self):
            """Click on the 'Print this page' button."""
            button = self.find_element(*self._print_preview_locator)
            Utility.switch_to(self.driver, element=button)
            return PrintPreview(self.driver)

        @property
        def notes(self):
            """Access each displayed highlight or annotation."""
            return [self.Note(self, note)
                    for note
                    in self.find_elements(*self._note_sections_locator)]

        class Note(Region):
            """An individual highlight or annotation."""

            _content_locator = (By.CSS_SELECTOR, '.note-content')
            _note_locator = (By.CSS_SELECTOR, '.plain-text')
            _edit_button_locator = (By.CSS_SELECTOR, '[title=Edit]')
            _note_box_locator = (By.CSS_SELECTOR, '.edit-box textarea')
            _view_button_locator = (By.CSS_SELECTOR, '.controls a')
            _delete_button_locator = (By.CSS_SELECTOR, '[title=Delete]')
            _delete_confirm_locator = (By.CSS_SELECTOR, '.btn-primary')
            _save_edit_button_locator = (By.CSS_SELECTOR, '[title=Save]')
            _cancel_edit_button_locator = (By.CSS_SELECTOR, '[title*=Cancel]')

            _pop_over_content_selector = '.popover'

            @property
            def content(self):
                """Return the full HTML content text."""
                return (self.find_element(*self._content_locator)
                        .get_attribute('innerHTML'))

            @property
            def note(self):
                """Return the associated note, if found."""
                return self.find_element(*self._note_locator).text

            def edit(self, text=''):
                """Edit the highlight note."""
                button = self.find_element(*self._edit_button_locator)
                Utility.click_option(self.driver, element=button)
                if text:
                    self.note_box.send_keys(text)
                    sleep(0.1)
                    self.save_edit()
                    sleep(0.25)
                return self.page.page

            @property
            def note_box(self):
                """Return the note edit box."""
                return self.find_element(*self._note_box_locator)

            def save_edit(self):
                """Click on the checkmark confirm button."""
                button = self.find_element(*self._save_edit_button_locator)
                Utility.click_option(self.driver, element=button)
                return self.page.page

            def cancel_edit(self):
                """Click on the X cancelation button."""
                button = self.find_element(*self._cancel_edit_button_locator)
                Utility.click_option(self.driver, element=button)
                return self.page.page

            def view(self):
                """Click on the view in book link."""
                button = self.find_element(*self._view_button_locator)
                Utility.switch_to(self.driver, element=button)
                return go_to_(
                    ReferenceBook(self.driver, self.page.page.base_url))

            def delete(self):
                """Delete the highlight."""
                button = self.find_element(*self._delete_button_locator)
                script = 'return document.querySelector("arguments[0]");'
                Utility.click_option(self.driver, element=button)
                pop_up = self.driver.execute_script(
                    script, self._pop_over_content_selector)
                confirm = pop_up.find_element(*self._delete_confirm_locator)
                Utility.click_option(self.driver, element=confirm)
                sleep(0.25)
                return self.page.page


class PrintPreview(Page):
    """The print preview of the selected sections."""

    _section_locator = (By.CSS_SELECTOR, '.section')

    _raw_text_selector = '.notes'

    @property
    def sections(self):
        """Access the individual sections."""
        return [self.PreviewSection(self, section)
                for section
                in self.find_elements(*self._section_locator)]

    @property
    def raw_text(self):
        """Return all of the visible text."""
        script = 'return document.querySelector("arguments[0]").textContent;'
        return self.driver.execute_script(script, self._raw_text_selector)

    class PreviewSection(Region):
        """A book section containing selected highlights."""

        _title_locator = (By.CSS_SELECTOR, 'h2')
        _highlight_locator = (By.CSS_SELECTOR, 'div[style]')

        @property
        def title(self):
            """Return the section title."""
            return self.find_element(*self._title_locator).text

        @property
        def highlights(self):
            """Access the list of highlights and annotations."""
            return [self.Highlight(self, mark)
                    for mark
                    in self.find_elements(*self._highlight_locator)]

        class Highlight(Region):
            """An individual hightlight or annotation."""

            _highlighted_content_locator = (
                                        By.CSS_SELECTOR, '.openstax-has-html')
            _note_locator = (By.CSS_SELECTOR, 'p[style]')

            @property
            def highlight(self):
                """Return the highlighted content."""
                return (self.find_element(*self._highlighted_content_locator)
                        .get_attribute('innerHTML'))

            @property
            def note(self):
                """Return the note."""
                return self.find_element(*self._note_locator).text
