"""The instructor's course settings page."""

from time import sleep

from pypom import Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from utils.tutor import TutorException
from utils.utilities import Utility, go_to_


class BookSection(Region):
    """A book chapter or book section performance listing."""

    _book_number_locator = (By.CSS_SELECTOR, '.number')
    _title_locator = (By.CSS_SELECTOR, '.title')
    _practice_button_locator = (By.CSS_SELECTOR, 'button')
    _progress_bar_locator = (By.CSS_SELECTOR, '.progress-bar , .no-data')
    _clue_stats_locator = (By.CSS_SELECTOR, '.clue li')
    _question_count_locator = (By.CSS_SELECTOR, '.count')

    @property
    def number(self):
        """Return the chapter or section number.

        :return: the book chapter number or the individual section number
        :rtype: str

        """
        return self.find_element(*self._book_number_locator).text

    @property
    def title(self):
        """Return the chapter or section title.

        :return: the book chapter title or the individual section title
        :rtype: str

        """
        return self.find_element(*self._title_locator).text

    def practice(self):
        """Click on the progress bar or work more button.

        :return: a new practice session for a chapter, section, or the weakest
            topics or return the performance forecast for instructors
        :rtype: :py:class:`~pages.tutor.practice.Practice` or
            :py:class:`PerformanceForecast`

        """
        try:
            button = self.find_element(*self._practice_button_locator)
            Utility.click_option(self.driver, element=button)
            sleep(1)
            from pages.tutor.practice import Practice
            return go_to_(
                Practice(self.driver, base_url=self.page.page.base_url))
        except NoSuchElementException:
            # teachers don't have practice button on their forecast
            return self.page.page

    @property
    def progress(self):
        """Return the progress value or no data statement.

        :return: the rounded CLUe value from 0 to 100 or the 'Not enough' data
            message
        :rtype: str

        """
        progress = self.find_element(*self._progress_bar_locator)
        clue = progress.get_attribute('aria-valuename')
        if not clue:
            # not enough data to return a CLUe
            return progress.text
        return clue

    @property
    def stats(self):
        """Return the debugging CLUe data.

        :return: the CLUe data as key: value pairs
        :rtype: dict(str, str)

        """
        data = self.find_elements(*self._clue_stats_locator)
        group = {}
        for pair in data:
            key, value = self.driver.execute_script(
                'return arguments[0].textContent;', pair).split(': ')
            group[key] = value
        return group

    @property
    def count(self):
        """Return the worked assessments text.

        :return: the worked assessments for students or the the number of
            students and their worked assessments for teachers
        :rtype: str

        """
        return self.find_element(*self._question_count_locator).text


class PerformanceForecast(TutorBase):
    """The performance forecast page."""

    _page_title_locator = (By.CSS_SELECTOR, '.guide-group-title')
    _guide_locator = (By.CSS_SELECTOR, '.guide-group-key')
    _go_back_button_locator = (By.CSS_SELECTOR, '.info a')
    _section_tab_locator = (By.CSS_SELECTOR, '[role=tab]')
    _no_data_locator = (By.CSS_SELECTOR, '.no-data-message')
    _group_forecast_locator = (By.CSS_SELECTOR, '.guide-group')

    @property
    def title(self):
        """Return the page title.

        :return: the page title
        :rtype: str

        """
        return self.find_element(*self._page_title_locator).text

    @property
    def guide(self):
        """Access the colored bar guide.

        :return: the list of possible bar colors and their associated keys
        :rtype: list(:py:class:`~PerformanceForecast.Bar`)

        """
        return [self.Bar(self, bar)
                for bar in self.find_elements(*self._guide_locator)]

    def go_back(self):
        """Return to the previous page.

        Clicking on the 'Back to ...' button returns the user to the previously
        visited Tutor page, which is often the student's course page or the
        teacher's calendar.

        :return: None

        """
        button = self.find_element(*self._go_back_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(1)
        return

    @property
    def section_tabs(self):
        """Access the section or period tabs.

        :return: the list of available sections or periods
        :rtype: list(:py:class:`PerformanceForecast.Section`)

        """
        return [self.Section(self, tab)
                for tab in self.find_elements(*self._section_tab_locator)]

    def view_section(self, name):
        """View a course section by its name.

        :return: the performance forecast for the requested section or period
        :rtype: :py:class:`PerformanceForecast`
        :raises :py:class:`utils.tutor.TutorException`: if the name doesn't
            match an available course section

        """
        for tab in self.section_tabs:
            if tab.name == name:
                tab.select()
                return self.page
        raise TutorException('"{0}" does not match any active section')

    @property
    def no_data(self):
        """Return the 'no questions worked' message, if found.

        :return: the 'no questions worked' message if found, otherwise an empty
            string
        :rtype: str

        """
        message = self.find_elements(*self._no_data_locator).text
        return message[0].text if message else ''

    @property
    def forecast(self):
        """Access the performance forecast rows.

        :return: the forecast panels
        :rtype: :py:class:`~PerformanceForecast.Guide`
        :raise :py:class:`~utils.tutor.TutorException`: if the guide is not
            found

        """
        try:
            forecast = self.find_element(*self._group_forecast_locator)
            return self.Guide(self, forecast)
        except NoSuchElementException:
            raise TutorException('Performance guide not found; is there data?')

    class Bar(Region):
        """A progress bar."""

        _bar_locator = (By.CSS_SELECTOR, '.progress-bar')
        _key_locator = (By.CSS_SELECTOR, '.title')

        @property
        def color(self):
            """Return the background color for a bar.

            :return: the background color value
            :rtype: str

            """
            bar = self.find_element(*self._bar_locator)
            script = ('return window.getComputedStyle(arguments[0])'
                      '.backgroundColor')
            return self.driver.execute_script(script, bar)

        @property
        def key(self):
            """Return the key text.

            :return: the text description for a bar color
            :rtype: str

            """
            return self.find_element(*self._key_locator).text

    class Guide(Region):
        """The performance guide weakest guide and chapters."""

        _weakest_section_locator = (By.CSS_SELECTOR, '.weaker')
        _chapter_locator = (By.CSS_SELECTOR, '.chapter-panel:not(.weaker)')

        @property
        def weakest(self):
            """Access the weakest row.

            :return: the weakest row
            :rtype: :py:class:`~PerformanceForecast.Guide.Weakest`

            """
            row_root = self.find_element(*self._weakest_section_locator)
            return self.Weakest(self, row_root)

        @property
        def chapters(self):
            """Access the chapter rows.

            :return: the list of chapter rows
            :rtype: list(:py:class:`~PerformanceForecast.Guide.Chapter`)

            """
            return [self.Chapter(self, row)
                    for row in self.find_elements(*self._chapter_locator)]

        class Weakest(Region):
            """The sections with the worst performance."""

            _title_locator = (By.CSS_SELECTOR, '.chapter .title')
            _explanation_locator = (By.CSS_SELECTOR, '.explanation p')
            _practice_all_button_locator = (By.CSS_SELECTOR, '.weakest')
            _lacking_data_locator = (By.CSS_SELECTOR, '.lacking-data')
            _section_locator = (By.CSS_SELECTOR, '.section')

            @property
            def title(self):
                """Return the row title.

                :return: the row title
                :rtype: str

                """
                return self.find_element(*self._title_locator).text

            @property
            def explanation(self):
                """Return the explanation text for the 'Weakest Areas'.

                :return: the Weakest Areas explanation
                :rtype: str

                """
                return ' '.join(list([
                    line.text
                    for line
                    in self.find_elements(*self._explanation_locator)]))

            def practice_all(self):
                """Click the 'Practice All' button to start a practice session.

                :return: a practice session for the weakest book sections or
                    the performance forecast if there isn't enough data to
                    determine the weakest book sections or the user is a
                    teacher
                :rtype: :py:class:`~pages.tutor.practice.Practice` or
                    :py:class:`PerformanceForecast`

                """
                try:
                    button = self.find_element(
                        *self._practice_all_button_locator)
                    Utility.click_option(self.driver, element=button)
                    sleep(1)
                    from pages.tutor.practice import Practice
                    return go_to_(
                        Practice(self.driver,
                                 base_url=self.page.page.base_url))
                except NoSuchElementException:
                    return self.page.page

            @property
            def lack_data(self):
                """Return the "haven't worked enough problems" message.

                :return: the "haven't worked enough problems" message, if
                    found, else an empty string
                :rtype: str

                """
                message = self.find_elements(*self._lacking_data_locator)
                return message[0].text if message else ''

            @property
            def sections(self):
                """Access the row's book section groups.

                :return: the list of poorest performing book sections
                :rtype: list(:py:class:`BookSection`)

                """
                return [BookSection(self, section)
                        for section
                        in self.find_elements(*self._section_locator)]

        class Chapter(Region):
            """An individual book chapter row."""

            _chapter_locator = (By.CSS_SELECTOR, '.chapter')
            _section_locator = (By.CSS_SELECTOR, '.section')

            @property
            def chapter(self):
                """Access the chapter performance data.

                :return: the chapter performance data
                :rtype: :py:class:`BookSection`

                """
                chapter_root = self.find_element(*self._chapter_locator)
                return BookSection(self, chapter_root)

            @property
            def sections(self):
                """Access the chapter sections performance data.

                :return: the list of assigned chapter sections performance data
                :rtype: list(:py:class:`BookSection`)

                """
                return [BookSection(self, section)
                        for section
                        in self.find_elements(*self._section_locator)]

    class Section(Region):
        """A course section or period tab."""

        _name_locator = (By.CSS_SELECTOR, 'span')
        _select_tab_locator = (By.CSS_SELECTOR, 'a')

        @property
        def name(self):
            """Return the section or period name.

            :return: the section or period name
            :rtype: str

            """
            return self.find_element(*self._name_locator).text

        def select(self):
            """Click on the section tab.

            :return: the performance forecast with the selected section active
            :rtype: :py:class:`PerformanceForecast`

            """
            button = self.find_element(*self._select_tab_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.5)
            return self.page

        @property
        def selected(self):
            """Return True if the tab is currently active.

            :return: ``True`` if the tab is active, ``False`` otherwise
            :rtype: bool

            """
            return 'active' in self.root.get_attribute('class')
