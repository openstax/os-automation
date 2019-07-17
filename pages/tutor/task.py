"""Student assignment tasks.

Externals, Events, Homeworks, and Readings

"""

from __future__ import annotations

from time import sleep
from typing import Dict, List, Union

from pypom import Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from pages.tutor.base import TutorBase
from pages.tutor.course import StudentCourse
from pages.tutor.reference import ReferenceBook
from regions.tutor.assessment import FreeResponse, MultipleChoice
from regions.tutor.print_preview import PrintPreview
from utils.tutor import Tutor, TutorException
from utils.utilities import Utility, go_to_

COMPUTED_STYLE = ('return window.getComputedStyle(document.querySelector('
                  '"{selector}")).{property} == "{expected_value}";')
TutorHighlight = Dict[str, List[WebElement]]


class Assignment(TutorBase):
    """The shared assignment features."""

    _internal_loading_locator = (
        By.CSS_SELECTOR, 'svg title')
    _joyride_root_locator = (
        By.CSS_SELECTOR, '.joyride')
    _tooltip_button_locator = (
        By.CSS_SELECTOR, '[class*="--primary"]')
    _assignment_nav_bar_locator = (
        By.CSS_SELECTOR, '[class*=SecondaryToolbar]')
    _assignment_body_locator = (
        By.CSS_SELECTOR, '[class*="Content-sc-"]')
    _assignment_footer_locator = (
        By.CSS_SELECTOR, '.tutor-navbar')
    _assignment_type_locator = (
        By.CSS_SELECTOR, '.task-screen')
    _debug_information_locator = (
        By.CSS_SELECTOR, '.visible-when-debugging li')

    _document_loading_selector = '.loading-animation'
    _step_loading_selector = '[aria-labelledby*=Loading]'

    @property
    def loaded(self) -> bool:
        """Return True when the various loading panes are gone.

        :return: ``True`` when the various loading message panes/SVGs are not
            found
        :rtype: bool

        """
        page_load = self.driver.execute_script(
            'return document.querySelector("{document} , {step}");'
            .format(document=self._document_loading_selector,
                    step=self._step_loading_selector))
        joyride = self.find_elements(*self._joyride_root_locator)
        tooltip = Utility.has_children(joyride[0]) if joyride else ''
        # quit if no page loader is present or a tooltip is found
        if not page_load or tooltip:
            return True
        # otherwise check for a reading panel loader
        try:
            internal_load = self.find_element(*self._internal_loading_locator)
            loading_text = internal_load.get_attribute('textContent')
            return 'Loading' not in loading_text
        except NoSuchElementException:
            return True

    @property
    def assignment_type(self) -> str:
        """Return the assignment type.

        :return: the assignment type
        :rtype: str

        """
        task_type = (self.find_element(*self._assignment_type_locator)
                     .get_attribute('class'))
        if Tutor.EVENT in task_type:
            return Tutor.EVENT
        elif Tutor.EXTERNAL in task_type:
            return Tutor.EXTERNAL
        elif Tutor.HOMEWORK in task_type:
            return Tutor.HOMEWORK
        return Tutor.READING

    @property
    def nav(self) -> Union[Assignment.Nav, None]:
        """Access the assignment navigaton bar.

        :return: the assignment navigation bar for readings and homeworks
        :rtype: :py:class:`~pages.tutor.task.Assignment.Nav` or None

        """
        assignment_type = self.assignment_type
        if assignment_type == Tutor.EVENT or assignment_type == Tutor.EXTERNAL:
            return
        nav_root = self.find_element(*self._assignment_nav_bar_locator)
        return self.Nav(self, nav_root)

    @property
    def body(self) -> Assignment.Content:
        """Access the assignment content and assessments.

        :return: the region housing the assignment content and assessments
        :rtype: :py:class:`~pages.tutor.task.Assignment.Content`

        """
        body_root = self.find_element(*self._assignment_body_locator)
        if self.assignment_type == Tutor.HOMEWORK:
            return self.Content(self, body_root).pane
        return self.Content(self, body_root)

    @property
    def footer(self) -> Assignment.Footer:
        """Access the assignment footer content.

        :return: the assignment footer
        :rtype: :py:class:`~pages.tutor.task.Assignment.Footer`

        """
        footer_root = self.find_element(*self._assignment_footer_locator)
        return self.Footer(self, footer_root)

    @property
    def debug_information(self) -> Dict[str, str]:
        """Return the debugging information for the current page.

        :return: the group of debugging keys and values for the current page,
            task, or assessment
        :rtype: dict(str, str)

        """
        data = {}
        lines = self.find_elements(*self._debug_information_locator)
        for line in lines:
            key, value = line.split(':', 1)
            stripped_value = value.strip()
            if stripped_value:  # it's not empty
                data[line.strip()] = stripped_value
        return data

    def clear_training_wheels(self) -> None:
        """Clear any joyride modals.

        :return: None

        """
        sleep(0.5)
        for attempt in range(6):
            tip = self.find_elements(*self._joyride_root_locator)
            if tip and Utility.has_children(tip[0]):
                button = self.driver.execute_script(
                    'return document.querySelector("[class*=\'--primary\']");')
                if button:
                    if attempt % 2 == 0:
                        Utility.click_option(self.driver, element=button)
                    else:
                        button.send_keys(Keys.RETURN)
                sleep(1)
                tip = self.find_elements(*self._joyride_root_locator)
            sleep(0.5)

    class Content(Region):
        """A placeholder for the assignment body."""

        def __init__(self):
            """Override the initialization to toss an implementation error."""
            raise NotImplementedError("Must use an individual assignment type,"
                                      " not Assignment")

    class Footer(Region):
        """The assignment footer."""

        _assignment_title_locator = (By.CSS_SELECTOR, '[class*=Title]')
        _assignment_due_date_locator = (By.CSS_SELECTOR, '[class*=DueDate]')
        _back_to_dashboard_button_locator = (By.CSS_SELECTOR, '.btn-default')

        @property
        def title(self) -> str:
            """Return the assignment name.

            :return: the assignment name
            :rtype: str

            """
            return self.find_element(*self._assignment_title_locator).text

        @property
        def due_date(self) -> str:
            r"""Return the assignment due date.

            https://docs.python.org/3.7/library/datetime.html \
            #strftime-and-strptime-behavior

            :return: the assignment due date as a string with the format
                "due %a, %b %d, %Y %I:%M %p"
            :rtype: str

            """
            return self.find_element(*self._assignment_due_date_locator).text

        def back_to_dashboard(self) -> StudentCourse:
            """Click the 'Back to Dashboard' button.

            :return: the student course page
            :rtype: :py:class:`~pages.tutor.course.StudentCourse`

            """
            button = self.find_element(*self._back_to_dashboard_button_locator)
            Utility.click_option(self.driver, element=button)
            return go_to_(
                StudentCourse(self.driver, base_url=self.page.base_url))

    class Nav(Region):
        """A placeholder for the assignment navigation bar."""

        def __init__(self):
            """Override the initialization to toss an implementation error."""
            raise NotImplementedError("Must use an individual assignment type,"
                                      " not Assignment")


class Event(Assignment):
    """A calendar event."""

    class Content(Region):
        """The interactive assignment body."""

        _assignment_name_locator = (By.CSS_SELECTOR, '.event-task h1')
        _assignment_description_locator = (By.CSS_SELECTOR, '.event-task h3')
        _back_to_dashboard_button_locator = (By.CSS_SELECTOR, '.event-task a')

        @property
        def name(self) -> str:
            """Return the assignment name.

            .. note:

               This should match the footer's assignment title.

            :return: the assignment name.
            :rtype: str

            """
            return self.find_element(*self._assignment_name_locator).text

        @property
        def description(self) -> str:
            """Return the assignment description, if present.

            :return: the assignment description, if found, otherwise an empty
                string
            :rtype: str

            """
            description = self.find_elements(
                *self._assignment_description_locator)
            return description[0].text if description else ''

        def back_to_dashboard(self) -> StudentCourse:
            """Click on the 'Back to Dashboard' button in the assignment body.

            :return: the student course page
            :rtype: :py:class:`~pages.tutor.course.StudentCourse`

            """
            button = self.find_element(*self._back_to_dashboard_button_locator)
            Utility.click_option(self.driver, element=button)
            return go_to_(StudentCourse(self.driver, base_url=self.base_url))


class External(Assignment):
    """An assignment found outside of OpenStax Tutor Beta."""

    class Content(Region):
        """The interactive assignment body."""

        _assignment_name_locator = (By.CSS_SELECTOR, '.external-url-task h1')
        _assignment_description_locator = (
                                    By.CSS_SELECTOR, '.external-url-task h3')
        _external_url_locator = (By.CSS_SELECTOR, '[class*=Link]')

        @property
        def name(self) -> str:
            """Return the assignment name.

            .. note:

               This should match the footer's assignment title.

            :return: the assignment name.
            :rtype: str

            """
            return self.find_element(*self._assignment_name_locator).text

        @property
        def description(self) -> str:
            """Return the assignment description, if present.

            :return: the assignment description, if found, otherwise an empty
                string
            :rtype: str

            """
            description = self.find_elements(
                *self._assignment_description_locator)
            return description[0].text if description else ''

        @property
        def assignment_url(self) -> str:
            """Return the external URL for the assignment.

            :return: the assignment URL
            :rtype: str

            """
            return (self.find_element(*self._external_url_locator)
                    .get_attribute('href'))

        def go_to_assignment(self) -> str:
            """Click on the assignment URL.

            :return: the assignment URL
            :rtype: str

            """
            link = self.find_element(*self._external_url_locator)
            url = link.get_attribute('href')
            Utility.switch_to(self.driver, element=link)
            sleep(1)
            return url


class Homework(Assignment):
    """A collection of assessments selected by the course instructor."""

    class Content(Region):
        """The assessment pane."""

        _is_free_response_locator = (
            By.CSS_SELECTOR, '[class*=FreeResponse]')
        _is_multipart_locator = (
            By.CSS_SELECTOR, '[class*=MultipartGroup]')
        _is_multiple_choice_locator = (
            By.CSS_SELECTOR, '[class*=ExerciseQuestion]')

        @property
        def pane(self):
            """Access the question pane."""
            multipart = self.find_elements(*self._is_multipart_locator)
            if multipart:
                from regions.tutor.assessment import MultipartQuestion
                return MultipartQuestion(self, multipart[0])
            free_response = self.find_elements(*self._is_free_response_locator)
            if free_response:
                from regions.tutor.assessment import FreeResponse
                return FreeResponse(self, free_response[0])
            multiple_choice = self.find_element(
                *self._is_multiple_choice_locator)
            from regions.tutor.assessment import MultipleChoice
            return MultipleChoice(self, multiple_choice)

    class Nav(Region):
        """The homework step navigation."""

        _homework_step_locator = (By.CSS_SELECTOR, '.breadcrumbs-wrapper span')

        @property
        def steps(self) -> List[Homework.Nav.Step]:
            """Access the individual homework steps.

            :return: the list of available steps
            :rtype: list(:py:class:`~pages.tutor.task.Homework.Nav.Step`)

            """
            return [self.Step(self, crumb)
                    for crumb
                    in self.find_elements(*self._homework_step_locator)]

        class Step(Region):
            """A homework step, review, or completion."""

            @property
            def title(self) -> str:
                """Return the homework step title.

                :return: the homework step title
                :rtype: str

                """
                return self.root.get_attribute('title')

            @property
            def step_id(self) -> str:
                """Return the step identification number.

                :return: the homework step ID number
                :rtype: str

                """
                return self.root.get_attribute('data-step-id')

            @property
            def index(self) -> int:
                """Return the exercise step index.

                :return: the exercise step index number or ``-1`` for non-
                    exercise steps
                :rtype: int

                """
                index = self.root.get_attribute('data-step-index')
                return int(index) if index else -1

            @property
            def step_type(self) -> str:
                """Return the step type.

                :return: the step type
                    :py:data:`~utils.tutor.Tutor.EXERCISE` or
                    :py:data:`~utils.tutor.Tutor.REVIEW_CARD` or
                    :py:data:`~utils.tutor.Tutor.END_CARD`
                :rtype: str

                """
                classes = self.root.get_attribute('class')
                if 'breadcrumb-exercise' in classes:
                    return Tutor.EXERCISE
                elif 'individual-review' in classes:
                    return Tutor.REVIEW_CARD
                elif 'breadcrumb-end' in classes:
                    return Tutor.END_CARD
                return TutorException(f'Step type not found in "{classes}"')

            @property
            def answered(self) -> bool:
                """Return True if the step is answered.

                :return: ``True`` if the step is answered, otherwise ``False``
                :rtype: bool

                """
                return 'completed' in self.root.get_attribute('class')

            @property
            def correctness(self) -> str:
                """Return the correctness for the step.

                :return: the correctness (answered correctly or incorrectly) of
                    the step if past the due date and answered
                    :py:data:`~utils.tutor.Tutor.CORRECT` or
                    :py:data:`~utils.tutor.Tutor.INCORRECT` or
                    :py:data:`~utils.tutor.Tutor.NOT_ANSWERED` or
                    :py:data:`~utils.tutor.Tutor.NOT_GRADED`
                :rtype: str

                """
                if not self.answered:
                    return Tutor.NOT_ANSWERED
                classes = self.root.get_attribute('class')
                if 'status-correct' in classes:
                    return Tutor.CORRECT
                elif 'status-incorrect' in classes:
                    return Tutor.INCORRECT
                return Tutor.NOT_GRADED

            @property
            def selection(self) -> str:
                """Return the selection type for the assessment.

                :return: the selection type for the assessment question or
                    :py:data:`~utils.tutor.Tutor.NOT_A_QUESTION` for an
                    interstitial card; standard responses will be
                    :py:data:`~utils.tutor.Tutor.CORE` or
                    :py:data:`~utils.tutor.Tutor.PERSONALIZED` or
                    :py:data:`~utils.tutor.Tutor.SPACED_PRACTICE`
                :rtype: str

                """
                classes = self.root.get_attribute('class')
                if 'core' in classes:
                    return Tutor.CORE
                elif 'personalized' in classes:
                    return Tutor.PERSONALIZED
                elif 'spaced' in classes:
                    return Tutor.SPACED_PRACTICE
                return Tutor.NOT_A_QUESTION

            @property
            def is_active(self) -> bool:
                """Return True if the step is currently selected and active.

                :return: ``True`` if the step is active and displayed in the
                    body, otherwise ``False``
                :rtype: bool

                """
                return 'active' in self.root.get_attribute('class')

            def select(self) -> Homework:
                """Select the step to display it in the main body.

                :return: the homework assignment with the selected step active
                :rtype: :py:class:`~pages.tutor.task.Homework`

                """
                Utility.click_option(self.driver, element=self.root)
                sleep(1)
                return self.page.page


class Reading(Assignment):
    """A collection of book sections selected by the course instructor."""

    _overlay_page_locator = (
        By.CSS_SELECTOR, '.overlay')
    _annotation_slide_out_box_locator = (
        By.CSS_SELECTOR, '.slide-out-edit-box')
    _highlight_segment_locator = (
        By.CSS_SELECTOR, 'span.tutor-highlight')
    _sidebar_annotation_icon_locator = (
        By.CSS_SELECTOR, 'button.sidebar-button')

    _main_content_selector = '.obscured-page .page'

    _highlighting_summary_toggle_selector = '.note-summary-toggle'
    _milestone_chart_toggle_selector = '.icons > button'
    _highlight_button_selector = 'button.highlight'
    _annotation_button_selector = 'button.annotate'

    def highlights(self, milestones=False) \
            -> Union[Reading, Reading.Highlights, Reading.Milestones]:
        """Toggle the highlighting or milestone summary page.

        Possible outcomes:
        |--------------------+-----------------------------------|
        |                    |              Toggle:              |
        | Currently Showing: | Highlights      | Milestones      |
        |--------------------+-----------------+-----------------|
        | Reading            | show highlights | show milestones |
        | Highlight Summary  | show reading    | show milestones |
        | Milestones         | show highlights | show reading    |
        |--------------------+-----------------+-----------------|

        :param bool milestones: (optional) use the milestone selector instead
            of the highlighting selector, returning the milestone chart
        :return: the reading, the highlighting summary, or the milestone chart
        :rtype: :py:class:`~pages.tutor.task.Reading` or
            :py:class:`~pages.tutor.task.Reading.Highlights` or
            :py:class:`~pages.tutor.task.Reading.Milestones`

        """
        # locate the toggle button
        if not milestones:
            toggle_selector = self._highlighting_summary_toggle_selector
        else:
            toggle_selector = self._milestone_chart_toggle_selector
        toggle = self.driver.execute_script(
            f'return document.querySelector("{toggle_selector}");')

        # locate the overlay element for the highlight and summary pages
        overlay_root = self.find_element(*self._overlay_page_locator)

        # find the current state of the overlay to figure out what page or
        # region to return
        overlay_open = 'hidden' in self.driver.execute_script(
            'return document.querySelector' +
            f'("{self._main_content_selector}").classList;')
        highlights_active = (
            overlay_root and
            'notes-summary' in overlay_root.get_attribute('class'))

        toggle.send_keys(Keys.RETURN)
        sleep(0.3)

        if (not overlay_open and not milestones) or \
                (overlay_open and not highlights_active and not milestones):
            # the reading is displayed and the user clicked on highlighting OR
            # milestones are displayed and the user clicked on highlighting
            return self.Highlights(self, overlay_root)
        elif (not overlay_open and milestones) or \
                (overlay_open and highlights_active and milestones):
            # the reading is displayed and the user clicked on milestones OR
            # the highlight summary is displayed and the user clicked on
            # milestones
            return self.Milestones(self, overlay_root)
        else:
            # the highlight summary is displayed and the user closed it OR
            # the milestones are displayed and the user closed them
            return self

    def milestones(self) -> Union[Reading, Reading.Milestones]:
        """Toggle the milestones chart.

        :return: the milestones chart if the chart isn't displayed or the
            reading step if the chart is displayed
        :rtype: :py:class:`~pages.tutor.task.Reading` or
            :py:class:`~pages.tutor.task.Reading.Milestones`

        """
        return self.highlights(milestones=True)

    def highlight(self) -> None:
        """Click the inline highlight button.

        Click the highlighter icon in the inline pop up button controls to add
        the selected text to the user's annotation list.

        :return: None

        """
        # Use the javascript selector to find the inline buttons wherever they
        # appear.
        highlighter = self.driver.execute_script(
            'return document.querySelector("' +
            f'{self._highlight_button_selector}");')
        if not highlighter:
            raise TutorException('Highlight button not available')
        Utility.click_option(self.driver, element=highlighter)
        sleep(1)

    def annotate(self) -> Reading.AnnotationBox:
        """Click the inline annotation button.

        Click the speech bubble icon in the inline pop up button controls to
        add the selected text to the user's annotation list.

        :return: the annotation slide out edit box
        :rtype: :py:class:`~pages.tutor.task.Reading.AnnotationBox`

        """
        annotater = self.driver.execute_script(
            'return document.querySelector("' +
            f'{self._annotation_button_selector}");')
        if not annotater:
            raise TutorException('Annotation button not available')
        Utility.click_option(self.driver, element=annotater)
        sleep(1)
        return self.AnnotationBox(self)

    @property
    def content_highlights(self) -> List[TutorHighlight]:
        """Return the list of highlights found within the page.

        :return: the list of highlights for the current book section or page
        :rtype: dict(str, list(WebElement))

        """
        group = {}
        for segment in self.find_elements(*self._highlight_segment_locator):
            highlight_id = segment.get_attribute('data-id')
            if highlight_id not in group:
                group[highlight_id] = [segment]
            else:
                group[highlight_id].append(segment)
        return group

    @property
    def sidebar_buttons(self) -> List[WebElement]:
        r"""Return the available annotation text bubbles.

        :return: the list of available annotations
        :rtype: list(:py:class:`~selenium.webdriver.remote \
                                .webelement.WebElement`)

        """
        return self.find_elements(*self._sidebar_annotation_icon_locator)

    class AnnotationBox(Region):
        """The annotation creation and edit box."""

        _annotation_content_box_locator = (
            By.CSS_SELECTOR, 'textarea')
        _save_annotation_button_locator = (
            By.CSS_SELECTOR, 'button[aria-label=save]')
        _delete_annotation_button_locator = (
            By.CSS_SELECTOR, 'button[aria-label=delete]')
        _view_previous_note_button_locator = (
            By.CSS_SELECTOR, 'button[aria-label="previous note"]')
        _view_next_note_button_locator = (
            By.CSS_SELECTOR, 'button[aria-label="next note"]')
        _view_all_highlights_button_locator = (
            By.CSS_SELECTOR, 'button:not([aria-label])')

        def is_displayed(self) -> bool:
            """Return True if the slide out edit box is displayed.

            :return: ``True`` when the slide out edit box is open
            :rtype: bool

            """
            if not self.root:
                return False
            return 'open' in self.root.get_attribute('class')

        @property
        def text(self) -> str:
            """Return the current annotation text.

            :return: the current annotation text
            :rtype: str

            """
            return (self.find_element(*self._annotation_content_box_locator)
                    .get_attribute('textContent'))

        @text.setter
        def text(self, note: str) -> None:
            """Enter the annotation text.

            :param str note: the annotation text
            :return: None

            """
            box = self.find_element(*self._annotation_content_box_locator)
            Utility.clear_field(self.driver, field=box)
            sleep(0.25)
            box.send_keys(note)
            sleep(0.25)

        def save(self) -> Reading:
            """Click the save annotation checkmark button.

            :return: the current reading task step
            :rtype: :py:class:`~pages.tutor.task.Reading`

            """
            checkmark = self.find_element(
                *self._save_annotation_button_locator)
            Utility.click_option(self.driver, element=checkmark)
            self.wait.until(lambda _: not self.is_displayed())
            sleep(0.75)
            return self.page

        def delete(self) -> Reading:
            """Click the delete annotation trashcan button.

            :return: the current reading task step
            :rtype: :py:class:`~pages.tutor.task.Reading`

            """
            trashcan = self.find_element(
                *self._delete_annotation_button_locator)
            Utility.click_option(self.driver, element=trashcan)
            self.wait.until(lambda _: not self.is_displayed())
            sleep(0.75)
            return self.page

        def previous(self) -> Reading.AnnotationBox:
            """Click the previous annotation up arrow button.

            :return: the previous annotation/highlight if one exists
            :rtype: :py:class:`~pages.tutor.task.Reading.AnnotationBox`

            """
            up_arrow = self.find_element(
                *self._view_previous_note_button_locator)
            Utility.click_option(self.driver, element=up_arrow)
            sleep(1)
            return self

        def next(self) -> Reading.AnnotationBox:
            """Click the next annotation down arrow button.

            :return: the following annotation/highlight if one exists
            :rtype: :py:class:`~pages.tutor.task.Reading.AnnotationBox`

            """
            down_arrow = self.find_element(
                *self._view_next_note_button_locator)
            Utility.click_option(self.driver, element=down_arrow)
            sleep(1)
            return self

        def see_all(self) -> Reading.Highlights:
            """Click the 'See all' annotations button.

            :return: the highlighting summary page
            :rtype: :py:class:`~pages.tutor.task.Reading.Highlights`

            """
            see_all = self.find_element(
                *self._view_all_highlights_button_locator)
            Utility.click_option(self.driver, element=see_all)
            sleep(1)
            overlay_root = self.driver.execute_script(
                'return document.querySelector("{0}");'
                .format(self.page._overlay_page_locator[1]))
            return self.page.Highlights(self, overlay_root)

    class Content(Region):
        """The reading assignment body."""

        _previous_page_arrow_locator = (By.CSS_SELECTOR, '.prev')
        _next_page_arrow_locator = (By.CSS_SELECTOR, '.next')
        _loading_card_locator = (By.CSS_SELECTOR, '[class*=LoadingCard]')
        _is_multiple_choice_locator = (By.CSS_SELECTOR, '.answers-table')
        _correctness_shown_locator = (By.CSS_SELECTOR, '.has-correct-answer')
        _is_free_response_locator = (By.CSS_SELECTOR, '[class*=FreeResponse]')
        _assignment_completion_locator = (By.CSS_SELECTOR, '.task-steps-end')
        _reading_content_locator = (By.CSS_SELECTOR, '#paged-content')
        _image_caption_locator = (By.CSS_SELECTOR, '.os-caption-container')
        _paragraph_locator = (By.CSS_SELECTOR, '.annotater-content p[id]')
        _back_to_dashboard_button_locator = (
            By.CSS_SELECTOR, '[class*=CenteredBackButton]')

        def previous_page(self) -> Reading:
            """Click on the left arrow button.

            :return: the previous step from the reading assignment
            :rtype: :py:class:`~pages.tutor.task.Reading`

            """
            try:
                button = self.find_element(*self._previous_page_arrow_locator)
                Utility.click_option(self.driver, element=button)
                sleep(1)
            except NoSuchElementException:
                pass
            return Reading(self.driver, base_url=self.page.base_url)

        @property
        def next_page_arrow(self) -> WebElement:
            r"""Return the next page transition arrow element.

            :return: the next page arrow
            :rtype: \
                :py:class:`~selenium.webdriver.remote.webelement.WebElement`

            """
            return self.find_element(*self._next_page_arrow_locator)

        @property
        def next_page_available(self) -> bool:
            """Return True if the next page arrow is available.

            :return: ``True`` if the next page transition arrow is available
            :rtype: bool

            """
            try:
                arrow = self.next_page_arrow
                return not self.driver.execute_script(
                    'return arguments[0].hasAttribute("disabled");', arrow)
            except NoSuchElementException:
                return False

        def next_page(self) -> Reading:
            """Click on the right arrow button.

            :return: the next step in the reading assignment
            :rtype: :py:class:`~pages.tutor.task.Reading`

            """
            try:
                Utility.click_option(self.driver, element=self.next_page_arrow)
            except NoSuchElementException:
                pass
            sleep(1)
            return Reading(self.driver, base_url=self.page.base_url)

        @property
        def loading_view(self) -> bool:
            """Return True if the latest step is still loading.

            :return: ``True`` if the loading card is found.
            :rtype: bool

            """
            return bool(self.find_elements(*self._loading_card_locator))

        @property
        def is_free_response(self) -> bool:
            """Return True if the current step contains a free response box.

            :return: ``True`` if the current assignment step contains a free
                response text box
            :rtype: bool

            """
            return bool(self.find_elements(*self._is_free_response_locator))

        @property
        def is_multiple_choice(self) -> bool:
            """Return True if the current shows multiple choice answers.

            :return: ``True`` if the current assignment step contains mutliple
                choice answers
            :rtype: bool

            """
            return bool(self.find_elements(*self._is_multiple_choice_locator))

        @property
        def has_correct_answer(self) -> bool:
            """Return True if the correct answer is displayed.

            :return: ``True`` if the correct answer is displayed; may include
                answer feedback
            :rtype: bool

            """
            return bool(self.find_elements(*self._correctness_shown_locator))

        @property
        def is_assessment(self) -> bool:
            """Return True if the current step is an assessment.

            :return: ``True`` if an assessment is displayed in the content
                frame
            :rtype: bool

            """
            return self.is_free_response or self.is_multiple_choice

        @property
        def assignment_complete(self) -> bool:
            """Return True if the assignment completion step is displayed.

            :return: ``True`` if the assignment completion card is displayed
            :rtype: bool

            """
            return bool(self.find_elements(
                *self._assignment_completion_locator))

        @property
        def pane(self) -> Union[str, FreeResponse, MultipleChoice]:
            """Access the body content.

            :return: the text for a reading page, a free response assessment
                step, or a multiple choice assessment step
            :rtype: str or :py:class:`~pages.tutor.assessment.FreeResponse` or
                :py:class:`~pages.tutor.assessment.MultipleChoice`

            """
            self.wait.until(lambda _: not self.loading_view)
            if self.is_free_response:
                return FreeResponse(self, self.root)
            if self.is_multiple_choice:
                return MultipleChoice(self, self.root)
            return (self.find_element(*self._reading_content_locator)
                    .get_attribute('textContent'))

        @property
        def captions(self) -> List[Reading.Content.Caption]:
            """Return a list of image captions found on the page.

            :return: the list of picture captions
            :rtype: list(:py:class:`~pages.tutor.task.Reading.Content.Caption`)

            """
            return [self.Caption(self, image_caption)
                    for image_caption
                    in self.find_elements(*self._image_caption_locator)]

        @property
        def paragraphs(self) -> List[str]:
            """Return a list of paragraphs found on the page.

            :return: the list of paragraphs
            :rtype: list(str)

            """
            return self.find_elements(*self._paragraph_locator)

        def back_to_dashboard(self) -> StudentCourse:
            """Click on the 'Back to Dashboard' button.

            :return: the student course page
            :rtype: :py:class:`~pages.tutor.course.StudentCourse`

            :raises :py:class:`~utils.tutor.TutorException`: if the reading
                assignment is not at the completion card (final) step

            """
            try:
                button = self.find_element(
                    *self._back_to_dashboard_button_locator)
                Utility.click_option(self.driver, element=button)
                sleep(1)
                return go_to_(
                    StudentCourse(self.driver, base_url=self.page.base_url))
            except NoSuchElementException:
                raise TutorException("Assignment not complete")

        class Caption(Region):
            """An image caption."""

            _figure_number_locator = (By.CSS_SELECTOR, '.os-number')
            _caption_text_locator = (By.CSS_SELECTOR, '.os-caption')

            @property
            def number(self) -> str:
                """Return the caption's figure number.

                :return: the figure number
                :rtype: str

                """
                return self.find_element(*self._figure_number_locator).text

            @property
            def text(self) -> str:
                """Return the caption text content.

                :return: the caption text
                :rtype: str

                """
                return (self.find_element(*self._caption_text_locator)
                        .get_attribute('textContent'))

    class Highlights(Region):
        """The highlighting summary page."""

        _description_locator = (
            By.CSS_SELECTOR, '.notes > h4 , .notes > h3 , .notes > p')
        _sections_toggle_locator = (
            By.CSS_SELECTOR, '.dropdown-toggle')
        _dropdown_menu_option_locator = (
            By.CSS_SELECTOR, '.multi-selection-option')
        _print_preview_locator = (
            By.CSS_SELECTOR, '.print-btn')
        _note_sections_locator = (
            By.CSS_SELECTOR, '.notes .section')
        _annotation_card_locator = (
            By.CSS_SELECTOR, '.note-card')

        def is_displayed(self) -> bool:
            """Return True when the main page is hidden.

            :return: ``True`` when the main content is not displayed
            :rtype: bool

            """
            sleep(0.5)
            return self.driver.execute_script(
                COMPUTED_STYLE.format(
                    selector=self.page._main_content_selector,
                    property='display',
                    expected_value='none'))

        @property
        def description(self) -> str:
            """Return the page description if no notes are available.

            :return: the empty highlighting summary text
            :rtype: str

            """
            return '\n'.join(
                [line.text
                 for line
                 in self.find_elements(*self._description_locator)])

        @property
        def drop_down(self) -> WebElement:
            r"""Return the section selector drop down menu.

            :return: the book section multi-select drop down
            :rtype: \
                :py:class:`~selenium.webdriver.remote.webelement.WebElement`

            """
            return self.find_element(*self._sections_toggle_locator)

        @property
        def menu_is_open(self) -> bool:
            """Return True if the section drop down menu is open.

            :return: ``True`` if the multi-select drop down menu is open, else
                ``False``
            :rtype: bool

            """
            return \
                self.drop_down.get_attribute('aria-expanded').lower() == 'true'

        @property
        def options(self) -> List[Reading.Highlights.DisplaySection]:
            r"""Return the list of sections with highlights.

            :return: the list of sections with highlights and/or annotations
            :rtype: list(:py:class:`~pages.tutor.task.Reading.Highlights \
                                    .DisplaySection`)

            """
            return [self.DisplaySection(self, section)
                    for section
                    in self.find_elements(*self._dropdown_menu_option_locator)]

        def show_sections(self, sections=[], show_all=False) \
                -> Reading.Highlights:
            """Select sections by section number.

            :param sections: a list of book section highlights to display
            :param bool show_all: (optional) select all available sections
            :type sections: list(str)
            :return: the highlighting summary page open
            :rtype: :py:class:`~pages.tutor.task.Reading.Highlights`

            """
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
            return self

        def show_print_preview(self) -> PrintPreview:
            """Click on the 'Print this page' button.

            :return: the print preview pop up window
            :rtype: :py:class:`PrintPreview`

            """
            button = self.find_element(*self._print_preview_locator)
            Utility.switch_to(self.driver, element=button)
            return PrintPreview(self.driver)

        @property
        def notes(self) -> List[Reading.Highlights.Note]:
            """Access each displayed highlight or annotation.

            :return: a list of displayed highlights and annotations
            :rtype: list(:py:class:`~pages.tutor.task.Reading.Highlights.Note`)

            """
            return [self.Note(self, note)
                    for note
                    in self.find_elements(*self._annotation_card_locator)]

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
            def content(self) -> str:
                """Return the full HTML content text.

                :return: the highlighted content with full markup
                :rtype: str

                """
                return (self.find_element(*self._content_locator)
                        .get_attribute('innerHTML'))

            @property
            def note(self) -> str:
                """Return the associated note, if found.

                :return: the highlight's associated note
                :rtype: str

                """
                return self.find_element(*self._note_locator).text

            def edit(self, text='') -> Reading.Highlights:
                """Edit the highlight note.

                :param str text: new text for the highlight's note
                :return: the highlighting summary page
                :rtype: :py:class:`~pages.tutor.task.Reading.Highlights`

                """
                button = self.find_element(*self._edit_button_locator)
                Utility.click_option(self.driver, element=button)
                if text:
                    self.note_box.send_keys(text)
                    sleep(0.1)
                    self.save_edit()
                    sleep(0.25)
                return self.page

            @property
            def note_box(self) -> WebElement:
                r"""Return the note edit box.

                :return: the highlight's note editing box
                :rtype: \
                    :py:class:`~selenium.webdriver.remote.webelement.WebElement`

                """
                return self.find_element(*self._note_box_locator)

            def save_edit(self) -> Reading.Highlights:
                """Click on the checkmark confirm button.

                :return: the highlighting summary page
                :rtype: :py:class:`~pages.tutor.task.Reading.Highlights`

                """
                button = self.find_element(*self._save_edit_button_locator)
                Utility.click_option(self.driver, element=button)
                return self.page

            def cancel_edit(self) -> Reading.Highlights:
                """Click on the X cancelation button.

                :return: the highlighting summary page
                :rtype: :py:class:`~pages.tutor.task.Reading.Highlights`

                """
                button = self.find_element(*self._cancel_edit_button_locator)
                Utility.click_option(self.driver, element=button)
                return self.page

            def view(self) -> ReferenceBook:
                """Click on the view in book link.

                :return: the reference book with the requested book section
                    displayed in the content region
                :rtype: :py:class:`~pages.tutor.reference.ReferenceBook`

                """
                button = self.find_element(*self._view_button_locator)
                Utility.switch_to(self.driver, element=button)
                return go_to_(
                    ReferenceBook(self.driver, self.page.page.base_url))

            def delete(self) -> Reading.Highlights:
                """Delete the highlight.

                :return: the highlighting summary page
                :rtype: :py:class:`~pages.tutor.task.Reading.Highlights`

                """
                button = self.find_element(*self._delete_button_locator)
                script = 'return document.querySelector("arguments[0]");'
                Utility.click_option(self.driver, element=button)
                pop_up = self.driver.execute_script(
                    script, self._pop_over_content_selector)
                confirm = pop_up.find_element(*self._delete_confirm_locator)
                Utility.click_option(self.driver, element=confirm)
                sleep(0.25)
                return self.page

    class Milestones(Region):
        """The reading step milestone chart."""

        _milestone_card_locator = (By.CSS_SELECTOR, '[data-step-index]')

        _milestone_chart_toggle_selector = '[class*=StyledToggle]'

        def is_displayed(self) -> bool:
            """Return True when the main page is hidden.

            :return: ``True`` when the main content is not displayed
            :rtype: bool

            """
            sleep(0.5)
            return self.driver.execute_script(
                COMPUTED_STYLE.format(
                    selector=self.page._main_content_selector,
                    property='display',
                    expected_value='none'))

        def close(self) -> Reading:
            """Click on the toggle to close the milestones pane.

            :return: the reading page
            :rtype: :py:class:`~pages.tutor.task.Reading`

            """
            toggle = self.driver.execute_script(
                'return document.querySelector("{0}");'
                .format(self._milestone_chart_toggle_selector))
            Utility.click_option(self.driver, element=toggle)
            sleep(0.3)
            return self.page

        @property
        def milestones(self) -> List[Reading.Milestones.Milestone]:
            r"""Access the individual milestone cards.

            :return: the list of milestones reached within the reading
                assignment
            :rtype: list(:py:class:`~pages.tutor.task.Reading \
                                    .Milestones.Milestone`)

            """
            return [self.Milestone(self, card)
                    for card
                    in self.find_elements(*self._milestone_card_locator)]

        class Milestone(Region):
            """A milestone card."""

            _milestone_information_locator = (By.CSS_SELECTOR, '.milestone')
            _milestone_status_locator = (By.CSS_SELECTOR, '[title]')
            _milestone_preview_locator = (
                By.CSS_SELECTOR, '.milestone-preview')
            _completed_step_locator = (By.CSS_SELECTOR, '.completed')

            @property
            def index(self) -> int:
                """Return the milestone index.

                :return: the milestone card's index within the assignment
                    starting from zero (0)
                rtype: int

                """
                return int(self.root.get_attribute('data-step-index'))

            @property
            def step_type(self) -> str:
                """Return the card step type.

                :return: the step type represented by the card
                :rtype: str

                :raises :py:class:`~utils.tutor.TutorException`: if a matching
                    card type isn't found within the information element class

                """
                step_info = (self.find_element(
                    *self._milestone_information_locator)
                    .get_attribute('class'))
                if 'milestone-reading' in step_info:
                    return Tutor.READING
                elif 'milestone-exercise' in step_info:
                    return Tutor.EXERCISE
                elif 'milestone-individual-review-intro' in step_info:
                    return Tutor.REVIEW_CARD
                elif 'milestone-end' in step_info:
                    return Tutor.END_CARD
                else:
                    raise TutorException(
                        f'No card type found within "{step_info}"')

            @property
            def status_element(self) -> Union[WebElement, None]:
                r"""Return the milestone status element.

                :return: the milestone status element
                :rtype: :py:class:`~selenium.webdriver.remote\
                                  .webelement.WebElement`

                """
                info_card = self.find_elements(*self._milestone_status_locator)
                if info_card:
                    return info_card[0]

            @property
            def title(self) -> str:
                """Return the card title, if found.

                :return: the card title, if found, otherwise an empty string
                :rtype: str

                """
                step_info = self.status_element
                return step_info[0].get_attribute('title') if step_info else ''

            @property
            def preview(self) -> str:
                """Return the card preview text.

                :return: the milestone preview card text
                :rtype: str

                """
                return (self.find_element(*self._milestone_preview_locator)
                        .get_attribute('textContent'))

            @property
            def is_complete(self) -> bool:
                """Return True if the step is complete.

                :return: ``True`` if the reading step is complete, otherwise
                    ``False``
                :rtype: bool

                """
                return bool(self.find_elements(*self._completed_step_locator))

            @property
            def correct(self) -> Union[str, None]:
                """Return the correctness for exercise steps.

                :return: the correctness for an exercise step or None for other
                    steps
                :rtype: str or None

                """
                step_info = self.status_element
                if not step_info:
                    return
                if 'status-correct' in step_info.get_attribute('class'):
                    return Tutor.CORRECT
                elif 'status-incorrect' in step_info.get_attribute('class'):
                    return Tutor.INCORRECT
                return Tutor.NOT_GRADED

    class Nav(Region):
        """The reading progress bar."""

        _progress_bar_locator = (By.CSS_SELECTOR, '.progressbar')

        @property
        def progress(self) -> int:
            """Return the current assignment progress.

            :return: the current assignment progress percentage out of 100
            :rtype: int

            """
            return int(self.find_element(*self._progress_bar_locator)
                       .get_attribute('aria-valuenow'))
