"""An assessment preview card."""

from __future__ import annotations

from time import sleep
from typing import Dict, List, Tuple, Union

from pypom import Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.tutor.base import TutorBase
from pages.tutor.reference import ReferenceBook
from pages.web.errata import ErrataForm
from utils.tutor import TutorException
from utils.utilities import Utility, go_to_

ByLocator = Tuple[str, str]
Tags = Dict[str, str]


class Assessment(Region):
    """An assessment preview card."""

    _add_question_locator = (By.CSS_SELECTOR, '.include')
    _remove_question_locator = (By.CSS_SELECTOR, '.exclude')
    _question_details_locator = (By.CSS_SELECTOR, '.details')
    _question_details_root_locator = (By.CSS_SELECTOR, '.exercise-details')
    _multipart_badge_locator = (By.CSS_SELECTOR, '.mpq')
    _interactive_badge_locator = (By.CSS_SELECTOR, '.interactive')
    _multipart_stimulus_locator = (By.CSS_SELECTOR, '.stimulus')
    _assessment_question_locator = (By.CSS_SELECTOR, '.openstax-question')
    _assessment_tag_locator = (By.CSS_SELECTOR, '.exercise-tag')

    def _modify_assessment(self, locator: ByLocator, no_return: bool = False) \
            -> Union[TutorBase, None]:
        """Add or remove an assessment.

        :param locator: the button locator
        :type locator: tuple(str, str)
        :return: the associated region parent page
        :rtype: :py:class:`~pages.tutor.base.TutorBase` or None

        :noindex:

        """
        button = self.find_element(*locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.5)
        if not no_return:
            return self.page

    def add_question(self) -> TutorBase:
        """Add an assessment to an assignment.

        :return: the associated page
        :rtype: :py:class:`~pages.tutor.TutorBase`

        """
        return self._modify_assessment(locator=self._add_question_locator)

    # a shortcut for the Question Library re-include assessment button
    reinclude_question = add_question

    def remove_question(self) -> TutorBase:
        """Remove the assessment from an assignment.

        :return: the associated page
        :rtype: :py:class:`~pages.tutor.TutorBase`

        """
        return self._modify_assessment(locator=self._remove_question_locator)

    # a shortcut for the Question Library exclude assessment button
    exclude_question = remove_question

    def question_details(self) -> Union[DetailedAssessment, None]:
        """Click on the 'Question details' button.

        :return: the detailed assessment view for the selected exercise
        :rtype: :py:class:`DetailedAssessment`

        """
        try:
            self._modify_assessment(locator=self._question_details_locator,
                                    no_return=True)
            details_root = self.find_element(
                *self._question_details_root_locator)
            return DetailedAssessment(self.page, details_root)
        except NoSuchElementException:
            return

    @property
    def is_multipart(self) -> bool:
        """Return True if the assessment has multiple questions.

        :return: ``True`` if the assessment contains more than one part or
            ``False`` if it is a basic, one response question
        :rtype: bool

        """
        return bool(self.find_elements(*self._multipart_badge_locator))

    @property
    def is_interactive(self) -> bool:
        """Return True if the assessment contains an interactive component.

        :return: ``True`` if there is an interactive component within the
            assessment, otherwise ``False``
        :rtype: bool

        """
        return bool(self.find_elements(*self._interactive_badge_locator))

    @property
    def stimulus(self) -> str:
        """Return the multipart stimulus if it exists.

        :return: the multipart introductory stimulus
        :rtype: str

        """
        try:
            return (self.find_element(*self._multipart_stimulus_locator)
                    .get_attribute('textContent'))
        except NoSuchElementException:
            return ''

    @property
    def questions(self) \
            -> Union[Assessment.Question, List[Assessment.Question]]:
        """Access the assessment question(s).

        :return: a single question or a list of questions
        :rtype: :py:class:`Assessment.Question` or
            list(:py:class:`Assessment.Question`)

        """
        questions = self.find_elements(*self._assessment_question_locator)
        if len(questions) == 1:
            return self.Question(self, questions[0])
        return [self.Questions(self, part) for part in questions]

    @property
    def tags(self) -> Tags:
        """Return a dictionary of tag and value pairs.

        :return: the group of tag key:value pairs
        :rtype: dict(str, str)

        """
        tags = {}
        for tag in self.find_elements(*self._assessment_tag_locator):
            key, value = tag.split(':', 1)
            tags[key] = value
        return tags

    class Question(Region):
        """An assessment question."""

        _question_stem_locator = (By.CSS_SELECTOR, '.question-stem')
        _has_image_locator = (By.CSS_SELECTOR, '.question-stem img')
        _question_answer_locator = (By.CSS_SELECTOR, '.openstax-answer')
        _detailed_solution_locator = (By.CSS_SELECTOR, '.solution')

        @property
        def question(self) -> bool:
            """Return the question stem.

            .. note::

               The question stem content may be confusing if the stem includes
               MathML or LaTeX

            :return: the text content for the question stem
            :rtype: str

            """
            return (self.find_element(*self._question_stem_locator)
                    .get_attribute('textContent'))

        @property
        def has_image(self) -> bool:
            """Return True if the question stem contains an image.

            :return: ``True`` if the question stem contains an image, otherwise
                ``False``
            :rtype: bool

            """
            return bool(self.find_elements(*self._has_image_locator))

        @property
        def image_text(self) -> str:
            """Return the image alt text.

            :return: the image alt text (new line-separated) if the answer has
                one or more images
            :rtype: str

            """
            if self.has_image:
                return '\n'.join(list(
                    [image.get_attribute('alt')
                     for image
                     in self.find_elements(*self._has_image_locator)]))
            return ''

        @property
        def answers(self) -> List[Assessment.Question.Answer]:
            """Access the question answer options.

            :return: the list of possible answers
            :rtype: list(:py:class:`~Assessment.Question.Answer`)

            """
            return [self.Answer(self, option)
                    for option
                    in self.find_elements(*self._question_answer_locator)]

        @property
        def detailed_solution(self) -> str:
            """Return the question's detailed solution.

            :return: the detailed solution for the question
            :rtype: str

            """
            solution = self.find_elements(*self._detailed_solution_locator)
            if solution:
                return solution[0].get_attribute('textContent')
            return ''

        class Answer(Region):
            """An answer option."""

            _is_correct_locator = (By.CSS_SELECTOR, '.correct-incorrect svg')
            _answer_letter_locator = (By.CSS_SELECTOR, '.answer-letter')
            _answer_content_locator = (By.CSS_SELECTOR, '.answer-content')
            _has_image_locator = (By.CSS_SELECTOR, '.answer-content img')
            _feedback_content_locator = (
                By.CSS_SELECTOR, '.question-feedback-content')

            @property
            def is_correct(self) -> bool:
                """Return True if the answer is correct for the question.

                :return: ``True`` if the answer is correct, otherwise ``False``
                :rtype: bool

                """
                return bool(self.find_elements(*self._is_correct_locator))

            @property
            def letter(self) -> str:
                """Return the answer letter.

                :return: the answer letter
                :rtype: str

                """
                return self.find_element(*self._answer_letter_locator).text

            @property
            def answer(self) -> str:
                """Return the answer content.

                .. note::

                   The answer content may be confusing if the answer includes
                   MathML or LaTeX

                :return: the text content for the answer
                :rtype: str

                """
                return (self.find_element(*self._answer_content_locator)
                        .get_attribute('textContent'))

            @property
            def has_image(self) -> bool:
                """Return True if the answer contains an image.

                :return: ``True`` if the answer contains an image, otherwise
                    ``False``
                :rtype: bool

                """
                return bool(self.find_elements(*self._has_image_locator))

            @property
            def image_text(self) -> str:
                """Return the image alt text.

                :return: the image alt text if the answer has an image
                :rtype: str

                """
                if self.has_image:
                    return (self.find_element(*self._has_image_locator)
                            .get_attribute('alt'))
                return ''


class DetailedAssessment(Assessment):
    """A detailed view of a single assessment."""

    _preview_feedback_toggle_locator = (
        By.CSS_SELECTOR, '.feedback-on , .feedback-off')
    _report_an_error_button_locator = (
        By.CSS_SELECTOR, '.report-error')
    _back_to_card_view_button_locator = (
        By.CSS_SELECTOR, '.show-cards')
    _previous_assessment_arrow_locator = (
        By.CSS_SELECTOR, '.paging-control.prev')
    _next_assessment_arrow_locator = (
        By.CSS_SELECTOR, '.paging-control.next')

    def preview_feedback(self) -> DetailedAssessment:
        """Click on the 'Preview Feedback' button.

        Toggle between showing answer feedback and a detailed solution, if
        available, and hiding them.

        :return: the detailed assessment pane
        :rtype: :py:class:`DetailedAssessment`

        """
        self._modify_assessment(locator=self._preview_feedback_toggle_locator,
                                no_return=True)
        return self

    @property
    def feedback_is_shown(self) -> bool:
        """Return True if feedback is available for display.

        .. note::

           Not all assessments have feedback or a detailed solution.

        :return: the detailed assessment pane
        :rtype: :py:class:`DetailedAssessment`

        """
        toggle = self.find_element(*self._preview_feedback_toggle_locator)
        return 'Hide' in toggle.get_attribute('textContent')

    def suggest_a_correction(self) -> ErrataForm:
        """Click on the 'Suggest a correction' button.

        Report an error on OpenStax.org.

        :return: the errata form on openstax.org
        :rtype: :py:class:`~pages.web.errata.ErrataForm`

        """
        button = self.find_element(*self._report_an_error_button_locator)
        Utility.switch_to(self.driver, element=button)
        return go_to_(ErrataForm(self.driver))


class QuestionBase(Region):
    """Shared assessment resources for student responses."""

    _question_stem_locator = (By.CSS_SELECTOR, '[class*=QuestionStem]')
    _answer_button_locator = (By.CSS_SELECTOR, '.btn-primary')
    _exercise_id_locator = (By.CSS_SELECTOR, '.exercise-identifier-link')
    _suggest_a_correction_link_locator = (By.CSS_SELECTOR, '[href*=errata]')
    _view_book_section_link_locator = (By.CSS_SELECTOR, '.reference')
    _book_section_number_locator = (By.CSS_SELECTOR, '.chapter-section')
    _book_section_title_locator = (By.CSS_SELECTOR, '.title')

    @property
    def step_id(self) -> str:
        """Return the step identification string.

        :return: the step ID number
        :rtype: str

        """
        return self.root.get_attribute('data-task-step-id')

    @property
    def stem(self) -> str:
        """Return the question stem.

        :return: the question stem
        :rtype: str

        """
        return (self.find_element(*self._question_stem_locator)
                .get_attribute('textContent'))

    @property
    def answer_button(self) -> WebElement:
        """Return the 'Answer' button element.

        :return: the answer button
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._answer_button_locator)

    @property
    def exercise_id(self) -> str:
        """Return the Exercises ID.

        :return: the Exercises assessment ID and version
        :rtype: str

        """
        return self.find_element(*self._exercise_id_locator).text.split()[1]

    def suggest_a_correction(self) -> ErrataForm:
        """Click on the 'Suggest a correction' link.

        :return: the OpenStax.org errata form
        :rtype: :py:class:`~pages.web.errata.ErrataForm`

        """
        link = self.find_element(*self._suggest_a_correction_link_locator)
        Utility.switch_to(self.driver, element=link)
        sleep(1)
        return go_to_(ErrataForm(self.driver))

    def view_reference(self) -> ReferenceBook:
        """Click on the associated book section name.

        :return: the reference book showing the requested chapter section
        :rtype: :py:class:`~pages.tutor.reference.RefernceBook`

        """
        link = self.find_element(*self._view_book_section_link_locator)
        Utility.switch_to(self.driver, element=link)
        sleep(1)
        return go_to_(ReferenceBook(self.driver, base_url=self.page.base_url))

    @property
    def chapter_section(self) -> str:
        """Return the book chapter and section number for the associated step.

        :return: the book chapter and section number containing the question
            explanation
        :rtype: str

        """
        return self.find_element(*self._chapter_number_locator).text

    @property
    def section_title(self) -> str:
        """Return the book section title for the associated step.

        :return: the title for the book section containing the question
            explanation
        :rtype: str

        """
        return self.find_element(*self._book_section_title_locator).text


class FreeResponse(QuestionBase):
    """A free response step for an assessment."""

    _free_response_box_locator = (By.CSS_SELECTOR, 'textarea')

    @property
    def free_response(self) -> str:
        """Return the current free response text.

        :return: the current free response answer text
        :rtype: str

        """
        return (self.find_element(*self._free_response_box_locator)
                .get_attribute('textContent'))

    @free_response.setter
    def free_response(self, answer) -> None:
        """Send the free response answer to the text box.

        Use the javascript value assignment just in case we need to overwrite
        a previous answer.

        :return: None

        """
        box = self.find_element(*self._free_response_box_locator)
        self.driver.execute_script(f'arguments[0].value = "{answer}";', box)


class MultipleChoice(QuestionBase):
    """A mutiple choice response step for an assessment."""

    _question_answer_locator = (By.CSS_SELECTOR, '.openstax-answer')

    @property
    def answers(self) -> List[MultipleChoice.Answer]:
        r"""Access the available multiple choice answers.

        :return: the list of available multiple choice answers
        :rtype: \
            list(:py:class:`~regions.tutor.assessment.MultipleChoice.Answer)

        """
        return [self.Answer(self, option)
                for option
                in self.find_elements(*self._question_answer_locator)]

    class Answer(Region):
        """A multiple choice answer."""

        _answer_button_locator = (By.CSS_SELECTOR, '.answer-input-box')
        _answer_letter_locator = (By.CSS_SELECTOR, '.answer-letter')
        _answer_content_locator = (By.CSS_SELECTOR, '.answer-content')

        @property
        def answer_id(self) -> str:
            """Return the answer ID.

            :return: the answer ID
            :rtype: str

            """
            return (self.find_element(*self._answer_button_locator)
                    .get_attribute('id'))

        @property
        def letter(self) -> str:
            """Return the answer letter.

            :return: the answer letter
            :rtype: str

            """
            return self.find_element(*self._answer_letter_locator).text

        @property
        def answer(self) -> str:
            """Return the answer content.

            :return: the answer content
            :rtype: str

            """
            return (self.find_element(*self._answer_content_locator)
                    .get_attribute('textContent'))

        def select(self) -> None:
            """Click on the button to select the answer.

            :return: None

            """
            button = self.find_element(*self._answer_button_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.5)


class MultipartQuestion(Region):
    """A multi-part assessment with two or more questions."""

    _question_locator = (By.CSS_SELECTOR, '[class*=MultipartGroup] > div')
    _is_free_response_locator = (By.CSS_SELECTOR, '[class*=FreeResponse]')
    _is_multiple_choice_locator = (
                                By.CSS_SELECTOR, '[class*=ExerciseQuestion]')

    @property
    def questions(self) -> List[QuestionBase]:
        """Access the list of questions.

        :return: the list of questions within the multi-part assessment
        :rtype: list(:py:class:`~regions.tutor.assessment.QuestionBase`)

        :raises :py:class:`~utils.tutor.TutorException`: if a task step doesn't
            match a free response or multiple choice question or if no
            assessment segments are found

        """
        parts = []
        for question in self.find_elements(*self._question_locator):
            if question.find_elements(*self._is_free_response_locator):
                parts.append(FreeResponse(self, question))
            elif question.find_elements(*self._is_multiple_choice_locator):
                parts.append(MultipleChoice(self, question))
            else:
                tag = question.get_attribute('data-task-step-id')
                raise TutorException(
                    f'Unknown assessment type in task step {tag}')
        if not parts:
            raise TutorException('No multi-part steps found in "{0}"'
                                 .format(self.driver.current_url))
        return parts
