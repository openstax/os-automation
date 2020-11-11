"""The book adoption form."""

from time import sleep

from pypom import Region
from selenium.common.exceptions import (ElementNotInteractableException,  # NOQA
                                        NoSuchElementException,  # NOQA
                                        TimeoutException,  # NOQA
                                        WebDriverException)  # NOQA
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility, go_to_
from utils.web import TechProviders, Web, WebException

ERROR = ' ~ .invalid-message'


class Adoption(WebBase):
    """The adoption form page."""

    URL_TEMPLATE = '/adoption'

    _banner_locator = (By.CSS_SELECTOR, '.subhead h1')
    _description_locator = (By.CSS_SELECTOR, '.subhead p:first-child')
    _drop_down_menu_locator = (By.CSS_SELECTOR, '[name=subject]')
    _interest_form_link_locator = (By.CSS_SELECTOR, '[href$=interest]')
    _form_root_locator = (By.CSS_SELECTOR, '.role-selector')
    _book_selection_locator = (By.CSS_SELECTOR, '.book-checkbox')
    _image_locator = (By.CSS_SELECTOR, '.has-image img')

    @property
    def loaded(self):
        """Wait until the form is found."""
        return (
            super().loaded and
            bool(self.find_elements(*self._drop_down_menu_locator)))

    def is_displayed(self):
        """Return True if the adoption form is displayed."""
        form = self.find_elements(*self._drop_down_menu_locator)
        if not form:
            return False
        visibility = self.driver.execute_script(
            'return window.getComputedStyle(arguments[0]).visibility;',
            form[0])
        return visibility == 'visible'

    def go_to_interest(self, link=None):
        """Switch to the interest form."""
        locator = link if link else self._interest_form_link_locator
        from pages.web.interest import Interest
        destination = Interest if not link else Adoption
        link = self.wait.until(
            lambda _: self.find_element(*locator))
        Utility.click_option(self.driver, element=link)
        sleep(1.0)
        return go_to_(destination(driver=self.driver, base_url=self.base_url))

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
        sleep(1.0)
        self.form.first_name = first
        self.form.last_name = last
        self.form.email = email
        self.form.phone = phone
        self.form.school = school
        self.form.next()
        sleep(1.0)
        user_errors = self.form.get_user_errors
        if user_errors:
            raise WebException(f'User errors: {user_errors}')
        self.wait.until(
            lambda _:
                Utility.is_image_visible(self.driver,
                                         locator=self._image_locator) and
                self.find_element(*self._book_selection_locator))
        Utility.scroll_to(self.driver, self._book_selection_locator, shift=-80)
        sleep(0.25)
        self.form.select_books(books)
        sleep(0.5)
        self.form.set_using(books)
        sleep(0.5)
        self.form.next()
        sleep(2.0)
        book_error = self.form.get_book_error
        if book_error:
            raise WebException(f'Book error: {book_error}')
        using_errors = self.form.get_using_errors
        if using_errors:
            raise WebException(f'Using error: {using_errors}')
        self.form.select_tech(tech_providers)
        if tech_providers and TechProviders.OTHER in tech_providers:
            self.form.other = other_provider
        self.form.submit()
        sleep(1.0)
        from pages.web.partners import Partners
        return go_to_(Partners(self.driver, self.base_url))

    @property
    def form(self):
        """Access the adoption form."""
        form_root = self.find_element(*self._form_root_locator)
        return self.Form(self, form_root)

    class Form(Region):
        """The adoption form."""

        # User role selection
        _user_select_locator = (By.CSS_SELECTOR, '.select')
        _user_select_option_locator = (By.CSS_SELECTOR, '.options .option')
        _user_selected_role_locator = (By.CSS_SELECTOR, 'span.item')

        # Student-specific locators
        _student_message_locator = (By.CSS_SELECTOR,
                                    '.student-form.text-content')
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
        _book_selector_error = (
            By.CSS_SELECTOR, '.book-selector .invalid-message')
        _book_checkbox_locator = (
            By.CSS_SELECTOR, '.book-selector .book-checkbox')

        # Book usage information
        _using_root_locator = (By.CSS_SELECTOR, '.page-2 .how-using')
        _using_locator = (By.CSS_SELECTOR, '.how-using > div')

        # Technology utilization information
        _tech_locator = (By.CSS_SELECTOR, '.book-checkbox')
        _other_option_locator = (By.CSS_SELECTOR, '[name*=Other]')

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

        def select(self, user_type, retry=0):
            """Select a user type from the user drop down menu."""
            sleep(0.33)
            user = self.find_element(*self._user_select_locator)
            Utility.click_option(self.driver, element=user)
            sleep(0.25)
            user = [group for group in self.options if group.text == user_type]
            if not user:
                raise WebException(f'User type `{user_type}` not available')
            Utility.click_option(self.driver, element=user[0])
            sleep(0.25)
            selected = (self.find_element(*self._user_selected_role_locator)
                        .get_attribute('textContent'))
            if selected == Web.NO_USER_TYPE and retry <= 2:
                self.select(user_type, retry=retry + 1)
            elif retry == 3:
                raise WebException('No user type selected after 3 tries')
            elif selected != user_type:
                raise WebException(
                    f'"{user_type}" not selected; found "{selected}"')
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

        def go_back(self, destination=WebBase, url=None):
            """Click the student GO BACK button."""
            back_button = self.find_element(*self._go_back_button_locator)
            Utility.click_option(self.driver, element=back_button)
            if url:
                return go_to_(destination(self.driver, url=url))
            return go_to_(destination(self.driver))

        @property
        def first_name(self):
            """Return the first name input box."""
            return self.find_element(*self._first_name_locator)

        @first_name.setter
        def first_name(self, name):
            """Type the first name."""
            self._setter_helper(self.first_name, name)

        @property
        def last_name(self):
            """Return the last name input box."""
            return self.find_element(*self._last_name_locator)

        @last_name.setter
        def last_name(self, name):
            """Type the last name."""
            self._setter_helper(self.last_name, name)

        @property
        def email(self):
            """Return the email input box."""
            return self.find_element(*self._email_locator)

        @email.setter
        def email(self, email):
            """Type the email."""
            self._setter_helper(self.email, email)

        @property
        def phone(self):
            """Return the phone number input box."""
            return self.find_element(*self._phone_locator)

        @phone.setter
        def phone(self, phone_number):
            """Type the phone number."""
            self._setter_helper(self.phone, phone_number)

        @property
        def school(self):
            """Return the school name input box."""
            return self.find_element(*self._school_locator)

        @school.setter
        def school(self, school_name):
            """Type the school name."""
            self._setter_helper(self.school, school_name)

        def _setter_helper(self, field, value):
            r"""Set an input text field value.

            :param field: the input box to fill out
            :param str value: the value to send to the input field
            :type field: \
                :py:class:`~selenium.webdriver.remote.webelement.WebElement`
            :return: None

            """
            sleep(0.25)
            for _ in range(20):
                try:
                    field.send_keys(value)
                    return
                except ElementNotInteractableException:
                    sleep(1)

        @property
        def school_suggestions(self):
            """Return a list of school name suggestions.

            Based on a filter of the text in the school name input box.
            """
            return [self.School(self, suggestion)
                    for suggestion
                    in self.find_elements(*self._suggestion_locator)]

        @property
        def get_user_errors(self):
            """Return the error messages."""
            errors = {}
            first = (self.find_element(*self._first_name_error_locator)
                     .get_attribute('textContent'))
            last = (self.find_element(*self._last_name_error_locator)
                    .get_attribute('textContent'))
            email = (self.find_element(*self._email_error_locator)
                     .get_attribute('textContent'))
            phone = (self.find_element(*self._phone_error_locator)
                     .get_attribute('textContent'))
            school = (self.find_element(*self._school_error_locator)
                      .get_attribute('textContent'))
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
                    for el in self.find_elements(*self._book_checkbox_locator)]

        def select_books(self, book_list):
            """Select the checkboxes for submitted book list."""
            self.wait.until(lambda _:
                            self.find_elements(*self._book_checkbox_locator))
            for book in self.books:
                if book.title in book_list and not book.checked:
                    book.select()
                    sleep(0.25)
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
                Utility.scroll_to(self.driver, element=book.root, shift=-100)
                if book.title in book_list:
                    sleep(0.25)
                    status = book_list.get(book.title).get('status')
                    if Web.ADOPTED in status:
                        book.adopted()
                    elif Web.RECOMMENDED in status:
                        book.recommend()
                    sleep(0.25)
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
                self.other = other
            return self

        @property
        def other(self):
            """Return the other option input box."""
            return self.find_element(*self._other_option_locator)

        @other.setter
        def other(self, value):
            """Send the other technology provider to the form."""
            Utility.scroll_to(self.driver, element=self.other, shift=-80)
            self.driver.execute_script(
                'arguments[0].value = "{0}";'.format(value),
                self.other)

        def next(self):
            """Click the Next button."""
            button = self.find_element(*self._next_button_locator)
            Utility.scroll_to(self.driver, element=button, shift=-80)
            Utility.click_option(self.driver, element=button)
            sleep(1.0)
            return self

        def back(self):
            """Click the Back button."""
            button = self.find_element(*self._back_button_locator)
            Utility.scroll_to(self.driver, element=button, shift=-80)
            Utility.click_option(self.driver, element=button)
            sleep(1.0)
            return self

        def submit(self):
            """Click the Submit form button."""
            button = self.find_element(*self._submit_button_locator)
            Utility.scroll_to(self.driver, element=button, shift=-80)
            Utility.click_option(self.driver, element=button)
            sleep(1.0)
            return self

        class School(Region):
            """A suggested school name."""

            @property
            def name(self):
                """Return the school name."""
                return self.root.text.strip()

            def select(self):
                """Click on the school name to select it."""
                Utility.click_option(self.driver, element=self.root)
                return self.page

        class Book(Region):
            """A book checkbox option."""

            _image_locator = (By.CSS_SELECTOR, 'img')
            _title_locator = (By.CSS_SELECTOR, 'label')
            _checkbox_locator = (By.CSS_SELECTOR, '[role=checkbox]')

            def __str__(self):
                """Print the book attributes."""
                book = ('Title: {title}\nImage: {has_image} - {image}\n'
                        'Checked: {checked}\n')
                return book.format(
                    title=self.title,
                    has_image=self.has_image,
                    image=(self.image.get_attribute('src')
                           if self.has_image else ''),
                    checked=self.checked)

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
                checkbox = self.find_element(*self._checkbox_locator)
                Utility.click_option(self.driver, element=checkbox)
                sleep(0.25)
                return self.page

            @property
            def checked(self):
                """Return True if the book option is checked."""
                return 'checked' in self.root.get_attribute('class')

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
                radio = self.find_element(*self._adopted_locator)
                Utility.click_option(self.driver, element=radio)
                return self.page

            def recommend(self):
                """Select the 'Recommending the book' option."""
                radio = self.find_element(*self._recommended_locator)
                Utility.click_option(self.driver, element=radio)
                return self.page

            @property
            def using_error(self):
                """Return the error message, if any, on the radio fields."""
                try:
                    return self.find_element(*self._radio_error_locator).text
                except NoSuchElementException:
                    return ''

            @property
            def students(self):
                """Return the students input element."""
                return self.find_element(*self._students_locator)

            @students.setter
            def students(self, number):
                """Set the number of students using the selected book."""
                sleep(0.25)
                for _ in range(20):
                    try:
                        self.students.send_keys(number)
                        return
                    except ElementNotInteractableException:
                        sleep(1)

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
        Utility.click_option(self.driver, element=self.another)
        return go_to_(Adoption(self.driver, self.base_url))

    @property
    def survey_available(self):
        """Return True if a survey is available."""
        return Utility.has_children(self.find_element(*self._survey_locator))
