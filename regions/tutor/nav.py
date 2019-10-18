"""Tutor shared region nav bar."""

import re
from time import sleep

from pypom import Region
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from utils.tutor import TutorException
from utils.utilities import Utility, go_to_, go_to_external_


class Menu(Region):
    """A Tutor nav bar menu."""

    _toggle_locator = (By.CSS_SELECTOR, 'button')

    def toggle(self):
        """Open or close a nav menu."""
        Utility.scroll_top(self.driver)
        menu = self.find_element(*self._toggle_locator)
        Utility.safari_exception_click(self.driver, element=menu)
        sleep(0.15)
        return self

    @property
    def is_open(self):
        """Return True if the menu is open."""
        return 'show' in self.root.get_attribute('class')

    def _select(self, locator, destination=None, external=False, file=False):
        """Select a menu option."""
        # Open the menu if it isn't already
        if not self.is_open:
            self.toggle()
        target = self.find_element(*locator)
        url = target.get_attribute('href')
        if external:
            # Go to the external site and wait for load;
            # pass the destination URL in case the external
            # site fails to load
            Utility.switch_to(self.driver, element=target)
            if file:
                # The target is a file for download so skip
                # the wait for page load
                return
            return go_to_external_(destination(self.driver), url)
        # Go to the internal site and wait for load; pass
        # the Page base URL (attached to the Page, not the
        # parent Region) so Page.open() can work
        Utility.safari_exception_click(self.driver, element=target)
        if destination:
            return go_to_(destination(self.driver, self.page.page.base_url))


class TutorNav(Region):
    """Tutor nav bar region for logged in users."""

    _root_locator = (By.CSS_SELECTOR, '.tutor-top-navbar')

    # Main buttons on the nav
    _openstax_logo_locator = (By.CSS_SELECTOR, '.ui-brand-logo')
    _help_menu_locator = (By.CSS_SELECTOR, '.support-menu')
    _student_payment_locator = (By.CSS_SELECTOR, '.student-pay-now')
    _action_menu_locator = (By.CSS_SELECTOR, '.actions-menu')
    _account_menu_locator = (By.CSS_SELECTOR, '.user-menu')

    @property
    def logo(self):
        """Return the OpenStax Tutor Beta logo."""
        return self.find_element(*self._openstax_logo_locator)

    def go_to_dashboard(self):
        """Click on the OpenStax Tutor Beta logo."""
        Utility.safari_exception_click(self.driver, element=self.logo)
        sleep(0.5)
        if 'dashboard' in self.driver.current_url:
            # The user has multiple courses and ends up at
            # the course picker page
            from pages.tutor.dashboard import Dashboard
            return go_to_(Dashboard(self.driver, self.page.base_url))
        # The student has a single course and ends up on
        # their This Week course view
        from pages.tutor.course import Course
        return go_to_(Course(self.driver, self.page.base_url))

    @property
    def help(self):
        """Access the 'Help' menu."""
        root = self.find_element(*self._help_dropdown_locator)
        return self.Help(self, root)

    @property
    def student_access(self):
        """Access the student payment information."""
        try:
            root = self.find_element(*self._student_payment_locator)
            return self.Payment(self, root)
        except WebDriverException:
            raise TutorException('No active trial')

    @property
    def menu(self):
        """Access the action menu."""
        root = self.find_element(*self._action_menu_locator)
        return self.Action(self, root)

    @property
    def user(self):
        """Access the user menu."""
        root = self.find_element(*self._account_menu_locator)
        return self.User(self, root)

    class Help(Menu):
        """The Help options."""

        _page_tips_locator = (
            By.CSS_SELECTOR, '.page-tips')
        _help_articles_locator = (
            By.CSS_SELECTOR, '.-help-link:first-child')
        _getting_started_locator = (
            By.CSS_SELECTOR, '.support-document-link')
        _best_practices_locator = (
            By.CSS_SELECTOR, '.best-practices-guide')
        _accessibility_statement_locator = (
            By.CSS_SELECTOR, '[href*=accessibility]')
        _chat_support_enabled_locator = (
            By.CSS_SELECTOR, '.chat.enabled')
        _chat_support_disabled_locator = (
            By.CSS_SELECTOR, '.chat.disabled span')

        def view_page_tips(self):
            """Trigger the current page's user tips."""
            self._select(locator=self._page_tips_locator)
            return self.page.page.page_tips()

        def view_help_articles(self):
            """Select the Help Articles menu option."""
            from pages.salesforce.home import Salesforce
            return self._select(locator=self._page_tips_locator,
                                destination=Salesforce,
                                external=True)

        @property
        def guide_url(self):
            """Return the Getting Started guide URL."""
            return (self.find_element(*self._getting_started_locator)
                    .get_attribute('href'))

        def view_getting_started_guide(self):
            """Download the Getting Started guide."""
            return self._select(locator=self._getting_started_locator,
                                external=True,
                                file=True)

        def verify_getting_started_guide(self, user_type='student'):
            """Test the guide URL."""
            url = self.guide_url
            filename = url.split('/')[-1]
            assert(user_type in filename), (
                'Wrong user guide (expected {user} to be in {filename})'
                .format(user=user_type, filename=filename))
            return Utility.test_url_and_warn(url=url,
                                             message='Getting Started guide',
                                             driver=self.driver)

        @property
        def best_practices_url(self):
            """Return the Best Practices guide URL."""
            return (self.find_element(*self._best_practices_locator)
                    .get_attribute('href'))

        def view_best_practices_guide(self):
            """Download the Best Practices guide."""
            return self._select(locator=self._best_practices_locator,
                                external=True,
                                file=True)

        def verify_best_practices_guide(self):
            """Test the guide URL."""
            return Utility.test_url_and_warn(url=self.best_practices_url,
                                             message='Best Practices guide',
                                             driver=self.driver)

        def view_accessibility_statement(self):
            """View the Accessibility Statement."""
            from pages.tutor.accessibility import Accessibility
            return self._select(locator=self._accessibility_statement_locator,
                                destination=Accessibility)

        @property
        def chat_available(self):
            """Return True if the customer support chat is available."""
            chat_enabled = self.find_element(
                *self._chat_support_enabled_locator)
            return self.driver.execute_script(
                'return arguments[0].style.display != "none";', chat_enabled)

        @property
        def chat_unavailable(self):
            """Return the chat offline message."""
            if not self.chat_available:
                return (self.find_element(*self._chat_support_disabled_locator)
                        .text)
            raise TutorException('Chat is currently available')

        def chat_with_support(self):
            """Begin a customer support chat session."""
            if self.chat_available:
                from pages.tutor.chat import Chat
                self._select(locator=self._chat_support_enabled_locator,
                             destination=Chat,
                             external=True)
            raise TutorException('Chat is not currently available')

    class Payment(Region):
        """Student trial and payment messaging."""

        _pay_now_locator = (By.CSS_SELECTOR, '.btn-primary')

        @property
        def status(self):
            """Return the trial status message."""
            return self.root.text

        @property
        def days_remaining(self):
            """Return the number of days remaining in the student trial."""
            status = self.status
            days = re.findall(r"\d+", status)
            assert(days), 'No number found ({0})'.format(status)
            return int(days[0])

        def pay_now(self):
            """Click the 'Pay now' button."""
            button = self.find_element(*self._pay_now_locator)
            Utility.safari_exception_click(self.driver, element=button)
            from regions.tutor.purchase import Purchase
            return Purchase(self.page.page)

    class Action(Menu):
        """User action options."""

        _my_courses_locator = (
            By.CSS_SELECTOR, '[data-name=myCourses]')
        _dashboard_locator = (
            By.CSS_SELECTOR, '[data-name=dashboard]')
        _browse_the_book_locator = (
            By.CSS_SELECTOR, '[name=browseBook]')
        _scores_locator = (
            By.CSS_SELECTOR, '[data-name=viewScores]')
        _performance_forecast_locator = (
            By.CSS_SELECTOR, '[data-name=viewPerformanceGuide]')
        _change_student_id_locator = (
            By.CSS_SELECTOR, 'data-name=changeStudentId]')
        _question_library_locator = (
            By.CSS_SELECTOR, '[data-name=viewQuestionsLibrary]')
        _course_settings_locator = (
            By.CSS_SELECTOR, '[data-name=courseSettings]')
        _course_roster_locator = (
            By.CSS_SELECTOR, '[data-name=courseRoster]')
        _create_a_course_locator = (
            # By.CSS_SELECTOR, '[data-item=createCourse]')
            By.XPATH,
            '//a[div[contains(@data-tour-anchor-id,"createNewCourse")]]')
        _copy_this_course_locator = (
            # By.CSS_SELECTOR, '[data-item=cloneCourse]')
            By.XPATH,
            '//a[div[contains(@data-tour-anchor-id),"clone-course"]]')
        _manage_payments_locator = (
            By.CSS_SELECTOR, '[data-name=managePayments]')
        _customer_service_locator = (
            By.CSS_SELECTOR, '[data-name=customer_service]')
        _admin_console_locator = (
            By.CSS_SELECTOR, '[data-name=admin]')
        _qa_dashboard_locator = (
            By.CSS_SELECTOR, '[data-name=QADashboard]')
        _content_analyst_locator = (
            By.CSS_SELECTOR, '[data-name=qaHome]')

        def view_my_courses(self):
            """Go to My Courses.

            See TutorNav.go_to_dashboard()
            Most users will be taken to the course picker.
            Students with one course will be taken to their course page.
            """
            self._select(locator=self._my_courses_locator)
            sleep(0.5)
            if 'dashboard' in self.driver.current_url:
                from pages.tutor.dashboard import Dashboard
                return go_to_(Dashboard(self.driver, self.page.page.base_url))
            from pages.tutor.course import Course
            return go_to_(Course(self.driver, self.page.page.base_url))

        def view_dashboard(self):
            """Go to the Dashboard.

            Instructors will be taken to the calendar.
            Students will be taken to their course page.
            """
            self._select(locator=self._dashboard_locator)
            sleep(0.5)
            if 'month' in self.driver.current_url:
                from pages.tutor.course import Calendar as Course
            else:
                from pages.tutor.course import Course
            return go_to_(Course(self.driver, self.page.page.base_url))

        def browse_the_book(self):
            """Open the book's reference view."""
            from pages.tutor.reference import Reference
            return self._select(locator=self._browse_the_book_locator,
                                destination=Reference,
                                external=True)

        def view_student_scores(self):
            """View the scores table."""
            from pages.tutor.scores import Scores
            return self._select(locator=self._scores_locator,
                                destination=Scores)

        def view_the_performance_forecast(self):
            """View the performance forecast."""
            from pages.tutor.performance import PerformanceForecast
            return self._select(locator=self._performance_forecast_locator,
                                destination=PerformanceForecast)

        def change_student_id(self):
            """Go to the ID change page."""
            from pages.tutor.student_id import ChangeID
            return self._select(locator=self._change_student_id_locator,
                                destination=ChangeID)

        def view_the_question_library(self):
            """Go to the ."""
            from pages.tutor.question_library import QuestionLibrary
            return self._select(locator=self._question_library_locator,
                                destination=QuestionLibrary)

        def view_the_course_settings(self):
            """Go to the course settings."""
            from pages.tutor.settings import CourseSettings
            return self._select(locator=self._course_settings_locator,
                                destination=CourseSettings)

        def view_the_course_roster(self):
            """Go to the course roster."""
            from pages.tutor.roster import CourseRoster
            return self._select(locator=self._course_roster_locator,
                                destination=CourseRoster)

        def create_a_course(self):
            """Go to course creation."""
            from pages.tutor.course_creation import CreateCourse
            return self._select(locator=self._create_a_course_locator,
                                destination=CreateCourse)

        def copy_this_course(self):
            """Clone the current course."""
            from pages.tutor.course_creation import CloneCourse
            return self._select(locator=self.self._create_a_course_locator,
                                destination=CloneCourse)

        def manage_payments(self):
            """Manage payments."""
            from pages.tutor.payments import PaymentManagement
            return self._select(locator=self._manage_payments_locator,
                                destination=PaymentManagement)

        def view_the_customer_service_board(self):
            """Open the customer service console."""
            from pages.tutor.admin import CustomerService
            return self._select(locator=self._customer_service_locator,
                                destination=CustomerService)

        def view_the_admin_console(self):
            """Go to the administrator's console."""
            from pages.tutor.admin import AdminConsole
            return self._select(locator=self._admin_console_locator,
                                destination=AdminConsole)

        def view_the_qa_dashboard(self):
            """Go to the QA dashboard."""
            from pages.tutor.qa import QAConsole
            return self._select(locator=self._qa_dashboard_locator,
                                destination=QAConsole)

        def view_the_content_analyst_board(self):
            """Go to the content analyst console."""
            from pages.tutor.content import ContentAnalystConsole
            return self._select(locator=self._content_analyst_locator,
                                destination=ContentAnalystConsole)

    class User(Menu):
        """User account information."""

        _initials_locator = (By.CSS_SELECTOR, '.initials')
        _my_account_locator = (By.CSS_SELECTOR, '[href$=profile]')
        _log_out_locator = (By.CSS_SELECTOR, '.logout')

        @property
        def initials(self):
            """Return the user's initials displayed in the user menu dot.

            Initials are case sensitive matching Accounts.
            """
            return self.find_element(*self._initials_locator).text.strip()

        def view_my_account(self):
            """View the user's profile on Accounts."""
            from pages.accounts.profile import Profile
            return self._select(locator=self._my_account_locator,
                                destination=Profile,
                                external=True)

        def log_out(self):
            """Log the current user out of Tutor."""
            from pages.tutor.home import TutorHome
            return self._select(locator=self._log_out_locator,
                                destination=TutorHome)
