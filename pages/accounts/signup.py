"""Break the signup process out of the base."""

from __future__ import annotations

from time import sleep
from typing import List, Tuple, Union

from pypom import Page
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as expect

from pages.accounts.base import AccountsBase
from pages.accounts.profile import Profile
from pages.web.verification import CompleteYourProfile
from regions.accounts.fields import Email, FirstName, LastName, Password, Phone, Pin  # NOQA
from regions.accounts.social import SocialLogins
from utils.accounts import AccountsException
from utils.email import RestMail
from utils.utilities import Utility, go_to_
from utils.web import Web, WebException

ERROR_SELECTOR = ' ~ .errors .invalid-message'


class ChangeYourEmail(AccountsBase):
    """The email change request page."""

    URL_TEMPLATE = '/i/change_your_email'

    class Content(AccountsBase.Content, Email):
        """The email change request pane."""

        _email_locator = (
            By.CSS_SELECTOR, '#change_signup_email_email')
        _information_message_locator = (
            By.CSS_SELECTOR, '.info-message')
        _send_my_pin_button_locator = (
            By.CSS_SELECTOR, '[type=submit]')

        _email_error_message_locator = (
            By.CSS_SELECTOR, _email_locator[1] + ERROR_SELECTOR)

        def send_my_pin(self) -> Union[ChangeYourEmail, ConfirmEmail]:
            """Click the 'Send my PIN' button.

            :return: the change your email page if there was an error or the
                email confirmation page
            :rtype: :py:class:`~pages.accounts.signup.ChangeYourEmail` or
                :py:class:`~pages.accounts.signup.ConfirmEmail`

            """
            button = self.find_element(*self._send_my_pin_button_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.5)
            if self.email_has_error:
                return self
            return go_to_(
                ConfirmEmail(self.driver, base_url=self.page.base_url))


class CompleteSignup(AccountsBase):
    """The account setup completion page."""

    URL_TEMPLATE = '/i/done'

    class Content(AccountsBase.Content):
        """The signup completion pane."""

        _email_locator = (
            By.CSS_SELECTOR, '.info-message b')
        _exit_button_locator = (
            By.CSS_SELECTOR, '#exit-icon a')
        _finish_button_locator = (
            By.CSS_SELECTOR, '[type=submit]')
        _information_message_locator = (
            By.CSS_SELECTOR, '.info-message')

        @property
        def information(self) -> str:
            """Return the email information message.

            :return: the email information message
            :rtype: str

            """
            return (self.find_element(*self._information_message_locator)
                    .get_attribute('textContent'))

        @property
        def email(self) -> str:
            """Return the email address used during registration.

            :return: the email address used during registration
            :rtype: str

            """
            return self.find_element(*self._email_locator).text

        def exit(self) -> Page:
            """Click the page return 'x' button.

            :return: the user profile or the origination page
            :rtype: :py:class:`~pypom.Page`

            """
            button = self.find_element(*self._exit_button_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.5)
            if 'profile' in self.current_url:
                return go_to_(
                    Profile(self.driver, base_url=self.page.base_url))
            return Page(self.driver)

        def finish(self) -> Page:
            """Click the 'Finish' button.

            :return: the account profile or the originating page
            :rtype: :py:class:`~pypom.Page`

            """
            button = self.find_element(*self._finish_button_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.5)
            if 'profile' in self.driver.current_url:
                return go_to_(
                    Profile(self.driver, base_url=self.page.base_url))
            return Page(self.driver)


class ConfirmEmail(AccountsBase):
    """The email confirmation page."""

    URL_TEMPLATE = '/i/confirmation_form'

    class Content(AccountsBase.Content, Pin):
        """The email confirmation pane."""

        _information_message_locator = (
            By.CSS_SELECTOR, '.info-message')
        _email_locator = (
            By.CSS_SELECTOR, '.info-message b')
        _edit_your_email_link_locator = (
            By.CSS_SELECTOR, '.info-message a')
        _pin_locator = (
            By.CSS_SELECTOR, '#confirm_pin')
        _use_a_different_email_link_locator = (
            By.CSS_SELECTOR, '.control-group a')
        _confirm_my_account_button_locator = (
            By.CSS_SELECTOR, '[type=submit]')

        _pin_error_message_locator = (
            By.CSS_SELECTOR, _pin_locator[1] + ERROR_SELECTOR)

        @property
        def email(self) -> str:
            """Return the email address used during registration.

            :return: the email address used during registration
            :rtype: str

            """
            return self.find_element(*self._email_locator).text

        @property
        def information(self) -> str:
            """Return the email information message.

            :return: the email information message
            :rtype: str

            """
            return (self.find_element(*self._information_message_locator)
                    .get_attribute('textContent'))

        @property
        def pin(self) -> str:
            """Return the current PIN value.

            :return: the current pin value
            :rtype: str

            """
            return (self.find_element(*self._pin_locator)
                    .get_attribute('value'))

        @pin.setter
        def pin(self, pin: str):
            """Enter the email verification number.

            :param str pin: the email verification number
            :return: None

            """
            field = self.find_element(*self._pin_locator)
            Utility.clear_field(self.driver, field=field)
            field.send_keys(pin)

        def confirm_my_account(self) \
                -> Union[CompleteSignup, VerifyInstructor]:
            """Click the Continue button.

            :return: the email confirmation (second step) if there are errors
                or the completion page (third step)
            :rtype: :py:class:`~pages.accounts.signup.CompleteSignup`
                or :py:class:`~pages.accounts.signup.VerifyInstructor`
            :raises :py:class:`~utils.accounts.AccountsException`: if an error
                in the form entries is found

            """
            current_page = self.page.location
            button = self.find_element(
                *self._confirm_my_account_button_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.5)
            if self.driver.current_url == current_page:
                raise AccountsException(
                    self.driver.execute_script(
                        'return document.querySelector(".invalid-message")'
                        '.textContent;'))
            if self.driver.current_url.endswith('/educator/apply'):
                return go_to_(VerifyInstructor(self.driver))
            return go_to_(
                CompleteSignup(self.driver, base_url=self.page.base_url))

        def edit_your_email(self) -> ChangeYourEmail:
            """Click the 'edit your email' link.

            :return: the change your email page
            :rtype: :py:class:`~pages.accounts.signup.ChangeYourEmail`

            """
            link = self.find_element(*self._edit_your_email_link_locator)
            Utility.click_option(self.driver, element=link)
            return go_to_(
                ChangeYourEmail(self.driver, base_url=self.page.base_url))

        def sign_up_with_a_different_email(self) -> ChangeYourEmail:
            """Click the 'sign up with a different email' link.

            :return: the change your email page
            :rtype: :py:class:`~pages.accounts.signup.ChangeYourEmail`

            """
            link = self.find_element(*self._use_a_different_email_link_locator)
            Utility.click_option(self.driver, element=link)
            return go_to_(
                ChangeYourEmail(self.driver, base_url=self.page.base_url))


class EducatorSignup(AccountsBase):
    """The educator sign up process."""

    URL_TEMPLATE = '/i/signup/educator'

    def sign_up(self,
                first: str,
                last: str,
                email: RestMail,
                password: str,
                phone: str,
                school: str,
                role: str = Web.ROLE_INSTRUCTOR,
                other: str = '',
                choice_by: str = Web.TEXTBOOK_BY_INSTRUCTOR,
                using: str = Web.USING_AS_PRIMARY,
                students: int = 1,
                books: List[str] = [],
                page: Page = None,
                base_url: str = None) \
            -> Page:
        """Register a new educator account.

        An normal instructor sign up:
        >>> sign_up(first='Open',
                    last='Stax',
                    email=<open.stax@domain-name.com>,
                    password=<password>,
                    phone='7135555555',
                    school='Openstax College',
                    role=Web.ROLE_INSTRUCTOR,
                    other=None,
                    choice_by=Web.TEXTBOOK_BY_INSTRUCTOR,
                    using=Web.USING_AS_PRIMARY,
                    students=85,
                    books=['College Algebra', 'Algebra and Trigonometry']
            )

        An administrative sign up:
        >>> sign_up(first='Open',
                    last='Stax',
                    email=<open.stax@domain-name.com>,
                    password=<password>,
                    phone='7135555555',
                    school='Openstax College',
                    role=Web.ROLE_ADMINISTRATOR,
                    other=None,
                    choice_by=Web.TEXTBOOK_BY_COORDINATOR,
                    using=Web.USING_AS_RECOMMENDED,
                    books=['Biology 2e', 'Microbiology']
            )

        A non-instructor/administrator sign up:
        >>> sign_up(first='Open',
                    last='Stax',
                    email=<open.stax@domain-name.com>,
                    password=<password>,
                    phone='7135555555',
                    school='Openstax College',
                    role=Web.ROLE_OTHER_EDUCATIONAL_STAFF,
                    other='Librarian'
            )

        :param str first: the educator's first name
        :param str last: the educator's last name
        :param RestMail email: the educator's accessible email address
        :param str password: the new account password
        :param str phone: the educator's telephone number
        :param str role: (optional) the educator's role at their institution,
            defaults to Instructor
            `Web.ROLE_INSTRUCTOR`, `Web.ROLE_ADMINISTRATOR`, or
            `Web.ROLE_OTHER_EDUCATIONAL_STAFF`
        :param str other: (optional) the educator's role if they are not an
            instructor or administrator, defaults to `''`
        :param str choice_by: (optional) who selects the course textbook,
            defaults to Instructor
            `Web.TEXTBOOK_BY_INSTRUCTOR`, `Web.TEXTBOOK_BY_COMMITTEE`, or
            `Web.TEXTBOOK_BY_COORDINATOR`
        :param str using: (optional) how is the textbook being used by the
            educator, defaults to Primary Textbook
            `Web.USING_AS_PRIMARY`, `Web.USING_AS_RECOMMENDED`, or
            `Web.USING_IN_FUTURE`
        :param int students: (optional) the number of students taught, defaults
            to `1`
        :param books: (optional) the list of book title the educator is using
            or is interested in, defaults to `[]`
        :type books: list(str)
        :param Page page: (optional) the expected destination page
        :param str base_url: (optional) the destination page base URL address
        :return: the new account profile if a destination page isn't provided
            or the destination page
        :rtype: :py:class:`~pypom.Page`

        """
        form = self.content
        form.first_name = first
        form.last_name = last
        form.phone = phone
        form.email = email.address
        form.password = password
        form.i_agree()
        if not email.address.endswith('.edu'):
            form._continue()
        confirm_email = form._continue().content

        pin = email.wait_for_mail()[-1].pin
        confirm_email.pin = pin
        instructor_access = confirm_email.confirm_my_account()

        if self.driver.current_url.endswith('/i/done'):
            youre_done = instructor_access.content
        else:  # enter educator profile data
            if not instructor_access.is_form_ready:
                raise WebException('School field not available')
            instructor_access.school_name = school
            if school not in instructor_access.school_name:
                print('Failed to set school name; retrying')
                clear = [Keys.BACKSPACE] * len(school) + \
                        [Keys.DELETE] * len(school)
                instructor_access.school_name = clear + school
            validated = instructor_access.verify_my_instructor_status()

            profile = validated._continue()

            profile.role(role, other)
            if role != Web.ROLE_OTHER_EDUCATIONAL_STAFF:
                profile.textbook_choice(choice_by)
                profile.using(using)
                if role == Web.ROLE_INSTRUCTOR:
                    profile.students = students
                if using == Web.USING_AS_PRIMARY:
                    profile.books_used = books
                else:
                    profile.interested_in = books
            youre_done = profile._continue().content

        youre_done.finish()

        if page:
            return go_to_(page(self.driver, base_url=base_url))
        return go_to_(Profile(self.driver, base_url=self.base_url))

        def get_errors(self) -> List[str]:
            """Return a list of error messages found on the page.

            :return: the list of error messages found on the current page
            :rtype: list(str)

            """
            errors = []
            if self.first_name_has_error:
                errors.append(f'First Name: {self.first_name_error}')
            if self.last_name_has_error:
                errors.append(f'Last Name: {self.last_name_error}')
            if self.email_has_error:
                errors.append(f'Email: {self.email_error}')
            if self.password_has_error:
                errors.append(f'Password: {self.password_error}')
            return errors

    class Content(AccountsBase.Content,
                  Email, FirstName, LastName, Password, Phone):
        """The sign up pane."""

        _continue_button_locator = (
            By.CSS_SELECTOR, '[type=submit]')
        _email_locator = (
            By.CSS_SELECTOR, '#signup_email')
        _first_name_locator = (
            By.CSS_SELECTOR, '#signup_first_name')
        _last_name_locator = (
            By.CSS_SELECTOR, '#signup_last_name')
        _newsletter_signup_locator = (
            By.CSS_SELECTOR, '#signup_newsletter')
        _password_locator = (
            By.CSS_SELECTOR, '#signup_password')
        _phone_locator = (
            By.CSS_SELECTOR, '#signup_phone_number')
        _policy_agreement_locator = (
            By.CSS_SELECTOR, '#signup_terms_accepted')
        _privacy_policy_link_locator = (
            By.CSS_SELECTOR, '.terms [href*=terms]:last-child')
        _show_password_toggle_locator = (
            By.CSS_SELECTOR, '#show-hide-button')
        _terms_of_use_link_locator = (
            By.CSS_SELECTOR, '.terms [href*=terms]:first-child')

        _email_error_message_locator = (
            By.CSS_SELECTOR, _email_locator[1] + ERROR_SELECTOR)
        _first_name_error_message_locator = (
            By.CSS_SELECTOR, _first_name_locator[1] + ERROR_SELECTOR)
        _last_name_error_message_locator = (
            By.CSS_SELECTOR, _last_name_locator[1] + ERROR_SELECTOR)
        _password_error_message_locator = (
            By.CSS_SELECTOR, _password_locator[1] + ERROR_SELECTOR)
        _phone_error_message_locator = (
            By.CSS_SELECTOR, _phone_locator[1] + ERROR_SELECTOR)

        def i_agree(self) -> StudentSignup:
            """Click the I agree checkbox.

            :return: the Accounts student sign up page
            :rtype: :py:class:`~pages.accounts.signup.StudentSignup`

            """
            checkbox = self.find_element(*self._policy_agreement_locator)
            Utility.click_option(self.driver, element=checkbox)
            return self.page

        def toggle_newsletter(self) -> StudentSignup:
            """Click the OpenStax newsletter checkbox.

            :return: the Accounts student sign up page
            :rtype: :py:class:`~pages.accounts.signup.StudentSignup`

            """
            checkbox = self.find_element(*self._newsletter_signup_locator)
            Utility.click_option(self.driver, element=checkbox)
            return self.page

        def toggle_password_display(self) -> StudentSignup:
            """Toggle the password field to show or hide the value.

            :return: the Accounts student sign up page
            :rtype: :py:class:`~pages.accounts.signup.StudentSignup`

            """
            toggle = self.find_element(*self._show_password_toggle_locator)
            Utility.click_option(self.driver, element=toggle)
            sleep(0.1)
            return self.page

        def _continue(self) -> Union[StudentSignup, ConfirmEmail]:
            """Click the Continue button.

            :param Page previous: (optional) the Page object for the initial
                page that sent the log in request
            :param str base_url: (optional) the base URL for the previous Page
            :param kwargs: (optional) additional keyword arguments for the Page
            :return: the student sign up (first step) if there are errors or
                the email confirmation (second step)
            :rtype: :py:class:`~pages.accounts.signup.StudentSignup` or
                :py:class:`~pages.accounts.signup.ConfirmEmail`

            """
            current_page = self.page.location
            button = self.find_element(*self._continue_button_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.5)
            if self.driver.current_url == current_page:
                error = self.driver.execute_script(
                    'return document.querySelector(".invalid-message");')
                if error:
                    raise AccountsException(error.get_attribute('textContent'))
            return go_to_(
                ConfirmEmail(self.driver, base_url=self.page.base_url))


class Signup(AccountsBase):
    """The Accounts sign up process."""

    URL_TEMPLATE = '/i/signup'

    class Content(AccountsBase.Content):
        """The sign up pane."""

        DESCRIPTION = ' ~ div'

        _educator_signup_button_locator = (
            By.CSS_SELECTOR, '[href$=educator]')
        _student_signup_button_locator = (
            By.CSS_SELECTOR, '[href$=student]')

        _educator_descrition_locator = (
            By.CSS_SELECTOR, _educator_signup_button_locator[1] + DESCRIPTION)
        _student_description_locator = (
            By.CSS_SELECTOR, _student_signup_button_locator[1] + DESCRIPTION)

        @property
        def educator_description(self) -> str:
            """Return the educator sign up explanation text.

            :return: the explanation why educators should register for an
                OpenStax account
            :rtype: str

            """
            return (self.find_element(*self._educator_descrition_locator)
                    .get_attribute('textContent'))

        @property
        def student_description(self) -> str:
            """Return the student sign up explanation text.

            :return: the explanation why students should register for an
                OpenStax account
            :rtype: str

            """
            return (self.find_element(*self._student_description_locator)
                    .get_attribute('textContent'))

        def sign_up_as_an_educator(self) -> EducatorSignup:
            """Click the educator sign up button.

            :return: the educator registration process
            :rtype: :py:class:`~pages.accounts.signup.EducatorSignup`

            """
            button = self.find_element(*self._educator_signup_button_locator)
            Utility.click_option(self.driver, element=button)
            return go_to_(
                EducatorSignup(self.driver, base_url=self.page.base_url))

        def sign_up_as_a_student(self) -> StudentSignup:
            """Click the student sign up button.

            :return: the student registration process
            :rtype: :py:class:`~pages.accounts.signup.StudentSignup`

            """
            button = self.find_element(*self._student_signup_button_locator)
            Utility.click_option(self.driver, element=button)
            return go_to_(
                StudentSignup(self.driver, base_url=self.page.base_url))


class StudentSignup(AccountsBase):
    """The student sign up process."""

    URL_TEMPLATE = '/i/signup/student'

    def sign_up(self,
                first: str, last: str, email: RestMail, password: str,
                page: Page = None, base_url: str = None) \
            -> Page:
        """Register a new student account.

        :param str first: the student's first name
        :param str last: the student's last name
        :param RestMail email: the student's accessible email address
        :param str password: the new account password
        :param Page page: (optional) the expected destination page
        :param str base_url: (optional) the destination page base URL address
        :return: the new account profile if a destination page isn't provided
            or the destination page
        :rtype: :py:class:`~pypom.Page`

        """
        form = self.content
        form.first_name = first
        form.last_name = last
        form.email = email.address
        form.password = password
        form.i_agree()
        confirm_email = form._continue().content
        pin = email.wait_for_mail()[-1].pin
        confirm_email.pin = pin
        complete_sign_up = confirm_email.confirm_my_account().content
        complete_sign_up.finish()
        if page:
            return go_to_(page(self.driver, base_url=base_url))
        return go_to_(Profile(self.driver, base_url=self.base_url))

    class Content(AccountsBase.Content,
                  Email, FirstName, LastName, Password, SocialLogins):
        """The sign up pane."""

        _continue_button_locator = (
            By.CSS_SELECTOR, '[type=submit]')
        _email_locator = (
            By.CSS_SELECTOR, '#signup_email')
        _first_name_locator = (
            By.CSS_SELECTOR, '#signup_first_name')
        _last_name_locator = (
            By.CSS_SELECTOR, '#signup_last_name')
        _newsletter_signup_locator = (
            By.CSS_SELECTOR, '#signup_newsletter')
        _password_locator = (
            By.CSS_SELECTOR, '#signup_password')
        _policy_agreement_locator = (
            By.CSS_SELECTOR, '#signup_terms_accepted')
        _privacy_policy_link_locator = (
            By.CSS_SELECTOR, '.terms [href*=terms]:last-child')
        _show_password_toggle_locator = (
            By.CSS_SELECTOR, '#show-hide-button')
        _terms_of_use_link_locator = (
            By.CSS_SELECTOR, '.terms [href*=terms]:first-child')

        _email_error_message_locator = (
            By.CSS_SELECTOR, _email_locator[1] + ERROR_SELECTOR)
        _first_name_error_message_locator = (
            By.CSS_SELECTOR, _first_name_locator[1] + ERROR_SELECTOR)
        _last_name_error_message_locator = (
            By.CSS_SELECTOR, _last_name_locator[1] + ERROR_SELECTOR)
        _password_error_message_locator = (
            By.CSS_SELECTOR, _password_locator[1] + ERROR_SELECTOR)

        def get_errors(self) -> List[str]:
            """Return a list of error messages found on the page.

            :return: the list of error messages found on the current page
            :rtype: list(str)

            """
            errors = []
            if self.first_name_has_error:
                errors.append(f'First Name: {self.first_name_error}')
            if self.last_name_has_error:
                errors.append(f'Last Name: {self.last_name_error}')
            if self.email_has_error:
                errors.append(f'Email: {self.email_error}')
            if self.password_has_error:
                errors.append(f'Password: {self.password_error}')
            return errors

        def i_agree(self) -> StudentSignup:
            """Click the I agree checkbox.

            :return: the Accounts student sign up page
            :rtype: :py:class:`~pages.accounts.signup.StudentSignup`

            """
            checkbox = self.find_element(*self._policy_agreement_locator)
            Utility.click_option(self.driver, element=checkbox)
            return self.page

        def toggle_newsletter(self) -> StudentSignup:
            """Click the OpenStax newsletter checkbox.

            :return: the Accounts student sign up page
            :rtype: :py:class:`~pages.accounts.signup.StudentSignup`

            """
            checkbox = self.find_element(*self._newsletter_signup_locator)
            Utility.click_option(self.driver, element=checkbox)
            return self.page

        def toggle_password_display(self) -> StudentSignup:
            """Toggle the password field to show or hide the value.

            :return: the Accounts student sign up page
            :rtype: :py:class:`~pages.accounts.signup.StudentSignup`

            """
            toggle = self.find_element(*self._show_password_toggle_locator)
            Utility.click_option(self.driver, element=toggle)
            sleep(0.1)
            return self.page

        def _continue(self) -> Union[StudentSignup, ConfirmEmail]:
            """Click the Continue button.

            :param Page previous: (optional) the Page object for the initial
                page that sent the log in request
            :param str base_url: (optional) the base URL for the previous Page
            :param kwargs: (optional) additional keyword arguments for the Page
            :return: the student sign up (first step) if there are errors or
                the email confirmation (second step)
            :rtype: :py:class:`~pages.accounts.signup.StudentSignup` or
                :py:class:`~pages.accounts.signup.ConfirmEmail`

            """
            current_page = self.page.location
            button = self.find_element(*self._continue_button_locator)
            Utility.click_option(self.driver, element=button)
            sleep(0.5)
            if self.driver.current_url == current_page:
                raise AccountsException(
                    self.driver.execute_script(
                        'return document.querySelector(".invalid-message")'
                        '.textContent;'))
            return go_to_(
                ConfirmEmail(self.driver, base_url=self.page.base_url))


class SuccessfulVerification(Page):
    """The successful verification page."""

    _continue_button_locator = (
        By.CSS_SELECTOR, '.sid-btn')
    _frame_reference_locator = (
        By.CSS_SELECTOR, 'iframe')

    def _continue(self) -> CompleteSignup:
        """Click the Continue button.

        :return: the account creation completion page
        :rtype: :py:class:`~pages.accounts.signup.CompleteSignup`

        """
        frame = self.find_element(*self._frame_reference_locator)
        self.driver.switch_to.frame(frame)
        sleep(0.5)
        try:
            button = self.wait.until(
                expect.element_to_be_clickable(
                    self._continue_button_locator))
        except TimeoutException:
            raise WebException('Continue button not available')
        Utility.click_option(self.driver, element=button)
        self.driver.switch_to.default_content()
        sleep(0.25)
        return go_to_(CompleteYourProfile(self.driver))


class VerifyInstructor(Page):
    """The SheerID instructor verification form."""

    _country_selection_locator = (
        By.CSS_SELECTOR, '#sid-country')
    _email_locator = (
        By.CSS_SELECTOR, '#sid-email')
    _first_name_locator = (
        By.CSS_SELECTOR, '#sid-first-name')
    _frame_reference_locator = (
        By.CSS_SELECTOR, 'iframe')
    _last_name_locator = (
        By.CSS_SELECTOR, '#sid-last-name')
    _school_name_locator = (
        By.CSS_SELECTOR, '#sid-teacher-school')
    _school_option_locator = (
        By.CSS_SELECTOR, '[role=listbox] [role=option]')
    _verify_my_instructor_status_button_locator = (
        By.CSS_SELECTOR, '[type=submit]')

    @property
    def country(self) -> str:
        """Return the currently selected country.

        :return: the currently selected country
        :rtype: str

        """
        return self._get_frame_value(self._country_selection_locator)

    @country.setter
    def country(self, country: str = 'United States'):
        """Set the user's country.

        :param str country: the country name
        :return: None

        """
        self._set_frame_value(self._country_selection_locator, country)

    @property
    def email(self) -> str:
        """Return the sign up email address.

        :return: the email used during sign up
        :rtype: str

        """
        return self._get_frame_value(self._email_locator)

    @property
    def first_name(self) -> str:
        """Return the user's first name.

        :return: the entered first name
        :rtype: str

        """
        return self._get_frame_value(self._first_name_locator)

    @first_name.setter
    def first_name(self, name: str):
        """Set the user's first name

        :param str name: the user's first name
        :return: None

        """
        self._set_frame_value(self._first_name_locator, name)

    @property
    def last_name(self) -> str:
        """Return the user's last name.

        :return: the entered last name
        :rtype: str

        """
        return self._get_frame_value(self._last_name_locator)

    @last_name.setter
    def last_name(self, name: str):
        """Set the user's last name

        :param str last_name: the user's last name
        :return: None

        """
        self._set_frame_value(self._last_name_locator, name)

    @property
    def is_form_ready(self) -> bool:
        """Return True when the school field is ready.

        :return: `True` when the school field in the iframe is ready
        :rtype: bool

        """
        try:
            self.wait.until(
                expect.frame_to_be_available_and_switch_to_it(
                    self._frame_reference_locator))
            self.wait.until(
                expect.visibility_of_element_located(
                    self._school_name_locator))
            self.driver.switch_to.default_content()
            return True
        except TimeoutException:
            return False

    @property
    def school_name(self) -> str:
        """Return the user's school name.

        :return: the entered school name
        :rtype: str

        """
        return self._get_frame_value(self._school_name_locator)

    @school_name.setter
    def school_name(self, school: str):
        """Set the user's school name

        :param str school: the user's school name
        :return: None

        """
        frame = self.find_element(*self._frame_reference_locator)
        self.driver.switch_to.frame(frame)
        school_name = self.find_element(*self._school_name_locator)
        Utility.clear_field(self.driver, field=school_name)
        school_name.send_keys(school)
        sleep(1.0)
        names = self.find_elements(*self._school_option_locator)
        if not names:
            raise IndexError(f'School name ({school}) not found')
        Utility.click_option(self.driver, element=names[0])
        sleep(0.5)
        self.driver.switch_to.default_content()

    def _get_frame_value(self, value_locator: Tuple[str, str]) -> str:
        """Return a field value from the form iframe.

        :param value_locator: the By-style locator for the desired field
        :type value_locator: tuple(str, str)
        :return: the selected field value
        :rtype: str

        """
        frame = self.find_element(*self._frame_reference_locator)
        self.driver.switch_to.frame(frame)
        value = (self.find_element(*value_locator).get_attribute('value'))
        self.driver.switch_to.default_content()
        return value

    def _set_frame_value(self, value_locator: Tuple[str, str], value: str):
        """Set a field value in the form iframe.

        :param value_locator: the By-style locator for the desired field
        :type value_locator: tuple(str, str)
        :param value: the new value for the selected field
        :type value: str
        :return: None

        """
        frame = self.find_element(*self._frame_reference_locator)
        self.driver.switch_to.frame(frame)
        field = self.find_element(*value_locator)
        Utility.clear_field(self.driver, field=field)
        field.send_keys(value)
        sleep(0.25)
        self.driver.switch_to.default_content()
        return value

    def verify_my_instructor_status(self) -> SuccessfulVerification:
        """Click the 'Verify my instructor status' button.

        :return: the successful verification page
        :rtype: :py:class:`~pages.accounts.signup.SuccessfulVerification`

        """
        frame = self.find_element(*self._frame_reference_locator)
        self.driver.switch_to.frame(frame)
        button = self.wait.until(
            expect.visibility_of_element_located(
                self._verify_my_instructor_status_button_locator))
        Utility.click_option(self.driver, element=button)
        self.driver.switch_to.default_content()
        return go_to_(
            SuccessfulVerification(self.driver, base_url=self.base_url))
