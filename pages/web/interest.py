"""The interest form page."""

from time import sleep

from selenium.webdriver.common.by import By

from pages.web.adoption import ERROR, Adoption, AdoptionConfirmation
from utils.utilities import Utility, go_to_
from utils.web import TechProviders, WebException


class Interest(Adoption):
    """The book interest form."""

    URL_TEMPLATE = '/interest'

    _adoption_form_link_locator = (By.CSS_SELECTOR, '[href$=adoption]')

    def go_to_adoption(self):
        """Switch to the adoption form."""
        return self.go_to_interest(link=self._adoption_form_link_locator)

    def submit_interest(self,
                        user_type, first, last, email, phone, school,
                        books, students, additional_resources, heard_on,
                        tech_providers=None, other_provider=None):
        """Fill out and submit the interest form.

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
            books (list): a list of book short names
            students (int): the number of students taught in a semester
                number must be greater than or equal to one
            additional_resources (list): a list of additional resource options
                Web.HOMEWORK, Web.COURSEWARE, and/or Web.TOOLS
            heard_on (list): a list of marketing sources
                Web.BY_WEB_SEARCH, Web.BY_COLLEAGUE, Web.AT_CONFERENCE,
                Web.BY_EMAIL, Web.BY_FACEBOOK, Web.BY_TWITTER, Web.BY_WEBINAR,
                Web.BY_PARTNER
            tech_providers (list): a list of tech partners user use
                [Web.TechProviders.<provider>]
            other_providers (str): a string of unlisted providers to be used
                when Web.TechProviders.OTHER is in tech_providers

        """
        self.form.select(user_type)
        self.form.first_name = first
        self.form.last_name = last
        self.form.email = email
        self.form.phone = phone
        self.form.school = school
        self.form.next()
        user_errors = self.form.get_user_errors
        if user_errors:
            raise WebException(f'User errors: {user_errors}')
        self.wait.until(
            lambda _:
                Utility.is_image_visible(self.driver,
                                         locator=self._image_locator) and
                self.find_element(*self._book_selection_locator))
        Utility.scroll_to(self.driver, self._book_selection_locator)
        self.form.select_books(books)
        sleep(0.5)
        self.form.students = students
        self.form.heard(heard_on)
        self.form.next()
        book_error = self.form.get_book_error
        if book_error:
            raise WebException(f'Book error - {book_error}')
        using_error = self.form.using_error
        if using_error:
            raise WebException(f'Using error - {using_error}')
        self.form.select_tech(tech_providers)
        if TechProviders.OTHER in tech_providers:
            self.form.other = other_provider
        self.form.submit()
        return go_to_(InterestConfirmation(self.driver, self.base_url))

    class Form(Adoption.Form):
        """The interest form."""

        _student_locator = (By.CSS_SELECTOR, '[name=Number_of_Students__c]')
        _additional_locator = (
                        By.CSS_SELECTOR, '[name=Partner_Category_Interest__c]')
        _heard_locator = (By.CSS_SELECTOR, '[name=How_did_you_Hear__c]')
        _student_error_locator = (By.CSS_SELECTOR, _student_locator[1] + ERROR)
        _selected_locator = (By.CSS_SELECTOR, '.checked')

        @property
        def students(self):
            """Return the semester student count element."""
            return self.find_element(*self._student_locator)

        @students.setter
        def students(self, total):
            """Set the number of students taught for these subjects."""
            self.students.send_keys(total)
            return self.page

        def receive(self, resources):
            """Select each additional resource option."""
            return self._selection_helper(
                resources, self._additional_locator, 'additional resource')

        def heard(self, heard_on):
            """Select each method of introduction to OpenStax."""
            return self._selection_helper(
                heard_on, self._heard_locator, 'introductory')

        @property
        def selection(self):
            """Return a list of selected books."""
            sleep(0.5)
            books = self.find_elements(
                By.CSS_SELECTOR, '.book-checkbox.checked label')
            return [book.text for book in books]

        @property
        def using_error(self):
            """Return the student section error message."""
            return self.find_element(*self._student_error_locator).text

        @property
        def selected_books(self):
            """Return a list of selected book elements."""
            return self.find_elements(*self._selected_locator)

        def _selection_helper(self, selected, options_locator, _type):
            """Click checkboxes for selected options."""
            if selected:
                group = {}
                for option in self.find_elements(*options_locator):
                    group[option.get_attribute('value')] = option
                if not group:
                    raise WebException(f'No {_type} options found')
                for option in group:
                    if option in selected:
                        group.get(option).click()
            return self.page


class InterestConfirmation(AdoptionConfirmation):
    """The interest confirmation page."""

    URL_TEMPLATE = '/interest-confirmation'

    _confirmation_locator = (By.CSS_SELECTOR, '.confirmation-page')
    _back_to_books_locator = (By.CSS_SELECTOR, '[href$=subjects]')
    _report_another_locator = _back_to_books_locator
    _response_text_locator = (By.CSS_SELECTOR, '.confirmation-page p')

    @property
    def response(self):
        """Return the response text."""
        return self.find_element(*self._response_text_locator).text.strip()

    @property
    def subjects(self):
        """Return the 'Back to the books' link."""
        return self.find_element(*self._back_to_books_locator)

    def back_to_books(self):
        """Return to the subjects page."""
        Utility.click_option(self.driver, element=self.subjects)
        from pages.web.subjects import Subjects
        return go_to_(Subjects(self.driver, self.base_url))
