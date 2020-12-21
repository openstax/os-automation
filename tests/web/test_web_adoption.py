"""Test the adoption form."""

from random import choice

import pytest

from pages.web.adoption import Adoption
from pages.web.book import Book
from pages.web.home import WebHome
from tests.markers import nondestructive, skip_test, smoke_test, test_case, web
from utils.email import RestMail
from utils.utilities import Utility
from utils.web import Library, Web, WebException


@test_case('C210385')
@nondestructive
@web
def test_adoption_form_loads(web_base_url, selenium):
    """Test the form loading."""
    # GIVEN: a user viewing the adoption page
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book(_from=Library.AVAILABLE)
    adoption = book.is_using()

    # WHEN:

    # THEN: the form is displayed
    assert(adoption.is_displayed())


@test_case('C210386')
@nondestructive
@web
def test_adoption_form_links_to_the_interest_form(web_base_url, selenium):
    """Test the cross-form link."""
    # GIVEN: a user viewing the adoption page
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book(_from=Library.AVAILABLE)
    adoption = book.is_using()

    # WHEN: they click on the "interest form" link
    interest = adoption.go_to_interest()

    # THEN: the interest page is displayed
    assert(interest.is_displayed())


@test_case('C210387')
@nondestructive
@web
def test_students_do_not_need_to_fill_out_the_adoption_form(
        web_base_url, selenium):
    """Test when students try to fill out the adoption form."""
    # GIVEN: a user viewing the adoption page
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book(_from=Library.AVAILABLE)
    adoption = book.is_using()

    # WHEN: they access the adoption form
    # AND:  select "Student" from the drop down menu
    adoption.form.select(Web.STUDENT)

    # THEN: a message "Students don't need to fill..." is displayed
    message = (
        "Students don't need to fill out any forms to use our books. "
        "Access them free now!")
    assert(adoption.form.student_message == message), \
        'Student menu option not selected or message not displayed'

    # WHEN: they go to the home page
    # AND:  select all subjects
    # AND:  click on a book
    # AND:  click on the "Using this book? Let us know."
    # AND:  select "Student" from the drop down menu
    # AND:  click on the "GO BACK" button
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book()
    book_title = book.title
    adoption = book.is_using()
    adoption.form.select(Web.STUDENT)
    adoption.form.go_back(destination=Book)

    # THEN: the book page is displayed
    assert(book.is_displayed() and book.title == book_title)


@test_case('C210388')
@web
def test_non_student_users_submit_the_adoption_form(web_base_url, selenium):
    """Test that a non-student user is able to submit the adoption form.

    Salesforce verification of the form is not tested.
    """
    # SETUP:
    user_type = Web.USERS[Utility.random(1, len(Web.USERS) - 1)]
    _, first_name, last_name, _ = Utility.random_name()
    email = RestMail(
        '{first}.{last}.{rand}'
        .format(first=first_name, last=last_name, rand=Utility.random_hex(3))
        .lower())
    phone = Utility.random_phone(713, False)
    school = 'Rice University'
    book_list = Library().random_book()
    books = {}
    for book in book_list:
        books[book] = {
            'status': Web.USING_STATUS[
                Utility.random(0, len(Web.USING_STATUS) - 1)],
            'students': Utility.random(Web.STUDENT_MIN, Web.STUDENT_MAX)
        }

    # GIVEN: a user viewing the adoption page
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
    initial_book = choice(list(books.keys()))
    book = subjects.select_book(initial_book)
    adoption = book.is_using()

    # WHEN: they select a non-Student role from the drop down menu
    # AND:  fill out the contact form fields
    # AND:  click on the "Next" button
    # AND:  select a book subject
    # AND:  select a radio option from "How are you using <book>?"
    # AND:  enter a number of students
    # AND:  click on the "Next" button
    # AND:  select a technology provider
    # AND:  click on the "Submit" button
    partners = adoption.submit_adoption(
        user_type=user_type,
        first=first_name,
        last=last_name,
        email=email.address,
        phone=phone,
        school=school,
        books=books)

    # THEN: the Tech Scout page (Partners) is displayed
    assert(partners.is_displayed())
    assert('partners' in partners.location)


@test_case('C210389')
@nondestructive
@web
def test_a_book_is_preselected_when_a_book_details_adoption_link_is_used(
        web_base_url, selenium):
    """Test using a book details page adoption link prefills the book."""
    # SETUP:
    user_type = Web.USERS[Utility.random(1, len(Web.USERS) - 1)]
    _, first_name, last_name, _ = Utility.random_name()
    email = RestMail(
        '{first}.{last}.{rand}'
        .format(first=first_name, last=last_name, rand=Utility.random_hex(4))
        .lower())
    phone = Utility.random_phone(713, False)
    school = 'Rice University'
    book, short, full, detail_append = Library().get_name_set()
    books = {short: {'status': '', 'students': '', }}

    # GIVEN: a user viewing a book page
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book(_from=Library.AVAILABLE)
    adoption = book.is_using()

    # WHEN: they click on the "Using this book? Let us know." link
    # AND:  select a non-Student role from the drop down menu
    # AND:  fill out the contact form fields
    # AND:  click on the "Next" button
    with pytest.raises(WebException) as error:
        adoption.submit_adoption(
            user_type=user_type,
            first=first_name,
            last=last_name,
            email=email.address,
            phone=phone,
            school=school,
            books=books)

    # THEN: the book is selected
    # AND:  the using questions for the book are displayed
    print(f'{Utility.get_error_information(error)}')
    assert(short in Utility.get_error_information(error)), \
        '{book} ({short}) not preselected'.format(book=full, short=short)


@test_case('C210390')
@nondestructive
@web
def test_adoption_form_identity_fields_are_required(web_base_url, selenium):
    """Test for error messages for all identification fields."""
    # SETUP:
    user_type = Web.USERS[Utility.random(1, len(Web.USERS) - 1)]

    # GIVEN: a user viewing the adoption page
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book(_from=Library.AVAILABLE)
    adoption = book.is_using()

    # WHEN: they select a non-Student role from the drop down menu
    # AND:  click on the "Next" button
    with pytest.raises(WebException) as error:
        adoption.submit_adoption(
            user_type=user_type,
            first='',
            last='',
            email='',
            phone='',
            school='',
            books={})

    # THEN: the contact form fields are shaded red
    # AND:  "Please fill out this field." is below each
    #       contact form field input box
    browser = selenium.capabilities.get('browserName').lower()
    expected_error = (
        ': {browser_front}ill out this field'
        .format(browser_front='F' if browser == 'safari' else 'Please f'))
    data_issues = Utility.get_error_information(error)
    first = ('first_name' + expected_error) in data_issues
    last = ('last_name' + expected_error) in data_issues
    email = ('email' + expected_error) in data_issues
    phone = ('phone' + expected_error) in data_issues
    school = ('school' + expected_error) in data_issues
    assert(first and last and email and phone and school), (
        'Errors not all shown:\n{errors}\n'.format(errors=data_issues)
        ('{first} {last} {email} {phone} {school}'
         .format(first=first, last=last, email=email,
                 phone=phone, school=school)))


@skip_test(reason='Not written')
@test_case('C210391')
@nondestructive
@web
def test_adoption_form_school_name_auto_complete(web_base_url, selenium):
    """Test the adoption form school name auto-completion."""
    # GIVEN: a user viewing the adoption page

    # WHEN: they select a non-Student role from the drop down menu
    # AND:  enter at least two letters in the "School name" input box

    # THEN: suggested institutions with the string are displayed

    # WHEN: one or more letters are appended

    # THEN: the suggestion list is filtered further


@skip_test(reason='Not written')
@test_case('C210392')
@web
def test_adoption_form_school_name_can_use_a_new_name(web_base_url, selenium):
    """Test that a new school name is accept."""
    # GIVEN: a user viewing the adoption page

    # WHEN: they select a non-Student role from the drop down menu
    # AND:  fill out the contact form fields
    # AND:  enter a random string in the "School name" field
    # AND:  click on the "Next" button

    # THEN: the textbook selection list is displayed


@test_case('C210393')
@nondestructive
@web
def test_adoption_form_requires_at_least_one_book_selection(
        web_base_url, selenium):
    """Test that the adoption form requires at least one book selection."""
    # SETUP:
    user_type = Web.USERS[Utility.random(1, len(Web.USERS) - 1)]
    _, first_name, last_name, _ = Utility.random_name()
    email = RestMail(
        '{first}.{last}.{rand}'
        .format(first=first_name, last=last_name, rand=Utility.random_hex(5))
        .lower())
    phone = Utility.random_phone(713, False)
    school = 'Rice University'

    # GIVEN: a user viewing the adoption page
    adoption = Adoption(selenium, web_base_url).open()

    # WHEN: they select a non-Student role from the drop down menu
    # AND:  fill out the contact form fields
    # AND:  click on the "Next" button
    # AND:  click on the "Next" button
    with pytest.raises(WebException) as error:
        adoption.submit_adoption(
            user_type=user_type,
            first=first_name,
            last=last_name,
            email=email.address,
            phone=phone,
            school=school,
            books={})

    # THEN: the textbook selection list is still displayed
    # AND:  an error message "Please select at least one book" is displayed
    assert('Please select at least one book'
           in Utility.get_error_information(error)), (
        'The book error was not displayed')


@skip_test(reason='Salesforce API not written')
@test_case('C210394')
@web
def test_book_use_questions_are_included_for_each_selected_book(
        web_base_url, selenium):
    """Test that an adoption question and student count is added for a book."""
    # GIVEN: a user viewing the adoption page

    # WHEN: they select a non-Student role from the drop down menu
    # AND:  fill out the contact form fields
    # AND:  click on the "Next" button
    # AND:  select a book

    # THEN: a question pair for that book are displayed below the book list

    # WHEN: another book is selected

    # THEN: a question pair for that book are displayed
    # AND:  the question pair for the first book are still displayed


@skip_test(reason='Salesforce API not written')
@test_case('C210395')
@web
def test_adoption_form_fields_are_sent_to_one_salesforce_lead(
        web_base_url, selenium):
    """Test the adoption form fields for a single adoption create one lead."""
    # GIVEN: a user viewing the adoption page

    # WHEN: they fill out the adoption form
    # AND:  select one book
    # AND:  submit the form

    # THEN: the form data is present in an adoption lead in Salesforce


@skip_test(reason='Salesforce API not written')
@test_case('C210396')
@web
def test_each_adopted_book_creates_a_separate_salesforce_lead(
        web_base_url, selenium):
    """Test that each adopted book creates a separate Salesforce lead."""
    # GIVEN: a user viewing the adoption page

    # WHEN: they fill out the adoption form
    # AND:  select two books
    # AND:  submit the form

    # THEN: two adoption leads are sent to Salesforce


@skip_test(reason='Salesforce API not written')
@test_case('C210397')
@smoke_test
@web
def test_all_tech_options_are_included_on_each_adoption_lead(
        web_base_url, selenium):
    """Test that selected tech options are included with each book lead."""
    # GIVEN: a user viewing the adoption page

    # WHEN: they fill out the adoption form
    # AND:  select two books
    # AND:  select two technology options
    # AND:  submit the form

    # THEN: two adoption leads are sent to Salesforce
    # AND:  each lead contains both technology options


@skip_test(reason='Confirmation page removed')
@test_case('C210399')
@nondestructive
@web
def test_able_to_submit_a_new_adoption_from_the_adoption_confirmation(
        web_base_url, selenium):
    """A link on the confirmation screen exists to submit another adoption."""
    # GIVEN: a user viewing the adoption confirmation page

    # WHEN: they click on the "Report another adopted textbook" button

    # THEN: the adoption page is displayed


@skip_test(reason='No current survey available')
@test_case('C210400')
@nondestructive
@web
def test_adopters_are_asked_to_take_a_marketing_survey(web_base_url, selenium):
    """Adopters are asked to take a marketing survey."""
    # GIVEN: a user viewing the adoption confirmation page

    # IF: a survey is available

    # WHEN: they click on the "Take the survey" button

    # THEN: the marketing survey page is displayed

    # TODO: need a survey to finish this
