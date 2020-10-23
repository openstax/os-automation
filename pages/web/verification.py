"""Faculty verification form, step 4 of 4."""

from __future__ import annotations

from time import sleep
from typing import List

from pypom import Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from pages.web.home import WebHome
from utils.utilities import Utility, go_to_
from utils.web import Web


class CompleteYourProfile(WebBase):
    """The Web faculty profile form."""

    _how_are_textbooks_chosen_question_locator = (
        By.CSS_SELECTOR, '.how-chosen')
    _describe_your_role_question_locator = (
        By.CSS_SELECTOR, '.completed-role')
    _how_are_you_using_question_locator = (
        By.CSS_SELECTOR, '.how-using')
    _logo_locator = (
        By.CSS_SELECTOR, '.logo a')
    _log_in_tab_locator = (
        By.CSS_SELECTOR, '.tab.login')
    _sign_up_tab_locator = (
        By.CSS_SELECTOR, '.tab.signup')
    _other_role_field_locator = (
        By.CSS_SELECTOR, '#signup_other_role_name')
    _student_count_locator = (
        By.CSS_SELECTOR, '#signup_num_students_per_semester_taught')
    _books_used_locator = (
        By.CSS_SELECTOR, '.books-used')
    _books_interested_in_locator = (
        By.CSS_SELECTOR, '.books-of-interest')
    _continue_button_locator = (
        By.CSS_SELECTOR, '[type=submit]')

    _value_selector = '[value={0}]'

    def openstax(self):
        logo = self.find_element(self._logo_locator)
        Utility.click_option(self.driver, element=logo)
        sleep(0.5)
        return go_to_(WebHome(self.driver, base_url=self.base_url))

    def log_in(self):
        tab = self.find_element(self._log_in_tab_locator)
        Utility.click_option(self.driver, element=tab)
        return self

    def sign_up(self):
        tab = self.find_element(self._sign_up_tab_locator)
        Utility.click_option(self.driver, element=tab)
        return self

    def role(self, user: str = Web.ROLE_INSTRUCTOR, other_role: str = None):
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

    def textbook_choice(self, choice: str = Web.TEXTBOOK_BY_INSTRUCTOR):
        textbook_selection = self.find_element(
            *self._how_are_textbooks_chosen_question_locator)
        selected_by = textbook_selection.find_element(
            By.CSS_SELECTOR, self._value_selector.format(choice))
        Utility.click_option(self.driver, element=selected_by)
        sleep(0.25)

    def using(self, using_as: str = Web.USING_AS_PRIMARY):
        how_using = self.find_element(
            *self._how_are_you_using_question_locator)
        use = how_using.find_element(
            By.CSS_SELECTOR, self._value_selector.format(using_as))
        Utility.click_option(self.driver, element=use)
        sleep(0.25)

    @property
    def students(self) -> int:
        student = self.find_element(*self._student_count_locator)
        total = student.get_attribute('value')
        return int(total) if total else 0

    @students.setter
    def students(self, count: int = 1):
        total = self.find_element(*self._student_count_locator)
        total.send_keys(count)

    @property
    def books_used(self) -> CompleteYourProfile.Multiselect:
        book_select = self.find_element(*self._books_used_locator)
        return self.Multiselect(self, book_select)

    @books_used.setter
    def books_used(self, books: List[str]):
        self._select_books(self.books_used, books)

    @property
    def interested_in(self) -> CompleteYourProfile.Multiselect:
        interest = self.find_element(*self._books_interested_in_locator)
        return self.Multiselect(self, interest)

    @interested_in.setter
    def interested_in(self, books: List[str]):
        self._select_books(self.interested_in, books)

    def _continue(self):
        button = self.find_element(*self._continue_button_locator)
        Utility.click_option(self.driver, element=button)
        from pages.accounts.signup import CompleteSignup
        return go_to_(CompleteSignup(self.driver))

    def _select_books(
            self, select: CompleteYourProfile.Multiselect, books: List[str]):
        if not select.list_is_open:
            select.toggle()
        book_list = books
        for book in select.books:
            if book.title in book_list:
                book_list.remove(book.title)
                book.select()
        select.toggle()

    class Multiselect(Region):

        _book_list_toggle_locator = (
            By.CSS_SELECTOR, '[type=button]')
        _book_list_arrow_icon_locator = (
            By.CSS_SELECTOR, 'i.fa')
        _book_title_bar_locator = (
            By.CSS_SELECTOR, '.result')

        def toggle(self):
            arrow = self.find_element(*self._book_list_toggle_locator)
            Utility.click_option(self.driver, element=arrow)
            sleep(0.25)

        @property
        def list_is_open(self) -> bool:
            icon = self.find_element(*self._book_list_arrow_icon_locator)
            return 'caret-up' in icon.get_attribute('class')

        @property
        def books(self) -> List[CompleteYourProfile.Multiselect.Book]:
            return [self.Book(self, book)
                    for book
                    in self.find_elements(*self._book_title_bar_locator)]

        class Book(Region):

            @property
            def title(self) -> str:
                return self.root.text

            def select(self):
                Utility.click_option(self.driver, element=self.root)
