"""Break the signup process out of the base."""

from time import sleep

from pypom import Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.accounts import home, profile
from pages.accounts.base import AccountsBase
from pages.utils.email import Google, GoogleBase, GuerrillaMail
from pages.utils.utilities import Utility


class Signup(AccountsBase):
    """Signup process."""

    URL_TEMPLATE = '/signup'

    STUDENT = 'Student'
    INSTRUCTOR = 'Instructor'
    ADMINISTRATOR = 'Administrator'
    LIBRARIAN = 'Librarian'
    DESIGNER = 'Instructional Designer'
    OTHER = 'Other'

    TITLE = 0
    FIRST = 1
    LAST = 2
    SUFFIX = 3

    ADOPTED = 'Fully adopted and using it as the primary textbook'
    RECOMMENDED = 'Recommending the book – my students buy a different book'
    INTEREST = 'Interested in using OpenStax in the future'
    NOT_USING = 'Not using OpenStax'

    SUBJECTS = [
        ('accounting', 'Accounting'),
        ('algebra_and_trigonometry', 'Algebra and Trigonometry'),
        ('american_government', 'American Government'),
        ('anatomy_physiology', 'Anatomy and Physiology'),
        ('astronomy', 'Astronomy'),
        ('biology', 'Biology'),
        ('calculus', 'Calculus'),
        ('chemistry', 'Chemistry'),
        ('chem_atoms_first', 'Chemistry: Atoms First'),
        ('college_algebra', 'College Algebra'),
        ('college_physics_algebra', 'College Physics'),
        ('concepts_of_bio_non_majors', 'Concepts of Biology'),
        ('introduction_to_sociology', 'Introduction to Sociology 2e'),
        ('introductory_statistics', 'Introductory Statistics'),
        ('microbiology', 'Microbiology'),
        ('pre_algebra', 'Prealgebra'),
        ('precalc', 'Precalculus'),
        ('economics', 'Principles of Economics'),
        ('macro_econ', 'Principles of Macroeconomics'),
        ('ap_macro_econ', 'Principles of Macroeconomics for AP® Courses'),
        ('micro_econ', 'Principles of Microeconomics'),
        ('ap_micro_econ', 'Principles of Microeconomics for AP® Courses'),
        ('psychology', 'Psychology'),
        ('ap_physics', 'The AP Physics Collection'),
        ('us_history', 'U.S. History'),
        ('university_physics_calc', 'University Physics'),
        ('not_listed', 'Not Listed')
    ]

    _next_button_locator = (By.CSS_SELECTOR, '[type=submit]')

    def account_signup(self, email,
                       password=None, _type='Student', provider='guerrilla',
                       **kwargs):
        """Single signup entry point.

        Sign up a new user. Social, Random, and Name are mutually exclusive.

        Args:
            email (str): An accessible e-mail address
            password (str): A user password
                default: None
            _type (:obj:`str`, optional): New user account type -
                Signup.STUDENT, Signup.INSTRUCTOR, Signup.ADMINISTRATOR,
                Signup.LIBRARIAN, Signup.DESIGNER, Signup.OTHER
                default: Signup.STUDENT
            provider (str): The e-mail host -
                'google': Google Gmail
                'guerrilla': Guerrilla Mail
            **kwargs: Arbitrary keyword arguments
                'email_password': (str) Webmail login password
                'name': user name fields
                    [title (str), first_name (str),
                     last_name (str), suffix(str)]
                'news': (bool) checked or unchecked
                    default: True
                'phone': (str) instructor phone number
                'school': (str) school name
                'social': (str) Use a social login -
                    facebook, google
                'students': (int) number of course students
                'subjects': ([str]) list of subject interest -
                    accounting, algebra_and_trigonometry, american_government,
                    anatomy_physiology, astronomy, biology, calculus,
                    chemistry, chem_atoms_first, college_algebra,
                    college_physics_algebra, concepts_of_bio_non_majors,
                    introduction_to_sociology, introductory_statistics,
                    microbiology, pre_algebra, precalc, economics, macro_econ,
                    ap_macro_econ, micro_econ, ap_micro_econ, psychology,
                    ap_physics, us_history, university_physics_calc, not_listed
                'use': (string) using OpenStax -
                    Signup.ADOPTED
                        'Fully adopted and using it as the primary textbook'
                    Signup.RECOMMENDED
                        'Recommending the book – my students buy a different
                            book'
                    Signup.INTEREST
                        'Interested in using OpenStax in the future'
                    Signup.NOT_USING
                        'Not using OpenStax'
                'webpage': (str) web URL for an individual

        Return:
            page.accounts.Profile: new user profile page
        """
        # prep the signup help
        if 'kwargs' in kwargs:
            kwargs = kwargs.get('kwargs')
        non_student_role = _type != Signup.STUDENT
        instructor = _type == Signup.INSTRUCTOR

        # select user type and email
        self.user_type.role = _type
        self.user_type.email = email
        self.next()
        if non_student_role and not email.endswith('edu'):
            self.next()

        # verify the pin
        email_password = None
        if 'google' in provider:
            mailer = GoogleBase(self.driver)
            email_password = kwargs['email_password']
        elif 'guerrilla' in provider:
            mailer = GuerrillaMail(self.driver)
        else:
            mailer = _type(self.driver)
            email_password = kwargs['email_password']
        pin = self._get_pin(page=mailer,
                            provider=provider,
                            return_url=(self.seed_url + '/verify_email'),
                            email=email,
                            password=email_password)
        self.pin.verify_pin = pin
        self.next()

        if 'social' not in kwargs:
            # set the initial password
            self.password.password = password
            self.password.confirmation = password
            self.next()
        elif kwargs['social'] == 'facebook':
            # use Facebook
            self.password.use_social_login().use_facebook.log_in(
                email, email_password)
        else:
            # use Google
            self.password.use_social_login().use_google.log_in(email,
                                                               email_password)

        # enter user details in group order
        # all users
        if 'social' not in kwargs:
            self.user.first_name = kwargs['name'][Signup.FIRST]
            self.user.last_name = kwargs['name'][Signup.LAST]
            self.user.suffix = kwargs['name'][Signup.SUFFIX]
        self.user.school = kwargs['school']
        # elevated users
        if non_student_role:
            self.instructor.phone = kwargs['phone']
            self.instructor.webpage = kwargs['webpage']
            self.instructor.subjects = kwargs['subjects']
        # instructor-only
        if instructor:
            self.instructor.students = kwargs['students']
            self.instructor.using = kwargs['use']
        # completion
        if not kwargs['news']:
            self.user.toggle_news()
        self.user.agree_to_terms()
        sleep(0.25)
        self.next()

        # request e-mail confirmation for an elevated account
        if non_student_role:
            self.notice.get_confirmation_email()
            sleep(0.5)
            self.next()

        return profile.Profile(self.driver)

    @property
    def user_type(self):
        """Fill out the user type."""
        return self.UserType(self)

    @property
    def pin(self):
        """Verify the e-mail pin."""
        return self.PinVerification(self)

    def _get_pin(self, page, provider, return_url, email=None, password=None):
        """Retrieve a signup pin."""
        page.open()
        if 'google' in provider:
            page = page.login.go(email, password)
        WebDriverWait(self.driver, 60.0).until(
            lambda _: page.emails[0].has_pin)
        pin = page.emails[0].get_pin
        page.driver.get(return_url)
        sleep(1.0)
        return pin

    @property
    def password(self):
        """Fill out the password fields."""
        return self.SetPassword(self)

    @property
    def social(self):
        """Use a social login."""
        return self.SocialLogin(self)

    @property
    def user(self):
        """Fill out the user data."""
        return self.UserFields(self)

    @property
    def instructor(self):
        """Fill out the instructor verification."""
        return self.InstructorVerification(self)

    @property
    def notice(self):
        """Request notice when instructor access is authorized."""
        return self.InstructorNotice(self)

    def next(self):
        """Proceed to the next step in the process."""
        Utility.scroll_to(self.selenium, self._next_button_locator)
        self.find_element(*self._next_button_locator).click()
        sleep(1)
        return self

    class UserType(Region):
        """Initial signup pane for type selection."""

        _signup_role_locator = (By.ID, 'signup_role')
        _signup_email_locator = (By.ID, 'signup_email')
        _warning_locator = (By.CLASS_NAME, 'warning')
        _sign_in_locator = (By.CSS_SELECTOR, '.sign-in a')

        @property
        def role(self):
            """Return the role select."""
            return self.find_element(*self._signup_role_locator)

        @role.setter
        def role(self, signup_role):
            """Select a user role."""
            Utility.select(self.driver, self._signup_role_locator, signup_role)
            return self

        @property
        def email(self):
            """Return the email input."""
            return self.find_element(*self._signup_email_locator)

        @email.setter
        def email(self, email):
            """Send the e-mail."""
            self.email.send_keys(email)
            return self

        @property
        def warning(self):
            """Return the warning text."""
            return self.find_element(*self._warning_locator).text

        @property
        def warning_present(self):
            """Return True if the e-mail warning is displayed."""
            return self.find_element(*self._warning_locator).is_displayed()

        def log_in(self):
            """Return to the login screen."""
            return self.find_element(*self._sign_in_locator).click()
            sleep(1)
            return home.Home(self.driver)

    class PinVerification(Region):
        """Pin verification."""

        _pin_locator = (By.ID, 'pin_pin')
        _email_edit_locator = (By.CSS_SELECTOR, '.extra-info a')

        @property
        def verify_pin(self):
            """Return the pin input."""
            return self.find_element(*self._pin_locator)

        @verify_pin.setter
        def verify_pin(self, pin):
            """Send the verification code."""
            self.verify_pin.send_keys(pin)
            return self

        def edit_email(self):
            """Return to the user type selection."""
            self.find_element(*self._email_edit_locator).click()
            sleep(1)
            return self.UserType(self)

    class SetPassword(Region):
        """Set the user's password."""

        _password_locator = (By.ID, 'signup_password')
        _password_confirmation_locator = (
            By.ID, 'signup_password_confirmation')
        _error_locator = (By.CLASS_NAME, 'alert')
        _multi_error_locator = (By.CSS_SELECTOR, '.alert li')
        _go_to_social_locator = (By.CSS_SELECTOR, '[href$=social]')

        @property
        def password(self):
            """Return the password field."""
            return self.find_element(*self._password_locator)

        @password.setter
        def password(self, password):
            """Set the password."""
            self.find_element(*self._password_locator).send_keys(password)
            return self

        @property
        def confirmation(self):
            """Return the confirmation field."""
            return self.find_element(*self._password_confirmation_locator)

        @confirmation.setter
        def confirmation(self, password):
            """Set the password confirmation."""
            self.confirmation.send_keys(password)
            return self

        @property
        def has_error(self):
            """Return True if error messages are displayed."""
            try:
                self.find_element(*self._error_locator)
            except Exception:
                return False
            return True

        @property
        def get_error(self):
            """Return password error(s)."""
            if not self.has_error:
                return []
            try:
                self.find_element(*self._multi_error_locator)
            except Exception:
                return [self.find_element(*self._error_locator).text]
            return [el.text for el in
                    self.find_elements(*self._multi_error_locator)]

        def use_social_login(self):
            """Go to the social login setup."""
            self.find_element(*self._go_to_social_locator).click()
            sleep(1)
            return Signup.SocialLogin(self)

    class UserFields(Region):
        """Standard user fields."""

        _first_name_locator = (By.ID, 'profile_first_name')
        _last_name_locator = (By.ID, 'profile_last_name')
        _suffix_locator = (By.ID, 'profile_suffix')
        _school_locator = (By.ID, 'profile_school')
        _news_locator = (By.ID, 'profile_newsletter')
        _policy_agreement_locator = (By.ID, 'profile_i_agree')

        @property
        def first_name(self):
            """Return the first name field."""
            return self.find_element(*self._first_name_locator)

        @first_name.setter
        def first_name(self, first):
            """Send the user's first name."""
            self.first_name.send_keys(first)
            return self

        @property
        def last_name(self):
            """Return the surname field."""
            return self.find_element(*self._last_name_locator)

        @last_name.setter
        def last_name(self, last):
            """Send the user's surname."""
            self.last_name.send_keys(last)
            return self

        @property
        def suffix(self):
            """Return the suffix field."""
            return self.find_element(*self._suffix_locator)

        @suffix.setter
        def suffix(self, suffix):
            """Send the user's suffix."""
            self.suffix.send_keys(suffix)
            return self

        @property
        def school(self):
            """Return the school field."""
            return self.find_element(*self._school_locator)

        @school.setter
        def school(self, school):
            """Send the user's school or affiliation."""
            self.school.send_keys(school)
            return self

        def toggle_news(self):
            """Toggle between receiving and not receiving news."""
            self.find_element(*self._news_locator).click()
            sleep(1)
            return self

        def agree_to_terms(self):
            """Accept the Accounts terms of use and the privacy policy."""
            self.find_element(*self._policy_agreement_locator).click()
            sleep(1)
            return self

    class SocialLogin(Region):
        """Sign up using a social app profile."""

        URL_TEMPLATE = '/social'

        _facebook_button_locator = (By.ID, 'facebook-login-button')
        _google_button_locator = (By.ID, 'google-login-button')
        _go_to_password_setup_locator = (By.CSS_SELECTOR, '[href$=password]')

        @property
        def use_facebook(self):
            """Use Facebook to log in."""
            self.find_element(*self._facebook_button_locator).click()
            sleep(0.5)
            from pages.facebook.home import Facebook
            return Facebook(self.driver)

        @property
        def use_google(self):
            """Use Google to log in."""
            self.find_element(*self._google_button_locator).click()
            sleep(0.5)
            return Google(self.driver)

        @property
        def use_a_password(self):
            """Use a non-social log in."""
            self.find_element(*self._go_to_password_setup_locator).click()
            sleep(0.5)
            return Signup.SetPassword(self)

    class InstructorVerification(Region):
        """Instructor verification fields."""

        _phone_locator = (By.ID, 'profile_phone_number')
        _student_number_locator = (By.ID, 'profile_num_students')
        _webpage_verification_locator = (By.ID, 'profile_url')
        _using_openstax_locator = (By.ID, 'profile_using_openstax')
        _subject_option_locator = (By.CLASS_NAME, 'subject')

        @property
        def phone(self):
            """Return the telephone number field."""
            return self.find_element(*self._phone_locator)

        @phone.setter
        def phone(self, phone_number):
            """Send the verification telephone number."""
            self.phone.send_keys(phone_number)
            return self

        @property
        def students(self):
            """Return the student count field."""
            return self.find_element(*self._student_number_locator)

        @students.setter
        def students(self, students):
            """Send the yearly course student count."""
            self.students.send_keys(str(students))
            return self

        @property
        def webpage(self):
            """Return the webpage verification field."""
            return self.find_element(*self._webpage_verification_locator)

        @webpage.setter
        def webpage(self, webpage):
            """Send the URL showing instructor status."""
            self.webpage.send_keys(webpage)
            return self

        @property
        def using(self):
            """Return the instructor's intent field."""
            return self.find_element(*self._using_openstax_locator)

        @using.setter
        def using(self, status):
            """Set the instructor's intent for using OpenStax."""
            Utility.select(self.driver, self._using_openstax_locator, status)
            return self

        @property
        def subjects(self):
            """Return a list of book subjects."""
            return [self.Subject(self, el) for
                    el in self.find_elements(*self._subject_option_locator)]

        @subjects.setter
        def subjects(self, subject_list):
            """Mark each interested subject."""
            for subject in self.subjects:
                if subject.title in subject_list:
                    subject.select()
            return self

        class Subject(Region):
            """Book subject."""

            _book_title_locator = (By.TAG_NAME, 'label')
            _checkbox_locator = (By.CSS_SELECTOR, '[type=checkbox]')

            @property
            def title(self):
                """Get the book title."""
                return self.find_element(*self._book_title_locator).text

            def select(self):
                """Select a book."""
                self.find_element(*self._checkbox_locator).click()
                return self

    class InstructorNotice(Region):
        """Complete the instructor signup."""

        _get_email_confirmation_locator = (By.CSS_SELECTOR, '[type=checkbox]')

        def get_confirmation_email(self):
            """Get an e-mail confirmation when instructor access approved."""
            print(self.find_element(*self._get_email_confirmation_locator)
                  .get_attribute('outerHTML'))
            self.find_element(*self._get_email_confirmation_locator).click()
            return self
