"""The instructor's course settings page."""

from time import sleep

from pypom import Region
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.tutor.base import TutorBase
from utils.tutor import Tutor, TutorException
from utils.utilities import Utility, go_to_

# a javascript query to get the modal and tooltip root that is a neighbor of
# the React root element
GET_ROOT = 'return document.querySelector("[role={0}]");'


# -------------------------------------------------------- #
# Regions shared between the pages and the modals
# -------------------------------------------------------- #

class Component(Region):
    """A key or other data needed for LMS integration."""

    _data_value_locator = (By.CSS_SELECTOR, 'input')

    @property
    def name(self):
        """Return the component's name.

        :return: the component name
        :rtype: str

        """
        return self.root.text

    @property
    def value(self):
        """Return the key value or URL of the component.

        :return: the value of the component
        :rtype: str

        """
        return (self.find_element(*self._data_value_locator)
                .get_attribute('value'))


class Section(Region):
    """Section information."""

    _enrollment_url_locator = (By.CSS_SELECTOR, 'input')

    @property
    def name(self):
        """Return the section name.

        :return: the section or period name
        :rtype: str

        """
        return self.root.text

    @property
    def enrollment_url(self):
        """Return the enrollment URL for the section or period.

        :return: the enrollment URL
        :rtype: str

        """
        return (self.find_element(*self._enrollment_url_locator)
                .get_attribute('value'))


class Tab(Region):
    """A section tab."""

    _name_locator = (By.CSS_SELECTOR, 'h2')
    _select_tab_locator = (By.CSS_SELECTOR, 'a')

    @property
    def name(self):
        """Return the name listed on the tab.

        :return: the name of the tab
        :rtype: str

        """
        return self.find_element(*self._name_locator).text

    @property
    def is_open(self):
        """Return True if the tab is currently selected.

        :return: ``True`` if the tab is currently active, else ``False``
        :rtype: bool

        """
        return 'active' in self.root.get_attribute('class')

    def select(self):
        """Click on the tab to open it.

        :return: the course settings page
        :rtype: :py:class:`CourseSettings`

        """
        tab = self.find_element(*self._select_tab_locator)
        Utility.click_option(self.driver, element=tab)
        sleep(0.25)
        return self.page


class Vendor(Region):
    """An LMS vendor."""

    _short_name_locator = (By.CSS_SELECTOR, 'input')

    @property
    def company(self):
        """Return the LMS vendor's company name.

        :return: the LMS company name
        :rtype: str

        """
        return self.root.text

    @property
    def short_name(self):
        """Return the internal vendor short name.

        :return: the LMS company short name
        :rtype: str

        """
        return (self.find_element(*self._short_name_locator)
                .get_attribute('value'))

    @property
    def is_active(self):
        """Return True if the LMS vendor is currently selected.

        :return: ``Ture`` if the vendor is currently selected else ``False``
        :rtype: bool

        """
        return 'active' in self.root.get_attribute('class')


# -------------------------------------------------------- #
# Course settings modals
# -------------------------------------------------------- #

class CourseSettingsModal(Region):
    """The base model for course settings modals."""

    _title_locator = (By.CSS_SELECTOR, '.modal-title')
    _close_x_locator = (By.CSS_SELECTOR, '.close')
    _close_locator = (By.CSS_SELECTOR, '.modal-footer button:last-child')

    @property
    def title(self):
        """Return the modal title."""
        return self.find_element(*self._title_locator).text

    def close(self, x_button=False):
        """Click the 'Close', 'Cancel', 'Rename', 'Save', or 'x' button.

        :param bool x_button: if ``True`` use the 'x' button in the upper right
            of the modal, otherwise use the footer button
        :return: the course settings page
        :rtype: :py:class:`CourseSettings`

        """
        locator = self._close_x_locator if x_button else self._close_locator
        button = self.find_element(*locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.25)
        return self.page


class ChangeCourseTimezone(CourseSettingsModal):
    """The timezone change modal."""

    _timezone_radio_locator = (By.CSS_SELECTOR, '.tutor-radio')
    _active_timezone_locator = (By.CSS_SELECTOR, '.tutor-radio.active')
    _time_preview_locator = (By.CSS_SELECTOR, '.timezone-preview')

    @property
    def timezones(self):
        """Access the available timezones for the course.

        :return: the list of available timezones
        :rtype: list(:py:class:`~ChangeCourseTimezone.Timezone`)

        """
        return [self.Timezone(self, zone)
                for zone in self.find_elements(*self._timezone_radio_locator)]

    @property
    def active(self):
        """Return the currently selected timezone.

        :return: the current timezone in use by the course
        :rtype: :py:class:`~ChangeCourseTimezone.Timezone`

        """
        current_timezone = self.find_element(*self._active_timezone_locator)
        return self.Timezone(self, current_timezone)

    def select_timezone(self, timezone=Tutor.CENTRAL_TIME):
        """Select a timezone from the available radio options.

        :param str timezone: (optional) the new timezone, defaults to
            :py:data:`~utils.tutor.Tutor.CENTRAL_TIME`
        :return: the timezone modal
        :rtype: :py:class:`ChangeCourseTimezone`

        :raise :py:class:`utils.tutor.TutorException`: if the timezone does not
            match an available option

        """
        for zone in self.timezones:
            if zone.name == timezone:
                zone.select()
                return self
        raise TutorException('"{0}" is not a known timezone'.format(timezone))

    @property
    def preview(self):
        """Return the preview time if using the selected timezone.

        :return: the preview time format if the selected timezone is accepted
        :rtype: str

        """
        return self.find_element(*self._time_preview_locator).text

    def save(self):
        """Click on the Save button.

        :return: the course settings page
        :rtype: :py:class:`CourseSettings`

        """
        return self.close(x_button=False)

    class Timezone(Region):
        """A timezone option for a course."""

        _name_locator = (By.CSS_SELECTOR, 'label')
        _button_locator = (By.CSS_SELECTOR, 'input')

        @property
        def name(self):
            """Return the timezone name or region name.

            :return: the name or affected region for the timezone setting
            :rtype: str

            """
            return self.find_element(*self._name_locator).text

        def select(self):
            """Click on the timezone radio button.

            :return: the timezone modal
            :rtype: :py:class:`ChangeCourseTimezone`

            """
            button = self.find_element(*self._button_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.25)  # to allow the preview time to update
            return self.page

        def is_current(self):
            """Return True if the timezone is currently selected.

            :return: ``True`` if the timezone option is currently selected,
                else ``False``
            :rtype: bool

            """
            return 'active' in self.root.get_attribute('class')


class DirectLinks(CourseSettingsModal):
    """The use 'Direct links instead of LMS integration' modal."""

    _content_locator = (By.CSS_SELECTOR, '.modal-body')
    _im_sure_button_locator = (
        By.CSS_SELECTOR, '.modal-footer button:first-child')

    @property
    def description(self):
        """Return the modal body content.

        :return: the text explaining what will happen if LMS integration is
            deactivated
        :rtype: str

        """
        return self.find_element(*self._content_locator).text

    def im_sure(self):
        """Click on the "I'm sure" button.

        Clicking on the button switches the enrollment option back to 'Give
        students direct links' and closes the modal.

        :return: the course settings page
        :rtype: :py:class:`CourseSettings`

        """
        button = self.find_element(*self._im_sure_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.25)
        return self.page

    def cancel(self):
        """Click on the 'Cancel' button.

        Close the modal without changing the enrollment option.

        :return: the course settings page
        :rtype: :py:class:`CourseSettings`

        """
        return self.close(x_button=False)


class LMSKeyPairings(CourseSettingsModal):
    """Key pairings review modal."""

    _lms_option_locator = (By.CSS_SELECTOR, '.lms-access label.button')
    _instructions_locator = (By.CSS_SELECTOR, '.lms-access p')
    _integration_help_locator = (By.CSS_SELECTOR, '.external-icon')
    _control_locator = (By.CSS_SELECTOR, 'label.copy-on-focus')

    @property
    def lms_option(self):
        """Access the LMS vendor options.

        :return: the LMS vendor options
        :rtype: list(:py:class:`Vendor`)

        """
        return [Vendor(self, option)
                for option in self.find_elements(*self._lms_option_locator)]

    @property
    def instructions(self):
        """Return the integration instructions.

        :return: the basic LMS integration instructions
        :rtype: str

        """
        return self.find_element(*self._instructions_locator).text

    def how_do_i_integrate_with(self):
        """Access the Salesforce LMS integration walkthrough.

        :return: the LMS integration walkthrough on Salesforce
        :rtype: :py:class:`~pages.salesforce.home.Salesforce`

        """
        link = self.find_element(*self._integration_help_locator)
        Utility.switch_to(self.driver, element=link)
        from pages.salesforce.home import Salesforce
        return go_to_(Salesforce(self.driver))

    @property
    def controls(self):
        """Access the keys and values to use LMS integration.

        :return: the keys, secrets, URL controls necessary to integrate with
            the selected LMS system
        :rtype: list(:py:class:`Component`)

        """
        return [Component(self, value)
                for value in self.find_elements(*self._control_locator)]


class RenameCourse(CourseSettingsModal):
    """The course renaming modal."""

    _course_name_input_locator = (By.CSS_SELECTOR, 'input')

    @property
    def name(self):
        """Return the course name.

        :return: the current value of the course name input text box
        :rtype: str

        """
        return (self.find_element(*self._course_name_input_locator)
                .get_attribute('value'))

    @name.setter
    def name(self, name):
        """Change the course name.

        :param str name: the course's new name or title
        :return: the course rename modal
        :rtype: :py:class:`RenameCourse`
        :raises :py:class:`~utils.tutor.TutorException`: if name is not a valid
            course name (``bool(name) == False``)

        """
        if not name:
            raise TutorException('"{0}" is not a valid course name'
                                 .format(name))
        field = self.find_element(*self._course_name_input_locator)
        Utility.clear_field(self.driver, field=field)
        sleep(0.25)
        field.send_keys(name)
        return self

    def rename(self):
        """Click on the 'Rename' button.

        :return: the course settings page with the new course title displayed
        :rtype: :py:class:`CourseSettings`

        """
        return self.close(x_button=False)


# -------------------------------------------------------- #
# The Course Settings page
# -------------------------------------------------------- #

class CourseSettings(TutorBase):
    """The Tutor course settings page."""

    _page_title_locator = (By.CSS_SELECTOR, '.title')
    _course_name_locator = (By.CSS_SELECTOR, '.course-settings-title')
    _edit_course_name_button_locator = (
        By.CSS_SELECTOR, '.course-settings-title button')
    _tab_locator = (By.CSS_SELECTOR, '[role=tab] a')
    _active_page_tab_locator = (By.CSS_SELECTOR, '.nav-tabs li.active h2')
    _course_term_locator = (By.CSS_SELECTOR, '.course-settings-term')
    _settings_body_locator = (
        By.CSS_SELECTOR, '.student-access , .dates-and-times')

    @property
    def page_title(self):
        """Return the page title.

        :return: the page title
        :rtype: str

        """
        return self.find_element(*self._page_title_locator).text

    @property
    def course_name(self):
        """Return the course name.

        :return: the course name
        :rtype: str

        """
        return self.find_element(*self._course_name_locator).text

    def edit_course_name(self):
        """Click on the edit icon next to the course name.

        :return: the course rename modal
        :rtype: :py:class:`RenameCourse`

        """
        button = self.find_element(*self._edit_course_name_button_locator)
        Utility.click_option(self.driver, element=button)
        sleep(0.25)
        modal_root = self.driver.execute_script(GET_ROOT.format('dialog'))
        return RenameCourse(self, modal_root)

    @property
    def tabs(self):
        """Access the page tabs.

        :return: the student access and dates and time tabs
        :rtype: list(:py:class:`Tab`)

        """
        return [Tab(self, option)
                for option in self.find_elements(*self._tab_locator)]

    @property
    def term(self):
        """Return the course term.

        :return: the course term
        :rtype: str

        """
        return self.find_element(*self._course_term_locator).text

    @property
    def content(self):
        """Access the main page content.

        :return: the student access content or the dates and times content
        :rtype: :py:class:`~CourseSettings.StudentAccess` or
            :py:class:`~CourseSettings.DatesAndTime`

        """
        active = self.find_element(*self._active_page_tab_locator).text.lower()
        body_root = self.find_element(*self._settings_body_locator)
        if 'dates' in active:
            return self.StudentAccess(self, body_root).panel
        return self.DatesAndTime(self, body_root)

    class StudentAccess(Region):
        """The course settings student access panel split.

        This is a pass-through region to select the correct setup for the
        course.

        """

        _lms_disabled_locator = (By.CSS_SELECTOR, '.direct-links-only')
        _lms_enabled_with_enrolled_locator = (By.CSS_SELECTOR, '.enrolled')
        _lms_enabled_without_enrolled_locator = (By.CSS_SELECTOR, '.card-body')

        @property
        def panel(self):
            """Return the correct subclass panel.

            :return: the subpanel according to the course settings
            :rtype: :py:class:`~CourseSettings.StudentAccess.DirectAccess` or
                :py:class:`~CourseSettings.StudentAccess.DirectLinksOnly` or
                :py:class:`~CourseSettings.StudentAccess.Enrolled` or
                :py:class:`~CourseSettings.StudentAccess.LMS`

            """
            try:
                self.find_element(*self._lms_disabled_locator)
                return self.DirectLinksOnly(self, self.root)
            except NoSuchElementException:
                try:
                    self.find_element(*self._lms_enabled_with_enrolled_locator)
                    return self.Enrolled(self, self.root)
                except NoSuchElementException:
                    enabled = self.find_elements(
                        *self._lms_enabled_without_enrolled_locator)
                    if Utility.has_children(enabled[1]):
                        return self.LMS(self, self.root)
                    else:
                        return self.DirectAccess(self, self.root)

        class DirectAccess(Region):
            """Direct student enrollment links."""

            _title_locator = (By.CSS_SELECTOR, '.title')
            _information_locator = (By.CSS_SELECTOR, '.info')
            _section_locator = (By.CSS_SELECTOR, '.card-body > label')

            @property
            def title(self):
                """Return the section title.

                :return: the panel section title
                :rtype: str

                """
                return self.find_element(*self._title_locator).text

            @property
            def information(self):
                """Return the enrollment information help text.

                :return: the direct link explanation text
                :rtype: str

                """
                return self.find_element(*self._information_locator).text

            @property
            def sections(self):
                """Access the individual section URLs.

                :return: the list of available section or period enrollment
                    URLs
                :rtype: list(:py:class:`Section`)

                """
                return [Section(self, section)
                        for section
                        in self.find_elements(*self._section_locator)]

        class DirectLinksOnly(Region):
            """The LMS option is not available for the course."""

            _integration_help_locator = (By.CSS_SELECTOR, '.external-icon')
            _section_locator = (By.CSS_SELECTOR, 'label')

            def find_out_more(self):
                """Access the Salesforce LMS integration overview.

                :return: the LMS integration walkthrough on Salesforce
                :rtype: :py:class:`~pages.salesforce.home.Salesforce`

                """
                link = self.find_element(*self._integration_help_locator)
                Utility.switch_to(self.driver, element=link)
                from pages.salesforce.home import Salesforce
                return go_to_(Salesforce(self.driver))

            @property
            def sections(self):
                """Access the individual section URLs.

                :return: the list of available section or period enrollment
                    URLs
                :rtype: list(:py:class:`Section`)

                """
                return [Section(self, section)
                        for section
                        in self.find_elements(*self._section_locator)]

        class Enrolled(Region):
            """The LMS option is enabled and students have registered."""

            _explanation_locator = (By.CSS_SELECTOR, 'p')
            _show_lms_keys_locator = (By.CSS_SELECTOR, 'a')

            @property
            def explanation(self):
                """Return the enrollment explanation for LMS students.

                :return: the enrollment explanation for LMS students
                :rtype: str

                """
                return self.find_element(*self._explanation_locator).text

            def show_lms_keys_again(self):
                """Click the link and display the LMS key modal.

                :return: the LMS key modal
                :rtype: :py:class:`LMSKeyPairings`

                """
                link = self.find_element(*self._show_lms_keys_locator)
                Utility.click_option(self.driver, element=link)
                sleep(0.25)
                modal_root = self.driver.execute_script(
                    GET_ROOT.format('dialog'))
                return LMSKeyPairings(self.page.page, modal_root)

        class LMS(Region):
            """LMS access."""

            _title_locator = (By.CSS_SELECTOR, '.title')
            _information_locator = (By.CSS_SELECTOR, '.info')
            _vendor_locator = (By.CSS_SELECTOR, '.lms-access label')
            _integration_help_locator = (
                By.CSS_SELECTOR, '.lms-access .external-icon')
            _control_locator = (By.CSS_SELECTOR, '.lms-access .copy-on-focus')

            @property
            def title(self):
                """Return the section title.

                :return: the panel section title
                :rtype: str

                """
                return self.find_element(*self._title_locator).text

            @property
            def information(self):
                """Return the enrollment information help text.

                :return: the direct link explanation text
                :rtype: str

                """
                return self.find_element(*self._information_locator).text

            @property
            def vendors(self):
                """Access the list of LMS vendors.

                :return: the list of available LMS providers
                :rtype: list(:py:class:`Vendor`)

                """
                return [Vendor(self, option)
                        for option
                        in self.find_elements(*self._vendor_locator)]

            def how_do_i_integrate_with(self):
                """Access the Salesforce LMS integration walkthrough.

                :return: the LMS integration walkthrough on Salesforce
                :rtype: :py:class:`~pages.salesforce.home.Salesforce`

                """
                link = self.find_element(*self._integration_help_locator)
                Utility.switch_to(self.driver, element=link)
                from pages.salesforce.home import Salesforce
                return go_to_(Salesforce(self.driver))

            @property
            def controls(self):
                """Access the keys and values to use LMS integration.

                :return: the keys, secrets, URL controls necessary to integrate
                    with the selected LMS system
                :rtype: list(:py:class:`Component`)

                """
                return [Component(self, value)
                        for value
                        in self.find_elements(*self._control_locator)]

    class DatesAndTime(Region):
        """The course settings dates and time panel."""

        _course_term_locator = (
            By.CSS_SELECTOR, '.dates-and-times div:first-child')
        _start_and_end_dates_locator = (
            By.CSS_SELECTOR, '.dates-and-times div:nth-child(2)')
        _timezone_locator = (
            By.CSS_SELECTOR, '.dates-and-times div:last-child')
        _edit_timezone_button_locator = (
            By.CSS_SELECTOR, '.dates-and-times button')

        @property
        def term(self):
            """Return the course term.

            :return: the course term
            :rtype: str

            """
            return self.find_element(*self._course_term_locator).text

        @property
        def course_dates(self):
            """Return the start and end date text.

            :return: the start and end date text string
            :rtype: str

            """
            return self.find_element(*self._start_and_end_dates_locator).text

        @property
        def start(self):
            """Return the course start date.

            :return: the course starting date string
            :rtype: str

            """
            return self.course_dates.split()[Tutor.START_DATE]

        @property
        def end(self):
            """Return the course end date.

            :return: the course ending date string
            :rtype: str

            """
            return self.course_dates.split()[Tutor.END_DATE]

        @property
        def timezone(self):
            """Return the assigned course timezone.

            :return: the course timezone
            :rtype: str

            """
            return self.find_element(*self._timezone_locator).text

        def edit_timezone(self):
            """Click on the edit icon nex to the course timezone.

            :return: the change course timezone modal
            :rtype: :py:class:`ChangeCourseTimezone`

            """
            button = self.find_element(*self._edit_timezone_button_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.25)
            modal_root = self.driver.execute_script(GET_ROOT.format('dialog'))
            return ChangeCourseTimezone(self.page, modal_root)
