"""The highlighting summary print preview pane."""

from pypom import Page, Region
from selenium.webdriver.common.by import By


class PrintPreview(Page):
    """The print preview of the selected sections."""

    _section_locator = (By.CSS_SELECTOR, '.section')

    _raw_text_selector = '.notes'

    @property
    def sections(self):
        """Access the individual sections.

        :return: a list of annotations
        :rtype: list(:py:class:`~PrintPreview.PreviewSection`)

        """
        return [self.PreviewSection(self, section)
                for section
                in self.find_elements(*self._section_locator)]

    @property
    def raw_text(self):
        """Return all of the visible text.

        :return: all of the visible text in the print preview window
        :rtype: str

        """
        script = 'return document.querySelector("arguments[0]").textContent;'
        return self.driver.execute_script(script, self._raw_text_selector)

    class PreviewSection(Region):
        """A book section containing selected highlights."""

        _title_locator = (By.CSS_SELECTOR, 'h2')
        _highlight_locator = (By.CSS_SELECTOR, 'div[style]')

        @property
        def title(self):
            """Return the section title.

            :return: the section title for the listed annotations
            :rtype: str

            """
            return self.find_element(*self._title_locator).text

        @property
        def highlights(self):
            """Access the list of highlights and annotations.

            :return: a list of the section highlights and annotations
            :rtype: list(:py:class:`~PrintPreview.ReviewSection.Highlight`)

            """
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
                """Return the highlighted content.

                :return: the content of the highlight including markup
                :rtype: str

                """
                return (self.find_element(*self._highlighted_content_locator)
                        .get_attribute('innerHTML'))

            @property
            def note(self):
                """Return the note.

                :return: the highlight's annotation
                :rtype: str

                """
                return self.find_element(*self._note_locator).text
