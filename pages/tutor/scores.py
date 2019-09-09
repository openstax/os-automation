"""The student and instructor scores page."""

from time import sleep
from typing import List, Union

from pypom import Region
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as expect

from pages.tutor.base import TutorBase
from pages.tutor.performance import PerformanceForecast
from utils.tutor import Tutor, TutorException
from utils.utilities import Utility, go_to_


def _average_helper(text):
    """Return a number from the text score or the text if it is not a number.

    .. py:function:: _average_helper(text)

       Return a number as an integer if the score is available or the text
       content (ie '---' or 'n/a') if it is not.

       :param str text: the possible score number
       :return: the score or the text
       :rtype: int or str

    :noindex:

    >>> _average_helper("70%")
    70
    >>> _average_helper("n/a")
    'n/a'
    >>> _average_helper("---")
    '---'

    """
    try:
        return int(text[:-1])
    except ValueError:
        return text


class Tooltip(Region):
    """A scores pop up tool tip."""

    _root_locator = (By.CSS_SELECTOR, '[role=tooltip]')


class Progress(Tooltip):
    """A progress tool tip."""

    _completion_locator = (By.CSS_SELECTOR, '.row:first-child div')
    _out_of_number_locator = (By.CSS_SELECTOR, '.row:nth-child(2) div')

    @property
    def completion(self):
        """Return the completion percentage.

        :return: the assignment completion percentage out of 100
        :rtype: int

        """
        complete = self.find_element(*self._completion_locator).text
        return int(complete.split()[-1][:-1])

    @property
    def number(self):
        """Return the number complete out of the total possible.

        :return: the number of completed questions out of the total possible
        :rtype: str

        """
        return self.find_element(*self._out_of_number_locator).text.strip()


class LateWork(Tooltip):
    """An instructor late work tool tip."""

    _heading_locator = (By.CSS_SELECTOR, '.popover-header')
    _title_locator = (By.CSS_SELECTOR, '.title')
    _status_locator = (By.CSS_SELECTOR, '.status')
    _button_locator = (By.CSS_SELECTOR, 'button')

    @property
    def heading(self):
        """Return the tool tip heading.

        :return: the tool tip heading
        :rtype: str

        """
        return self.find_element(*self._heading_locator).text

    @property
    def title(self):
        """Return the status lead in.

        :return: the status lead in title - either the score on the due date or
            the score on the last day of work
        :rtype: str

        """
        return self.find_element(*self._title_locator).text

    @property
    def status(self):
        """Return the status percentage.

        :return: the status percentage number out of 100
        :rtype: int

        """
        return int(self.find_element(*self._status_locator).text[:-1])

    def use_this_score(self):
        """Click on the late work button.

        :return: the scores page
        :rtype: :py:class:`Scores`

        """
        button = self.find_element(*self._button_locator)
        Utility.click_option(self.driver, element=button)
        self.wait.until(expect.staleness_of(self.root))
        return self.page

    accept_late_score = use_this_score


class Weights(Region):
    """The scores page weight scoring."""

    _heading_locator = (By.CSS_SELECTOR, '.modal-header')
    _x_button_locator = (By.CSS_SELECTOR, '.close')
    _cancel_close_button_locator = (
                            By.CSS_SELECTOR, '.modal-footer button:last-child')

    _root_selector = '.set-weights.modal'

    @property
    def root(self):
        """Return the weights modal root element.

        :return: the modal root element
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.driver.execute_script(
            f'return document.querySelector("{self._root_selector}");')

    def is_displayed(self):
        """Return True if the weights modal root is found.

        :return: ``True`` if the weights modal is found
        :rtype: bool

        """
        try:
            return bool(self.root)
        except NoSuchElementException:
            return False

    @property
    def heading(self):
        """Return the modal heading.

        :return: the set weights modal heading
        :rtype: str

        """
        return self.find_element(*self._heading_locator).text

    def close(self, x=False):
        """Click on the 'Close', 'x', or 'Cancel' button.

        :param bool x: (optional) ``True`` if using the 'x' close button
        :return: the scores page
        :rtype: :py:class:`Scores` or :py:class:`StudentScores`

        :raises :py:class:`~utils.tutor.TutorException`: if an instructor tries
            to use the 'x' close button

        """
        locator = self._x_button_locator if x \
            else self._cancel_close_button_locator
        try:
            button = self.find_element(*locator)
        except NoSuchElementException:
            raise TutorException('x close not available for teachers')
        Utility.click_option(self.driver, element=button)
        return self.page


class SetWeights(Weights):
    """The instructor's set weights modal."""

    _see_why_link_locator = (By.CSS_SELECTOR, 'a')
    _homework_score_locator = (By.CSS_SELECTOR, '.weight:first-child input')
    _homework_progress_locator = (
                                By.CSS_SELECTOR, '.weight:nth-child(2) input')
    _reading_score_locator = (By.CSS_SELECTOR, '.weight:nth-child(3) input')
    _reading_progress_locator = (By.CSS_SELECTOR, '.weight:nth-child(4) input')
    _restore_default_locator = (By.CSS_SELECTOR, '.weights-set button')
    _weights_status_locator = (By.CSS_SELECTOR, '.weights-msg')
    _save_button_locator = (By.CSS_SELECTOR, '.async-button')
    _dialog_locator = (By.CSS_SELECTOR, '.modal-dialog')

    def _set_value(self, field: WebElement, value: Union[str, int]) -> None:
        r"""Set a weights value.

        :param field: the field to modify
        :param value: the new field value
        :type field: \
            :py:class:`~selenium.webdriver.remote.webelement.WebElement`
        :type: value: str or int
        :return: None

        """
        test = int(value)
        if test < 0 or test > 100:
            raise ValueError("Value must be between 0 and 100")
        for _ in range(3):
            field.send_keys(Keys.BACKSPACE)
            field.send_keys(Keys.DELETE)
        for ch in str(value):
            field.send_keys(ch)

    def see_why(self):
        """Click on the 'See why' link to view the weights blog post.

        :return: the blog entry on openstax.org in a new tab describing why
            homework scores and reading progress are the suggested metrics to
            use for Tutor
        :rtype: :py:class:`~pages.web.blog.Article`

        """
        link = self.find_element(*self._see_why_link_locator)
        Utility.switch_to(self.driver, element=link)
        from pages.web.blog import Article
        return go_to_(Article(self.driver))

    @property
    def homework_score_input(self):
        """Return the homework score input box.

        :return: the homework score input element
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        :noindex:

        """
        return self.find_element(*self._homework_score_locator)

    @property
    def homework_score(self):
        """Return the current homework score weight value.

        :return: the value of the homework score weight out of 100 or 0 if the
            value is missing/blank
        :rtype: int

        """
        value = self.homework_score_input.get_attribute('value')
        return int(value) if value else 0

    @homework_score.setter
    def homework_score(self, value):
        """Set the homework score weight.

        :param value: the new value for the homework score weight
        :type value: int or str
        :return: None

        :raises ValueError: if value is not a number, is less than 0, or
            is greater than 100

        """
        self._set_value(self.homework_score_input, value)

    @property
    def homework_progress_input(self):
        """Return the homework progress input box.

        :return: the homework progress input element
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        :noindex:

        """
        return self.find_element(*self._homework_progress_locator)

    @property
    def homework_progress(self):
        """Return the current homework progress weight value.

        :return: the value of the homework progress weight out of 100 or 0 if
            the value is missing/blank
        :rtype: int

        """
        value = self.homework_progress_input.get_attribute('value')
        return int(value) if value else 0

    @homework_progress.setter
    def homework_progress(self, value):
        """Set the homework progress weight.

        :param value: the new value for the homework progress weight
        :type value: int or str
        :return: None

        :raises ValueError: if value is not a number, is less than 0, or
            is greater than 100

        """
        self._set_value(self.homework_progress_input, value)

    @property
    def reading_score_input(self):
        """Return the reading score input box.

        :return: the reading score input element
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        :noindex:

        """
        return self.find_element(*self._reading_score_locator)

    @property
    def reading_score(self):
        """Return the current reading score weight value.

        :return: the value of the reading score weight out of 100 or 0 if the
            value is missing/blank
        :rtype: int

        """
        value = self.reading_score_input.get_attribute('value')
        return int(value) if value else 0

    @reading_score.setter
    def reading_score(self, value):
        """Set the reading score weight.

        :param value: the new value for the reading score weight
        :type value: int or str
        :return: None

        :raises ValueError: if value is not a number, is less than 0, or
            is greater than 100

        """
        self._set_value(self.reading_score_input, value)

    @property
    def reading_progress_input(self):
        """Return the reading progress input box.

        :return: the reading progress input element
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        :noindex:

        """
        return self.find_element(*self._reading_progress_locator)

    @property
    def reading_progress(self):
        """Return the current reading progress weight value.

        :return: the value of the reading progress weight out of 100 or 0 if
            the value is missing/blank
        :rtype: int

        """
        value = self.reading_progress_input.get_attribute('value')
        return int(value) if value else 0

    @reading_progress.setter
    def reading_progress(self, value):
        """Set the reading progress weight.

        :param value: the new value for the reading progress weight
        :type value: int or str
        :return: None

        :raises ValueError: if value is not a number, is less than 0, or
            is greater than 100

        """
        self._set_value(self.reading_progress_input, value)

    def restore_default(self):
        """Reset the weight to their default.

        :return: the set weights modal
        :rtype: :py:class:`SetWeights`

        :raises :py:class:`~utils.tutor.TutorException`: if values are set to
            thier defaults and the restore button is not available

        """
        try:
            button = self.find_element(*self._restore_default_locator)
        except NoSuchElementException:
            raise TutorException("Weights are already set to their defaults")
        Utility.click_option(self.driver, element=button)
        return self

    def set(self, weights: List[int]) -> None:
        """Assign weights to each assignment category.

        :param weights: the whole number percentages for each category in
            order - homework score, homework progress, reading score, reading
            progress; if less that 4 numbers are provided, default remaining
            values to 0; list elements beyond 4 will be ignored
        :type weights: list(int)
        :return: None

        """
        weights = weights + [0, 0, 0, 0] if isinstance(weights, list) \
            else [100, 0, 0, 0]
        self.homework_score = weights[0]
        self.homework_progress = weights[1]
        self.reading_score = weights[2]
        self.reading_progress = weights[3]
        sleep(0.25)

    @property
    def status_message(self):
        """Return the status message element.

        :return: the status message element
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        :noindex:

        """
        return self.find_element(*self._weights_status_locator)

    @property
    def status(self):
        """Return the status message.

        :return: the status message
        :rtype: str

        """
        return self.status_message.text

    @property
    def weights_are_valid(self):
        """Return True if the sum of the weights equals 100.

        :return: ``True`` if the sum of the weight values is 100, else
            ``False``
        :rtype: bool

        """
        return 'invalid' not in self.status_message.get_attribute('class')

    def save(self):
        """Click the 'Save' button if the weights are valid.

        :return: the scores page
        :rtype: :py:class:`Scores`

        """
        if not self.weights_are_valid:
            raise TutorException("Cannot save weights while they are invalid")
        button = self.find_element(*self._save_button_locator)
        Utility.click_option(self.driver, element=button)
        self.page.wait.until(expect.staleness_of(self.root))
        return self.page

    def cancel(self):
        """Click the 'Cancel' button to close the weights dialog.

        :return: the scores page
        :rtype: :py:class:`Scores`

        """
        return super().close


class ViewWeights(Weights):
    """The student's weights review modal."""

    _homework_score_locator = (
                        By.CSS_SELECTOR, '.weight:nth-child(2) div:last-child')
    _homework_progress_locator = (
                        By.CSS_SELECTOR, '.weight:nth-child(3) div:last-child')
    _reading_score_locator = (
                        By.CSS_SELECTOR, '.weight:nth-child(4) div:last-child')
    _reading_progress_locator = (
                        By.CSS_SELECTOR, '.weight:nth-child(5) div:last-child')

    @property
    def homework_score(self):
        """Return the weight for homework scores.

        :return: the weight for homework scores out of 100
        :rtype: int

        """
        return int(self.find_element(*self._homework_score_locator).text[:-1])

    @property
    def homework_progress(self):
        """Return the weight for homework completeness.

        :return: the weight for homework progress out of 100
        :rtype: int

        """
        return int(
            self.find_element(*self._homework_progress_locator).text[:-1])

    @property
    def reading_score(self):
        """Return the weight for reading scores.

        :return: the weight for reading scores out of 100
        :rtype: int

        """
        return int(self.find_element(*self._reading_score_locator).text[:-1])

    @property
    def reading_progress(self):
        """Return the weight for reading completeness.

        :return: the weight for reading progress out of 100
        :rtype: int

        """
        return int(
            self.find_element(*self._reading_progress_locator).text[:-1])

    @property
    def weights(self):
        """Return the currently assigned weights.

        :return: the set of weights for homework scores, homework progress,
            reading scores, and reading progress
        :rtype: list(int)

        """
        return [self.homework_score, self.homework_progress,
                self.reading_score, self.reading_progress]


class Scores(TutorBase):
    """The shared scores page elements."""

    _active_button_locator = (By.CSS_SELECTOR, '.active')
    _as_percentage_button_locator = (By.CSS_SELECTOR, '[value=percentage]')
    _as_number_button_locator = (By.CSS_SELECTOR, '[value=number]')
    _export_message_locator = (By.CSS_SELECTOR, '.scores-export span')
    _export_scores_file_locator = (By.CSS_SELECTOR, '.ox-icon-download')
    _no_data_button_locator = (By.CSS_SELECTOR, 'a[class]')
    _no_data_link_locator = (By.CSS_SELECTOR, 'a:not([class])')
    _no_data_locator = (By.CSS_SELECTOR, '.no-students p , .no-assignments p')
    _section_tab_locator = (By.CSS_SELECTOR, 'li a')
    _table_root_locator = (By.CSS_SELECTOR, '.scores-table')
    _title_locator = (By.CSS_SELECTOR, 'h1[class*=Title]')
    _toast_message_popup_locator = (By.CSS_SELECTOR, '.toast-notification')

    @property
    def loaded(self) -> bool:
        """Return True when the scores table is found.

        :return: ``True`` when the score table is loaded.
        :rtype: bool

        """
        return bool(self.find_elements(*self._table_root_locator))

    @property
    def is_teacher(self):
        """Return True if the current user is an instructor.

        :return: ``True`` if the current user is a teacher and has access to
            the instructor controls, else ``False``
        :rtype: bool

        """
        return 'Student' in self.title

    @property
    def modal_open(self) -> bool:
        """Return True if a modal is found open.

        :return: ``True`` if a modal is found

        """
        return bool(self.driver.execute_script(
            'return document.querySelectorAll(".modal");'))

    @property
    def title(self):
        """Return the page title.

        :return: the scores page title
        :rtype: str

        """
        return self.find_element(*self._title_locator).text

    @property
    def toast_seen(self) -> bool:
        """Return True if a toast-style popup is seen.

        :return: ``True`` if a toast-style popup message is displayed and then
            closed
        :rtype: bool

        """
        try:
            toast = self.wait.until(
                expect.presence_of_element_located(
                    self._toast_message_popup_locator))
        except TimeoutException:
            return False
        try:
            self.wait.until(expect.staleness_of(toast))
        except TimeoutException:
            return False
        return True

    # ---------------------------------------------------- #
    # Controls
    # ---------------------------------------------------- #

    def show_as_percentage(self):
        """Click the '%' button to show scores as percentages.

        :return: the scores page
        :rtype: :py:class:`StudentScores` or :py:class:`Scores`

        """
        button = self.find_element(*self._as_percentage_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.25)
        return self

    def show_as_number(self):
        """Click the '#' button to show scores as numbers.

        :return: the scores page
        :rtype: :py:class:`StudentScores` or :py:class:`Scores`

        """
        button = self.find_element(*self._as_number_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.25)
        return self

    @property
    def active_show_as(self):
        """Return the currently selected show as option.

        :return: :py:const:`Tutor.AS_PERCENTAGE` or :py:const:`Tutor.AS_NUMBER`
        :rtype: str

        """
        active_button = self.find_element(self._active_button_locator).text
        return Tutor.AS_PERCENTAGE if active_button == '%' else Tutor.AS_NUMBER

    def export(self):
        """Click on the download button to export the scores worksheet.

        :return: the scores page
        :rtype: :py:class:`Scores`

        """
        if not self.is_teacher:
            return self
        message = self.export_message
        button = self.find_element(*self._export_scores_file_locator)
        Utility.click_option(self.driver, element=button)
        self.wait.until(
            lambda _: self.export_message != message
            and 'Exporting' not in self.export_message)
        return self

    @property
    def export_message(self):
        """Return the export scores message text.

        :return: the text to the right of the export button; may include the
            last date and time the scores were exported
        :rtype: str

        """
        try:
            return self.find_element(*self._export_message_locator).text
        except NoSuchElementException:
            return ''

    @property
    def sections(self):
        """Return the list of course sections.

        :return: the list of course sections or periods
        :rtype: list(:py:class:`~Scores.Section`)

        """
        return [self.Section(self, section)
                for section in self.find_elements(*self._section_tab_locator)]

    def view_section(self, by_name=None, by_id=None):
        """Click on the section tab to view the section or period report.

        :param str by_name: view a specific section by its name
        :param int by_id: view a specific section by its order ID from 1 to the
            number of sections in the course
        :return: the scores page with the selected tab visible
        :rtype: :py:class:`Scores`

        :raises :py:class:`~utils.tutor.TutorException`: if a section is not
            found to match by_name

        """
        sections = self.sections

        # if there aren't any sections, or the user is a student, return
        if not sections:
            return self

        # try an array index
        if by_id:
            if by_id <= 0 or by_id > len(sections):
                raise ValueError('ID must be between 1 and {0}'
                                 .format(len(sections)))
            sections[by_id - 1].select()
            return self

        # search for a section name
        for section in sections:
            if section.name == by_name:
                section.select()
                return self
        raise TutorException('No section found to match "{0}"'.format(by_name))

    # ---------------------------------------------------- #
    # No students enrolled or no assignments available
    # ---------------------------------------------------- #

    @property
    def explanation(self):
        """Return the explanation text.

        For situations where there are either no students or no assignments.

        :return: the explanation text for when data is not possible or an empty
            string when there is data in the table
        :rtype: str

        """
        try:
            return self.find_element(*self._no_data_locator).text
        except NoSuchElementException:
            return ''

    def dashboard(self, use_button=False):
        """Click on the 'Course settings' or 'dashboard' link.

        :param bool use_button: (optional) use the 'Back to dashboard' or
            'Manage student access' button instead of the links
        :return: the course settings page (teacher), the current week
            (student), the course calendar (teacher), or the scores page if
            the link/button is not found
        :rtype: :py:class:`~pages.tutor.settings.Settings` or
            :py:class:`~pages.tutor.course.StudentCourse` or
            :py:class:`~pages.tutor.calendar.Calendar` or
            :py:class:`ScoresBase`

        """
        locator = self._no_data_button_locator if use_button \
            else self._no_data_link_locator
        try:
            link = self.find_element(*locator)
        except NoSuchElementException:
            return self
        if 'settings' in link.text or 'access' in link.text:
            from pages.tutor.settings import Settings as Destination
        elif self.is_teacher:
            from pages.tutor.calendar import Calendar as Destination
        else:
            from pages.tutor.course import StudentCourse as Destination
        Utility.click_option(self.driver, element=link)
        return go_to_(Destination(self.driver, base_url=self.base_url))

    def back_to_dashboard(self):
        """Click on the 'Manage student access' or 'Back to dashboard' button.

        :return: the course settings page (teacher), the current week
            (student), the course calendar (teacher), or the scores page if
            the link/button is not found
        :rtype: :py:class:`~pages.tutor.settings.Settings` or
            :py:class:`~pages.tutor.course.StudentCourse` or
            :py:class:`~pages.tutor.calendar.Calendar` or
            :py:class:`ScoresBase`

        """
        return self.course_settings(use_button=True)

    course_settings = dashboard
    manage_student_access = back_to_dashboard

    # ---------------------------------------------------- #
    # Normal Scores
    # ---------------------------------------------------- #

    @property
    def table(self):
        """Access the scores table.

        :return: the scores table
        :rtype: :py:class:`~pages.tutor.scores.Scores.Table`

        """
        table_root = self.find_element(*self._table_root_locator)
        return self.Table(self, table_root)

    class Section(Region):
        """A section or period tab."""

        _name_locator = (By.CSS_SELECTOR, 'span')

        @property
        def name(self):
            """Return the tab/section/period name.

            :return: the tab name
            :rtype: str

            """
            return self.find_element(*self._name_locator).text

        def select(self):
            """Click on the tab to view the section scores table.

            :return: the scores page showing the table for the selected tab
            :rtype: :py:class:`Scores`

            """
            Utility.click_option(self.driver, element=self.root)
            return self.page

    class Table(Region):
        """The scores table."""

        _table_heading_locator = (
            By.CSS_SELECTOR,
            '[class*="_rowsContainer"] > div:nth-child(3)')
        _table_students_locator = (
            By.CSS_SELECTOR,
            '[class*="_rowsContainer"] > div:nth-child(4) > div')
        _table_legend_locator = (By.CSS_SELECTOR, '[class*=Legend]')

        @property
        def heading(self):
            """Access the scores table heading information.

            :return: the table heading region
            :rtype: :py:class:`~Scores.Table.Heading`

            """
            overview_root = self.find_element(*self._table_heading_locator)
            return self.Heading(self, overview_root)

        @property
        def students(self):
            """Access the student row(s).

            :return: the list of student score rows
            :rtype: list(:py:class:`~Scores.Table.Student`)

            """
            return [self.Student(self, student)
                    for student
                    in self.find_elements(*self._table_students_locator)]

        @property
        def legend(self):
            """Return the legend text, if found.

            :return: the legend text or a blank string if not found
            :rtype: str

            """
            try:
                return self.find_element(*self._table_legend_locator).text
            except NoSuchElementException:
                return ''

        class Heading(Region):
            """The table column headings and average information region."""

            _overview_root_locator = (
                By.CSS_SELECTOR, '[class*="cellGroupW"]:first-child > div')
            _name_sort_locator = (
                By.CSS_SELECTOR, '.student-names .sortable')
            _averages_toggle_locator = (
                By.CSS_SELECTOR, 'button.averages-toggle')
            _set_weights_locator = (
                By.CSS_SELECTOR, '.set-weights')
            _course_average_locator = (
                By.CSS_SELECTOR,
                'div:nth-child(2) .overview-row > div:first-child')
            _homework_score_locator = (
                By.CSS_SELECTOR, '.overview-row .homework div:first-child')
            _homework_progress_locator = (
                By.CSS_SELECTOR, '.overview-row .homework div:last-child')
            _reading_score_locator = (
                By.CSS_SELECTOR, '.overview-row .reading div:first-child')
            _reading_progress_locator = (
                By.CSS_SELECTOR, '.overview-row .reading div:last-child')
            _assignment_locator = (
                By.CSS_SELECTOR,
                '[class*="cellGroupW"]:nth-child(2) [role=columnheader]')

            @property
            def _overview_root(self):
                r"""Return the root element for the student names and averages.

                :return: the overview and averages column root element
                :rtype: \
                    :py:class:`~selenium.webdriver.remote.webelement.WebElement`

                :noindex:

                """
                return self.find_element(*self._overview_root_locator)

            @property
            def name_sort(self):
                r"""Return the name sort toggle button.

                :return: the 'Overall' column header and sort toggle
                :rtype: \
                    :py:class:`~selenium.webdriver.remote.webelement.WebElement`

                """
                return self.find_element(*self._name_sort_locator)

            def sort_by_name(self):
                """Sort the table by last name.

                :return: the scores table sorted by last name
                :rtype: :py:class:`Scores`

                """
                Utility.click_option(self.driver, element=self.name_sort)
                sleep(0.5)
                return self.page.page

            @property
            def names_sorted(self):
                """Return the type of sort currently on the name column.

                :return: what sort option is affecting the name column
                :rtype: :py:data:`~utils.tutor.Tutor.ASCENDING` or
                    :py:data:`~utils.tutor.Tutor.DESCENDING` or
                    :py:data:`~utils.tutor.Tutor.NO_SORT`

                """
                current_sort = self.name_sort.get_attribute('class')
                if Tutor.ASCENDING in current_sort:
                    return Tutor.ASCENDING
                elif Tutor.DESCENDING in current_sort:
                    return Tutor.DESCENDING
                # the default is in place without a sort class on the column
                return Tutor.NO_SORT

            @property
            def averages_toggle(self):
                r"""Return the hide and show averages toggle button.

                :return: the 'Averages' column set header show/hide toggle
                :rtype: \
                    :py:class:`~selenium.webdriver.remote.webelement.WebElement`

                """
                return self.find_element(*self._averages_toggle_locator)

            def toggle_averages(self):
                """Open or close the 'Averages' columns.

                :return: the scores table
                :rtype: :py:class:`Scores`

                """
                Utility.click_option(self.driver, element=self.averages_toggle)
                sleep(1)
                return self.page.page

            @property
            def averages_open(self):
                """Return True if the 'Averages' panel is open.

                :return: ``True`` if the averages panel is open else ``False``
                :rtype: bool

                """
                return ('chevron-left'
                        in self.averages_toggle.get_attribute('class'))

            def view_weights(self):
                """Open the weights modal.

                :return: the weights modal
                :rtype: :py:class:`SetWeights` or :py:class:`ViewWeights`

                """
                link = self.find_element(*self._set_weights_locator)
                Utility.click_option(self.driver, element=link)
                sleep(0.25)
                modal_root = self.driver.execute_script(
                    'return document.querySelector("[role=dialog]");')
                if self.page.page.is_teacher:
                    return SetWeights(self.page.page, modal_root)
                return ViewWeights(self.page.page, modal_root)

            def set_weights(self):
                """Open the weights modal.

                :return: the weights modal
                :rtype: :py:class:`~pages.tutor.scores.SetWeights` or
                    :py:class:`~pages.tutor.scores.ViewWeights`

                """
                return self.view_weights()

            @property
            def course_average(self):
                """Return the current class average.

                :return: the current class average out of 100, if available
                :rtype: int or str

                """
                average = self.find_elements(*self._course_average_locator)
                if len(average) > 1:
                    return _average_helper(average[1].text)
                return _average_helper(average[0].text)

            @property
            def homework_average_score(self):
                """Return the current homework score average.

                :return: the current homework score average out of 100, if
                    available
                :rtype: int or str

                """
                average = self.find_element(*self._homework_score_locator).text
                return _average_helper(average)

            @property
            def homework_average_progress(self):
                """Return the current homework progress average.

                :return: the current homework progress average out of 100, if
                    available
                :rtype: int or str

                """
                average = (self.find_element(*self._homework_progress_locator)
                           .text)
                return _average_helper(average)

            @property
            def reading_average_score(self):
                """Return the current reading score average.

                :return: the current reading score average out of 100, if
                    available
                :rtype: int or str

                """
                average = self.find_element(*self._reading_score_locator).text
                return _average_helper(average)

            @property
            def reading_average_progress(self):
                """Return the current reading progress average.

                :return: the current reading progress average out of 100, if
                    available
                :rtype: int or str

                """
                average = (self.find_element(*self._reading_progress_locator)
                           .text)
                return _average_helper(average)

            @property
            def assignments(self):
                """Access the assignment column headers.

                :return: a list of assignment headers
                :rtype: list(:py:class:`~Scores.Table.Heading.AssignmentInfo`)

                """
                return [self.AssignmentInfo(self, assignment)
                        for assignment
                        in self.find_elements(*self._assignment_locator)]

            class AssignmentInfo(Region):
                """An assignment column header."""

                _assignment_type_locator = (
                    By.CSS_SELECTOR, '.header-cell.group')
                _due_on_locator = (
                    By.CSS_SELECTOR, 'time')
                _score_sort_locator = (
                    By.CSS_SELECTOR, '.sortable:first-child')
                _progress_sort_locator = (
                    By.CSS_SELECTOR, '.sortable:last-child')
                _assignment_average_locator = (
                    By.CSS_SELECTOR, '.average , .click-rate')
                _review_assignment_locator = (
                    By.CSS_SELECTOR, 'a')

                @property
                def assignment_type(self):
                    """Return the assignment type.

                    :return: the assignment type
                    :rtype: str

                    """
                    return (self.find_element(*self._assignment_type_locator)
                            .get_attribute('data-assignment-type'))

                @property
                def name(self):
                    """Return the assignment name.

                    :return: the assignment name
                    :rtype: str

                    """
                    return (self.find_element(*self._assignment_type_locator)
                            .text)

                @property
                def due_on(self):
                    """Return the date the assignment is or was due.

                    :return: the assignment due date as a 'month/date' string
                    :rtype: str

                    """
                    return self.find_element(*self._due_on_locator).text

                @property
                def score_sort(self):
                    r"""Return the score sort toggle button.

                    :return: the assignment score sort toggle
                    :rtype: :py:class:`~selenium.webdriver.remote \
                                       .webelement.WebElement`

                    """
                    if self.assignment_type == Tutor.EXTERNAL:
                        return None
                    return self.find_element(*self._score_sort_locator)

                def sort_by_score(self):
                    """Sort the table by the assignment scores.

                    :return: the scores table sorted by the assignment scores
                    :rtype: :py:class:`Scores`

                    """
                    if self.assignment_type != Tutor.EXTERNAL:
                        Utility.click_option(self.driver,
                                             element=self.score_sort)
                        sleep(0.5)
                    return self.page.page.page

                @property
                def scores_sorted(self):
                    """Return the sort type currently on the name column.

                    :return: what sort option is affecting the name column
                    :rtype: :py:data:`~utils.tutor.Tutor.ASCENDING` or
                        :py:data:`~utils.tutor.Tutor.DESCENDING` or
                        :py:data:`~utils.tutor.Tutor.NO_SORT`

                    """
                    if self.assignment_type != Tutor.EXTERNAL:
                        current_sort = self.score_sort.get_attribute('class')
                        if Tutor.ASCENDING in current_sort:
                            return Tutor.ASCENDING
                        elif Tutor.DESCENDING in current_sort:
                            return Tutor.DESCENDING
                    # the default is in place without a sort class on the
                    # column or the assignment is an external without a score
                    return Tutor.NO_SORT

                @property
                def progress_sort(self):
                    r"""Return the progress sort toggle button.

                    :return: the assignment progress sort toggle
                    :rtype: :py:class:`~selenium.webdriver.remote \
                                       .webelement.WebElement`

                    """
                    return self.find_element(*self._score_sort_locator)

                def sort_by_progress(self):
                    """Sort the table by the assignment progress.

                    :return: the scores table sorted by the assignment progress
                    :rtype: :py:class:`Scores`

                    """
                    Utility.click_option(self.driver, element=self.score_sort)
                    sleep(0.5)
                    return self.page.page.page

                @property
                def progress_sorted(self):
                    """Return the sort type currently on the progress column.

                    :return: what sort option is affecting the progress column
                    :rtype: :py:data:`~utils.tutor.Tutor.ASCENDING` or
                        :py:data:`~utils.tutor.Tutor.DESCENDING` or
                        :py:data:`~utils.tutor.Tutor.NO_SORT`

                    """
                    current_sort = self.progress_sort.get_attribute('class')
                    if Tutor.ASCENDING in current_sort:
                        return Tutor.ASCENDING
                    elif Tutor.DESCENDING in current_sort:
                        return Tutor.DESCENDING
                    # the default is in place without a sort class on the
                    # column
                    return Tutor.NO_SORT

                @property
                def assignment_average(self):
                    """Return the assignment average.

                    :return: the assignment average for readings and homeworks
                        or the click-on-time percentage for externals
                    :rtype: int

                    """
                    average = self.find_element(
                        *self._assignment_average_locator).text
                    return _average_helper(average.split()[0])

                def review_assignment(self):
                    """Click on the 'Review' link to view the metrics.

                    :return: the review metrics page for the assignment or the
                        scores page for externals
                    :rtype: :py:class:`~pages.tutor.review.Metrics` or
                        :py:class:`Scores`

                    """
                    if self.assignment_type == Tutor.EXTERNAL:
                        return self.page.page.page
                    link = self.find_element(*self._review_assignment_locator)
                    Utility.click_option(self.driver, element=link)
                    from pages.tutor.review import Metrics
                    return go_to_(
                        Metrics(self.driver,
                                base_url=self.page.page.page.base_url))

        class Student(Region):
            """A student row."""

            _name_locator = (By.CSS_SELECTOR, '.-name')
            _student_id_locator = (By.CSS_SELECTOR, '.student-id')
            _performance_forecast_link_locator = (
                By.CSS_SELECTOR, 'a.name-cell')
            _course_average_locator = (By.CSS_SELECTOR, '.course')
            _homework_score_locator = (By.CSS_SELECTOR, '.homework .score')
            _homework_progress_locator = (
                                    By.CSS_SELECTOR, '.homework .completed')
            _reading_score_locator = (By.CSS_SELECTOR, '.reading .score')
            _reading_progress_locator = (
                                    By.CSS_SELECTOR, '.reading .completed')
            _assignment_locator = (
                By.CSS_SELECTOR,
                '[class*="cellGroupWrapper"]:nth-child(2) ' +
                '.public_fixedDataTableCell_main')

            @property
            def name(self):
                """Return the student's name.

                :return: the student's name
                :rtype: str

                """
                return self.find_element(*self._name_locator).text

            @property
            def student_id(self):
                """Return the student's ID number.

                :return: the student's ID number
                :rtype: str

                """
                return self.find_element(*self._student_id_locator).text

            def performance_forecast(self) -> PerformanceForecast:
                r"""View the performance forecast for the student.

                :return: the performance forecast for the individual student
                :rtype: :py:class:`~pages.tutor \
                                   .performance.PerformanceForecast`

                """
                link = self.find_element(
                    *self._performance_forecast_link_locator)
                Utility.click_option(self.driver, element=link)
                return go_to_(
                    PerformanceForecast(
                        self.driver, base_url=self.page.page.base_url))

            @property
            def course_average(self):
                """Return the student's course average.

                :return: the student's current course grade or N/A if
                    unavailable
                :rtype: int or str

                """
                average = self.find_element(*self._course_average_locator).text
                return _average_helper(average)

            @property
            def homework_score(self):
                """Return the student's homework score average.

                :return: the student's current homework score average or N/A if
                    unavailable
                :rtype: int or str

                """
                average = self.find_element(*self._homework_score_locator).text
                return _average_helper(average)

            @property
            def homework_progress(self):
                """Return the student's homework progress average.

                :return: the student's current progress score average or N/A is
                    unavailable
                :rtype: int or str

                """
                average = (self.find_element(*self._homework_progress_locator)
                           .text)
                return _average_helper(average)

            @property
            def reading_score(self):
                """Return the student's reading score average.

                :return: the student's current reading score average or N/A if
                    unavailable
                :rtype: int or str

                """
                average = self.find_element(*self._reading_score_locator).text
                return _average_helper(average)

            @property
            def reading_progress(self):
                """Return the student's reading progress average.

                :return: the student's current reading progress average or N/A
                    if unavailable
                :rtype: int or str

                """
                average = (self.find_element(*self._reading_progress_locator)
                           .text)
                return _average_helper(average)

            @property
            def assignments(self):
                """Access the individual student assignments.

                :return: a list of student assignment performance results
                :rtype: list(:py:class:`~Scores.Table.Student.Assignment`)

                """
                return [self.Assignment(self, assignment)
                        for assignment
                        in self.find_elements(*self._assignment_locator)]

            class Assignment(Region):
                """A student assignment result."""

                _student_work_locator = (By.CSS_SELECTOR, 'a')
                _score_locator = (By.CSS_SELECTOR, '.correct-score , a span')
                _tooltip_locator = (By.CSS_SELECTOR, '.worked')
                _late_work_locator = (By.CSS_SELECTOR, '.late-caret')

                @property
                def assignment_type(self):
                    """Return the assignment type.

                    :return: the assignment type
                    :rtype: str

                    """
                    return (self.find_element(*self._student_work_locator)
                            .get_attribute('data-assignment-type'))

                @property
                def score(self):
                    """Return the assignment score.

                    :return: the assignment score, whether an external has been
                        clicked, or dashes if no work has been done
                    :rtype: int or str

                    """
                    average = self.find_element(*self._score_locator).text
                    return _average_helper(average)

                def view_student_work(self):
                    """Click on the score to view the student's work.

                    :return: the instructor's view of the student's assignment
                        or the scores page is no work has been done
                    :rtype: :py:class:`~pages.tutor.task.External` or
                        :py:class:`~pages.tutor.task.Homework` or
                        :py:class:`~pages.tutor.task.Reading` or
                        :py:class:`Scores`

                    :raises :py:class:`~utils.tutor.TutorException`: if the
                        assignment type isn't known (external, homework, or
                        reading)

                    """
                    try:
                        link = self.find_element(*self._student_work_locator)
                    except NoSuchElementException:
                        return self.page.page.page
                    _type = self.assignment_type
                    Utility.click_option(self.driver, element=link)
                    if _type == Tutor.EXTERNAL:
                        from pages.tutor.task import External as Destination
                    elif _type == Tutor.HOMEWORK:
                        from pages.tutor.task import Homework as Destination
                    elif _type == Tutor.READING:
                        from pages.tutor.task import Reading as Destination
                    else:
                        raise TutorException(
                            '"{0}" is not a known assignment type'
                            .format(_type))
                    return go_to_(
                        Destination(self.driver,
                                    base_url=self.page.page.page.base_url))

                @property
                def has_late_work(self):
                    """Return True if the assignment has late work.

                    :return: ``True`` if the student worked at least part of
                        the assignment after the assignment came due, else
                        ``False``
                    :rtype: bool

                    """
                    return bool(self.find_elements(*self._late_work_locator))

                def view_late_work_tooltip(self):
                    """Click on the late work caret.

                    Click on the late work caret to open the late work tooltip.

                    :return: the late work pop over tooltip
                    :rtype: :py:class:`LateWork`

                    """
                    try:
                        link = self.find_element(*self._late_work_locator)
                    except NoSuchElementException:
                        return self.page.page.page
                    Utility.click_option(self.driver, element=link)
                    sleep(0.25)
                    popover_root = self.driver.execute_script(
                        'return document.querySelector('
                        '".late-work-info-popover");')
                    return LateWork(self.page.page.page, popover_root)

                @property
                def late_work_accepted(self):
                    """Return True if the late work has been accepted.

                    :return: ``True`` if an instructor has accepted the late
                        work as the new grade, else ``False``
                    :rtype: bool

                    """
                    try:
                        late_work = self.find_element(*self._late_work_locator)
                    except NoSuchElementException:
                        return False
                    return 'accepted' in late_work.get_attribute('class')

                def progress_tooltip(self):
                    """Hover over progress and save the tooltip info.

                    :return: the progress information
                    :rtype: TODO

                    """
                    raise NotImplementedError("progress_tooltip: TODO")
