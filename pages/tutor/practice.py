"""An OpenStax Tutor Beta practice session."""

from __future__ import annotations

from time import sleep
from typing import List, Union

from pypom import Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.tutor.course import StudentCourse
from pages.tutor.performance import PerformanceForecast
from pages.tutor.task import Homework
from pages.web.errata import ErrataForm
from utils.tutor import TutorException
from utils.utilities import Utility, go_to_

# -------------------------------------------------------- #
# Javascript page requests
# -------------------------------------------------------- #

# get the modal and tooltip root that is a neighbor of the React root element
GET_ROOT = 'return document.querySelector("[role={0}]");'


# -------------------------------------------------------- #
# Tooltips and Dialog boxes
# -------------------------------------------------------- #

class ButtonTooltip(Region):
    """The assessment explanation tooltips."""

    _explanation_locator = (By.CSS_SELECTOR, 'p , .tooltip-inner')

    @property
    def root(self) -> WebElement:
        """Locate the tooltip trunk.

        :return: the root element for a tooltip
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.driver.execute_script(GET_ROOT.format('tooltip'))

    @property
    def description(self) -> str:
        """Return the tooltip content.

        :return: the tooltip text content
        :rtype: str

        """
        return ' '.join(list(
            [line.get_attribute('textContent')
             for line in self.find_elements(*self._explanation_locator)]))


# -------------------------------------------------------- #
# Practice page
# -------------------------------------------------------- #

class Practice(Homework):
    """A practice session."""

    _body_locator = (By.CSS_SELECTOR, 'body')
    _exercise_breadcrumb_locator = (By.CSS_SELECTOR, '.breadcrumb-exercise')
    _personalized_badge_locator = (By.CSS_SELECTOR, '.personalized')
    _personalized_tooltip_locator = (By.CSS_SELECTOR, '.personalized svg')
    _question_stimulus_locator = (By.CSS_SELECTOR, '.exercise-stimulus')
    _question_stem_locator = (
        By.CSS_SELECTOR, '.question-stem , [class*=QuestionStem]')
    _free_response_box_locator = (By.CSS_SELECTOR, 'textarea')
    _answer_button_locator = (By.CSS_SELECTOR, '.btn-primary')
    _exercise_id_locator = (By.CSS_SELECTOR, '.exercise-identifier-link')
    _suggest_a_correction_link_locator = (
        By.CSS_SELECTOR, '.exercise-identifier-link a')
    _book_section_locator = (By.CSS_SELECTOR, '.chapter-section')
    _book_section_title_locator = (By.CSS_SELECTOR, '.title')
    _view_book_section_link_locator = (By.CSS_SELECTOR, '.reference')
    _debug_information_locator = (
        By.CSS_SELECTOR, '.visible-when-debugging li')
    _footer_root_locator = (
        By.CSS_SELECTOR, '.tutor-navbar:not(:first-child)')

    @property
    def loaded(self) -> bool:
        """Return True when all loading messages are done.

        :return: ``True`` if no loading message is found
        :rtype: bool

        """
        body_source = (self.find_element(*self._body_locator)
                       .get_attribute('outerHTML'))
        loaded = ('Loading' not in body_source and
                  'is-loading' not in body_source)
        if loaded:
            sleep(1)
        return loaded

    @property
    def exercises(self) -> int:
        """Return the number of practice assessments.

        :return: the number of assessments in this practice session
        :rtype: int

        """
        return len(self.find_elements(*self._exercise_breadcrumb_locator))

    @property
    def is_personalized(self) -> bool:
        """Return True if the assessment is personalized to the user.

        :return: ``True`` if the assessment is personalized, otherwise
            ``False``
        :rtype: bool

        """
        return bool(self.find_elements(*self._personalized_badge_locator))

    @property
    def personalized_tooltip(self) -> ButtonTooltip:
        """Hover over the personalized badge info icon to show the help text.

        :return: the personalized assessment tooltip
        :rtype: :py:class:`~pages.tutor.practice.ButtonTooltip`

        """
        # TODO: hover over the icon and return the text content of the tooltip

    @property
    def stimulus(self) -> str:
        """Return the assessment stimulus if present.

        :return: the assessment stimulus if present or an empty string if not
        :rtype: str

        """
        try:
            return (self.find_element(*self._question_stimulus_locator)
                    .get_attribute('textContent'))
        except NoSuchElementException:
            return ''

    @property
    def stem(self) -> str:
        """Return the question stem content.

        :return: the question stem text content
        :rtype: str

        """
        return (self.find_element(*self._question_stem_locator)
                .get_attribute('textContent'))

    @property
    def has_free_response(self) -> bool:
        """Return True if the assessment has a free response text box.

        :return: ``True`` if a free response textbox is present, else ``False``
        :rtype: bool

        """
        return bool(self.find_elements(*self._free_response_box_locator))

    @property
    def question(self) \
            -> Union[Practice.MultipleChoice, Practice.FreeResponse]:
        """Access the step-type features of the assessment.

        :return: the inner assessment function - either multiple choice or a
            free response
        :rtype: :py:class:`~pages.tutor.practice.Practice.MultipleChoice` or
            :py:class:`~pages.tutor.practice.Practice.FreeResponse`

        """
        if self.has_free_response:
            return self.FreeResponse(self)
        return self.MultipleChoice(self)

    @property
    def answer_enabled(self) -> bool:
        """Return True if the 'Answer' button is enabled.

        :return: ``True`` if the Answer button is clickable, otherwise
            ``False``
        :rtype: bool

        """
        answer_button = self.find_element(*self._answer_button_locator)
        return self.driver.execute_script('return !arguments[0].disabled;',
                                          answer_button)

    def answer(self) -> Practice:
        """Submit the answer.

        :return: the next step in the practice session
        :rtype: :py:class:`~pages.tutor.practice.Practice`

        :raises :py:class:`~utils.tutor.TutorException`: if the answer button
            is disabled

        """
        if not self.answer_enabled:
            raise TutorException("The answer button is currently disabled; "
                                 "next step not available")
        button = self.find_element(*self._answer_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(1)
        return self

    @property
    def exercise_id(self) -> str:
        """Return the exercise identification number for the assessment.

        :return: the Exercise ID number and version
        :rtype: str

        """
        return self.find_element(*self._exercise_id_locator).split()[1]

    def suggest_a_correction(self) -> ErrataForm:
        """Click the 'Suggest a correction' link.

        :return: the errata submission form for the course book
        :rtype: :py:class:`~pages.web.errata.ErrataForm`

        """
        link = self.find_element(*self._suggest_a_correction_link_locator)
        Utility.switch_to(self.driver, element=link)
        return go_to_(ErrataForm(self.driver))

    @property
    def section(self) -> str:
        """Return the assessment's associated chapter section.

        :return: the chapter and section containing the answer to the current
            assessment
        :rtype: str

        """
        return self.find_element(*self._book_section_locator).text

    @property
    def section_title(self) -> str:
        """Return the assessment's associated chapter section title.

        :return: the title for the book section containing the answer to the
            current assessment
        :rtype: str

        """
        return self.find_element(*self._book_section_title_locator).text

    @property
    def footer(self) -> Practice.Footer:
        """Access the practice assignment footer.

        :return: the footer region
        :rtype: :py:class:`~pages.tutor.practice.Practice.Footer`

        """
        footer_root = self.find_element(*self._footer_root_locator)
        return self.Footer(self, footer_root)

    class Footer(Region):
        """The practice session footer."""

        _title_locator = (By.CSS_SELECTOR, '.left-side-controls div')
        _back_to_page_locator = (By.CSS_SELECTOR, '.btn-default')

        @property
        def title(self) -> str:
            """Return the practice session title.

            :return: the practice session title
            :rtype: str

            """
            return (self.find_element(*self._title_locator)
                    .get_attribute('textContent'))

        def back_to(self) -> Union[StudentCourse, PerformanceForecast]:
            """Click the 'Back to ...' button.

            Clicking the button will return the student to the page they
            followed to get to the practice session; that may be either the
            student course page or the student's performance forecast.

            :return: the student course page or the performance forecast
            :rtype: :py:class:`~pages.tutor.course.StudentCourse` or
                :py:class:`~pages.tutor.performance.PerformanceForecast`

            """
            button = self.find_element(*self._back_to_page_locator)
            go_to_guide = button.get_attribute('href').endswith('guide')
            Utility.click_option(self.driver, element=button)
            if go_to_guide:
                return go_to_(
                    PerformanceForecast(self.driver,
                                        base_url=self.page.base_url))
            return go_to_(StudentCourse(self.driver,
                                        base_url=self.page.base_url))

    class FreeResponse(Region):
        """A free response assessment step."""

        _nudge_shown_locator = (By.CSS_SELECTOR, '[class*=NudgeMessage]')
        _submit_this_answer_locator = (
                                By.CSS_SELECTOR, '.related-content-link ~ a')

        @property
        def free_response(self) -> str:
            """Return the current content of the free response text box.

            :return: the free response content
            :rtype: str

            """
            if not self.has_free_response:
                return ''
            return (self.find_element(*self.page._free_response_box_locator)
                    .get_attribute('textContent'))

        @free_response.setter
        def free_response(self, answer: str) -> None:
            """Send the answer to the free response text box.

            :param str answer: the answer text to send to the free response
                text box
            :return: None

            """
            if not self.has_free_response:
                return
            self.find_element(*self._free_response_box_locator) \
                .send_keys(answer)

        @property
        def nudge_shown(self) -> bool:
            """Return True if the answer validation message is displayed.

            If the nudge message is displayed, then the free response failed
            answer validation.

            :return: ``True`` if the validation message is displayed, otherwise
                ``False``

            """
            return bool(self.find_elements(*self._nudge_shown_locator))

        def submit_this_answer(self) -> Practice:
            """Submit the invalid free response.

            :return: the multiple choice answer step for the assessment
            :rtype: :py:class:`~pages.tutor.practice.Practice`

            """
            link = self.find_element(*self._submit_this_answer_locator)
            Utility.click_option(self.driver, element=link)
            sleep(1)
            return self

    class MultipleChoice(Region):
        """A multiple choice assessment step."""

        _instructions_locator = (By.CSS_SELECTOR, '.instructions')
        _answer_option_locator = (By.CSS_SELECTOR, '.openstax-answer')

        @property
        def instructions(self) -> str:
            """Return the assessment instructions.

            :return: the assessment instructions
            :rtype: str

            """
            return self.find_element(*self._instructions_locator).text

        @property
        def answers(self) -> List[Practice.MultipleChoice.Answer]:
            r"""Access the multiple choice answers.

            :return: the list of available answer options
            :rtype: list(:py:class:`~pages.tutor.practice. \
                         Practice.MultipleChoice.Answer`)

            """
            return [self.Answer(self, option)
                    for option
                    in self.find_elements(*self._answer_option_locator)]

        class Answer(Region):
            """An assessment answer choice."""

            _question_id_locator = (By.CSS_SELECTOR, '[type=radio]')
            _answer_letter_locator = (By.CSS_SELECTOR, 'button')
            _answer_content_locator = (By.CSS_SELECTOR, '.answer-content')
            _is_selected_status_locator = (By.CSS_SELECTOR, 'section')

            @property
            def question_id(self) -> int:
                """Return the assessment question identification number.

                :return: the question ID number
                :rtype: int

                """
                return int(self.find_element(*self._question_id_locator)
                           .get_attribute('id')
                           .split('-')[0])

            @property
            def letter(self) -> str:
                """Return the answer option letter.

                :return: the answer letter
                :rtype: str

                """
                return self.find_element(*self._answer_letter_locator).text

            @property
            def answer(self) -> str:
                """Return the answer content.

                :return: the answer content text
                :rtype: str

                """
                return (self.find_element(*self._answer_content_locator)
                        .get_attribute('textContent'))

            def select(self) -> None:
                """Click on the answer to select it.

                :return: None

                """
                button = self.find_element(*self._answer_letter_locator)
                Utility.click_option(self.driver, element=button)
                sleep(0.5)

            @property
            def is_selected(self) -> bool:
                """Return True if the answer option is currently selected.

                :return: ``True`` if the answer is selected, otherwise
                    ``False``
                :rtype: bool

                """
                status = self.find_element(*self._is_selected_status_locator)
                return 'answer-checked' in status.get_attribute('class')

    class Nav(Region):
        """The practice session assessment navigation."""

        _root_locator = (By.CSS_SELECTOR, '[class*=SecondaryToolbar]')
        _step_icon_locator = (By.CSS_SELECTOR, '.breadcrumb-exercise')
        _completion_locator = (By.CSS_SELECTOR, '.breadcrumb-end')

        @property
        def steps(self) -> List[Practice.Nav.Icon]:
            """Access the practice session steps.

            :return: the list of available assessment steps
            :rtype: list(:py:class:`~Practice.Nav.Icon`)

            """
            return [self.Icon(self, step)
                    for step
                    in self.find_elements(*self._step_icon_locator)]

        @property
        def completion(self) -> Practice.Nav.Icon:
            """Access the completion/final step.

            :return: the completion step
            :rtype: :py:class:`~Practice.Nav.Icon`

            """
            return self.Icon(self,
                             self.find_element(*self._completion_locator))

        class Icon(Region):
            """A practice session step icon."""

            @property
            def is_actice(self) -> bool:
                """Return True if this step is currently active.

                :return: ``True`` if the step is active and displayed,
                    otherwise ``False``
                :rtype: bool

                """
                return 'active' in self.root.get_attribute('class')

            @property
            def position(self) -> int:
                """Return the step's position.

                :return: the step's positon within the practice session
                :rtype: int

                """
                return int(self.root.get_attribute('data-step-index'))

            @property
            def step_id(self) -> int:
                """Return the step identification number.

                :return: the step ID number
                :rtype: int

                """
                return int(self.root.get_attribute('data-step-id'))

            def select(self) -> Practice:
                """Click the icon to view the practice step.

                :return: the practice session with the selected step in the
                    practice window
                :rtype: :py:class:`~pages.tutor.practice.Practice`

                """
                Utility.click_option(self.driver, element=self.root)
                sleep(1)
                return self.page.page
