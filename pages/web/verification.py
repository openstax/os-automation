"""Faculty verification form, step 4 of 4.

SheerID managed by Web

"""

from __future__ import annotations

from time import sleep
from typing import List

from pypom import Page, Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from pages.web.home import WebHome
from utils.utilities import Utility, go_to_
from utils.web import Web


class CompleteYourProfile(WebBase):
    """The Web faculty profile form."""

    _books_interested_in_locator = (
        By.CSS_SELECTOR, '.books-of-interest')
    _books_used_locator = (
        By.CSS_SELECTOR, '.books-used')
    _continue_button_locator = (
        By.CSS_SELECTOR, '[type=submit]')
    _describe_your_role_question_locator = (
        By.CSS_SELECTOR, '.completed-role')
    _how_are_textbooks_chosen_question_locator = (
        By.CSS_SELECTOR, '.how-chosen')
    _how_are_you_using_question_locator = (
        By.CSS_SELECTOR, '.how-using')
    _log_in_tab_locator = (
        By.CSS_SELECTOR, '.tab.login')
    _logo_locator = (
        By.CSS_SELECTOR, '.logo a')
    _other_role_field_locator = (
        By.CSS_SELECTOR, '#signup_other_role_name')
    _sign_up_tab_locator = (
        By.CSS_SELECTOR, '.tab.signup')
    _student_count_locator = (
        By.CSS_SELECTOR, '#signup_num_students_per_semester_taught')

    _value_selector = '[value={0}]'

    @property
    def books_used(self) -> CompleteYourProfile.Multiselect:
        r"""Access the Books used multiselection.

        :return: the "Books you've used in your courses" multiselector
        :rtype: :py:class:`~pages.web.verification \
                           .CompleteYourProfile.Multiselect`

        """
        book_select = self.find_element(*self._books_used_locator)
        return self.Multiselect(self, book_select)

    @books_used.setter
    def books_used(self, books: List[str]):
        """Select the books in use by the educator.

        :param books: the list of book titles in use by the educator
        :type books: list(str)
        :return: None

        """
        self._select_books(self.books_used, books)

    @property
    def interested_in(self) -> CompleteYourProfile.Multiselect:
        """Access the Interested in multiselection.

        :return: the "Books of interest" multiselector
        :rtype: :py:class:`~pages.web.verification \
                           .CompleteYourProfile.Multiselect`

        """
        interest = self.find_element(*self._books_interested_in_locator)
        return self.Multiselect(self, interest)

    @interested_in.setter
    def interested_in(self, books: List[str]):
        """Select the books of interest to the educator.

        :param books: the list of book titles the educator is interested in
        :type books: list(str)
        :return: None

        """
        self._select_books(self.interested_in, books)

    @property
    def students(self) -> int:
        """Return the number of students taught by the instructor.

        :return: the instructor's self-reported number of students to be taught
        :rtype: int

        """
        student = self.find_element(*self._student_count_locator)
        total = student.get_attribute('value')
        return int(total) if total else 0

    @students.setter
    def students(self, count: int = 1):
        """Enter the number of students taught by the instructor.

        :param int count: (optional) the number of students to be taught by the
            instructor, defaults to `1`
        :return: None

        """
        total = self.find_element(*self._student_count_locator)
        total.send_keys(count)

    def log_in(self) -> CompleteYourProfile:
        """Click the Log in tab.

        The result is the current page because the new user is logged in.

        :return: the current page
        :rtype: :py:class:`~pages.web.verification.CompleteYourProfile`

        """
        tab = self.find_element(self._log_in_tab_locator)
        Utility.click_option(self.driver, element=tab)
        return self

    def openstax(self) -> WebHome:
        """Click the Sign up tab.

        The result is the Web home page because the profile form is managed by
        Web, not Accounts.

        :return: the current page
        :rtype: :py:class:`~pages.web.home.WebHome`

        """
        logo = self.find_element(self._logo_locator)
        Utility.click_option(self.driver, element=logo)
        sleep(0.5)
        return go_to_(WebHome(self.driver, base_url=self.base_url))

    def role(self, user: str = Web.ROLE_INSTRUCTOR, other_role: str = None):
        """Select the educator's role.

        :param str user: (optional) the user's role, defaults to
            `Web.ROLE_INSTRUCTOR`
            `Web.ROLE_INSTRUCTOR`, `Web.ROLE_ADMINISTRATOR`, or
            `Web.ROLE_OTHER_EDUCATIONAL_STAFF`
        :param str other_role: (optional) the user's non-instructor,
            non-administrative role, defaults to `None` because it is only used
            with `Web.ROLE_OTHER_EDUCATIONAL_STAFF`
        :return: None

        """
        educator_role = self.find_element(
            *self._describe_your_role_question_locator)
        user_type = educator_role.find_element(
            By.CSS_SELECTOR, self._value_selector.format(user))
        Utility.click_option(self.driver, element=user_type)
        sleep(0.25)
        if other_role:
            other_field = self.find_element(*self._other_role_field_locator)
            other_field.send_keys(other_role)
            sleep(0.25)

    def sign_up(self):
        """Click the Sign up tab.

        The result is the current page because the new user is signed up but
        the profile is incomplete.

        :return: the current page
        :rtype: :py:class:`~pages.web.verification.CompleteYourProfile`

        """
        tab = self.find_element(self._sign_up_tab_locator)
        Utility.click_option(self.driver, element=tab)
        return self

    def textbook_choice(self, choice: str = Web.TEXTBOOK_BY_INSTRUCTOR):
        """Select the textbook selection choice for the institution.

        :param str choice: (optional) the selection method for the institution,
            defaults to `Web.TEXTBOOK_BY_INSTRUCTOR`
            `Web.TEXTBOOK_BY_INSTRUCTOR`, `Web.TEXTBOOK_BY_COMMITTEE`, or
            `Web.TEXTBOOK_BY_COORDINATOR`
        :return: None

        """
        textbook_selection = self.find_element(
            *self._how_are_textbooks_chosen_question_locator)
        selected_by = textbook_selection.find_element(
            By.CSS_SELECTOR, self._value_selector.format(choice))
        Utility.click_option(self.driver, element=selected_by)
        sleep(0.25)

    def using(self, using_as: str = Web.USING_AS_PRIMARY):
        """Select the current course or institutional use of OpenStax material.

        :param str using_as: (optional) the method of use for OpenStax material
            in the instructor's course to educator's institution, defaults to
            `Web.USING_AS_PRIMARY`
            `Web.USING_AS_PRIMARY`, `Web.USING_AS_RECOMMENDED`, or
            `Web.USING_IN_FUTURE`
        :return: None

        """
        how_using = self.find_element(
            *self._how_are_you_using_question_locator)
        use = how_using.find_element(
            By.CSS_SELECTOR, self._value_selector.format(using_as))
        Utility.click_option(self.driver, element=use)
        sleep(0.25)

    def _continue(self) -> Page:
        """Click the Continue button.

        :return: the profile complete "You're done" page
        :rtype: :py:class:`~pages.accounts.signup.CompleteSignup`

        """
        button = self.find_element(*self._continue_button_locator)
        Utility.click_option(self.driver, element=button)
        from pages.accounts.signup import CompleteSignup
        return go_to_(CompleteSignup(self.driver))

    def _select_books(
            self, select: CompleteYourProfile.Multiselect, books: List[str]):
        r"""Select books using a Multiselect region tool.

        :param select: the Multiselect region to use
        :type select: :py:class:`~pages.web.verification \
                                 .CompleteYourProfile.Multiselect`
        :param books: the list of books to select
        :type books: list(str)

        """
        if not select.list_is_open:
            select.toggle()
        book_list = books
        for book in select.books:
            if book.title in book_list:
                book_list.remove(book.title)
                book.select()
        select.toggle()

    class Multiselect(Region):
        """A book multi-selection widget."""

        _book_list_arrow_icon_locator = (
            By.CSS_SELECTOR, 'i.fa')
        _book_list_toggle_locator = (
            By.CSS_SELECTOR, '[type=button]')
        _book_title_bar_locator = (
            By.CSS_SELECTOR, '.result')

        @property
        def books(self) -> List[CompleteYourProfile.Multiselect.Book]:
            r"""Return the list of available books.

            :return: the list of books available for selection
            :rtype: list(:py:class:`~pages.web.verification \
                                    .CompleteYourProfile.Multiselect`)

            """
            return [self.Book(self, book)
                    for book
                    in self.find_elements(*self._book_title_bar_locator)]

        @property
        def list_is_open(self) -> bool:
            """Return True is the multiselect box is open/expanded.

            :return: `True` if the multiselect box is open
            :rtype: bool

            """
            icon = self.find_element(*self._book_list_arrow_icon_locator)
            return 'caret-up' in icon.get_attribute('class')

        def toggle(self):
            """Toggle the multiselect open or closed.

            :return: None

            """
            arrow = self.find_element(*self._book_list_toggle_locator)
            Utility.click_option(self.driver, element=arrow)
            sleep(0.25)

        class Book(Region):
            """A book option box within the multiselect widget."""

            @property
            def title(self) -> str:
                """Return the book title.

                :return: the book bar title
                :rtype: str

                """
                return self.root.text

            def select(self):
                """Click the book bar.

                :return: None

                """
                Utility.click_option(self.driver, element=self.root)
