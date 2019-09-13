"""The assignment review."""

from __future__ import annotations

from typing import List, Union

from pypom import Region
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from pages.tutor.calendar import Calendar
from pages.tutor.scores import Scores
from pages.web.errata import Errata
from utils.utilities import Utility, go_to_


class Metrics(TutorBase):
    """The assignment review metrics."""

    _assessment_column_locator = (By.CSS_SELECTOR, '.col-sm-8')
    _assignment_book_sections_locator = (By.CSS_SELECTOR, 'h2[data-section]')
    _assignment_exercise_locator = (By.CSS_SELECTOR, '.openstax-exercise-card')
    _metrics_overview_sidebar_locator = (By.CSS_SELECTOR, '.col-sm-4')
    _metrics_toolbar_locator = (By.CSS_SELECTOR, '[class*=SecondaryToolbar]')

    @property
    def loaded(self) -> bool:
        """Return True when the metrics columns are found.

        :return: ``True`` when the assessments column and the sidebar are found
        :rtype: bool

        """
        assessments = self.find_elements(*self._assessment_column_locator)
        sidebar = self.find_elements(*self._metrics_overview_sidebar_locator)
        return assessments and sidebar

    def is_displayed(self) -> bool:
        """Return True if the assignment metrics page is displayed.

        :return: ``True`` if the metrics page is displayed
        :rtype: bool

        """
        content = self.find_elements(*self._assessment_column_locator)
        return self.loaded and content[0].get_attribute('textContent')

    @property
    def exercises(self) -> List[Metrics.Assessment]:
        """Access the assignment questions."""
        return [self.Assessment(self, question)
                for question
                in self.find_elements(*self._assignment_exercise_locator)]

    @property
    def sections(self) -> List[str]:
        """Return the list of book sections in the assignment and review.

        :return: the list of book section numbers with their titles found in
            the assignment or in spaced practice assessments
        :rtype: list(str)

        """
        return [section.get_attribute('textContent')
                for section
                in self.find_elements(*self._assignment_book_sections_locator)]

    @property
    def sidebar(self) -> Metrics.Sidebar:
        """Access the review metrics overview and section selector.

        :return: the sidebar
        :rtype: :py:class:`~pages.tutor.review.Metrics.Sidebar`

        """
        sidebar = self.find_element(*self._metrics_overview_sidebar_locator)
        return self.Sidebar(self, sidebar)

    @property
    def toolbar(self) -> Metrics.Toolbar:
        """Access the assignment toolbar.

        :return: the assignment navigation toolbar
        :rtype: :py:class:`~pages.tutor.review.Metrics.Toolbar`

        """
        toolbar = self.find_element(*self._metrics_toolbar_locator)
        return self.Toolbar(self, toolbar)

    class Assessment(Region):
        """An assignment question."""

        _assessment_answer_locator = (By.CSS_SELECTOR, '.openstax-answer')
        _assessment_id_locator = (By.CSS_SELECTOR, 'div[data-section]')
        _question_stem_locator = (By.CSS_SELECTOR, '.question-stem')
        _suggest_a_correction_link_locator = (
            By.CSS_SELECTOR, '.exercise-identifier-link a')

        @property
        def answers(self) -> List[Metrics.Assessment.Answer]:
            r"""Access the assessment answers.

            :return: the list of available assessment answers
            :rtype: \
                list(:py:class:`~pages.tutor.review.Metrics.Assessment.Answer`)

            """
            return [self.Answer(self, option)
                    for option
                    in self.find_elements(*self._assessment_answer_locator)]

        @property
        def assessment_id(self) -> str:
            """Return the Exercises identification number and version.

            :return: the OpenStax Exercises identification number and
                assessment version for the question
            :rtype: str

            """
            return (self.find_element(*self._assessment_id_locator)
                    .get_attribute('data-section'))

        @property
        def question_stem(self) -> str:
            """Return the assessment question stem content.

            :return: the question stem text
            :rtype: str

            """
            return (self.find_element(*self._question_stem_locator)
                    .get_attribute('textContent'))

        def suggest_a_correction(self) -> Errata:
            """Click the 'Suggest a correction' link.

            :return: the Web errata form in a new tab
            :rtype: :py:class:`~pages.web.errata.Errata`

            """
            # TODO: Issue - errata link points to the wrong URL

        class Answer(Region):
            """An answer to the parent question."""

            _answer_content_text_locator = (By.CSS_SELECTOR, '.answer-answer')
            _answer_correctness_locator = (By.CSS_SELECTOR, '.answers-answer')
            _answer_letter_locator = (By.CSS_SELECTOR, '.answer-letter')
            _selected_by_students_count_locator = (
                By.CSS_SELECTOR, '.selected-count')

            @property
            def answered_by(self) -> int:
                """Return the number of students who selected this answer.

                :return: the number of students who selected this answer option
                :rtype: int

                """
                return int(self.find_element(
                    *self._selected_by_students_count_locator))

            @property
            def content(self) -> str:
                """Return the answer text.

                :return: the answer text
                :rtype: str

                """
                return (self.find_element(*self._answer_content_text_locator)
                        .get_attribute('textContent'))

            @property
            def is_correct(self) -> bool:
                """Return True if this answer is correct.

                :return: ``True`` if this answer is correct for the assessment
                :rtype: bool

                """
                correctness = self.find_element(
                    *self._answer_correctness_locator)
                return 'answer-correct' in correctness.get_attribute('class')

            @property
            def letter(self) -> str:
                """Return the answer letter.

                :return: the answer letter
                :rtype: str

                """
                return self.find_element(*self._answer_letter_locator).text

    class Sidebar(Region):
        """The review metrics assignment overview sidebar."""

        _course_section_tab_locator = (By.CSS_SELECTOR, '[role=tab]')
        _assignment_stats_locator = (By.CSS_SELECTOR, '.task-stats-data')

        @property
        def sections(self) -> List[Metrics.Sidebar.Tab]:
            """Access the course section tab options.

            :return: the list of available course sections for this assignment
            :rtype: list(:py:class:`~pages.tutor.review.Metrics.Sidebar.Tab`)

            """
            return [self.Tab(self, section)
                    for section
                    in self.find_elements(*self._course_section_tab_locator)]

        @property
        def stats(self) -> Metrics.Sidebar.Stats:
            """Access the assignment statistics.

            :return: the sidebar statistics panel
            :rtype: :py:class:`~pages.tutor.review.Metrics.Sidebar.Stats`

            """
            panel = self.find_element(*self._assignment_stats_locator)
            return self.Stats(self, panel)

        class Stats(Region):
            """The sidebar section stats."""

            _current_assignment_topics_locator = (
                By.CSS_SELECTOR, 'section:nth-child(2) .reading-progress')
            _spaced_practice_topics_locator = (
                By.CSS_SELECTOR, 'section:nth-child(3) .reading-progress')
            _students_completed_locator = (
                By.CSS_SELECTOR, '.complete div')
            _students_in_progress_locator = (
                By.CSS_SELECTOR, '.in-progress div')
            _students_not_started_locator = (
                By.CSS_SELECTOR, '.not-started div')

            @property
            def completed(self) -> int:
                """Return the number of students who have completed the work.

                :return: the number of students who have completed the
                    assignment
                :rtype: int

                """
                return self._completed

            @property
            def current_topics(self) \
                    -> List[Metrics.Sidebar.Stats.BookSection]:
                r"""Access the stats for current assignment topics.

                :return: the list of book section stats specified by the
                    instructor in the assignment
                :rtype: list(:py:class:`~pages.tutor.review \
                                        .Metrics.Sidebar.Stats.BookSection`)

                """
                return [self.BookSection(self, section)
                        for section
                        in self.find_elements(
                            *self._current_assignment_topics_locator)]

            @property
            def in_progress(self) -> int:
                """Return the number of students who have started the work.

                :return: the number of students who have started but not
                    completed the assignment
                :rtype: int

                """
                return self._in_progress

            @property
            def not_started(self) -> int:
                """Return the number of students who have not started the work.

                :return: the number of students who have not started the
                    assignment
                :rtype: int

                """
                return self._not_started

            @property
            def spaced_practice(self) \
                    -> List[Metrics.Sidebar.Stats.BookSection]:
                r"""Access the stats for spaced practice topics.

                :return: the list of book section stats selected by Tutor in
                    the assignment
                :rtype: list(:py:class:`~pages.tutor.review \
                                        .Metrics.Sidebar.Stats.BookSection`)

                """
                return [self.BookSection(self, section)
                        for section
                        in self.find_elements(
                            *self._spaced_practice_topics_locator)]

            class BookSection(Region):
                """The stats for a single book section."""

                _book_section_correct_percentage_locator = (
                    By.CSS_SELECTOR, '[type=correct] span')
                _book_section_incorrect_percentage_locator = (
                    By.CSS_SELECTOR, '[type=incorrect] span')
                _book_section_number_locator = (
                    By.CSS_SELECTOR, '.text-success')
                _book_section_title_locator = (
                    By.CSS_SELECTOR, 'strong')

                @property
                def correct(self) -> str:
                    """Return the percentage who responded correctly.

                    .. note:
                       100% includes ' correct' or ' incorrect' while other
                       percentages are just the percentage

                    :return: the percentage of questions from the section that
                        were answered correctly
                    :rtype: str

                    """
                    return self.find_element(
                        *self._book_section_correct_percentage_locator).text

                @property
                def incorrect(self):
                    """Return the percentage who responded incorrectly.

                    .. note:
                       100% includes ' correct' or ' incorrect' while other
                       percentages are just the percentage

                    :return: the percentage of questions from the section that
                        were answered incorrectly
                    :rtype: str

                    """
                    return self.find_element(
                        *self._book_section_incorrect_percentage_locator).text

                @property
                def section_number(self) -> str:
                    """Return the section number.

                    :return: the book section number
                    :rtype: str

                    """
                    return self.find_element(
                        *self._book_section_number_locator).text

                @property
                def section_title(self) -> str:
                    """Return the section title.

                    :return: the book section title
                    :rtype: str

                    """
                    return self.find_element(
                        *self._book_section_title_locator).text

        class Tab(Region):
            """A course section or period selection tab."""

            _section_name_locator = (By.CSS_SELECTOR, '.tab-item-period-name')
            _tab_link_locator = (By.CSS_SELECTOR, 'a')

            @property
            def is_selected(self) -> bool:
                """Return True if the course section is currently selected.

                :return: ``True`` if the course section is active
                :rtype: bool

                """
                return 'active' in self.root.get_attribute('class')

            @property
            def name(self) -> str:
                """Return the course section name or title.

                :return: the course section name or title
                :rtype: str

                """
                return self.find_element(*self._section_name_locator).text

            def select(self) -> Metrics:
                """Click on the course section tab to display its review.

                :return: the assignment metrics for this course section or
                    period
                :rtype: :py:class:`~pages.tutor.review.Metrics`

                """
                tab = self.find_element(*self._tab_link_locator)
                Utility.click_option(self.driver, element=tab)
                return go_to_(
                    Metrics(self.driver, base_url=self.page.page.base_url))

    class Toolbar(Region):
        """The assignment navigation toolbar."""

        _assignment_section_breadcrumb_locator = (
            By.CSS_SELECTOR, '[class*="Steps-sc"]')
        _assignment_title_locator = (By.CSS_SELECTOR, '[class*=Title]')
        _back_to_previous_screen_locator = (By.CSS_SELECTOR, '.btn-default')

        @property
        def assignment_name(self) -> str:
            """Return the assignment title or name.

            :return: the assignment title or name
            :rtype: str

            """
            return self.find_element(*self._assignment_title_locator).text

        def back_to_calendar(self) -> Union[Calendar, Scores]:
            """Click the 'Back to Calendar' button.

            :return: the instructor's calendar or the scores page
            :rtype: :py:class:`~pages.tutor.calendar.Calendar` or
                :py:class:`~pages.tutor.scores.Scores`

            """
            button = self.find_element(*self._back_to_previous_screen_locator)
            destination = Calendar if 'calendar' in button.text else Scores
            Utility.click_option(self.driver, element=button)
            return go_to_(
                destination(self.driver, base_url=self.page.base_url))

        def back_to_scores(self) -> Scores:
            """Click the 'Back to Scores' button.

            :return: the instructor's calendar or the scores page
            :rtype: :py:class:`~pages.tutor.calendar.Calendar` or
                :py:class:`~pages.tutor.scores.Scores`

            """
            return self.back_to_calendar()

        @property
        def steps(self) -> List[Metrics.Toolbar.Step]:
            """Access the assignment book section jump links.

            :return: the list of book section links in the assignment
            :rtype: list(:py:class:`~pages.tutor.review.Metrics.Toolbar.Step`)

            """
            return [self.Step(self, breadcrumb)
                    for breadcrumb
                    in self.find_elements(
                        *self._assignment_section_breadcrumb_locator)]

        class Step(Region):
            """An assignment navigation jump link."""

            # TODO: toolbar currently missing from the page after load
