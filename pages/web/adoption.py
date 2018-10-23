"""The book adoption form."""

from time import sleep

from pypom import Region
from selenium.common.exceptions import NoSuchElementException  # NOQA
from selenium.common.exceptions import WebDriverException  # NOQA
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility, go_to_
from utils.web import TechProviders, Web

ERROR = ' ~ .invalid-message'


class Adoption(WebBase):
    """The adoption form page."""

    URL_TEMPLATE = '/adoption'

    _loaded_locator = (By.CSS_SELECTOR, '.page-loaded')
    _banner_locator = (By.CSS_SELECTOR, '.subhead h1')
    _description_locator = (By.CSS_SELECTOR, '.subhead p:first-child')
    _drop_down_menu_locator = (By.CSS_SELECTOR, '.proxy-select')
    _interest_form_link_locator = (By.CSS_SELECTOR, '[href$=interest]')
    _form_root_locator = (By.CSS_SELECTOR, '.role-selector')
    _book_selection_locator = (By.CSS_SELECTOR, '.book-selector')
    _image_locator = (By.CSS_SELECTOR, '.has-image img')

    @property
    def loaded(self):
        """Wait until the form is displayed."""
        return (
            self.find_element(*self._loaded_locator).is_displayed() and
            self.find_element(*self._drop_down_menu_locator).is_displayed()
        )

    def is_displayed(self):
        """Return True if the adoption form is displayed."""
        return self.find_element(*self._drop_down_menu_locator).is_displayed()

    def go_to_interest(self):
        """Switch to the interest form."""
        self.wait.until(
            lambda _: self.find_element(*self._interest_form_link_locator)
        ).click()
        sleep(1.0)
        from pages.web.interest import Interest
        return go_to_(Interest(self.driver))

    def submit_adoption(self,
                        user_type, first, last, email, phone, school,
                        books,
                        tech_providers=None, other_provider=None):
        """Fill out and submit the adoption form.

        Args:
            user_type (str): the user's role
                Web.STUDENT, Web.INSTRUCTOR, Web.ADMINISTRATOR,
                Web.LIBRARIAN, Web.DESIGNER, Web.HOMESCHOOL,
                Web.ADJUNCT, or Web.OTHER
            first (str): the user's first name
            last (str): the user's last name
            email (str): the user's email address
            phone (str): the user's telephone number
            school (str): the user's school affiliation
            books (dict): a dictionaries of dictionaries for adopted books
                Book short name (str): the shortened book title
                Adoption status (str): Web.ADOPTED or Web.RECOMMENDED
                Students (int): number of students being taught per semester
                    {
                        'AP Biology': {
                            'status': Web.ADOPTED,
                            'students': 30
                        },
                        <book-short-name>: {
                            'status': <status>,
                            'students': <students>
                        }
                    }
            tech_providers (list): a list of technology partners under use
                [Web.TechProviders.<provider>]
            other_provider (str): a string of unlisted providers to be
                used when Web.TechProviders.OTHER is in tech_providers
        """
        self.form.select(user_type)
        self.form.first_name = first
        self.form.last_name = last
        self.form.email = email
        self.form.phone = phone
        self.form.school = school
        self.form.next()
        user_errors = self.form.get_user_errors
        assert(not user_errors), \
            'User errors: {issues}'.format(issues=user_errors)
        self.wait.until(
            lambda _: Utility.is_image_visible(self.driver,
                                               locator=self._image_locator))
        sleep(1)
        Utility.scroll_to(self.driver, self._book_selection_locator)
        sleep(0.5)
        self.form.select_books(books)
        sleep(0.5)
        self.form.set_using(books)
        sleep(0.5)
        self.form.next()
        book_error = self.form.get_book_error
        assert(not book_error), \
            'Book error - {book}'.format(book=book_error)
        using_errors = self.form.get_using_errors
        assert(not using_errors), \
            'Using error - {using}'.format(using=using_errors)
        self.form.select_tech(tech_providers)
        if TechProviders.OTHER in tech_providers:
            self.form.usage.other = other_provider
        self.form.submit()
        return go_to_(AdoptionConfirmation(self.driver))

    @property
    def form(self):
        """Access the adoption form."""
        form_root = self.find_element(*self._form_root_locator)
        return self.Form(self, form_root)

    class Form(Region):
        """The adoption form."""

        # User role selection
        _user_select_locator = (By.CSS_SELECTOR, '.proxy-select')
        _user_select_option_locator = (By.CSS_SELECTOR, '.options .option')

        # Student-specific locators
        _student_message_locator = (By.CSS_SELECTOR,
                                    '.student-form .text-content')
        _go_back_button_locator = (By.CSS_SELECTOR, '.student-form button')

        # User information
        _first_name_locator = (By.CSS_SELECTOR, '[name=first_name]')
        _last_name_locator = (By.CSS_SELECTOR, '[name=last_name]')
        _email_locator = (By.CSS_SELECTOR, '[name=email]')
        _phone_locator = (By.CSS_SELECTOR, '[name=phone]')
        _school_locator = (By.CSS_SELECTOR, '[name=company]')
        _first_name_error_locator = (
            By.CSS_SELECTOR, _first_name_locator[1] + ERROR)
        _last_name_error_locator = (
            By.CSS_SELECTOR, _last_name_locator[1] + ERROR)
        _email_error_locator = (
            By.CSS_SELECTOR, _email_locator[1] + ERROR)
        _phone_error_locator = (
            By.CSS_SELECTOR, _phone_locator[1] + ERROR)
        _school_error_locator = (
            By.CSS_SELECTOR, _school_locator[1] + ERROR)

        # Book information
        _books_locator = (By.CSS_SELECTOR, '[data-book-checkbox]')
        _book_selector_error = (
                By.CSS_SELECTOR, '.book-selector .invalid-message')

        # Book usage information
        _using_locator = (By.CSS_SELECTOR, '.how-using > div')

        # Technology utilization information
        _tech_locator = (By.CSS_SELECTOR, '.book-checkbox')

        # Form controls
        _next_button_locator = (By.CSS_SELECTOR, '.next')
        _back_button_locator = (By.CSS_SELECTOR, '.back')
        _submit_button_locator = (By.CSS_SELECTOR, '[type=submit]')

        @property
        def loaded(self):
            """Return True when the form is visible."""
            return self.root.is_displayed()

        @property
        def options(self):
            """Return the option menu responses."""
            return self.find_elements(*self._user_select_option_locator)

        def select(self, user_type):
            """Select a user type from the user drop down menu."""
            self.find_element(*self._user_select_locator).click()
            sleep(0.25)
            [option for option in self.options
             if option.get_attribute('data-value') == user_type][0].click()
            return self

        @property
        def student_message(self):
            """Return the message content for student users.

            Drop the text from the child element first.
            """
            message = (self.find_element(*self._student_message_locator)
                       .get_attribute('innerHTML')
                       .split('\n')[0]
                       .split('<')[0])
            return message

        def go_back(self):
            """Click the student GO BACK button."""
            self.find_element(*self._go_back_button_locator).click()
            sleep(1.0)
            return go_to_(WebBase(self.driver))

        @property
        def first_name(self):
            """Return the first name input box."""
            return self.find_element(*self._first_name_locator)

        @first_name.setter
        def first_name(self, name):
            """Type the first name."""
            self.first_name.send_keys(name)

        @property
        def last_name(self):
            """Return the last name input box."""
            return self.find_element(*self._last_name_locator)

        @last_name.setter
        def last_name(self, name):
            """Type the last name."""
            self.last_name.send_keys(name)

        @property
        def email(self):
            """Return the email input box."""
            return self.find_element(*self._email_locator)

        @email.setter
        def email(self, email):
            """Type the email."""
            self.email.send_keys(email)

        @property
        def phone(self):
            """Return the phone number input box."""
            return self.find_element(*self._phone_locator)

        @phone.setter
        def phone(self, phone_number):
            """Type the phone number."""
            self.phone.send_keys(phone_number)

        @property
        def school(self):
            """Return the school name input box."""
            return self.find_element(*self._school_locator)

        @school.setter
        def school(self, school_name):
            """Type the school name."""
            self.school.send_keys(school_name)

        @property
        def get_user_errors(self):
            """Return the error messages."""
            errors = {}
            first = self.find_element(*self._first_name_error_locator).text
            last = self.find_element(*self._last_name_error_locator).text
            email = self.find_element(*self._email_error_locator).text
            phone = self.find_element(*self._phone_error_locator).text
            school = self.find_element(*self._school_error_locator).text
            if first:
                errors['first_name'] = first
            if last:
                errors['last_name'] = last
            if email:
                errors['email'] = email
            if phone:
                errors['phone'] = phone
            if school:
                errors['school'] = school
            return errors

        @property
        def books(self):
            """Access the book selector checkboxes."""
            return [self.Book(self, el)
                    for el in self.find_elements(*self._books_locator)]

        def select_books(self, book_list):
            """Select the checkboxes for submitted book list."""
            for book in self.books:
                if book.title in book_list and not book.checked:
                    book.select()
            return self

        @property
        def get_book_error(self):
            """Return the book section error message."""
            try:
                return self.find_element(*self._book_selector_error).text
            except WebDriverException:
                return ''

        @property
        def usage(self):
            """Access the usage information section for each selected book."""
            return [self.Using(self, el)
                    for el in self.find_elements(*self._using_locator)]

        def set_using(self, book_list):
            """Select the status and student count for each book."""
            for book in self.usage:
                Utility.scroll_to(self.driver,
                                  element=book.root,
                                  shift=-80)
                if book.title in book_list:
                    status = book_list.get(book.title).get('status')
                    if Web.ADOPTED in status:
                        book.adopted()
                    elif Web.RECOMMENDED in status:
                        book.recommend()
                    book.students = book_list.get(book.title).get('students')
            return self

        @property
        def get_using_errors(self):
            """Return the usage section error messages."""
            errors = {}
            for book in self.usage:
                if book.title == '' or (
                        not book.using_error and not book.students_error):
                    continue
                else:
                    errors[book.title] = (
                        'Book error: "{book}" / Student error: "{student}"'
                        .format(book=book.using_error,
                                student=book.students_error))
            return errors

        @property
        def technology(self):
            """Access the technology provider information sections."""
            return [self.Technology(self, el)
                    for el in self.find_elements(*self._tech_locator)]

        def select_tech(self, providers, other=None):
            """Select the tech partners in use."""
            if not providers:
                return self
            for tech in self.technology:
                if tech.company in providers and not tech.checked:
                    tech.select()
            if TechProviders.OTHER in providers:
                self.technology.other = other
            return self

        def next(self):
            """Click the Next button."""
            button = self.find_element(*self._next_button_locator)
            Utility.scroll_to(self.driver, element=button, shift=-80)
            button.click()
            sleep(1.0)
            return self

        def back(self):
            """Click the Back button."""
            button = self.find_element(*self._back_button_locator)
            Utility.scroll_to(self.driver, element=button, shift=-80)
            button.click()
            sleep(1.0)
            return self

        def submit(self):
            """Click the Submit form button."""
            button = self.find_element(*self._submit_button_locator)
            Utility.scroll_to(self.driver, element=button, shift=-80)
            button.click()
            sleep(1.0)
            return self

        class Book(Region):
            """A book checkbox option."""

            _status_indicator_locator = (By.CSS_SELECTOR, '.book-checkbox')
            _image_locator = (By.CSS_SELECTOR, 'img')
            _title_locator = (By.CSS_SELECTOR, 'label')
            _checkbox_locator = (By.CSS_SELECTOR, '[role=checkbox]')

            @property
            def has_image(self):
                """Return True if the book check option has an image."""
                return ('has-image' in
                        self.find_element(*self._status_indicator_locator)
                        .get_attribute('class'))

            @property
            def image(self):
                """Return the image element."""
                if self.has_image:
                    return self.find_element(*self._image_locator)

            @property
            def title(self):
                """Return the book title."""
                return self.find_element(*self._title_locator).text

            def select(self):
                """Click the checkbox."""
                Utility.scroll_to(self.driver, element=self.root, shift=-80)
                self.find_element(*self._checkbox_locator).click()
                sleep(1.0)
                return self.page

            @property
            def checked(self):
                """Return True if the book option is checked."""
                return ('checked' in
                        self.find_element(*self._status_indicator_locator)
                        .get_attribute('class'))

        class Using(Region):
            """Additional information concerning each book adoption."""

            _title_locator = (By.CSS_SELECTOR, 'div:first-child')
            _adopted_locator = (By.CSS_SELECTOR, '[value*=Adoption]')
            _recommended_locator = (By.CSS_SELECTOR, '[value*=Recommend]')
            _radio_error_locator = (
                By.XPATH,
                ('//label[*[contains(@value,"Recommend")]]'
                 '/following-sibling::div'))
            _students_locator = (By.CSS_SELECTOR, '[type=number]')
            _students_error_locator = (
                By.CSS_SELECTOR, _students_locator[1] + ERROR)

            @property
            def title(self):
                """Return the book title."""
                return (self.find_element(*self._title_locator).text
                        .split('How are you using ')[-1]
                        .split('?')[0])

            def adopted(self):
                """Select the 'Fully adopted' option."""
                self.find_element(*self._adopted_locator).click()
                sleep(1.0)
                return self.page

            def recommend(self):
                """Select the 'Recommending the book' option."""
                self.find_element(*self._recommended_locator).click()
                sleep(1.0)
                return self.page

            @property
            def using_error(self):
                """Return the error message, if any, on the radio fields."""
                try:
                    return (self.find_element(*self._radio_error_locator)
                            .text)
                except NoSuchElementException:
                    return ''

            @property
            def students(self):
                """Return the students input element."""
                return self.find_element(*self._students_locator)

            @students.setter
            def students(self, number):
                """Set the number of students using the selected book."""
                self.find_element(*self._students_locator).send_keys(number)

            @property
            def students_error(self):
                """Return the error message, if any, on the student field."""
                try:
                    return (self.find_element(*self._students_error_locator)
                            .text)
                except NoSuchElementException:
                    return ''

        class Technology(Region):
            """Technology in use by the instructor or school."""

            _name_locator = (By.CSS_SELECTOR, 'label')
            _checkbox_locator = (By.CSS_SELECTOR, '.indicator')
            _other_option_locator = (By.CSS_SELECTOR, '[name*=Other]')

            @property
            def company(self):
                """Return the company or product name."""
                return self.find_element(*self._name_locator).text

            def select(self):
                """Click the checkbox."""
                self.find_element(*self._checkbox_locator).click()
                sleep(1.0)
                return self.page

            @property
            def checked(self):
                """Return True if the company option is checked."""
                return 'checked' in self.root.get_attribute('class')

            @property
            def other(self):
                """Return the other option input box."""
                return self.find_element(*self._other_option_locator)

            @other.setter
            def other(self, value):
                """Send the other technology provider to the form."""
                self.find_element(*self._other_option_locator).send_keys(value)


class AdoptionConfirmation(WebBase):
    """The adoption confirmation page."""

    URL_TEMPLATE = '/adoption-confirmation'

    _confirmation_locator = (By.CLASS_NAME, 'adoption-confirmation')
    _report_another_locator = (By.CSS_SELECTOR, '.outlined')
    _survey_locator = (By.CSS_SELECTOR, '.survey-request')

    @property
    def loaded(self):
        """Wait until the confirmation is displayed."""
        return self.find_element(*self._confirmation_locator).is_displayed()

    def is_displayed(self):
        """Return True if the 'Report another ...' link is displayed."""
        return self.another.is_displayed()

    @property
    def another(self):
        """Return the 'Report another ...' link."""
        return self.find_element(*self._report_another_locator)

    def report_another(self):
        """Click on the 'Report another ...' link."""
        Utility.safari_exception_click(self.driver, element=self.another)
        return go_to_(Adoption(self.driver))

    @property
    def survey_available(self):
        """Return True if a survey is available."""
        return Utility.has_children(self.find_element(*self._survey_locator))
