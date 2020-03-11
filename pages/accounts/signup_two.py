"""Break the signup process out of the base."""

from time import sleep
from urllib.parse import urlparse

from pypom import Region
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.accounts.base import AccountsBase
from pages.accounts.home import AccountsHome
from utils.accounts import Accounts
from utils.email import GmailReader, GuerrillaMail, RestMail
from utils.utilities import Utility, go_to_

ERROR = ' ~ .errors .alert'


class Pagination(Region):
    """Shared page features."""

    _continue_locator = (By.CSS_SELECTOR, '[type=submit]')

    def next(self):
        """Click the continuation button."""
        button = self.find_element(*self._continue_locator)
        Utility.click_option(self.driver, element=button)
        return self.page


class Signup(AccountsBase):
    """Signup process."""

    URL_TEMPLATE = '/signup'

    def account_signup(
            self, email, password=None,
            role=Accounts.STUDENT, provider=Accounts.RESTMAIL,
            destination=None, base_url=None, **kwargs):
        """Single signup entry point."""
        import pprint
        pprint.PrettyPrinter(indent=2, width=140).pprint(kwargs)
        # branching prep
        non_student_role = role != Accounts.STUDENT
        instructor = role == Accounts.INSTRUCTOR

        # select the user type and initial email for verification
        self.sign_up.role = role
        self.sign_up.email = email
        self.sign_up.next()
        error = self.sign_up.email_error
        assert(not error), '{0}'.format(error)
        if non_student_role and not email.endswith('edu'):
            self.sign_up.next()

        # verify the email using the assigned pin number
        not_verified = True
        pause = 0.25
        while not_verified:
            email_password = None
            if provider == Accounts.RESTMAIL:
                account_name = email[:email.rfind('@')]
                mailer = RestMail(account_name)
            elif provider == Accounts.GOOGLE:
                pin = (GmailReader(email[0:7])
                       .read_mail().sort_mail()
                       .latest.get_pin)
                email_password = kwargs.get('email_password')
            elif provider == Accounts.GUERRILLA_MAIL:
                mailer = GuerrillaMail(self.driver)
            else:
                from utils.email import EmailVerificationError
                raise EmailVerificationError(
                    '{0} is not an accepted email provider'.format(provider))
            if provider != Accounts.GOOGLE:
                pin = self._get_pin(
                    page=mailer,
                    provider=provider,
                    return_url=self.seed_url + '/verify_email',
                    email=email,
                    password=email_password)
            if not pin:
                raise ValueError('PIN not found')
            self.pin_verification.clear_pin()
            self.pin_verification.verify_pin = pin
            self.pin_verification.confirm()
            sleep(pause)
            error = self.pin_verification.pin_error
            if not error:
                not_verified = False
        assert(not error), '{0}'.format(error)

        # set the account password or social login
        if 'social' not in kwargs:
            # use a password
            self.password.password = password
            self.password.confirmation = password
            self.password.submit()
            errors = self.password.password_errors
            assert(not errors), '{0}'.format(' '.join(errors))
        elif kwargs.get('social') == Accounts.FACEBOOK:
            # use Facebook
            (self.password.use_social_login()
             .user_facebook.log_in(kwargs.get('social_login'),
                                   kwargs.get('social_password')))
            sleep(3)
        else:
            # use Google
            (self.password.use_social_login()
             .use_google.log_in(kwargs.get('social_login'),
                                kwargs.get('social_password')))
            sleep(3)
        self.wait.until(
            lambda _: 'accounts' in urlparse(self.driver.current_url).netloc)

        # enter the first page profile information
        sleep(2)
        if 'social' not in kwargs:
            _, first, last, _ = kwargs.get('name')
            self.profile.first_name = first
            self.profile.last_name = last
        if non_student_role:
            self.profile.phone_number = kwargs.get('phone')
        self.profile.school_name = kwargs.get('school')
        if non_student_role:
            self.profile.webpage = kwargs.get('webpage')
            use = kwargs.get('use')
            self.profile.using_openstax(use)
        self.profile.next()

        # enter the second page courseware information
        if non_student_role:
            subjects = kwargs.get('subjects', {})
            subjects_to_select = []
            for subject, name in Accounts.SUBJECTS:
                if name in subjects:
                    subjects_to_select.append(name)
            if subjects_to_select:
                self.courseware.select_subjects(subjects_to_select)
                self.courseware.set_using(subjects)
        if instructor and use == Accounts.RECOMMENDED:
            self.courseware.students = kwargs.get('students')
        if not kwargs.get('news'):
            self.courseware.no_newsletter()
        self.courseware.agree_to_policies()
        self.courseware.create_account()
        errors = self.profile.profile_errors
        assert(not errors), '{0}'.format(' '.join(errors))
        error = self.courseware.book_error
        assert(not error), '{0}'.format(error)

        # register for a confirmation upon approval
        if non_student_role:
            if kwargs.get('access_notice'):
                self.instructor_access.receive_instructor_access_notice()
            self.instructor_access.ok()

        # return to submitted destination
        if destination:
            return go_to_(destination(self.driver, base_url=base_url))
        # or the user's new profile
        from pages.accounts.profile import Profile
        return go_to_(Profile(self.driver, self.base_url))

    def _get_pin(self, page, provider, return_url, email=None, password=None):
        """Retrieve a signup pin."""
        if 'restmail' in provider:
            box = page.wait_for_mail()
            return box[-1].pin
        else:
            page.open()
            if 'google' in provider:
                page = page.login.go(email, password)
            WebDriverWait(page.driver, 60.0).until(
                lambda _: page.emails[0].has_pin and page.emails[0].is_new)
            sleep(5.0)
            pin = page.emails[0].get_pin
            page.driver.get(return_url)
            sleep(1.0)
        return pin

    @property
    def sign_up(self):
        """Access the signup page elements."""
        return self.Signup(self)

    @property
    def pin_verification(self):
        """Access the pin verification."""
        return self.Pin(self)

    @property
    def password(self):
        """Access the password fields."""
        return self.Password(self)

    @property
    def profile(self):
        """Access the profile fields."""
        return self.Profile(self)

    @property
    def courseware(self):
        """Access the courseware books."""
        return self.Courseware(self)

    @property
    def instructor_access(self):
        """Access the approval confirmation fields."""
        return self.Approval(self)

    class Signup(Pagination):
        """Basic user data."""

        _user_type_locator = (By.CSS_SELECTOR, '#signup_role')
        _options_locator = (
            By.CSS_SELECTOR, _user_type_locator[1] + ' option:not([disabled])')
        _email_parent_locator = (By.CSS_SELECTOR, '.email-input-group')
        _email_locator = (By.CSS_SELECTOR, '#signup_email')
        _email_error_locator = (By.CSS_SELECTOR, _email_locator[1] + ERROR)
        _warning_locator = (By.CSS_SELECTOR, '.warning')
        _sign_in_locator = (By.CSS_SELECTOR, '[href$=login]')

        @property
        def role(self):
            """Return the role select parent."""
            return self.find_element(*self._user_type_locator)

        @role.setter
        def role(self, signup_role):
            """Select a user role."""
            options = [role.text
                       for role in self.find_elements(*self._options_locator)]
            assert(signup_role in options), \
                '"{0}" not found in the role options'.format(signup_role)
            Utility.select(self.driver, self._user_type_locator, signup_role)
            return self.page

        @property
        def email_box_is_visible(self):
            """Return True if the email input box is visible."""
            return self.driver.execute_script(
                'return window.getComputedStyle(arguments[0]).height!="0px";',
                self.find_element(*self._email_parent_locator))

        @property
        def email(self):
            """Return the email input box."""
            return self.find_element(*self._email_locator)

        @email.setter
        def email(self, email):
            """Enter the email address."""
            self.email.send_keys(email)
            return self.page

        @property
        def email_error(self):
            """Return the email entry error."""
            try:
                return self.find_element(*self._email_error_locator).text
            except WebDriverException:
                return ''

        @property
        def warning(self):
            """Return the warning text."""
            return self.find_element(*self._warning_locator).text

        @property
        def warning_is_present(self):
            """Return True if the warning is displayed."""
            return self.driver.execute_script(
                'return window.getComputedStyle(arguments[0]).height!="auto";',
                self.find_element(*self._warning_locator))

        def log_in(self):
            """Return to the login home page."""
            link = self.find_element(*self._sign_in_locator)
            Utility.click_option(self.driver, element=link)
            return go_to_(AccountsHome(self.driver, self.page.base_url))

    class Pin(Pagination):
        """Pin verification."""

        _pin_locator = (By.CSS_SELECTOR, '#pin_pin')
        _pin_error_locator = (By.CSS_SELECTOR, '.alert')
        _email_change_locator = (By.CSS_SELECTOR, '[href$=signup]')

        @property
        def verify_pin(self):
            """Return the pin verification input box."""
            return self.find_element(*self._pin_locator)

        @verify_pin.setter
        def verify_pin(self, pin):
            """Enter the verification code."""
            self.verify_pin.send_keys(pin)
            return self.page

        def edit_email(self):
            """Return to the user role selection to enter a new email."""
            link = self.find_element(*self._email_change_locator)
            Utility.click_option(self.driver, element=link)
            return self.page

        @property
        def pin_error(self):
            """Return the pin entry error message."""
            try:
                return self.find_element(*self._pin_error_locator).text
            except WebDriverException:
                return ''

        def clear_pin(self):
            """Clear the pin field for Chrome and Firefox."""
            Utility.clear_field(self.selenium, self.verify_pin)

        def confirm(self):
            """Click the 'Confirm' button."""
            return self.next()

    class Password(Pagination):
        """Password assignment."""

        _password_locator = (By.CSS_SELECTOR, '#signup_password')
        _password_conf_locator = (
            By.CSS_SELECTOR, '#signup_password_confirmation')
        _password_error_locator = (By.CSS_SELECTOR, '.alert')
        _multi_error_locator = (By.CSS_SELECTOR, '.alert li')
        _use_social_locator = (By.CSS_SELECTOR, '[href$=social]')

        @property
        def password(self):
            """Return the password input field."""
            return self.find_element(*self._password_locator)

        @password.setter
        def password(self, password):
            """Enter the password."""
            self.password.send_keys(password)
            return self.page

        @property
        def confirmation(self):
            """Return the password confirmation input field."""
            return self.find_element(*self._password_conf_locator)

        @confirmation.setter
        def confirmation(self, password):
            """Enter the password in the confirmation box."""
            self.confirmation.send_keys(password)
            return self.page

        @property
        def password_errors(self):
            """Return the password errors."""
            try:
                issue = self.find_element(*self._password_error_locator)
            except WebDriverException:
                return []
            errors = self.find_elements(*self._multi_error_locator)
            if not errors:
                return [issue.text]
            return list([error.text for error in errors])

        def submit(self):
            """Click the 'Submit' button."""
            return self.next()

        def use_social_login(self):
            """Go to the social login setup."""
            link = self.find_element(*self._use_social_locator)
            Utility.click_option(self.driver, element=link)
            return Signup.SocialLogin(self.page)

    class Profile(Pagination):
        """User details."""

        _first_name_locator = (By.CSS_SELECTOR, '#profile_first_name')
        _first_name_error_locator = (
            By.CSS_SELECTOR, _first_name_locator[1] + ERROR)
        _last_name_locator = (By.CSS_SELECTOR, '#profile_last_name')
        _last_name_error_locator = (
            By.CSS_SELECTOR, _last_name_locator[1] + ERROR)
        _phone_locator = (By.CSS_SELECTOR, '#profile_phone_number')
        _phone_error_locator = (By.CSS_SELECTOR, _phone_locator[1] + ERROR)
        _school_locator = (By.CSS_SELECTOR, '#profile_school')
        _school_error_locator = (By.CSS_SELECTOR, _school_locator[1] + ERROR)
        _webpage_locator = (By.CSS_SELECTOR, '#profile_url')
        _webpage_error_locator = (By.CSS_SELECTOR, _webpage_locator[1] + ERROR)
        _adopted_locator = (
            By.CSS_SELECTOR, '#profile_using_openstax_confirmed_adoption_won')
        _not_using_locator = (
            By.CSS_SELECTOR, '#profile_using_openstax_not_using')
        _continue_locator = (By.CSS_SELECTOR, '[data-bind*=nextPage]')

        @property
        def first_name(self):
            """Return the first name input field."""
            return self.find_element(*self._first_name_locator)

        @first_name.setter
        def first_name(self, name):
            """Enter the user's first name."""
            self.first_name.send_keys(name)
            return self.page

        @property
        def last_name(self):
            """Return the last name input field."""
            return self.find_element(*self._last_name_locator)

        @last_name.setter
        def last_name(self, name):
            """Enter the user's last name."""
            self.last_name.send_keys(name)
            return self.page

        @property
        def phone_number(self):
            """Return the telephone number input field."""
            return self.find_element(*self._phone_locator)

        @phone_number.setter
        def phone_number(self, number):
            """Enter the user's telephone number."""
            self.phone_number.send_keys(number)
            return self.page

        @property
        def school_name(self):
            """Return the school name input field."""
            return self.find_element(*self._school_locator)

        @school_name.setter
        def school_name(self, name):
            """Enter the school name."""
            self.school_name.send_keys(name)
            return self.page

        @property
        def webpage(self):
            """Return the faculty verification webpage field."""
            return self.find_element(*self._webpage_locator)

        @webpage.setter
        def webpage(self, url):
            """Enter the webpage URL."""
            self.webpage.send_keys(url)
            return self.page

        def using_openstax(self, method):
            """Select the current using state."""
            if method == Accounts.ADOPTED:
                option = self.find_element(*self._adopted_locator)
            elif method == Accounts.NOT_USING:
                option = self.find_element(*self._not_using_locator)
            Utility.click_option(self.driver, element=option)
            return self.page

        @property
        def profile_errors(self):
            """Return a list of errors."""
            errors = []
            try:
                first = self.find_element(*self._first_name_error_locator).text
                errors.append('{0}: {1}'.format('First name', first))
            except WebDriverException:
                pass
            try:
                last = self.find_element(*self._last_name_error_locator).text
                errors.append('{0}: {1}'.format('Last name', last))
            except WebDriverException:
                pass
            try:
                phone = self.find_element(*self._phone_error_locator).text
                errors.append('{0}: {1}'.format('Phone number', phone))
            except WebDriverException:
                pass
            try:
                school = self.find_element(*self._school_error_locator).text
                errors.append('{0}: {1}'.format('School name', school))
            except WebDriverException:
                pass
            try:
                url = self.find_element(*self._webpage_error_locator).text
                errors.append('{0}: {1}'.format('Webpage', url))
            except WebDriverException:
                pass
            return errors

    class SocialLogin(Region):
        """Sign up using a social app profile."""

        _facebook_button_locator = (By.CSS_SELECTOR, '#facebook-login-button')
        _google_button_locator = (By.CSS_SELECTOR, '#google-login-button')
        _go_to_password_setup_locator = (By.CSS_SELECTOR, '[href$=password]')

        @property
        def use_facebook(self):
            """Use Facebook to log in."""
            Utility.click_option(
                self.driver, locator=self._facebook_button_locator)
            from pages.facebook.home import Facebook
            return Facebook(self.driver)

        @property
        def use_google(self):
            """Use Google to log in."""
            Utility.click_option(
                self.driver, locator=self._google_button_locator)
            from pages.google.home import Google
            return Google(self.driver)

        @property
        def use_a_password(self):
            """Use a non-social log in."""
            Utility.click_option(
                self.driver, locator=self._go_to_password_setup_locator)
            return self.page

    class Courseware(Pagination):
        """Book details."""

        _adopted_book_selector = '#how_using_book_{book_code}_adoption_won'
        _recommend_book_selector = '#how_using_book_{book_code}_will_recommend'
        _student_number_selector = '[type=number][name*={book_code}]'

        _book_locator = (By.CSS_SELECTOR, '.book-checkbox')
        _book_error_locator = (By.CSS_SELECTOR, '.alert')
        _number_students_locator = (By.CSS_SELECTOR, '#profile_num_students')
        _newsletter_locator = (By.CSS_SELECTOR, '#profile_newsletter')
        _policy_agreement_locator = (By.CSS_SELECTOR, '#profile_i_agree')
        _terms_locator = (By.CSS_SELECTOR, '[href*=terms]:nth-child(3)')
        _privacy_locator = (By.CSS_SELECTOR, '[href*=terms]:nth-child(4)')
        _back_button_locator = (By.CSS_SELECTOR, '[data-bind*=prevPage]')

        @property
        def books(self):
            """Return the list of available books."""
            return [self.Book(self, book)
                    for book in self.find_elements(*self._book_locator)]

        def select_subjects(self, subject_list):
            """Mark each interested or adopted book."""
            for book in self.books:
                if book.title in subject_list:
                    book.select()
            return self.page

        def set_using(self, subject_list):
            """Mark the adoption status and students for each book."""
            for subject in subject_list:
                code = Accounts.get_book_code(subject)
                status = subject_list.get(subject).get('status')
                students = subject_list.get(subject).get('students')
                if status == Accounts.ADOPTED:
                    selector = (self._adopted_book_selector
                                .format(book_code=code))
                else:
                    selector = (self._recommend_book_selector
                                .format(book_code=code))
                button = self.find_element(By.CSS_SELECTOR, selector)
                Utility.click_option(self.driver, element=button)
                self.find_element(
                    By.CSS_SELECTOR,
                    self._student_number_selector.format(book_code=code)
                ).send_keys(students)
                sleep(0.5)
            return self.page

        @property
        def students(self):
            """Return the general student count input box."""
            return self.find_element(*self._number_students_locator)

        @students.setter
        def students(self, total):
            """Enter the number of students taught."""
            self.students.send_keys(total)
            return self.page

        @property
        def newsletter(self):
            """Return the newsletter checkbox."""
            return self.find_element(*self._newsletter_locator)

        def no_newsletter(self):
            """Uncheck the newsletter box."""
            if self.driver.execute_script('return arguments[0].checked;',
                                          self.newsletter):
                Utility.click_option(self.driver, element=self.newsletter)
            return self.page

        @property
        def agreement(self):
            """Return the 'I agree' checkbox."""
            return self.find_element(*self._policy_agreement_locator)

        def agree_to_policies(self):
            """Check the 'I agree' checkbox."""
            if not self.driver.execute_script('return arguments[0].checked;',
                                              self.agreement):
                Utility.click_option(self.driver, element=self.agreement)
            return self.page

        def view_terms(self):
            """Open the Terms of Use."""
            link = self.find_element(*self._terms_locator)
            Utility.click_option(self.driver, element=link)
            return self.page

        def view_privacy_policy(self):
            """Open the Privacy Policy."""
            link = self.find_element(*self._privacy_locator)
            Utility.click_option(self.driver, element=link)
            return self.page

        @property
        def policy(self):
            """Access the policy modal."""
            modal_root = self.driver.execute_script(
                'return document.querySelector("#terms_dialog");')
            return self.Modal(self, modal_root)

        def back(self):
            """Return to the previous page."""
            button = self.find_element(*self._back_button_locator)
            Utility.click_option(self.driver, element=button)
            return self.page

        def create_account(self):
            """Click the 'Create Account' button."""
            return self.next()

        @property
        def book_error(self):
            """Return the book error."""
            try:
                return self.find_element(*self._book_error_locator).text
            except WebDriverException:
                return ''

        class Book(Region):
            """An OpenStax book."""

            _title_locator = (By.CSS_SELECTOR, 'label')
            _image_locator = (By.CSS_SELECTOR, 'img')
            _checkbox_locator = (By.CSS_SELECTOR, '.indicator')

            @property
            def title(self):
                """Return the book title."""
                return self.find_element(*self._title_locator).text

            @property
            def image(self):
                """Return the image element."""
                return self.find_element(*self._image_locator)

            @property
            def checkbox(self):
                """Return the checkbox element."""
                return self.find_element(*self._checkbox_locator)

            def select(self):
                """Select the book."""
                Utility.click_option(self.driver, element=self.checkbox)
                return self.page.page

            @property
            def is_checked(self):
                """Return True if the box is checked."""
                return 'checked' in self.root.get_attribute('class')

        class Modal(Region):
            """The Terms of Use and Privacy Policy display window."""

            _content_locator = (By.CSS_SELECTOR, '.modal-body')
            _close_locator = (By.CSS_SELECTOR, 'button')

            @property
            def content(self):
                """Return the modal content text."""
                return self.find_element(*self._content_locator).text

            def close(self):
                """Close the modal."""
                button = self.find_element(*self._close_locator)
                Utility.click_option(self.driver, element=button)
                return self.page.page

    class Approval(Pagination):
        """Acceptance email."""

        _approval_email_locator = (By.CSS_SELECTOR, '[type=checkbox]')

        @property
        def approval(self):
            """Return the email request upon approval checkbox."""
            return self.find_element(*self._approval_email_locator)

        def receive_instructor_access_notice(self):
            """Click the checkbox to receive notice."""
            if not self.driver.execute_script('return arguments[0].checked;',
                                              self.approval):
                Utility.click_option(self.driver, element=self.approval)
            return self.page

        def ok(self):
            """Click the OK button."""
            return self.next()
