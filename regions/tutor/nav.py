"""Tutor shared region nav bar."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.utils.utilities import Utility


class TutorNav(Region):
    """Tutor nav bar region for logged in users."""

    _root_locator = (By.CLASS_NAME, 'tutor-top-navbar')

    # Main buttons on nav
    _help_dropdown_locator = (By.CLASS_NAME, 'support-menu')
    _menu_dropdown_locator = (By.CLASS_NAME, 'actions-menu')
    _account_icon_locator = (By.CLASS_NAME, 'user-menu')
    _openstax_logo_locator = (By.CLASS_NAME, 'ui-brand-logo')

    # Buttons from account icon dropdown
    _my_account_locator = (By.CSS_SELECTOR, '.user-menu li a')
    _log_out_locator = (By.CLASS_NAME, 'logout')

    # Buttons from help dropdown (some are not available to students)
    _help_articles_locator = (By.PARTIAL_LINK_TEXT, 'Articles')
    _get_started_locator = (By.CLASS_NAME, 'support-document-link')
    _accessibility_statement_locator = (By.PARTIAL_LINK_TEXT, 'Accessibility')
    _chat_with_support_locator = (By.CLASS_NAME, 'chat')
    _page_tip_locator = (By.CLASS_NAME, 'page-tips')
    _preview_videos_locator = (By.ID, 'student-preview-videos')
    _best_practice_locator = (By.CLASS_NAME, 'best-practices-guide')

    # Buttons from menu dropdown that student and teacher share
    _my_courses_locator = (By.CLASS_NAME, 'myCourses')
    _dashboard_locator = (By.CLASS_NAME, 'dashboard')
    _scores_locator = (By.CLASS_NAME, 'viewScores')
    _browse_the_book_locator = (By.CSS_SELECTOR, '[name=browseBook]')
    _performance_forecast_locator = (By.CLASS_NAME, 'viewPerformanceGuide')

    # Buttons from students menu dropdown
    _manage_payments_locator = (By.CLASS_NAME, 'managePayments')
    _change_student_id_locator = (By.CLASS_NAME, 'changeStudentId')

    # Buttons from teacher menu dropdown
    _question_library_locator = (By.CLASS_NAME, 'viewQuestionsLibrary')
    _course_settings_locator = (By.CLASS_NAME, 'courseSettings')
    _course_roster_locator = (By.CLASS_NAME, 'courseRoster')
    _create_course_locator_ = (By.PARTIAL_LINK_TEXT, 'Create')
    _copy_this_course_locator = (By.PARTIAL_LINK_TEXT, 'Copy')

    # Account dropdown buttons
    def go_to_my_account(self):
        """Go to account profile for current user."""
        self.find_element(*self._account_icon_locator).click()
        Utility.switch_to(self.driver, *self._my_account_locator)
        from pages.accounts.profile import Profile
        return Profile(self.driver)

    def log_out(self):
        """Log out of current user."""
        self.find_element(*self._account_icon_locator).click()
        self.find_element(*self._log_out_locator).click()
        from pages.tutor.home import TutorHome
        return TutorHome(self.driver)

    # Help dropdown buttons
    def click_logo(self):
        """Click openstax logo to go back to tutor dashboard."""
        self.find_element(*self._openstax_logo_locator).click()
        from pages.tutor.dashboard import TutorDashboard
        return TutorDashboard(self.driver)

    def go_to_help_articles(self):
        """Go to tutor help articles."""
        self.find_element(*self._help_dropdown_locator).click()
        self.find_element(*self._help_articles_locator).click()
        from pages.salesforce.home import Salesforce
        return Salesforce(self.driver)

    def go_to_get_started(self):
        """Open tutor get started guide in a new tab."""
        self.find_element(*self._help_dropdown_locator).click()
        Utility.switch_to(self.driver, self._get_started_locator)

    def go_to_accessibility(self):
        """Go to tutor accessibility statement page."""
        self.find_element(*self._help_dropdown_locator).click()
        self.find_element(*self._accessibility_statement_locator).click()
        from pages.tutor.accessibility import Accessibility
        return Accessibility(self.driver)

    def go_to_chat(self):
        """Open tutor chat support in a new tab."""
        self.find_element(*self._help_dropdown_locator).click()
        Utility.switch_to(self.driver, self._chat_with_support_locator)

    def click_page_tips(self):
        """Start tutor page tips on current page as teacher."""
        self.find_element(*self._help_dropdown_locator).click()
        self.find_element(*self._page_tip_locator).click()

    def go_to_preview_videos(self):
        """Go to student preview videos for current course as teacher."""
        self.find_element(*self._help_dropdown_locator).click()
        self.find_element(*self._preview_videos_locator).click()

    def go_to_best_practices(self):
        """Open tutor best practices guide as teacher."""
        self.find_element(*self._help_dropdown_locator).click()
        Utility.switch_to(self.driver, self._best_practice_locator)

    # Menu functions
    def go_to_course_picker(self):
        """Go to tutor dashboard."""
        self.find_element(*self._menu_dropdown_locator).click()
        self.find_element(*self._my_courses_locator).click()
        from pages.tutor.dashboard import TutorDashboard
        return TutorDashboard(self.driver)

    def go_to_dashboard(self):
        """Go to the main course page of current course."""
        self.find_element(*self._menu_dropdown_locator).click()
        self.find_element(*self._dashboard_locator).click()
        from pages.tutor.course import TutorCourse
        return TutorCourse(self.driver)

    def go_to_scores(self):
        """Go to scores  page of current course."""
        self.find_element(*self._menu_dropdown_locator).click()
        self.find_element(*self._scores_locator).click()
        from pages.tutor.scores import Scores
        return Scores(self.driver)

    def click_browse_book(self):
        """Open the book of current course in a new tab."""
        self.find_element(*self._menu_dropdown_locator).click()
        Utility.switch_to(self.driver, self._browse_the_book_locator)

    def go_to_performance_forecast(self):
        """Go to performance forecast page of current course."""
        self.find_element(*self._menu_dropdown_locator).click()
        self.find_element(*self._performance_forecast_locator).click()
        from pages.tutor.performance import Performance
        return Performance(self.driver)

    def go_to_manage_payments(self):
        """Go to manage payments page as student."""
        self.find_element(*self._menu_dropdown_locator).click()
        self.find_element(*self._manage_payments_locator).click()
        from pages.tutor.payments import TutorPayments
        return TutorPayments(self.driver)

    def go_to_change_student_id(self):
        """Go to change id page of current course as student."""
        self.find_element(*self._menu_dropdown_locator).click()
        self.find_element(*self._change_student_id_locator).click()
        from pages.tutor.student_id import StudentID
        return StudentID(self.driver)

    def go_to_question_library(self):
        """Go to question library of current course as teacher."""
        self.find_element(*self._menu_dropdown_locator).click()
        self.find_element(*self._question_library_locator).click()
        from pages.tutor.question_library import QuestionLibrary
        return QuestionLibrary(self.driver)

    def go_to_course_settings(self):
        """Go to course settings of current course as teacher."""
        self.find_element(*self._menu_dropdown_locator).click()
        self.find_element(*self._course_settings_locator).click()
        from pages.tutor.settings import Settings
        return Settings(self.driver)

    def go_to_course_roster(self):
        """Go to course roster of current course as teacher."""
        self.find_element(*self._menu_dropdown_locator).click()
        self.find_element(*self._course_roster_locator).click()
        from pages.tutor.roster import Roster
        return Roster(self.driver)

    def go_to_create_course(self):
        """Go to create a new course page as teacher."""
        self.find_element(*self._menu_dropdown_locator).click()
        self.find_element(*self._create_course_locator_).click()
        from pages.tutor.new_course import NewCourse
        return NewCourse(self.driver)

    def go_to_copy_course(self):
        """Go to copy the current course page as teacher."""
        self.find_element(*self._menu_dropdown_locator).click()
        self.find_element(*self._copy_this_course_locator).click()
        from pages.tutor.new_course import NewCourse
        return NewCourse(self.driver)

